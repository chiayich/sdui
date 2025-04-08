import { Component } from 'vue';
import SDContainer from './SDContainer.vue';
import SDText from './SDText.vue';
import SDButton from './SDButton.vue';
import SDInput from './SDInput.vue';
import SDList from './SDList.vue';
import SDTable from './SDTable.vue';
import SDInfiniteScroll from './SDInfiniteScroll.vue';
import SDSelect from './SDSelect.vue';
import SDCheckbox from './SDCheckbox.vue';
import SDRadio from './SDRadio.vue';
import SDSwitch from './SDSwitch.vue';
import SDRow from './SDRow.vue';
import SDCol from './SDCol.vue';
import SDCard from './SDCard.vue';
import SDDivider from './SDDivider.vue';
import SDIcon from './SDIcon.vue';
import SDTitle from './SDTitle.vue';
import SDFilterBar from './SDFilterBar.vue';
import SDHeader from './SDHeader.vue';

// 组件映射表类型
type ComponentMap = {
  [key: string]: any;
};

// 导出组件映射表
const componentMap: ComponentMap = {
  // 布局组件
  Header: SDHeader,
  header: SDHeader,

  // 容器组件
  Page: SDContainer,
  page: SDContainer,
  Container: SDContainer,
  container: SDContainer,
  Row: SDRow,
  row: SDRow,
  Col: SDCol,
  col: SDCol,
  Card: SDCard,
  card: SDCard,

  // 表单组件
  Input: SDInput,
  input: SDInput,
  Button: SDButton,
  button: SDButton,

  // 展示组件
  Text: SDText,
  text: SDText,
  Title: SDTitle,
  title: SDTitle,
  Icon: SDIcon,
  icon: SDIcon,
  Table: SDTable,
  table: SDTable,
  List: SDList,
  list: SDList,
  InfiniteScroll: SDInfiniteScroll,
  infinitescroll: SDInfiniteScroll,
  Select: SDSelect,
  select: SDSelect,
  Checkbox: SDCheckbox,
  checkbox: SDCheckbox,
  Radio: SDRadio,
  radio: SDRadio,
  Switch: SDSwitch,
  switch: SDSwitch,
  Divider: SDDivider,
  divider: SDDivider,

  // 过滤栏组件
  FilterBar: SDFilterBar,
  filterBar: SDFilterBar,
};

// 创建一个大小写不敏感的版本用于匹配
Object.keys(componentMap).forEach(key => {
  const lowerKey = key.toLowerCase();
  if (!componentMap[lowerKey]) {
    componentMap[lowerKey] = componentMap[key];
  }
});

export default componentMap; 