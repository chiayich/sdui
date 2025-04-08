import axios from 'axios';

// 接口类型定义
export interface SDUIConfig {
    id: string;
    type: string;
    title?: string;
    is_public?: boolean;
    content?: any[];
    styles?: Record<string, any>;
    scripts?: Record<string, any>;
    [key: string]: any;
}

// SDUI接口服务
export const sduiService = {
    /**
     * 获取页面配置
     * @param configCode - 配置代码
     */
    getConfig: async (configCode: string): Promise<SDUIConfig> => {
        const response = await axios.get(`/api/sdui/${configCode}`);
        return response.data;
    },

    /**
     * 获取公共页面配置（无需认证）
     * @param configCode - 配置代码
     */
    getPublicConfig: async (configCode: string): Promise<SDUIConfig> => {
        const response = await axios.get(`/api/sdui/public/${configCode}`);
        return response.data;
    }
};

export default sduiService; 