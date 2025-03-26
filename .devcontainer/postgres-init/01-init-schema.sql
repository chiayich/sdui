-- 创建sdui_schema
CREATE SCHEMA IF NOT EXISTS sdui_schema;

-- 创建初始表结构
CREATE TABLE IF NOT EXISTS sdui_schema.sdui_demo (
    id SERIAL PRIMARY KEY,
    component_type VARCHAR(50) NOT NULL,
    component_name VARCHAR(100) NOT NULL,
    properties JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sdui_schema.ui_templates (
    id SERIAL PRIMARY KEY,
    screen_id VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS sdui_schema.components (
    id SERIAL PRIMARY KEY,
    template_id INTEGER REFERENCES sdui_schema.ui_templates(id) ON DELETE CASCADE,
    component_id VARCHAR(50) NOT NULL,
    component_type VARCHAR(50) NOT NULL,
    parent_id INTEGER REFERENCES sdui_schema.components(id),
    position INTEGER NOT NULL,
    properties JSONB NOT NULL DEFAULT '{}',
    style JSONB NOT NULL DEFAULT '{}',
    actions JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 插入初始测试数据
INSERT INTO sdui_schema.sdui_demo (component_type, component_name, properties)
VALUES 
    ('container', 'MainContainer', '{"style": {"width": "100%", "padding": "16px"}, "layout": "column"}'),
    ('text', 'TitleText', '{"content": "Welcome to SDUI", "fontSize": 24, "fontWeight": "bold", "color": "#333"}'),
    ('button', 'SubmitButton', '{"label": "Submit", "type": "primary", "action": "submit_form"}'),
    ('input', 'NameInput', '{"placeholder": "Enter your name", "type": "text", "validation": {"required": true}}'),
    ('card', 'InfoCard', '{"title": "Information", "shadow": true, "padding": 16}');

-- 创建一个简单的模板示例
INSERT INTO sdui_schema.ui_templates (screen_id, title, version, description)
VALUES ('home', 'Home Screen', '1.0.0', 'Home screen with basic components');

-- 获取插入的模板ID
DO $$
DECLARE
    template_id INTEGER;
    parent_id INTEGER;
BEGIN
    SELECT id INTO template_id FROM sdui_schema.ui_templates WHERE screen_id = 'home';
    
    -- 插入主容器
    INSERT INTO sdui_schema.components (template_id, component_id, component_type, parent_id, position, properties, style)
    VALUES (template_id, 'main-container', 'container', NULL, 1, '{"layout": "column"}', '{"padding": 16}')
    RETURNING id INTO parent_id;
    
    -- 插入标题文本
    INSERT INTO sdui_schema.components (template_id, component_id, component_type, parent_id, position, properties, style)
    VALUES (template_id, 'welcome-text', 'text', parent_id, 1, '{"content": "Welcome to SDUI"}', '{"fontSize": 24, "fontWeight": "bold"}');
    
    -- 插入按钮
    INSERT INTO sdui_schema.components (template_id, component_id, component_type, parent_id, position, properties, style, actions)
    VALUES (template_id, 'action-button', 'button', parent_id, 2, '{"label": "Click Me"}', '{"marginTop": 16}', '[{"type": "navigate", "target": "detail"}]');
END $$; 