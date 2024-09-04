<template>
  <h3>
    自动化管理
    <el-switch
      v-model="isMgrRunning"
      size="large"
      inline-prompt
      active-text="运行"
      inactive-text="停止"
      @change="updateMgrInfo"
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
          @change="(val) => taskToggle(row.name, val)"
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
          @click="moduleToggle(row.name, module.name, !module.enable)"
        >
          {{ module.name }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column fixed="right" label="操作" min-width="40">
      <template #default="scope">
        <el-button
          plain
          :icon="Operation"
          @click="showModulesDialog(scope.$index)"
        />
        <el-button
          type="danger"
          :icon="Delete"
          @click="deleteTask(scope.row.name)"
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

import Modules from "./modules.vue";
import Location from "./location.vue";

defineProps({
  msg: String,
});

const timer = reactive(null);
const tableData = ref([]);
const isMgrRunning = ref(false);
const createTaskName = ref("");
const isLocationDialogVisible = ref(false);
const locationTask = ref("");
const locationInfo = reactive({});

const isModulesDialogVisible = ref(false);
const modulesTaskIdx = ref(0);

const loadingData = {
  lock: true,
  text: "请等待",
  background: "rgba(0, 0, 0, 0.7)",
};

onMounted(async () => {
  refresh();
  const timer = setInterval(() => {
    refresh();
  }, 5000);
  onBeforeMount(() => {
    clearInterval(timer);
  });
});

const onError = async (msg, error) => {
  ElNotification({
    title: "失败",
    message: `${msg} - ${error}`,
    type: "error",
  });
};

const refresh = async () => getMgrInfo();
const getMgrInfo = async () => {
  axios.get("/api/mgr").then((res) => {
    tableData.value = res.data.data.tasks;
    isMgrRunning.value = res.data.data.is_running;
  })
  .catch((error) => onError("获取管理器信息失败", error));
};

const updateMgrInfo = async (val) => {
  const loading = ElLoading.service(loadingData);
  axios
    .put("/api/mgr", { is_running: !!val })
    .then((res) => {
      loading.close();
      refresh();
    })
    .catch((error) => onError("更新管理器状态失败", error));
};

const createTask = async () => {
  if (!createTaskName.value) {
    onError("创建任务失败", "任务名不能为空");
    return;
  }
  const loading = ElLoading.service(loadingData);
  axios
    .post(`/api/mgr/task/${createTaskName.value}`, {})
    .then((res) => {
      createTaskName.value = "";
      loading.close();
      refresh();
    })
    .catch((error) => onError("创建任务失败", error));
};

const taskToggle = async (taskName, enable) =>
  updateTask(taskName, { enable: enable });

const updateTask = async (taskName, taskData) => {
  if (!taskName) {
    onError("更新任务失败", "任务名不能为空");
    return;
  }
  const loading = ElLoading.service(loadingData);
  axios
    .post(`/api/mgr/task/${taskName}`, taskData)
    .then((res) => {
      loading.close();
      refresh();
    })
    .catch((error) => onError("更新任务失败", error));
};

const deleteTask = async (taskName) => {
  if (!taskName) {
    onError("删除任务失败", "任务名不能为空");
    return;
  }
  const loading = ElLoading.service(loadingData);
  axios
    .delete(`/api/mgr/task/${taskName}`, {})
    .then((res) => {
      loading.close();
      refresh();
    })
    .catch((error) => onError("删除任务失败", error));
};

const moduleToggle = async (taskName, moduleName, enable) =>
  updateModule(taskName, moduleName, { enable: enable });

const updateModule = async (taskName, moduleName, moduleData) => {
  if (!taskName || !moduleName) {
    onError("更新模块失败", "任务名/模块名不能为空");
    return;
  }
  const loading = ElLoading.service(loadingData);
  axios
    .put(`/api/mgr/task/${taskName}/module/${moduleName}`, moduleData)
    .then((res) => {
      loading.close();
      refresh();
    })
    .catch((error) => onError("更新模块失败", error));
};

function showLocationDialog(taskName, location) {
  isLocationDialogVisible.value = true;
  locationTask.value = taskName;
  locationInfo.value = location;
}

function showModulesDialog(taskIdx) {
  console.log(taskIdx);
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
