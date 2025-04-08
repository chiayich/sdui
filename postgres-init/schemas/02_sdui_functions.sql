-- 创建更新时间戳函数
CREATE OR REPLACE FUNCTION sdui_schema.update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为各个表创建更新时间戳触发器
DROP TRIGGER IF EXISTS update_organization_nodes_updated_at ON sdui_schema.organization_nodes;
CREATE TRIGGER update_organization_nodes_updated_at
    BEFORE UPDATE ON sdui_schema.organization_nodes
    FOR EACH ROW
    EXECUTE FUNCTION sdui_schema.update_updated_at();

DROP TRIGGER IF EXISTS update_users_updated_at ON sdui_schema.users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON sdui_schema.users
    FOR EACH ROW
    EXECUTE FUNCTION sdui_schema.update_updated_at();

DROP TRIGGER IF EXISTS update_permissions_updated_at ON sdui_schema.permissions;
CREATE TRIGGER update_permissions_updated_at
    BEFORE UPDATE ON sdui_schema.permissions
    FOR EACH ROW
    EXECUTE FUNCTION sdui_schema.update_updated_at();

DROP TRIGGER IF EXISTS update_roles_updated_at ON sdui_schema.roles;
CREATE TRIGGER update_roles_updated_at
    BEFORE UPDATE ON sdui_schema.roles
    FOR EACH ROW
    EXECUTE FUNCTION sdui_schema.update_updated_at();

DROP TRIGGER IF EXISTS update_user_roles_updated_at ON sdui_schema.user_roles;
CREATE TRIGGER update_user_roles_updated_at
    BEFORE UPDATE ON sdui_schema.user_roles
    FOR EACH ROW
    EXECUTE FUNCTION sdui_schema.update_updated_at();

DROP TRIGGER IF EXISTS update_role_permissions_updated_at ON sdui_schema.role_permissions;
CREATE TRIGGER update_role_permissions_updated_at
    BEFORE UPDATE ON sdui_schema.role_permissions
    FOR EACH ROW
    EXECUTE FUNCTION sdui_schema.update_updated_at();

DROP TRIGGER IF EXISTS update_role_org_permissions_updated_at ON sdui_schema.role_org_permissions;
CREATE TRIGGER update_role_org_permissions_updated_at
    BEFORE UPDATE ON sdui_schema.role_org_permissions
    FOR EACH ROW
    EXECUTE FUNCTION sdui_schema.update_updated_at();

DROP TRIGGER IF EXISTS update_sdui_configs_updated_at ON sdui_schema.sdui_configs;
CREATE TRIGGER update_sdui_configs_updated_at
    BEFORE UPDATE ON sdui_schema.sdui_configs
    FOR EACH ROW
    EXECUTE FUNCTION sdui_schema.update_updated_at();

DROP TRIGGER IF EXISTS update_sdui_config_relations_updated_at ON sdui_schema.sdui_config_relations;
CREATE TRIGGER update_sdui_config_relations_updated_at
    BEFORE UPDATE ON sdui_schema.sdui_config_relations
    FOR EACH ROW
    EXECUTE FUNCTION sdui_schema.update_updated_at(); 