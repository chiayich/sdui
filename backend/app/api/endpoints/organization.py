from typing import Any, List, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps
from app.schemas.organization import (
    OrganizationNode, OrganizationNodeCreate, OrganizationNodeUpdate,
    Role, RoleCreate, RoleUpdate,
    Permission, PermissionCreate, PermissionUpdate,
    RoleOrgPermission, RoleOrgPermissionCreate,
    UpdateRolePermissionsRequest, UpdateRoleOrgPermissionsRequest,
    PermissionCheckResponse
)
from app.models.user import User

router = APIRouter()


# 组织节点管理API
@router.get("/tree", response_model=List[Dict])
def get_organization_tree(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """获取组织树结构"""
    # 超级管理员可以获取完整树结构
    if crud.user.is_superuser(current_user):
        org_tree = crud.organization_node.get_tree(db)
        return org_tree
    
    # 非超级管理员只能获取有权限的组织节点
    # 获取用户角色
    user_roles = current_user.roles
    if not user_roles:
        return []
    
    # 获取用户所有角色的组织权限
    accessible_org_nodes = set()
    for role in user_roles:
        org_permissions = crud.role.get_role_org_permissions(db, role_id=role.id)
        for org_node in org_permissions:
            accessible_org_nodes.add(org_node.id)
            
            # 如果有父节点，也需要加入，以确保树形结构完整
            ancestors = crud.organization_node.get_ancestors(db, node_id=org_node.id)
            for ancestor in ancestors:
                accessible_org_nodes.add(ancestor.id)
    
    # 获取可访问节点的树形结构
    if not accessible_org_nodes:
        return []
    
    # 找到最高级别的节点作为根节点
    top_nodes = []
    for node_id in accessible_org_nodes:
        node = crud.organization_node.get(db, id=node_id)
        if not node:
            continue
            
        # 如果节点的父节点不在可访问列表中，则为顶级节点
        if not node.parent_id or node.parent_id not in accessible_org_nodes:
            top_nodes.append(node.id)
    
    # 获取每个顶级节点的树
    org_trees = []
    for node_id in top_nodes:
        tree = crud.organization_node.get_tree(db, root_id=node_id)
        # 过滤掉不可访问的节点
        filtered_tree = filter_tree_by_accessible_nodes(tree, accessible_org_nodes)
        if filtered_tree:
            org_trees.extend(filtered_tree)
    
    return org_trees


def filter_tree_by_accessible_nodes(tree: List[Dict], accessible_nodes: set) -> List[Dict]:
    """过滤树形结构，只保留可访问的节点"""
    filtered_tree = []
    
    for node in tree:
        if node["id"] in accessible_nodes:
            node_copy = node.copy()
            
            # 递归过滤子节点
            if "children" in node and node["children"]:
                node_copy["children"] = filter_tree_by_accessible_nodes(
                    node["children"], accessible_nodes
                )
            
            filtered_tree.append(node_copy)
    
    return filtered_tree


@router.get("/node/{node_id}", response_model=OrganizationNode)
def get_organization_node(
    node_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """获取组织节点详情"""
    node = crud.organization_node.get(db, id=node_id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织节点不存在"
        )
    
    # 检查权限：超级管理员拥有所有权限
    if crud.user.is_superuser(current_user):
        return node
    
    # 非超级管理员需要检查是否有权限访问此节点
    has_permission = False
    for role in current_user.roles:
        org_permissions = crud.role.get_role_org_permissions(db, role_id=role.id)
        if node.id in [org.id for org in org_permissions]:
            has_permission = True
            break
    
    if not has_permission:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限访问此组织节点"
        )
    
    return node


@router.post("/node", response_model=OrganizationNode)
def create_organization_node(
    *,
    db: Session = Depends(deps.get_db),
    node_in: OrganizationNodeCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """创建组织节点"""
    # 检查权限：超级管理员或有创建权限的用户
    if not crud.user.is_superuser(current_user):
        has_permission = False
        for role in current_user.roles:
            permissions = crud.role.get_role_permissions(db, role_id=role.id)
            if "org:create" in [p.code for p in permissions]:
                has_permission = True
                break
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限创建组织节点"
            )
        
        # 如果有父节点，还需要检查是否有权限在父节点下创建
        if node_in.parent_id:
            parent_accessible = False
            for role in current_user.roles:
                org_permissions = crud.role.get_role_org_permissions(db, role_id=role.id)
                if node_in.parent_id in [org.id for org in org_permissions]:
                    parent_accessible = True
                    break
            
            if not parent_accessible:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="没有权限在指定的父节点下创建组织节点"
                )
    
    # 检查code是否已存在
    existing = db.query(crud.organization_node.model).filter(
        crud.organization_node.model.code == node_in.code
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="组织节点代码已存在"
        )
    
    # 创建节点
    node = crud.organization_node.create_with_path(db=db, obj_in=node_in)
    return node


