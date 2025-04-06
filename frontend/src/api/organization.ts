import request from '@/utils/request';

/**
 * 获取组织架构树
 * @returns 组织树数据
 */
export function fetchOrganizationTree() {
    return request({
        url: '/api/organization/tree',
        method: 'get'
    });
}

/**
 * 获取组织节点详情
 * @param nodeId 节点ID
 * @returns 节点详情
 */
export function fetchOrganizationNode(nodeId: string) {
    return request({
        url: `/api/organization/node/${nodeId}`,
        method: 'get'
    });
}

/**
 * 创建组织节点
 * @param data 节点数据
 * @returns 创建结果
 */
export function createOrganizationNode(data: any) {
    return request({
        url: '/api/organization/node',
        method: 'post',
        data
    });
}

/**
 * 更新组织节点
 * @param nodeId 节点ID
 * @param data 更新数据
 * @returns 更新结果
 */
export function updateOrganizationNode(nodeId: string, data: any) {
    return request({
        url: `/api/organization/node/${nodeId}`,
        method: 'put',
        data
    });
}

/**
 * 删除组织节点
 * @param nodeId 节点ID
 * @returns 删除结果
 */
export function deleteOrganizationNode(nodeId: string) {
    return request({
        url: `/api/organization/node/${nodeId}`,
        method: 'delete'
    });
}

/**
 * 获取角色列表
 * @returns 角色列表
 */
export function fetchRoles() {
    return request({
        url: '/api/roles',
        method: 'get'
    });
}

/**
 * 创建角色
 * @param data 角色数据
 * @returns 创建结果
 */
export function createRole(data: any) {
    return request({
        url: '/api/roles',
        method: 'post',
        data
    });
}

/**
 * 更新角色
 * @param roleId 角色ID
 * @param data 更新数据
 * @returns 更新结果
 */
export function updateRole(roleId: string, data: any) {
    return request({
        url: `/api/roles/${roleId}`,
        method: 'put',
        data
    });
}

/**
 * 删除角色
 * @param roleId 角色ID
 * @returns 删除结果
 */
export function deleteRole(roleId: string) {
    return request({
        url: `/api/roles/${roleId}`,
        method: 'delete'
    });
}

/**
 * 获取角色权限
 * @param roleId 角色ID
 * @returns 权限列表
 */
export function fetchRolePermissions(roleId: string) {
    return request({
        url: `/api/roles/${roleId}/permissions`,
        method: 'get'
    });
}

/**
 * 更新角色权限
 * @param roleId 角色ID
 * @param data 权限数据
 * @returns 更新结果
 */
export function updateRolePermissions(roleId: string, data: any) {
    return request({
        url: `/api/roles/${roleId}/permissions`,
        method: 'post',
        data
    });
}

/**
 * 获取角色的组织权限
 * @param roleId 角色ID
 * @returns 组织权限
 */
export function fetchRoleOrgPermissions(roleId: string) {
    return request({
        url: `/api/roles/${roleId}/org-permissions`,
        method: 'get'
    });
}

/**
 * 更新角色的组织权限
 * @param roleId 角色ID
 * @param data 组织权限数据
 * @returns 更新结果
 */
export function updateRoleOrgPermissions(roleId: string, data: any) {
    return request({
        url: `/api/roles/${roleId}/org-permissions`,
        method: 'post',
        data
    });
}

/**
 * 检查当前用户是否有指定权限
 * @param permissionCode 权限代码
 * @returns 检查结果
 */
export function checkPermission(permissionCode: string) {
    return request({
        url: `/api/check-permission/${permissionCode}`,
        method: 'get'
    });
}

/**
 * 获取当前用户可访问的组织节点
 * @returns 可访问的组织节点列表
 */
export function fetchUserAccessibleOrgs() {
    return request({
        url: '/api/user-accessible-orgs',
        method: 'get'
    });
} 