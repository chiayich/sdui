-- 更新时间戳函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为所有需要的表添加时间戳更新触发器
CREATE TRIGGER update_ui_templates_timestamp
BEFORE UPDATE ON ui_templates
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ui_components_timestamp
BEFORE UPDATE ON ui_components
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 审计日志函数 - 模板变更
CREATE OR REPLACE FUNCTION log_template_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE') THEN
        INSERT INTO ui_audit_log(
            entity_type, entity_id, action, user_id, 
            old_value, new_value
        ) VALUES (
            'template', OLD.id, 'update', 'system',
            row_to_json(OLD), row_to_json(NEW)
        );
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO ui_audit_log(
            entity_type, entity_id, action, user_id, 
            new_value
        ) VALUES (
            'template', NEW.id, 'insert', 'system',
            row_to_json(NEW)
        );
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO ui_audit_log(
            entity_type, entity_id, action, user_id, 
            old_value
        ) VALUES (
            'template', OLD.id, 'delete', 'system',
            row_to_json(OLD)
        );
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_ui_templates_changes
AFTER INSERT OR UPDATE OR DELETE ON ui_templates
FOR EACH ROW EXECUTE FUNCTION log_template_changes();

-- 审计日志函数 - 组件变更
CREATE OR REPLACE FUNCTION log_component_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'UPDATE') THEN
        INSERT INTO ui_audit_log(
            entity_type, entity_id, action, user_id, 
            old_value, new_value
        ) VALUES (
            'component', OLD.id, 'update', 'system',
            row_to_json(OLD), row_to_json(NEW)
        );
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO ui_audit_log(
            entity_type, entity_id, action, user_id, 
            new_value
        ) VALUES (
            'component', NEW.id, 'insert', 'system',
            row_to_json(NEW)
        );
    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO ui_audit_log(
            entity_type, entity_id, action, user_id, 
            old_value
        ) VALUES (
            'component', OLD.id, 'delete', 'system',
            row_to_json(OLD)
        );
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_ui_components_changes
AFTER INSERT OR UPDATE OR DELETE ON ui_components
FOR EACH ROW EXECUTE FUNCTION log_component_changes();

-- 创建组件树函数 - 递归获取组件树结构
CREATE OR REPLACE FUNCTION get_component_tree(p_template_id INTEGER)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    WITH RECURSIVE component_tree AS (
        -- 获取根组件
        SELECT 
            c.id,
            c.component_id,
            c.component_type,
            c.properties,
            c.style,
            c.events,
            c.position,
            NULL::INTEGER AS parent_id,
            0 AS level
        FROM ui_components c
        WHERE c.template_id = p_template_id AND c.parent_id IS NULL
        
        UNION ALL
        
        -- 递归获取子组件
        SELECT 
            c.id,
            c.component_id,
            c.component_type,
            c.properties,
            c.style,
            c.events,
            c.position,
            c.parent_id,
            ct.level + 1
        FROM ui_components c
        JOIN component_tree ct ON c.parent_id = ct.id
    )
    SELECT jsonb_agg(
        jsonb_build_object(
            'id', component_id,
            'type', component_type,
            'properties', properties,
            'style', style,
            'events', events,
            'children', (
                SELECT COALESCE(jsonb_agg(sub.children ORDER BY sub.position), '[]'::jsonb)
                FROM (
                    SELECT 
                        jsonb_build_object(
                            'id', c2.component_id,
                            'type', c2.component_type,
                            'properties', c2.properties,
                            'style', c2.style,
                            'events', c2.events,
                            'children', '[]'::jsonb
                        ) AS children,
                        c2.position
                    FROM component_tree c2
                    WHERE c2.parent_id = component_tree.id
                ) sub
            )
        ) ORDER BY component_tree.position
    )
    INTO result
    FROM component_tree
    WHERE parent_id IS NULL;

    RETURN COALESCE(result, '[]'::jsonb);
END;
$$ LANGUAGE plpgsql;

-- 创建自动版本化函数
CREATE OR REPLACE FUNCTION create_template_version()
RETURNS TRIGGER AS $$
DECLARE
    template_data JSONB;
    components JSONB;
BEGIN
    -- 获取模板信息
    SELECT jsonb_build_object(
        'id', t.id,
        'screen_id', t.screen_id,
        'title', t.title,
        'version', t.version,
        'description', t.description
    ) INTO template_data
    FROM ui_templates t
    WHERE t.id = NEW.id;
    
    -- 获取组件树
    SELECT get_component_tree(NEW.id) INTO components;
    
    -- 创建版本快照
    INSERT INTO ui_template_versions(
        template_id, version, snapshot, created_by
    ) VALUES (
        NEW.id, 
        NEW.version, 
        jsonb_build_object(
            'template', template_data,
            'components', components
        ),
        NEW.created_by
    );
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER create_template_version_on_update
AFTER UPDATE OF version ON ui_templates
FOR EACH ROW EXECUTE FUNCTION create_template_version();

CREATE TRIGGER create_template_version_on_insert
AFTER INSERT ON ui_templates
FOR EACH ROW EXECUTE FUNCTION create_template_version(); 