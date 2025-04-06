import axios, { AxiosRequestConfig } from 'axios';
import router from './router';

// 创建axios统一配置实例
const api = axios.create({
    baseURL: '',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求状态记录
const pendingRequests = new Map();

// 请求拦截器 - 添加认证信息和重复请求控制
api.interceptors.request.use(config => {
    // 生成请求的唯一标识符
    const url = config.url;
    const method = config.method || 'get';
    const requestId = `${method}-${url}`;

    // 检查该请求是否正在进行中
    if (pendingRequests.has(requestId)) {
        // 如果相同的请求已在处理中，取消本次请求
        console.log(`请求已在进行中，取消重复请求: ${requestId}`);
        return Promise.reject(new Error('重复请求已取消'));
    }

    // 记录请求
    pendingRequests.set(requestId, true);

    // 从本地获取认证令牌并添加到请求头
    const token = localStorage.getItem('auth_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
}, error => {
    return Promise.reject(error);
});

// 响应拦截器 - 处理错误和清理请求状态
api.interceptors.response.use(
    response => {
        // 请求完成后，清除请求记录
        const url = response.config.url;
        const method = response.config.method || 'get';
        const requestId = `${method}-${url}`;
        pendingRequests.delete(requestId);

        return response;
    },
    error => {
        // 请求异常时，也需要清除请求记录
        if (error.config) {
            const url = error.config.url;
            const method = error.config.method || 'get';
            const requestId = `${method}-${url}`;
            pendingRequests.delete(requestId);
        }

        // 处理401错误 - 未授权
        if (error.response && error.response.status === 401) {
            console.log('拦截到401错误，重定向到登录页');
            localStorage.removeItem('auth_token');
            router.push('/login');
        }

        return Promise.reject(error);
    }
);

// 工具函数 - 清除所有正在进行的请求
export const clearAllRequests = () => {
    pendingRequests.clear();
};

// 工具函数 - 添加缓存控制
export const addNoCacheHeaders = (config: AxiosRequestConfig = {}) => {
    return {
        ...config,
        headers: {
            ...(config.headers || {}),
            'Cache-Control': 'no-cache, no-store',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    };
};

export default api; 