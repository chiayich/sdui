-- UI模板表
CREATE TABLE IF NOT EXISTS ui_templates (
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

-- 组件表
CREATE TABLE IF NOT EXISTS ui_components (
    id SERIAL PRIMARY KEY,
    template_id INTEGER REFERENCES ui_templates(id) ON DELETE CASCADE,
    component_id VARCHAR(50) NOT NULL,
    component_type VARCHAR(50) NOT NULL,
    parent_id INTEGER REFERENCES ui_components(id),
    position INTEGER NOT NULL,
    properties JSONB NOT NULL DEFAULT '{}',
    style JSONB NOT NULL DEFAULT '{}',
    events JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 增加索引提高查询效率
CREATE INDEX IF NOT EXISTS idx_components_template_id ON ui_components(template_id);
CREATE INDEX IF NOT EXISTS idx_components_parent_id ON ui_components(parent_id);

-- 版本管理表
CREATE TABLE IF NOT EXISTS ui_template_versions (
    id SERIAL PRIMARY KEY,
    template_id INTEGER REFERENCES ui_templates(id) ON DELETE CASCADE,
    version VARCHAR(20) NOT NULL,
    snapshot JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50)
);
CREATE INDEX IF NOT EXISTS idx_template_versions_template_id ON ui_template_versions(template_id);

-- A/B测试变体表
CREATE TABLE IF NOT EXISTS ui_template_variants (
    id SERIAL PRIMARY KEY,
    template_id INTEGER REFERENCES ui_templates(id) ON DELETE CASCADE,
    variant_name VARCHAR(50) NOT NULL,
    criteria JSONB NOT NULL DEFAULT '{}',
    weight INTEGER DEFAULT 50,
    is_active BOOLEAN DEFAULT TRUE,
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE
);
CREATE INDEX IF NOT EXISTS idx_template_variants_template_id ON ui_template_variants(template_id);

-- 变体组件覆盖表（用于A/B测试中覆盖特定组件）
CREATE TABLE IF NOT EXISTS ui_variant_components (
    id SERIAL PRIMARY KEY,
    variant_id INTEGER REFERENCES ui_template_variants(id) ON DELETE CASCADE,
    component_id VARCHAR(50) NOT NULL,
    properties JSONB NOT NULL DEFAULT '{}',
    style JSONB NOT NULL DEFAULT '{}',
    events JSONB NOT NULL DEFAULT '[]'
);
CREATE INDEX IF NOT EXISTS idx_variant_components_variant_id ON ui_variant_components(variant_id);

-- 使用记录表（分析和优化用）
CREATE TABLE IF NOT EXISTS ui_template_usage (
    id SERIAL PRIMARY KEY,
    template_id INTEGER REFERENCES ui_templates(id) ON DELETE CASCADE,
    variant_id INTEGER REFERENCES ui_template_variants(id) ON DELETE SET NULL,
    user_id VARCHAR(50),
    session_id VARCHAR(100),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    device_info JSONB,
    performance_metrics JSONB
);
CREATE INDEX IF NOT EXISTS idx_template_usage_template_id ON ui_template_usage(template_id);
CREATE INDEX IF NOT EXISTS idx_template_usage_timestamp ON ui_template_usage(timestamp);

-- 审计日志表
CREATE TABLE IF NOT EXISTS ui_audit_log (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER NOT NULL,
    action VARCHAR(50) NOT NULL,
    user_id VARCHAR(50),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    old_value JSONB,
    new_value JSONB
);
CREATE INDEX IF NOT EXISTS idx_audit_log_entity ON ui_audit_log(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_timestamp ON ui_audit_log(timestamp); 