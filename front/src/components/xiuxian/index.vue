<template>
  <h1>
    自动化管理
    <el-switch v-model="isTaskMgrStart" size="large" inline-prompt active-text="运行" inactive-text="停止" />
  </h1>

  <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="name" label="识别号" width="180" />
    <el-table-column prop="modules" label="插件情况" min-width="180">
      <template #default="{ row }">
        <el-tag
          v-for="(module, key) of row.modules"
          :key="key"
          :type="row.enable ? 'success' : 'danger'"
        >
          {{ key }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column fixed="right" label="操作" min-width="120">
      <template #default="{ row }">
        <el-button type="primary" size="small" @click="showDetail"
          >详情</el-button
        >
        <el-button type="danger" size="small" @click="deleteTask(row.name)"
          >删除</el-button
        >
      </template>
    </el-table-column>
  </el-table>
  <el-button @click="getTaskList">刷新</el-button>
  <el-button type="success" @click="showCreate">创建自动化任务</el-button>

  <detail />

</template>

<script setup>
import { defineProps, ref, reactive, onMounted, onBeforeMount } from "vue";
import axios from "axios";
import { ElNotification } from 'element-plus'

import Detail from './detail.vue'
// import Create from './create.vue'

defineProps({
  msg: String,
});

const state = reactive({ count: 0 });
const data = reactive({ text1: "" });

const tableData = ref([{}]);
const isTaskMgrStart = ref(false);
const timer = reactive(null);
const isDetailDialogVisible = ref(false);
const isCreateDialogVisible = ref(false);

onMounted(async () => {
  getTaskList();
  const timer = setInterval(() => {
    getTaskList();
  }, 5000);
  onBeforeMount(() => {
    clearInterval(timer);
  });
});

const getTaskList = async () => {
  axios.get("http://127.0.0.1:8010/task/list").then((res) => {
    console.log(res.data);
    tableData.value = res.data;
  });
};

const showCreate = () => {
  isCreateDialogVisible = true;
};

const deleteTask = async (name) => {
  axios.post("http://127.0.0.1:8010/task/delete/"+name).then((res) => {
    ElNotification({
      title: '成功',
      message: '成功删除任务'+res.data.result,
      type: 'success',
    })
    this.getTaskList();
  });
};

const showDetail = () => {
  isDetailDialogVisible = true;
};
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
