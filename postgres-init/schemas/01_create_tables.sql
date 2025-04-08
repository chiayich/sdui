-- 创建sdui_schema
CREATE SCHEMA IF NOT EXISTS sdui_schema;

-- 创建组织表
CREATE TABLE IF NOT EXISTS sdui_schema.organization_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    node_type VARCHAR(50) NOT NULL,
    parent_id UUID REFERENCES sdui_schema.organization_nodes(id),
    path VARCHAR(255) NOT NULL,
    level INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建用户表
CREATE TABLE IF NOT EXISTS sdui_schema.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建权限表
CREATE TABLE IF NOT EXISTS sdui_schema.permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    parent_id UUID REFERENCES sdui_schema.permissions(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建角色表
CREATE TABLE IF NOT EXISTS sdui_schema.roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    is_system_role BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建用户角色关联表
CREATE TABLE IF NOT EXISTS sdui_schema.user_roles (
    user_id UUID REFERENCES sdui_schema.users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES sdui_schema.roles(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);

-- 创建角色权限关联表
CREATE TABLE IF NOT EXISTS sdui_schema.role_permissions (
    role_id UUID REFERENCES sdui_schema.roles(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES sdui_schema.permissions(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (role_id, permission_id)
);

-- 创建角色组织权限关联表
CREATE TABLE IF NOT EXISTS sdui_schema.role_org_permissions (
    role_id UUID REFERENCES sdui_schema.roles(id) ON DELETE CASCADE,
    org_node_id UUID REFERENCES sdui_schema.organization_nodes(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (role_id, org_node_id)
);

-- 创建配置表
CREATE TABLE IF NOT EXISTS sdui_schema.sdui_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,  -- system, page, component 等
    version INTEGER NOT NULL DEFAULT 1,
    config_data JSONB NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    creator_id UUID REFERENCES sdui_schema.users(id),
    updater_id UUID REFERENCES sdui_schema.users(id)
);

-- 创建配置版本历史表
CREATE TABLE IF NOT EXISTS sdui_schema.sdui_config_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    config_id UUID REFERENCES sdui_schema.sdui_configs(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    config_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    creator_id UUID REFERENCES sdui_schema.users(id)
);

-- 创建配置关系表（用于组件组合和页面引用）
CREATE TABLE IF NOT EXISTS sdui_schema.sdui_config_relations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_id UUID REFERENCES sdui_schema.sdui_configs(id) ON DELETE CASCADE,
    child_id UUID REFERENCES sdui_schema.sdui_configs(id) ON DELETE CASCADE,
    relation_type VARCHAR(20) NOT NULL, -- contains, references
    position INTEGER,
    properties JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_sdui_config_relations UNIQUE (parent_id, child_id, relation_type)
);

-- 创建审计日志表
CREATE TABLE IF NOT EXISTS sdui_schema.sdui_audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL,
    old_value JSONB,
    new_value JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    creator_id UUID REFERENCES sdui_schema.users(id)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_sdui_configs_category ON sdui_schema.sdui_configs(category);
CREATE INDEX IF NOT EXISTS idx_sdui_config_versions_config_id ON sdui_schema.sdui_config_versions(config_id);
CREATE INDEX IF NOT EXISTS idx_sdui_config_relations_parent ON sdui_schema.sdui_config_relations(parent_id);
CREATE INDEX IF NOT EXISTS idx_sdui_config_relations_child ON sdui_schema.sdui_config_relations(child_id);
CREATE INDEX IF NOT EXISTS idx_sdui_audit_logs_entity ON sdui_schema.sdui_audit_logs(entity_type, entity_id);

-- 创建更新时间触发器
CREATE OR REPLACE FUNCTION sdui_schema.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_sdui_configs_updated_at
    BEFORE UPDATE ON sdui_schema.sdui_configs
    FOR EACH ROW
    EXECUTE FUNCTION sdui_schema.update_updated_at(); 