@router.put("/node/{node_id}", response_model=OrganizationNode)
def update_organization_node(
    *,
    db: Session = Depends(deps.get_db),
    node_id: int,
    node_in: OrganizationNodeUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """更新组织节点"""
    node = crud.organization_node.get(db, id=node_id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织节点不存在"
        )
    
    # 检查权限：超级管理员或有编辑权限的用户
    if not crud.user.is_superuser(current_user):
        has_permission = False
        for role in current_user.roles:
            permissions = crud.role.get_role_permissions(db, role_id=role.id)
            if "org:edit" in [p.code for p in permissions]:
                has_permission = True
                break
            
            # 还需要检查是否有权限编辑此节点
            org_permissions = crud.role.get_role_org_permissions(db, role_id=role.id)
            if node.id in [org.id for org in org_permissions]:
                has_permission = True
                break
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限编辑此组织节点"
            )
    
    # 如果更新了code，检查是否已存在
    if node_in.code and node_in.code != node.code:
        existing = db.query(crud.organization_node.model).filter(
            crud.organization_node.model.code == node_in.code,
            crud.organization_node.model.id != node_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="组织节点代码已存在"
            )
    
    # 更新节点
    node = crud.organization_node.update(db=db, db_obj=node, obj_in=node_in)
    return node


@router.delete("/node/{node_id}", response_model=OrganizationNode)
def delete_organization_node(
    *,
    db: Session = Depends(deps.get_db),
    node_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """删除组织节点"""
    node = crud.organization_node.get(db, id=node_id)
    if not node:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织节点不存在"
        )
    
    # 检查权限：超级管理员或有删除权限的用户
    if not crud.user.is_superuser(current_user):
        has_permission = False
        for role in current_user.roles:
            permissions = crud.role.get_role_permissions(db, role_id=role.id)
            if "org:delete" in [p.code for p in permissions]:
                has_permission = True
                break
            
            # 还需要检查是否有权限删除此节点
            org_permissions = crud.role.get_role_org_permissions(db, role_id=role.id)
            if node.id in [org.id for org in org_permissions]:
                has_permission = True
                break
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限删除此组织节点"
            )
    
    # 检查是否有子节点
    children = db.query(crud.organization_node.model).filter(
        crud.organization_node.model.parent_id == node_id
    ).all()
    if children:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除有子节点的组织节点，请先删除子节点"
        )
    
    # 检查是否有用户属于此组织
    users = db.query(crud.user.model).filter(
        crud.user.model.organization_id == node_id
    ).all()
    if users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除有用户的组织节点，请先将用户转移到其他组织"
        )
    
    # 删除节点
    node = crud.organization_node.remove(db=db, id=node_id)
    return node


# 角色权限管理API
@router.get("/roles", response_model=List[Role])
def read_roles(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """获取角色列表（仅限超级管理员）"""
    roles = crud.role.get_multi(db, skip=skip, limit=limit)
    return roles


@router.post("/roles", response_model=Role)
def create_role(
    *,
    db: Session = Depends(deps.get_db),
    role_in: RoleCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """创建角色（仅限超级管理员）"""
    # 检查角色名是否已存在
    role = crud.role.get_by_name(db, name=role_in.name)
    if role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色名已存在"
        )
    
    role = crud.role.create(db=db, obj_in=role_in)
    return role


@router.put("/roles/{role_id}", response_model=Role)
def update_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    role_in: RoleUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """更新角色（仅限超级管理员）"""
    role = crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 不允许更新系统角色
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能修改系统角色"
        )
    
    # 如果更新了名称，检查是否已存在
    if role_in.name and role_in.name != role.name:
        existing = crud.role.get_by_name(db, name=role_in.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="角色名已存在"
            )
    
    role = crud.role.update(db=db, db_obj=role, obj_in=role_in)
    return role


