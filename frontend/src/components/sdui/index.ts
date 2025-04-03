import { Component } from 'vue';
import SDContainer from './SDContainer.vue';
import SDText from './SDText.vue';
import SDButton from './SDButton.vue';

// 定义组件映射表接口
interface ComponentMap {
  [key: string]: Component;
}

// 导出组件映射表
const componentMap: ComponentMap = {
  container: SDContainer,
  text: SDText,
  button: SDButton,
};

export default componentMap; 