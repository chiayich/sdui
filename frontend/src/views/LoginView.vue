<template>
    <div class="login-container">
        <div class="login-card">
            <h1 class="login-title">登录系统</h1>

            <div class="alert error" v-if="authStore.error">
                {{ authStore.error }}
            </div>

            <form @submit.prevent="handleLogin" class="login-form">
                <div class="form-group">
                    <label for="username">用户名</label>
                    <input type="text" id="username" v-model="credentials.username" placeholder="请输入用户名" required
                        :disabled="authStore.isLoading" />
                </div>

                <div class="form-group">
                    <label for="password">密码</label>
                    <input type="password" id="password" v-model="credentials.password" placeholder="请输入密码" required
                        :disabled="authStore.isLoading" />
                </div>

                <div class="form-group check">
                    <input type="checkbox" id="remember" v-model="credentials.remember"
                        :disabled="authStore.isLoading" />
                    <label for="remember">记住我</label>
                </div>

                <div class="form-group">
                    <button type="submit" class="login-button" :disabled="authStore.isLoading || !isFormValid">
                        <span v-if="authStore.isLoading">登录中...</span>
                        <span v-else>登录</span>
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

// 获取认证状态存储
const authStore = useAuthStore();
const router = useRouter();

// 登录表单数据
const credentials = ref({
    username: '',
    password: '',
    remember: false
});

// 表单有效性验证
const isFormValid = computed(() => {
    return credentials.value.username.trim() !== '' &&
        credentials.value.password.trim() !== '';
});

// 处理登录逻辑
const handleLogin = async () => {
    // 登录操作
    const success = await authStore.login(
        credentials.value.username,
        credentials.value.password
    );

    if (success) {
        // 登录成功，跳转到主页
        router.push('/');
    }
};
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f7fa;
}

.login-card {
    width: 100%;
    max-width: 400px;
    padding: 32px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.login-title {
    text-align: center;
    margin-bottom: 24px;
    color: #333;
    font-size: 1.8rem;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group.check {
    flex-direction: row;
    align-items: center;
    gap: 8px;
}

label {
    font-size: 0.9rem;
    color: #555;
    font-weight: 500;
}

input[type="text"],
input[type="password"] {
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

input[type="text"]:focus,
input[type="password"]:focus {
    border-color: #4a90e2;
    outline: none;
    box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

.login-button {
    padding: 12px;
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
}

.login-button:hover:not(:disabled) {
    background-color: #3a7bbf;
}

.login-button:disabled {
    background-color: #a0c3e8;
    cursor: not-allowed;
}

.alert {
    padding: 12px;
    border-radius: 4px;
    margin-bottom: 16px;
}

.alert.error {
    background-color: #fff1f0;
    border: 1px solid #ffccc7;
    color: #f5222d;
}
</style>