@router.delete("/roles/{role_id}", response_model=Role)
def delete_role(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """删除角色（仅限超级管理员）"""
    role = crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 不允许删除系统角色
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除系统角色"
        )
    
    # 检查是否有用户使用此角色
    if role.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除有用户使用的角色，请先取消用户的角色分配"
        )
    
    role = crud.role.remove(db=db, id=role_id)
    return role


@router.get("/permissions", response_model=List[Permission])
def read_permissions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """获取权限列表（仅限超级管理员）"""
    permissions = crud.permission.get_multi(db, skip=skip, limit=limit)
    return permissions


@router.get("/permissions/tree", response_model=List[Dict])
def read_permission_tree(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """获取权限树（仅限超级管理员）"""
    permission_tree = crud.permission.get_tree(db)
    return permission_tree


@router.get("/roles/{role_id}/permissions", response_model=List[Permission])
def read_role_permissions(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """获取角色的权限（仅限超级管理员）"""
    role = crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    return crud.role.get_role_permissions(db, role_id=role_id)


@router.post("/roles/{role_id}/permissions", response_model=Role)
def update_role_permissions(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    permissions_in: UpdateRolePermissionsRequest,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """更新角色的权限（仅限超级管理员）"""
    role = crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 检查所有权限ID是否存在
    for permission_id in permissions_in.permission_ids:
        permission = crud.permission.get(db, id=permission_id)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"权限ID {permission_id} 不存在"
            )
    
    # 更新角色权限
    role = crud.role.update_permissions(
        db, role_id=role_id, permission_ids=permissions_in.permission_ids
    )
    return role


@router.get("/roles/{role_id}/org-permissions", response_model=List[OrganizationNode])
def read_role_org_permissions(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """获取角色的组织权限（仅限超级管理员）"""
    role = crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    return crud.role.get_role_org_permissions(db, role_id=role_id)


@router.post("/roles/{role_id}/org-permissions", response_model=Role)
def update_role_org_permissions(
    *,
    db: Session = Depends(deps.get_db),
    role_id: int,
    org_permissions_in: UpdateRoleOrgPermissionsRequest,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """更新角色的组织权限（仅限超级管理员）"""
    role = crud.role.get(db, id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 检查所有组织节点ID是否存在
    for org_node_id in org_permissions_in.org_node_ids:
        org_node = crud.organization_node.get(db, id=org_node_id)
        if not org_node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"组织节点ID {org_node_id} 不存在"
            )
    
    # 更新角色组织权限
    role = crud.role.update_org_permissions(
        db, role_id=role_id, org_node_ids=org_permissions_in.org_node_ids
    )
    return role


@router.get("/check-permission/{permission_code}", response_model=PermissionCheckResponse)
def check_permission(
    *,
    db: Session = Depends(deps.get_db),
    permission_code: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """检查当前用户是否拥有指定权限"""
    # 超级管理员拥有所有权限
    if crud.user.is_superuser(current_user):
        return {"has_permission": True}
    
    # 获取用户角色
    user_roles = current_user.roles
    if not user_roles:
        return {"has_permission": False}
    
    # 检查用户角色是否拥有此权限
    for role in user_roles:
        permissions = crud.role.get_role_permissions(db, role_id=role.id)
        permission_codes = [p.code for p in permissions]
        if permission_code in permission_codes:
            return {"has_permission": True}
    
    return {"has_permission": False}


@router.get("/user-accessible-orgs", response_model=List[OrganizationNode])
def get_user_accessible_orgs(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """获取当前用户可访问的组织节点"""
    # 超级管理员可访问所有组织
    if crud.user.is_superuser(current_user):
        return crud.organization_node.get_multi(db)
    
    # 获取用户角色
    user_roles = current_user.roles
    if not user_roles:
        return []
    
    # 获取用户通过角色可访问的组织
    accessible_orgs = set()
    for role in user_roles:
        org_permissions = crud.role.get_role_org_permissions(db, role_id=role.id)
        for org in org_permissions:
            accessible_orgs.add(org.id)
    
    # 获取组织节点
    result = []
    for org_id in accessible_orgs:
        org = crud.organization_node.get(db, id=org_id)
        if org:
            result.append(org)
    
    return result 