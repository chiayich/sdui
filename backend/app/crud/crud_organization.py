from typing import List, Optional, Dict, Any, Union
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.models.organization import (
    OrganizationNode, Role, Permission, RolePermission, 
    RoleOrgPermission, user_role as UserRoleTable
)
from app.schemas.organization import (
    OrganizationNodeCreate, OrganizationNodeUpdate, 
    RoleCreate, RoleUpdate, 
    PermissionCreate, PermissionUpdate, 
    RoleOrgPermissionCreate, RoleOrgPermissionUpdate
)
from app.crud.base import CRUDBase


class CRUDOrganizationNode(CRUDBase[OrganizationNode, OrganizationNodeCreate, OrganizationNodeUpdate]):
    def create(self, db: Session, *, obj_in: OrganizationNodeCreate) -> OrganizationNode:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        
        # 处理路径和级别
        if obj_in.parent_id:
            parent = db.query(self.model).filter(self.model.id == obj_in.parent_id).first()
            if parent:
                db_obj.path = f"{parent.path}.{obj_in.code}"
                db_obj.level = parent.level + 1
            else:
                db_obj.path = obj_in.code
                db_obj.level = 0
        else:
            db_obj.path = obj_in.code
            db_obj.level = 0
            
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: OrganizationNode, obj_in: Union[OrganizationNodeUpdate, Dict[str, Any]]) -> OrganizationNode:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            
        # 如果更新了code，需要更新path
        if "code" in update_data:
            new_code = update_data["code"]
            if db_obj.parent_id:
                parent = db.query(self.model).filter(self.model.id == db_obj.parent_id).first()
                if parent:
                    update_data["path"] = f"{parent.path}.{new_code}"
            else:
                update_data["path"] = new_code
                
            # 更新子节点的path
            self._update_children_paths(db, db_obj)
            
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def _update_children_paths(self, db: Session, node: OrganizationNode):
        """递归更新子节点的路径"""
        children = db.query(self.model).filter(self.model.parent_id == node.id).all()
        for child in children:
            child.path = f"{node.path}.{child.code}"
            db.add(child)
            self._update_children_paths(db, child)
    
    def get_tree(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[OrganizationNode]:
        """获取组织树结构"""
        root_nodes = db.query(self.model).filter(self.model.parent_id == None).offset(skip).limit(limit).all()
        return self._build_tree(db, root_nodes)
    
    def _build_tree(self, db: Session, nodes: List[OrganizationNode]) -> List[OrganizationNode]:
        """递归构建树结构"""
        result = []
        for node in nodes:
            children = db.query(self.model).filter(self.model.parent_id == node.id).all()
            node_dict = jsonable_encoder(node)
            if children:
                node_dict["children"] = self._build_tree(db, children)
            else:
                node_dict["children"] = []
            result.append(node_dict)
        return result
    
    def get_node_with_children(self, db: Session, *, node_id: UUID) -> Optional[Dict]:
        """获取节点及其子节点"""
        node = db.query(self.model).filter(self.model.id == node_id).first()
        if not node:
            return None
        
        node_dict = jsonable_encoder(node)
        children = db.query(self.model).filter(self.model.parent_id == node.id).all()
        if children:
            node_dict["children"] = self._build_tree(db, children)
        else:
            node_dict["children"] = []
        
        return node_dict
    
    def get_node_ancestors(self, db: Session, *, node_id: UUID) -> List[OrganizationNode]:
        """获取节点的所有祖先节点"""
        node = db.query(self.model).filter(self.model.id == node_id).first()
        if not node or not node.path:
            return []
        
        path_parts = node.path.split(".")
        if len(path_parts) <= 1:
            return []
        
        # 构建祖先路径列表
        ancestor_paths = []
        current_path = path_parts[0]
        ancestor_paths.append(current_path)
        
        for i in range(1, len(path_parts) - 1):
            current_path = f"{current_path}.{path_parts[i]}"
            ancestor_paths.append(current_path)
        
        # 查询祖先节点
        ancestors = db.query(self.model).filter(self.model.path.in_(ancestor_paths)).all()
        return ancestors
    
    def get_nodes_by_type(self, db: Session, *, node_type: str, skip: int = 0, limit: int = 100) -> List[OrganizationNode]:
        """获取特定类型的节点"""
        return db.query(self.model).filter(self.model.node_type == node_type).offset(skip).limit(limit).all()

    def create_with_path(self, db: Session, *, obj_in: OrganizationNodeCreate) -> OrganizationNode:
        """创建组织节点，自动生成路径信息"""
        # 准备基础数据
        create_data = obj_in.dict()
        parent_id = create_data.get("parent_id")
        level = 0
        path = "/"
        
        # 如果有父节点，获取父节点信息
        if parent_id:
            parent = self.get(db, id=parent_id)
            if parent:
                level = parent.level + 1
                path = f"{parent.path}{parent_id}/"
        
        # 创建节点
        db_obj = OrganizationNode(
            **create_data,
            path=path,
            level=level
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_descendants(self, db: Session, *, node_id: int) -> List[OrganizationNode]:
        """获取指定节点的所有后代节点"""
        node = self.get(db, id=node_id)
        if not node:
            return []
        # 使用path字段进行Like查询，找到所有后代
        descendants = db.query(OrganizationNode).filter(
            OrganizationNode.path.like(f"{node.path}{node_id}/%")
        ).all()
        return descendants
    
    def get_ancestors(self, db: Session, *, node_id: int) -> List[OrganizationNode]:
        """获取指定节点的所有祖先节点"""
        node = self.get(db, id=node_id)
        if not node or not node.path or node.path == "/":
            return []
        
        # 解析路径中的ID
        path_ids = [int(id_str) for id_str in node.path.strip("/").split("/") if id_str]
        if not path_ids:
            return []
        
        # 查询所有祖先节点
        ancestors = db.query(OrganizationNode).filter(
            OrganizationNode.id.in_(path_ids)
        ).all()
        # 按路径顺序排序
        ancestors.sort(key=lambda x: path_ids.index(x.id))
        return ancestors
    
    def get_tree(self, db: Session, *, root_id: Optional[int] = None) -> List[OrganizationNode]:
        """获取组织树结构，可选指定根节点"""
        if root_id:
            # 获取指定根节点及其所有后代
            root = self.get(db, id=root_id)
            if not root:
                return []
            
            # 查找根节点及所有后代
            nodes = [root] + self.get_descendants(db, node_id=root_id)
        else:
            # 获取所有顶级节点及其后代
            top_nodes = db.query(OrganizationNode).filter(
                OrganizationNode.parent_id.is_(None)
            ).all()
            nodes = []
            for node in top_nodes:
                nodes.append(node)
                nodes.extend(self.get_descendants(db, node_id=node.id))
        
        # 构建节点ID到节点对象的映射
        node_map = {node.id: node for node in nodes}
        
        # 构建树结构
        tree = []
        for node in nodes:
            # 深拷贝节点以避免修改原始对象
            node_dict = node.__dict__.copy()
            node_dict.pop('_sa_instance_state', None)  # 移除SQLAlchemy状态
            node_obj = OrganizationNode(**node_dict)
            node_obj.children = []
            
            if node.parent_id and node.parent_id in node_map:
                # 将节点添加到父节点的children列表
                if not hasattr(node_map[node.parent_id], 'children'):
                    node_map[node.parent_id].children = []
                node_map[node.parent_id].children.append(node_obj)
            else:
                # 顶级节点直接添加到结果列表
                tree.append(node_obj)
            
            # 更新映射
            node_map[node.id] = node_obj
        
        return tree


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Role]:
        return db.query(self.model).filter(self.model.name == name).first()
    
    def get_user_roles(self, db: Session, *, user_id: UUID) -> List[Role]:
        return db.query(self.model).join(UserRoleTable).filter(UserRoleTable.user_id == user_id).all()
    
    def add_permission_to_role(self, db: Session, *, role_id: UUID, permission_id: UUID) -> bool:
        db_obj = RolePermission(role_id=role_id, permission_id=permission_id)
        db.add(db_obj)
        db.commit()
        return True
    
    def remove_permission_from_role(self, db: Session, *, role_id: UUID, permission_id: UUID) -> bool:
        db.query(RolePermission).filter(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id
        ).delete()
        db.commit()
        return True
    
    def update_role_permissions(self, db: Session, *, role_id: UUID, permission_ids: List[UUID]) -> bool:
        # 先删除所有现有权限
        db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
        
        # 添加新权限
        for permission_id in permission_ids:
            db_obj = RolePermission(role_id=role_id, permission_id=permission_id)
            db.add(db_obj)
        
        db.commit()
        return True
    
    def get_role_permissions(self, db: Session, *, role_id: UUID) -> List[Permission]:
        role = db.query(self.model).filter(self.model.id == role_id).first()
        if not role:
            return []
        return role.permissions

    def create_with_permissions(
        self, db: Session, *, obj_in: RoleCreate, permission_ids: List[int]
    ) -> Role:
        """创建角色并分配权限"""
        # 创建角色
        role = self.create(db, obj_in=obj_in)
        
        # 查询权限
        permissions = db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        
        # 分配权限
        for permission in permissions:
            role_permission = RolePermission(role_id=role.id, permission_id=permission.id)
            db.add(role_permission)
        
        db.commit()
        db.refresh(role)
        return role
    
    def update_permissions(
        self, db: Session, *, role_id: int, permission_ids: List[int]
    ) -> Role:
        """更新角色的权限"""
        # 获取角色
        role = self.get(db, id=role_id)
        if not role:
            return None
        
        # 删除现有权限关联
        db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
        
        # 创建新的权限关联
        for permission_id in permission_ids:
            role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
            db.add(role_permission)
        
        db.commit()
        db.refresh(role)
        return role
    
    def update_org_permissions(
        self, db: Session, *, role_id: int, org_node_ids: List[int]
    ) -> Role:
        """更新角色的组织权限"""
        # 获取角色
        role = self.get(db, id=role_id)
        if not role:
            return None
        
        # 删除现有组织权限关联
        db.query(RoleOrgPermission).filter(RoleOrgPermission.role_id == role_id).delete()
        
        # 创建新的组织权限关联
        for org_node_id in org_node_ids:
            role_org_permission = RoleOrgPermission(role_id=role_id, org_node_id=org_node_id)
            db.add(role_org_permission)
        
        db.commit()
        db.refresh(role)
        return role
    
    def get_role_org_permissions(self, db: Session, *, role_id: int) -> List[OrganizationNode]:
        """获取角色的组织权限"""
        role = self.get(db, id=role_id)
        if not role:
            return []
        return role.org_permissions


class CRUDPermission(CRUDBase[Permission, PermissionCreate, PermissionUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Permission]:
        return db.query(self.model).filter(self.model.code == code).first()
    
    def get_by_module(self, db: Session, *, module: str) -> List[Permission]:
        return db.query(self.model).filter(self.model.module == module).all()
    
    def get_permission_tree(self, db: Session) -> List[Dict]:
        """构建权限树，按模块分组"""
        permissions = db.query(self.model).all()
        
        # 按模块分组
        modules = {}
        for perm in permissions:
            if perm.module not in modules:
                modules[perm.module] = {
                    "code": f"module:{perm.module}",
                    "name": perm.module,
                    "module": perm.module,
                    "type": "module",
                    "children": []
                }
            
            modules[perm.module]["children"].append({
                "code": perm.code,
                "name": perm.name,
                "module": perm.module,
                "type": perm.type,
                "children": []
            })
        
        return list(modules.values())

    def get_tree(self, db: Session) -> List[Permission]:
        """获取权限树结构"""
        # 获取所有权限
        permissions = db.query(Permission).all()
        
        # 构建权限ID到权限对象的映射
        permission_map = {p.id: p for p in permissions}
        
        # 构建树结构
        tree = []
        for p in permissions:
            # 深拷贝权限以避免修改原始对象
            p_dict = p.__dict__.copy()
            p_dict.pop('_sa_instance_state', None)  # 移除SQLAlchemy状态
            p_obj = Permission(**p_dict)
            p_obj.children = []
            
            if p.parent_id and p.parent_id in permission_map:
                # 将权限添加到父权限的children列表
                if not hasattr(permission_map[p.parent_id], 'children'):
                    permission_map[p.parent_id].children = []
                permission_map[p.parent_id].children.append(p_obj)
            else:
                # 顶级权限直接添加到结果列表
                tree.append(p_obj)
            
            # 更新映射
            permission_map[p.id] = p_obj
        
        return tree


class CRUDRoleOrgPermission(CRUDBase[RoleOrgPermission, RoleOrgPermissionCreate, RoleOrgPermissionUpdate]):
    def get_by_role_and_node(self, db: Session, *, role_id: UUID, org_node_id: UUID) -> Optional[RoleOrgPermission]:
        return db.query(self.model).filter(
            self.model.role_id == role_id,
            self.model.org_node_id == org_node_id
        ).first()
    
    def get_by_role(self, db: Session, *, role_id: UUID) -> List[RoleOrgPermission]:
        return db.query(self.model).filter(self.model.role_id == role_id).all()
    
    def update_role_org_permissions(self, db: Session, *, role_id: UUID, org_permissions: List[RoleOrgPermissionCreate]) -> bool:
        # 先删除所有现有组织权限
        db.query(self.model).filter(self.model.role_id == role_id).delete()
        
        # 添加新组织权限
        for perm in org_permissions:
            db_obj = self.model(
                role_id=role_id,
                org_node_id=perm.org_node_id,
                access_type=perm.access_type,
                include_children=perm.include_children
            )
            db.add(db_obj)
        
        db.commit()
        return True
    
    def get_user_accessible_orgs(self, db: Session, *, user_id: UUID) -> List[UUID]:
        """获取用户可访问的组织节点ID"""
        # 获取用户角色
        user_roles = db.query(Role).join(UserRoleTable).filter(UserRoleTable.user_id == user_id).all()
        if not user_roles:
            return []
        
        role_ids = [role.id for role in user_roles]
        
        # 获取角色的组织权限
        role_org_perms = db.query(self.model).filter(self.model.role_id.in_(role_ids)).all()
        if not role_org_perms:
            return []
        
        # 收集可访问的组织节点ID
        accessible_node_ids = set()
        for perm in role_org_perms:
            # 添加直接授权的节点
            accessible_node_ids.add(perm.org_node_id)
            
            # 如果包含子节点，添加子节点
            if perm.include_children:
                org_node = db.query(OrganizationNode).filter(OrganizationNode.id == perm.org_node_id).first()
                if org_node:
                    child_nodes = db.query(OrganizationNode).filter(
                        OrganizationNode.path.like(f"{org_node.path}.%")
                    ).all()
                    for child in child_nodes:
                        accessible_node_ids.add(child.id)
        
        return list(accessible_node_ids)


organization_node = CRUDOrganizationNode(OrganizationNode)
role = CRUDRole(Role)
permission = CRUDPermission(Permission)
role_org_permission = CRUDRoleOrgPermission(RoleOrgPermission) 