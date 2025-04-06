<template>
    <nav class="nav-menu">
        <div class="logo-container">
            <img v-if="config?.logo" :src="config.logo" alt="Logo" class="logo" />
            <h1 v-if="config?.title">{{ config.title }}</h1>
        </div>

        <div class="menu-items">
            <template v-if="config?.items && config.items.length > 0">
                <div v-for="(item, index) in config.items" :key="`nav-item-${index}`" class="menu-item"
                    :class="{ 'active': isActiveRoute(item.route) }">
                    <router-link v-if="item.route" :to="item.route" class="menu-link">
                        <i v-if="item.icon" :class="item.icon"></i>
                        <span>{{ item.label }}</span>
                    </router-link>

                    <div v-else-if="item.items" class="menu-dropdown" @click="toggleSubmenu(index)">
                        <div class="dropdown-header">
                            <i v-if="item.icon" :class="item.icon"></i>
                            <span>{{ item.label }}</span>
                            <i class="dropdown-arrow" :class="openSubmenus.includes(index) ? 'up' : 'down'"></i>
                        </div>

                        <div v-if="openSubmenus.includes(index)" class="submenu">
                            <router-link v-for="(subitem, subindex) in item.items" :key="`submenu-${index}-${subindex}`"
                                :to="subitem.route" class="submenu-item"
                                :class="{ 'active': isActiveRoute(subitem.route) }">
                                <i v-if="subitem.icon" :class="subitem.icon"></i>
                                <span>{{ subitem.label }}</span>
                            </router-link>
                        </div>
                    </div>
                </div>
            </template>

            <div v-else class="no-menu-items">
                <p>No menu items available</p>
            </div>
        </div>

        <div class="menu-footer" v-if="config?.footer">
            {{ config.footer }}
        </div>
    </nav>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps({
    config: {
        type: Object,
        default: () => ({
            title: 'SDUI Application',
            items: []
        })
    }
});

const route = useRoute();
const openSubmenus = ref<number[]>([]);

// 切换子菜单的展开/折叠状态
const toggleSubmenu = (index: number) => {
    const position = openSubmenus.value.indexOf(index);
    if (position === -1) {
        openSubmenus.value.push(index);
    } else {
        openSubmenus.value.splice(position, 1);
    }
};

// 检查路由是否激活
const isActiveRoute = (path: string): boolean => {
    if (!path) return false;

    // 精确匹配
    if (route.path === path) return true;

    // 前缀匹配（用于子路由）
    if (path !== '/' && route.path.startsWith(path)) return true;

    return false;
};
</script>

<style scoped>
.nav-menu {
    display: flex;
    flex-direction: column;
    background-color: #f5f5f5;
    border-right: 1px solid #e0e0e0;
    width: 240px;
    height: 100%;
    padding: 16px 0;
}

.logo-container {
    display: flex;
    align-items: center;
    padding: 0 16px 16px;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 16px;
}

.logo {
    max-height: 40px;
    margin-right: 12px;
}

.logo-container h1 {
    font-size: 18px;
    margin: 0;
    font-weight: 500;
}

.menu-items {
    flex: 1;
    overflow-y: auto;
}

.menu-item {
    margin-bottom: 4px;
}

.menu-link {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    color: #333;
    text-decoration: none;
    transition: background-color 0.2s;
}

.menu-link:hover,
.menu-link.active {
    background-color: #e8e8e8;
}

.menu-link.active {
    border-left: 3px solid #1976d2;
    font-weight: 500;
}

.menu-link i {
    margin-right: 12px;
    width: 20px;
    text-align: center;
}

.menu-dropdown {
    cursor: pointer;
}

.dropdown-header {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    transition: background-color 0.2s;
}

.dropdown-header:hover {
    background-color: #e8e8e8;
}

.dropdown-arrow {
    margin-left: auto;
    transition: transform 0.2s;
}

.dropdown-arrow.up {
    transform: rotate(180deg);
}

.submenu {
    background-color: #f0f0f0;
    padding: 8px 0;
}

.submenu-item {
    display: flex;
    align-items: center;
    padding: 8px 16px 8px 32px;
    color: #333;
    text-decoration: none;
    transition: background-color 0.2s;
}

.submenu-item:hover,
.submenu-item.active {
    background-color: #e0e0e0;
}

.submenu-item.active {
    border-left: 3px solid #1976d2;
    font-weight: 500;
}

.submenu-item i {
    margin-right: 8px;
    width: 16px;
    text-align: center;
}

.no-menu-items {
    padding: 16px;
    color: #999;
    text-align: center;
}

.menu-footer {
    margin-top: auto;
    padding: 16px;
    border-top: 1px solid #e0e0e0;
    font-size: 12px;
    color: #666;
    text-align: center;
}
</style>