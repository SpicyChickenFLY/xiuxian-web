<template>
  <el-tabs type="border-card" v-model="activeTab">
    <el-tab-pane label="任务" name="任务">
      <task v-if="activeTab === '任务'" />
    </el-tab-pane>
    <el-tab-pane label="插件" name="插件">
      <plugin v-if="activeTab === '插件'" />
    </el-tab-pane>
    <el-tab-pane label="方法" name="方法">
      <func v-if="activeTab === '方法'" />
    </el-tab-pane>
    <el-tab-pane label="数据" name="数据">
      <misc v-if="activeTab === '数据'" />
    </el-tab-pane>
  </el-tabs>
</template>

<script setup>
import { defineProps, ref, reactive, onMounted, onBeforeMount } from "vue";
import Next from "./module_next.vue";

import Task from "./task.vue";
import Plugin from "./plugin.vue";
import Func from "./func.vue";
import Misc from "./misc.vue";

const activeTab = ref("任务");

const isConfigDialogVisible = ref(false);

const isModulesDialogVisible = ref(false);
const moduleTaskIdx = ref(0);

function showConfigDialog (taskIdx) {
  isConfigDialogVisible.value = true;
}

function showModulesDialog (taskIdx) {
  isModulesDialogVisible.value = true;
  moduleTaskIdx.value = taskIdx;
}
</script>

<style scoped>
:deep(.el-switch){
  --el-switch-on-color: #95d475;
  --el-switch-off-color: #f89898;
}
</style>
