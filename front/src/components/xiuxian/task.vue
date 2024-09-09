<template>
  <div>
    <el-row>
      <el-col :span="8">
        <el-switch
          v-model="isMgrRunning"
          size="large"
          inline-prompt
          active-text="自动化管理运行中"
          inactive-text="自动化管理停止"
          @change="updateMgrInfo"
        />
      </el-col>
      <el-col :span="16">
        <el-input
          v-model="createTaskName"
          placeholder="新任务名称(建议使用用户名)"
        >
          <template #append>
            <el-button @click="createTask">创建自动化任务</el-button>
          </template>
        </el-input>
      </el-col>
    </el-row>
    <el-collapse v-model="activeProgress" accordion>
      <el-collapse-item v-for="task in mgrData" :key="task.name">
        <template #title>
          <el-space>
            <el-switch
              v-model="task.enable"
              size="large"
              inline-prompt
              :active-text="task.name"
              :inactive-text="task.name"
              @change="(val) => setTaskEnable(task.name, val)"
              @click.stop.prevent=""
            />
            <el-button
              link
              type="primary"
              size="small"
              @click.stop.prevent="showLocationDialog(task.name, task.bot)"
            >
              输入框({{ task.bot.i_x }}, {{ task.bot.i_y }})
              <br />
              消息框({{ task.bot.o_x }}, {{ task.bot.o_y }})
            </el-button>
            <span>
              支持插件{{ task.modules.length }}
              /
              启用模块{{ task.modules.filter((obj) => obj.enable).length }}
              /
              就绪待触发模块
            </span>
            <span>
              <!-- 可触发模块{{ task.modules.filter(obj => obj.enable && obj.next).length }} -->
            </span>
          </el-space>
        </template>
        <el-table
          :data="task.modules"
          size="small"
          :row-style="{ height: '20px' }"
          :cell-style="{ padding: '0px' }"
          style="width: 100%"
        >
          <el-table-column label="模块" width="80">
            <template #default="{ row }">
              <el-tag
                :type="row.enable ? 'success' : 'danger'"
                size="small"
                @click="setModuleEnable(task.name, row.name, !row.enable)"
              >
                {{ row.name }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="上次触发" width="100">
            <template #default="{ row }">
              {{ calcDayTime(row.prev, "尚未触发") }}
            </template>
          </el-table-column>
          <el-table-column label="下次触发" width="100">
            <template #default="{ row }">
              <el-button
                type="primary"
                size="small"
                link
                @click="showNextDialog(task.name, row.name)"
                >{{ calcDayTime(row.next, "随时可以") }}</el-button
              >
            </template>
          </el-table-column>
          <el-table-column label="当前状态" width="100" show-overflow-tooltip>
            <template #default="{ row }">
              {{ !!row.progress ? row.progress : "未开始" }}
            </template>
          </el-table-column>
          <el-table-column label="当前等待" width="80" show-overflow-tooltip>
            <template #default="{ row }">
              {{ !!row.wait ? row.wait : "无" }}
            </template>
          </el-table-column>
          <el-table-column label="执行结果" show-overflow-tooltip>
            <template #default="{ row }">
              {{ !!row.log ? row.log : "无" }}
            </template>
          </el-table-column>
        </el-table>
      </el-collapse-item>
    </el-collapse>

    <location
      v-if="isLocationDialogVisible"
      v-model:visible="isLocationDialogVisible"
      :taskName="locationTask"
      :info="locationInfo"
      @refresh="refresh"
    />

    <next
      v-if="isNextDialogVisible"
      v-model:visible="isNextDialogVisible"
      :taskName="nextTask"
      :moduleName="nextModule"
      @refresh="refresh"
    />
  </div>
</template>

<script setup>
import {
  defineProps,
  ref,
  reactive,
  onMounted,
  onBeforeMount,
  onBeforeUnmount,
} from "vue";
import axios from "axios";
import moment from "moment";
import { ElNotification, ElLoading } from "element-plus";

import Location from "./location.vue";
import Next from "./next.vue";

const isLocationDialogVisible = ref(false);
const locationTask = ref("");
const locationInfo = reactive({});

const isNextDialogVisible = ref(false);
const nextTask = ref("");
const nextModule = ref("");

const activeProgress = ref("");
const createTaskName = ref("");

const timer = reactive(null);
const mgrData = ref([]);
const isMgrRunning = ref(false);

const loadingData = {
  lock: true,
  text: "请等待",
  background: "rgba(0, 0, 0, 0.7)",
};

onMounted(async () => {
  refresh();
  const timer = setInterval(() => refresh(), 5000);
  onBeforeMount(() => clearInterval(timer));
  onBeforeUnmount(() => clearInterval(timer));
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
  axios
    .get("/api/mgr")
    .then((res) => {
      mgrData.value = res.data.data.tasks;
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

const setTaskEnable = async (taskName, enable) =>
  updateTask(taskName, { enable: enable });

const updateTask = async (taskName, taskData) => {
  if (!taskName) {
    onError("更新任务失败", "任务名不能为空");
    return;
  }
  const loading = ElLoading.service(loadingData);
  axios
    .put(`/api/mgr/task/${taskName}`, taskData)
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

const setModuleEnable = async (taskName, moduleName, enable) =>
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

function showLocationDialog (taskName, location) {
  isLocationDialogVisible.value = true;
  locationTask.value = taskName;
  locationInfo.value = location;
}

function showNextDialog (taskName, moduleName) {
  isNextDialogVisible.value = true;
  nextTask.value = taskName;
  nextModule.value = moduleName;
}

function calcDayTime(tsStr, missStr) {
  if (!tsStr) {
    return missStr;
  }
  const ts = moment.unix(parseInt(tsStr));
  const today = moment().startOf("day");
  let prefix = "";
  const time = ts.format("HH:mm:ss");
  const diff = Math.trunc(moment(ts.diff(today, "days")));
  if (diff > 0) {
    prefix = diff + "天后 ";
  }
  if (diff < 0) {
    prefix = diff * -1 + "天前 ";
  }
  return prefix + time;
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
