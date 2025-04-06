import { defineStore } from 'pinia';
import axios from 'axios';
import { ref, computed, watch } from 'vue';
import { useAuthStore } from './authStore';

// 用于跟踪请求状态的Map
const pendingRequests = new Map<string, Promise<any>>();

/**
 * SDUI状态管理，负责全局SDUI配置的获取和缓存
 * 确保应用范围内只请求一次配置信息
 */
export const useSduiStore = defineStore('sdui', () => {
    // 认证存储
    const authStore = useAuthStore();

    // 全局状态
    const isLoading = ref(false);
    const error = ref<string | null>(null);
    const isInitialized = ref(false);

    // 配置缓存
    const structureConfig = ref<any>(null);
    const homeConfig = ref<any>(null);
    const screenConfigs = ref<Map<string, any>>(new Map());

    // 计算属性：应用结构是否已加载
    const isStructureLoaded = computed(() => !!structureConfig.value);

    // 计算属性：首页配置是否已加载
    const isHomeLoaded = computed(() => !!homeConfig.value);

    // 计算属性：导航配置
    const navigationConfig = computed(() => structureConfig.value?.navigation || null);

    // 计算属性：全局组件
    const globalComponents = computed(() => structureConfig.value?.global_components || []);

    /**
     * 执行防重复请求
     * @param key 请求唯一标识
     * @param requestFn 请求函数
     */
    const executeRequest = async <T>(key: string, requestFn: () => Promise<T>): Promise<T> => {
        // 如果相同请求正在进行中，返回已有Promise
        if (pendingRequests.has(key)) {
            console.log(`[SDUI] 请求已在进行中，复用Promise: ${key}`);
            return pendingRequests.get(key)!;
        }

        // 创建新的Promise并保存
        const promise = requestFn().finally(() => {
            // 请求完成后删除缓存
            pendingRequests.delete(key);
        });

        pendingRequests.set(key, promise);
        return promise;
    };

    /**
     * 加载应用结构
     * @param force 是否强制重新加载
     */
    const loadStructure = async (force = false) => {
        // 如果已加载且不是强制刷新，直接返回
        if (isStructureLoaded.value && !force) {
            console.log('[SDUI] 应用结构已加载，跳过请求');
            return structureConfig.value;
        }

        // 如果未认证，不加载结构
        if (!authStore.isAuthenticated) {
            console.log('[SDUI] 未认证状态，跳过加载结构');
            return null;
        }

        const apiUrl = '/api/v1/sdui/structure';
        console.log('[SDUI] 开始加载应用结构...');

        // 防止重复请求机制
        const requestKey = `GET:${apiUrl}:${force ? Date.now() : 'default'}`;

        // 开始加载
        isLoading.value = true;
        error.value = null;

        try {
            const response = await executeRequest(requestKey, () =>
                axios.get(apiUrl, {
                    headers: {
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache'
                    }
                })
            );

            // 保存结构配置
            structureConfig.value = response.data;
            console.log('[SDUI] 应用结构加载成功：', {
                导航项: response.data?.navigation?.items?.length || 0,
                全局组件: response.data?.global_components?.length || 0
            });
            return response.data;
        } catch (err: any) {
            console.error('[SDUI] 加载应用结构失败:', err);
            error.value = '加载应用结构失败';

            // 处理认证错误
            if (err.response?.status === 401) {
                authStore.logout();
            }

            return null;
        } finally {
            isLoading.value = false;
        }
    };

    /**
     * 加载首页配置
     * @param force 是否强制重新加载
     */
    const loadHomeConfig = async (force = false) => {
        console.log(`[SDUI] loadHomeConfig调用，force=${force}, 当前状态:`, {
            已加载: isHomeLoaded.value,
            正在加载: isLoading.value,
            错误: error.value
        });

        // 如果已加载且不是强制刷新，直接返回
        if (isHomeLoaded.value && !force) {
            console.log('[SDUI] 首页配置已加载，直接返回缓存数据');
            return homeConfig.value;
        }

        const apiUrl = '/api/v1/sdui/home';
        console.log('[SDUI] 开始加载首页配置...');

        // 防止重复请求机制
        const requestKey = `GET:${apiUrl}:${force ? Date.now() : 'default'}`;
        console.log(`[SDUI] 使用请求键: ${requestKey}`);

        // 开始加载
        isLoading.value = true;
        error.value = null;

        try {
            console.log('[SDUI] 准备发送首页配置请求');
            const response = await executeRequest(requestKey, () =>
                axios.get(apiUrl, {
                    headers: {
                        'Cache-Control': 'no-cache, no-store',
                        'Pragma': 'no-cache',
                        'Expires': '0'
                    },
                    // 添加随机参数以防止浏览器缓存
                    params: force ? { _t: Date.now() } : {}
                })
            );

            console.log('[SDUI] 首页配置请求成功，数据:', response.data);

            // 保存首页配置
            homeConfig.value = response.data;
            console.log('[SDUI] 首页配置已保存到store');
            return response.data;
        } catch (err: any) {
            const status = err.response?.status;
            console.error(`[SDUI] 加载首页配置失败 [${status}]:`, err);

            // 具体错误消息
            const errMsg = err.response?.data?.detail || err.message || '未知错误';
            error.value = `加载首页配置失败: ${errMsg}`;

            // 如果是401错误，可能需要重新登录
            if (status === 401) {
                console.log('[SDUI] 检测到401未授权错误，可能需要重新登录');
            }

            return null;
        } finally {
            isLoading.value = false;
            console.log('[SDUI] 首页配置加载流程完成，isLoading设为false');
        }
    };

    /**
     * 加载特定屏幕的配置
     * @param screenId 屏幕ID
     * @param force 是否强制重新加载
     */
    const loadScreenConfig = async (screenId: string, force = false) => {
        // 如果已加载且不是强制刷新，直接返回
        if (screenConfigs.value.has(screenId) && !force) {
            console.log(`[SDUI] 屏幕配置 ${screenId} 已加载，跳过请求`);
            return screenConfigs.value.get(screenId);
        }

        const apiUrl = `/api/v1/sdui/${screenId}`;
        console.log(`[SDUI] 开始加载屏幕配置 ${screenId}...`);

        // 防止重复请求机制
        const requestKey = `GET:${apiUrl}:${force ? Date.now() : 'default'}`;

        // 开始加载
        isLoading.value = true;
        error.value = null;

        try {
            const response = await executeRequest(requestKey, () =>
                axios.get(apiUrl, {
                    headers: {
                        'Cache-Control': 'no-cache',
                        'Pragma': 'no-cache'
                    }
                })
            );

            // 保存屏幕配置
            screenConfigs.value.set(screenId, response.data);
            console.log(`[SDUI] 屏幕配置 ${screenId} 加载成功`);
            return response.data;
        } catch (err: any) {
            console.error(`[SDUI] 加载屏幕配置 ${screenId} 失败:`, err);
            error.value = `加载屏幕 ${screenId} 配置失败`;
            return null;
        } finally {
            isLoading.value = false;
        }
    };

    /**
     * 初始化SDUI状态（应用启动时调用一次）
     */
    const initialize = async () => {
        if (isInitialized.value) {
            console.log('[SDUI] 已初始化，跳过');
            return;
        }

        isInitialized.value = true;
        console.log('[SDUI] 开始初始化...');

        // 如果已认证，立即加载结构
        if (authStore.isAuthenticated && authStore.isInitialized) {
            await loadStructure();
            console.log('[SDUI] 初始化完成，结构已加载');
        } else {
            console.log('[SDUI] 未认证或认证未初始化，跳过加载结构');
        }
    };

    /**
     * 清除所有缓存
     */
    const clearCache = () => {
        structureConfig.value = null;
        homeConfig.value = null;
        screenConfigs.value.clear();
        console.log('[SDUI] 缓存已清除');
    };

    // 监听认证状态变化
    watch(() => authStore.isAuthenticated, async (isAuthenticated) => {
        console.log(`[SDUI] 认证状态变化: ${isAuthenticated ? '已登录' : '未登录'}`);
        if (isAuthenticated) {
            // 用户登录后，加载系统结构
            console.log('[SDUI] 用户已登录，加载系统结构');
            await loadStructure();
        } else {
            // 用户登出后，清除缓存
            console.log('[SDUI] 用户已登出，清除缓存');
            clearCache();
        }
    });

    return {
        // 状态
        isLoading,
        error,
        isInitialized,
        isStructureLoaded,
        isHomeLoaded,

        // 配置数据
        structureConfig,
        homeConfig,
        navigationConfig,
        globalComponents,

        // 方法
        loadStructure,
        loadHomeConfig,
        loadScreenConfig,
        initialize,
        clearCache
    };
});

export default useSduiStore; 