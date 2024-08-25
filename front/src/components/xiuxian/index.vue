<template>
  <h1>
    修仙机器人自动化管理
    <el-button type="success" @click="handleClick">创建自动化任务</el-button>
  </h1>

  <el-table :data="tableData" style="width: 100%">
    <el-table-column prop="name" label="道号" width="180" />
    <el-table-column prop="modules" label="插件情况" />
    <el-table-column fixed="right" label="操作" min-width="120">
      <template #default>
        <el-button type="primary" size="small" @click="handleClick">详情</el-button>
        <el-button type="danger" size="small" @click="handleClick">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

</template>

<script setup>
import { defineProps, reactive, onMounted } from 'vue'

defineProps({
  msg: String
})


const state = reactive({ count: 0 })
const data = reactive({ text1: "" })

const tableData = []

onMounted(async () => {
  const rsp2 = await fetch(`http://127.0.0.1:8010/task/list`, {method: 'GET'}).then(rsp => rsp.text())
  tableData = rsp2
})
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
