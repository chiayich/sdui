import axios from 'axios';

// 创建axios实例用于认证API
const authApi = axios.create({
    baseURL: '', // 使用相对路径，将通过Vite的代理转发
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 接口类型定义
export interface LoginPayload {
    username: string;
    password: string;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
    user?: any;
}

export interface UserInfoResponse {
    id: number;
    username: string;
    email: string;
    full_name: string;
    is_active: boolean;
    is_superuser: boolean;
    permissions?: string[];
    roles?: any[];
}

// 认证相关API函数
export const authService = {
    /**
     * 用户登录
     * @param payload - 登录载荷
     */
    login: async (payload: LoginPayload): Promise<LoginResponse> => {
        // 使用application/x-www-form-urlencoded格式，这是OAuth2PasswordRequestForm所需的
        const params = new URLSearchParams();
        params.append('username', payload.username);
        params.append('password', payload.password);

        const response = await authApi.post('/api/v1/login/access-token', params, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        });

        console.log('Login response:', response);
        return response.data;
    },

    /**
     * 获取当前用户信息
     * @param token - 认证令牌
     */
    getUserInfo: async (token: string): Promise<UserInfoResponse> => {
        const response = await authApi.get('/api/v1/users/me', {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return response.data;
    },

    /**
     * 保存认证令牌
     * @param token - 认证令牌
     */
    saveToken: (token: string): void => {
        localStorage.setItem('auth_token', token);
        // 设置全局请求头
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    },

    /**
     * 清除认证令牌
     */
    clearToken: (): void => {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_info');
        localStorage.removeItem('remember_me');
        delete axios.defaults.headers.common['Authorization'];
    },

    /**
     * 检查是否已认证
     */
    isAuthenticated: (): boolean => {
        return !!localStorage.getItem('auth_token');
    }
};

export default authService; 