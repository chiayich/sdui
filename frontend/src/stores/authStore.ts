import { defineStore } from 'pinia';
import authService, { UserInfoResponse } from '@/api/auth';

// 认证状态接口
interface AuthState {
    token: string | null;
    user: UserInfoResponse | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;
    isInitialized: boolean;
}

export const useAuthStore = defineStore('auth', {
    state: (): AuthState => ({
        token: localStorage.getItem('auth_token'),
        user: null,
        isAuthenticated: !!localStorage.getItem('auth_token'),
        isLoading: false,
        error: null,
        isInitialized: false
    }),

    getters: {
        // 获取当前用户
        currentUser: (state) => state.user,

        // 检查用户是否有特定权限
        hasPermission: (state) => (permission: string) => {
            if (!state.user || !state.user.permissions) return false;

            // 超级管理员拥有所有权限
            if (state.user.is_superuser) return true;

            return state.user.permissions.includes(permission);
        },

        // 检查用户是否有特定角色
        hasRole: (state) => (roleName: string) => {
            if (!state.user || !state.user.roles) return false;

            return state.user.roles.some(role => role.name === roleName);
        }
    },

    actions: {
        /**
         * 登录操作
         */
        async login(username: string, password: string) {
            this.isLoading = true;
            this.error = null;

            try {
                const response = await authService.login({ username, password });

                // 保存令牌
                this.token = response.access_token;
                authService.saveToken(response.access_token);
                this.isAuthenticated = true;

                // 获取用户信息
                await this.fetchUserInfo();

                return true;
            } catch (error: any) {
                this.isAuthenticated = false;
                this.token = null;
                this.user = null;
                this.error = error.response?.data?.detail || '登录失败';

                return false;
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * 登出操作
         */
        logout() {
            this.token = null;
            this.user = null;
            this.isAuthenticated = false;
            authService.clearToken();
        },

        /**
         * 获取当前用户信息
         */
        async fetchUserInfo() {
            if (!this.token) return null;

            this.isLoading = true;

            try {
                const userInfo = await authService.getUserInfo(this.token);
                this.user = userInfo;
                return userInfo;
            } catch (error: any) {
                this.error = '获取用户信息失败';
                console.error('获取用户信息失败:', error);
                return null;
            } finally {
                this.isLoading = false;
            }
        },

        /**
         * 初始化认证状态，确保只初始化一次
         * 返回Promise以便确保完成
         */
        async initAuth() {
            // 如果已经初始化完成，直接返回
            if (this.isInitialized) {
                console.log('[AUTH] 已初始化，跳过');
                return this.user;
            }

            console.log('[AUTH] 开始初始化');
            const token = localStorage.getItem('auth_token');

            if (token) {
                this.token = token;
                this.isAuthenticated = true;

                // 自动设置全局请求头的Authorization
                authService.saveToken(token);

                // 获取用户信息并等待完成
                try {
                    const user = await this.fetchUserInfo();
                    this.isInitialized = true;
                    console.log('[AUTH] 初始化完成');
                    return user;
                } catch (error) {
                    console.error('[AUTH] 初始化失败', error);
                    this.isInitialized = true; // 即使失败也标记为已初始化
                    return null;
                }
            } else {
                console.log('[AUTH] 未找到有效令牌');
                this.isInitialized = true;
                return null;
            }
        }
    }
});

export default useAuthStore; 