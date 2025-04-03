-- 设置当前用户（用于审计）
-- 注释掉有问题的设置，PostgreSQL版本可能不支持这种语法
-- SET LOCAL app.current_user = 'system';

-- 清理数据（仅测试环境使用）
TRUNCATE ui_template_versions CASCADE;
TRUNCATE ui_components CASCADE;
TRUNCATE ui_templates CASCADE;
TRUNCATE ui_audit_log CASCADE;

-- 添加示例模板 - 首页
INSERT INTO ui_templates(screen_id, title, version, description, created_by, is_active)
VALUES ('home', '首页', '1.0.0', '应用首页模板', 'system', TRUE)
RETURNING id;

-- 保存返回的模板ID
DO $$
DECLARE
    home_template_id INTEGER;
    header_id INTEGER;
    content_id INTEGER;
BEGIN
    -- 获取首页模板ID
    SELECT id INTO home_template_id FROM ui_templates WHERE screen_id = 'home';
    
    -- 添加头部容器组件
    INSERT INTO ui_components(
        template_id, component_id, component_type, parent_id, position,
        properties, style, events
    ) VALUES (
        home_template_id, 'header', 'container', NULL, 0,
        '{}',
        '{"padding": "16px", "backgroundColor": "#f5f5f5"}',
        '{}'
    ) RETURNING id INTO header_id;
    
    -- 添加头部标题文本
    INSERT INTO ui_components(
        template_id, component_id, component_type, parent_id, position,
        properties, style, events
    ) VALUES (
        home_template_id, 'title', 'text', header_id, 0,
        '{"content": "SDUI 演示应用"}',
        '{"fontSize": "24px", "fontWeight": "bold"}',
        '{}'
    );
    
    -- 添加内容容器组件
    INSERT INTO ui_components(
        template_id, component_id, component_type, parent_id, position,
        properties, style, events
    ) VALUES (
        home_template_id, 'content', 'container', NULL, 1,
        '{}',
        '{"padding": "16px"}',
        '{}'
    ) RETURNING id INTO content_id;
    
    -- 添加欢迎文本
    INSERT INTO ui_components(
        template_id, component_id, component_type, parent_id, position,
        properties, style, events
    ) VALUES (
        home_template_id, 'welcome', 'text', content_id, 0,
        '{"content": "欢迎使用SDUI框架"}',
        '{"marginBottom": "16px"}',
        '{}'
    );
    
    -- 添加按钮
    INSERT INTO ui_components(
        template_id, component_id, component_type, parent_id, position,
        properties, style, events
    ) VALUES (
        home_template_id, 'details_button', 'button', content_id, 1,
        '{"label": "查看详情"}',
        '{"backgroundColor": "#1890ff", "color": "white", "padding": "8px 16px"}',
        '{"click": {"type": "navigation", "url": "/sdui/details"}}'
    );
END $$;

-- 添加示例模板 - 详情页
INSERT INTO ui_templates(screen_id, title, version, description, created_by, is_active)
VALUES ('details', '详情页', '1.0.0', '应用详情页模板', 'system', TRUE);

-- 添加详情页组件
DO $$
DECLARE
    details_template_id INTEGER;
    header_id INTEGER;
    content_id INTEGER;
BEGIN
    -- 获取详情页模板ID
    SELECT id INTO details_template_id FROM ui_templates WHERE screen_id = 'details';
    
    -- 添加头部容器组件
    INSERT INTO ui_components(
        template_id, component_id, component_type, parent_id, position,
        properties, style, events
    ) VALUES (
        details_template_id, 'header', 'container', NULL, 0,
        '{}',
        '{"padding": "16px", "backgroundColor": "#f5f5f5"}',
        '{}'
    ) RETURNING id INTO header_id;
    
    -- 添加头部标题文本
    INSERT INTO ui_components(
        template_id, component_id, component_type, parent_id, position,
        properties, style, events
    ) VALUES (
        details_template_id, 'title', 'text', header_id, 0,
        '{"content": "详情页"}',
        '{"fontSize": "24px", "fontWeight": "bold"}',
        '{}'
    );
    
    -- 添加内容容器组件
    INSERT INTO ui_components(
        template_id, component_id, component_type, parent_id, position,
        properties, style, events
    ) VALUES (
        details_template_id, 'content', 'container', NULL, 1,
        '{}',
        '{"padding": "16px"}',
        '{}'
    ) RETURNING id INTO content_id;
    
    -- 添加详情文本
    INSERT INTO ui_components(
        template_id, component_id, component_type, parent_id, position,
        properties, style, events
    ) VALUES (
        details_template_id, 'description', 'text', content_id, 0,
        '{"content": "这是一个SDUI驱动的UI示例"}',
        '{"marginBottom": "16px"}',
        '{}'
    );
    
    -- 添加返回按钮
    INSERT INTO ui_components(
        template_id, component_id, component_type, parent_id, position,
        properties, style, events
    ) VALUES (
        details_template_id, 'back_button', 'button', content_id, 1,
        '{"label": "返回首页"}',
        '{"backgroundColor": "#1890ff", "color": "white", "padding": "8px 16px"}',
        '{"click": {"type": "navigation", "url": "/sdui/home"}}'
    );
END $$; 