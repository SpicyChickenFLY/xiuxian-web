<template>
  <h3>
    自动化管理
    <el-switch
      v-model="isTaskMgrStart"
      size="large"
      inline-prompt
      active-text="运行"
      inactive-text="停止"
      @change="taskMgrToggle"
    />
  </h3>

  <el-input v-model="createTaskName" placeholder="新任务名称(建议使用用户名)">
    <template #append>
      <el-button type="success" @click="createTask">创建自动化任务</el-button>
    </template>
  </el-input>
  <el-table
    :data="tableData"
    size="small"
    :row-style="{ height: '20px' }"
    :cell-style="{ padding: '0px' }"
    style="width: 100%"
  >
    <el-table-column label="状态" width="100">
      <template #default="{ row }">
        <el-switch
          v-model="row.enable"
          size="large"
          inline-prompt
          :active-text="row.name"
          :inactive-text="row.name"
          @change="(val) => taskToggle(val, row.name)"
        />
      </template>
    </el-table-column>
    <el-table-column label="位置" width="160">
      <template #default="{ row }">
        <div v-if="!!row.bot">
          <el-tag size="large" @click="showLocationDialog(row.name, row.bot)">
            输入框({{ row.bot.i_x }}, {{ row.bot.i_y }})
            <br />
            消息框({{ row.bot.o_x }}, {{ row.bot.o_y }})</el-tag
          >
        </div>
      </template>
    </el-table-column>
    <el-table-column label="插件情况" min-width="180">
      <template #default="{ row }">
        <el-tag
          v-for="module of row.modules"
          :key="module.name"
          :type="module.enable ? 'success' : 'danger'"
          size="large"
          @click="setModuleEnable(!module.enable, row.name, module.name)"
        >
          {{ module.name }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column fixed="right" label="操作" min-width="80">
      <template #default="{ row }">
        <el-button
          plain
          :icon="Operation"
          @click="showModulesDialog(row['row-index'])"
        />
        <el-button
          plain
          :icon="FolderAdd"
          @click="saveTask(row.name)"
        />
        <el-button
          type="danger"
          :icon="Delete"
          @click="deleteTask(row.name)"
        />
      </template>
    </el-table-column>
  </el-table>

  <modules
    v-if="isModulesDialogVisible"
    v-model:visible="isModulesDialogVisible"
    :taskIdx="modulesTaskIdx"
    :tableData="tableData"
    @refresh="refresh"
  />
  <location
    v-if="isLocationDialogVisible"
    v-model:visible="isLocationDialogVisible"
    :task="locationTask"
    :info="locationInfo"
    @refresh="refresh"
  />
</template>

<script setup>
import { defineProps, ref, reactive, onMounted, onBeforeMount } from "vue";
import axios from "axios";
import { ElNotification, ElLoading } from "element-plus";
import { Operation, Delete, FolderAdd } from "@element-plus/icons-vue";

import Detail from "./detail.vue";
import Modules from "./modules.vue";
import Location from "./location.vue";

defineProps({
  msg: String,
});

const timer = reactive(null);
const tableData = ref([]);
const isTaskMgrStart = ref(false);
const createTaskName = ref("");
const isLocationDialogVisible = ref(false);
const locationTask = ref("");
const locationInfo = reactive({});

const isModulesDialogVisible = ref(false);
const modulesTaskIdx = ref(0);
onMounted(async () => {
  refresh();
  const timer = setInterval(() => {
    getTaskList();
  }, 5000);
  onBeforeMount(() => {
    clearInterval(timer);
  });
});

const refresh = async () => {
  await getTaskMgrStatus();
  await getTaskList();
};
const getTaskMgrStatus = async () => {
  axios.get("http://127.0.0.1:8010/taskMgr/status").then((res) => {
    isTaskMgrStart.value = res.data.result;
  });
};

const getTaskList = async () => {
  axios.get("http://127.0.0.1:8010/task/list").then((res) => {
    tableData.value = res.data;
  });
};

const postReq = async (url, data = null) => {
  const loading = ElLoading.service({
    lock: true,
    text: "请等待",
    background: "rgba(0, 0, 0, 0.7)",
  });
  axios
    .post(`http://127.0.0.1:8010/${url}`, data)
    .then((res) => {
      ElNotification({ title: "成功", message: "成功", type: "success" });
      loading.close();
      refresh();
    })
    .catch((error) => {
      ElNotification({ title: "失败", message: "程序异常", type: "error" });
    });
};

function taskMgrToggle(val) {
  postReq(!!val ? "taskMgr/start" : "taskMgr/stop");
}

function taskToggle(val, taskName) {
  postReq(!!val ? `task/enable/${taskName}` : `task/disable/${taskName}`);
}

function saveTask(taskName) {
  postReq(`task/save/${taskName}`);
}

function deleteTask(taskName) {
  postReq(`task/delete/${taskName}`);
}

function createTask() {
  if (!!createTaskName.value) {
    postReq(`task/create/${createTaskName.value}`);
    createTaskName.value = "";
  } else {
    ElNotification({ title: "失败", message: "任务名不能为空", type: "error" });
  }
}

function setModuleEnable(val, taskName, moduleName) {
  postReq(
    !!val
      ? `module/enable/${taskName}/${moduleName}`
      : `module/disable/${taskName}/${moduleName}`,
  );
}

function showLocationDialog(taskName, location) {
  isLocationDialogVisible.value = true;
  locationTask.value = taskName;
  locationInfo.value = location;
}

function showModulesDialog(taskIdx) {
  isModulesDialogVisible.value = true;
  modulesTaskIdx.value = taskIdx;
}
</script>

<style scoped>
a {
  color: #42b983;
}

.el-switch {
  --el-switch-on-color: #95d475;
  --el-switch-off-color: #f89898;
}
</style>
