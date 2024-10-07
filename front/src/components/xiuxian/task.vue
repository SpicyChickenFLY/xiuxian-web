<template>
  <div>
    <el-space>
      <el-switch
        v-model="isMgrRunning"
        size="default"
        inline-prompt
        active-text="自动化"
        inactive-text="自动化"
        @change="updateMgrInfo"
      />
      <el-select v-model="moduleListMode" size="small" style="width: 80px">
        <el-option
          v-for="o in moduleListModeOpts"
          :key="o.value"
          :label="o.label"
          :value="o.value"
        />
      </el-select>
      <!-- <el-radio-group -->
      <!--   v-model="moduleListMode" -->
      <!--   size="small" -->
      <!--   :fill="moduleListModeFillColorMap[moduleListMode]" -->
      <!-- > -->
      <!--   <el-radio-button label="全部组件" value="all" /> -->
      <!--   <el-radio-button label="已启用" value="enabled" /> -->
      <!--   <el-radio-button label="今日" value="today" /> -->
      <!--   <el-radio-button label="待触发" value="ready" /> -->
      <!-- </el-radio-group> -->
      <el-switch
        v-model="isCollapseAccordion"
        inline-prompt
        active-text="风琴折叠"
        inactive-text="随意展开"
        @change="changeCollapseAccordion"
      />
      <el-button size="small" type="primary" :icon="Plus" @click="createTask" />
      <el-button size="small" type="primary" :icon="Camera" @click="screen" />
    </el-space>
    <el-collapse v-if="isCollapseAccordion" v-model="activeTask" accordion>
      <el-collapse-item
        v-for="task in taskListData"
        :key="task.name"
        :name="task.name"
      >
        <template #title>
          <el-space>
            <el-switch
              v-model="task.enable"
              size="default"
              width="80"
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
              <el-tag
                :type="task.modules.length > 0 ? 'primary' : 'info'"
                size="small"
              >
                <a>插件 {{ task.modules.length }}</a>
              </el-tag>
              <el-tag
                :type="
                  filterModules(task.modules, 'enable').length > 0
                    ? 'success'
                    : 'info'
                "
                size="small"
              >
                <a>已启用 {{ filterModules(task.modules, "enable").length }}</a>
              </el-tag>
              <el-tag
                :type="
                  filterModules(task.modules, 'ready').length > 0
                    ? 'warning'
                    : 'info'
                "
                size="small"
              >
                <a>待触发 {{ filterModules(task.modules, "ready").length }}</a>
              </el-tag>
            </span>
            <el-button
              plain
              type="info"
              size="small"
              :icon="Promotion"
              @click.stop.prevent="showCmdDialog(task.name)"
            />
          </el-space>
        </template>
        <el-table
          :data="filterModules(task.modules, moduleListMode)"
          size="small"
          border
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
                <a>{{ row.name }}</a>
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="上次触发" width="70">
            <template #default="{ row }">
              {{ calcDayTime(row.prev, "尚未触发") }}
            </template>
          </el-table-column>
          <el-table-column label="下次触发" width="70">
            <template #default="{ row }">
              <el-button
                :type="
                  !row.enable || (!!row.next && row.next > moment().unix())
                    ? 'info'
                    : 'warning'
                "
                size="small"
                link
                @click="showNextDialog(task.name, row.name)"
              >
                {{ calcDayTime(row.next, "随时可以") }}
              </el-button>
            </template>
          </el-table-column>
          <el-table-column label="当前状态" width="100" show-overflow-tooltip>
            <template #default="{ row }">
              <el-button
                :type="row.enable ? 'primary' : 'info'"
                size="small"
                link
                @click="showProgressDialog(task.name, row.name)"
              >
                {{ !!row.progress ? row.progress : "未开始" }}
              </el-button>
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
    <el-collapse v-else v-model="activeTasks">
      <el-collapse-item
        v-for="task in taskListData"
        :key="task.name"
        :name="task.name"
      >
        <template #title>
          <el-space>
            <el-switch
              v-model="task.enable"
              size="default"
              width="80"
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
              <el-tag
                :type="task.modules.length > 0 ? 'primary' : 'info'"
                size="small"
              >
                <a>插件 {{ task.modules.length }}</a>
              </el-tag>
              <el-tag
                :type="
                  filterModules(task.modules, 'enable').length > 0
                    ? 'success'
                    : 'info'
                "
                size="small"
              >
                <a>已启用 {{ filterModules(task.modules, "enable").length }}</a>
              </el-tag>
              <el-tag
                :type="
                  filterModules(task.modules, 'ready').length > 0
                    ? 'warning'
                    : 'info'
                "
                size="small"
              >
                <a>待触发 {{ filterModules(task.modules, "ready").length }}</a>
              </el-tag>
            </span>
            <el-button
              plain
              type="info"
              size="small"
              :icon="Promotion"
              @click.stop.prevent="showCmdDialog(task.name)"
            />
          </el-space>
        </template>
        <el-table
          :data="filterModules(task.modules, moduleListMode)"
          size="small"
          border
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
                <a>{{ row.name }}</a>
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="上次触发" width="70">
            <template #default="{ row }">
              {{ calcDayTime(row.prev, "尚未触发") }}
            </template>
          </el-table-column>
          <el-table-column label="下次触发" width="70">
            <template #default="{ row }">
              <el-button
                :type="
                  !row.enable || (!!row.next && row.next > moment().unix())
                    ? 'info'
                    : 'warning'
                "
                size="small"
                link
                @click="showNextDialog(task.name, row.name)"
              >
                {{ calcDayTime(row.next, "随时可以") }}
              </el-button>
            </template>
          </el-table-column>
          <el-table-column label="当前状态" width="100" show-overflow-tooltip>
            <template #default="{ row }">
              <el-button
                :type="row.enable ? 'primary' : 'info'"
                size="small"
                link
                @click="showProgressDialog(task.name, row.name)"
              >
                {{ !!row.progress ? row.progress : "未开始" }}
              </el-button>
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
      :taskName="updateTaskName"
      :info="locationInfo"
      @refresh="refresh"
    />
    <cmd
      v-if="isCmdDialogVisible"
      v-model:visible="isCmdDialogVisible"
      :taskName="updateTaskName"
      @refresh="refresh"
    />

    <module-progress
      v-if="isProgressDialogVisible"
      v-model:visible="isProgressDialogVisible"
      :taskName="updateTaskName"
      :moduleName="updateModuleName"
      @refresh="refresh"
    />
    <module-next
      v-if="isNextDialogVisible"
      v-model:visible="isNextDialogVisible"
      :taskName="updateTaskName"
      :moduleName="updateModuleName"
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
  computed,
} from "vue";
import axios from "axios";
import moment from "moment";
import { ElNotification, ElLoading, ElMessageBox } from "element-plus";
import { Promotion, Camera, Plus } from "@element-plus/icons-vue";

import Cmd from "./cmd.vue";
import Location from "./location.vue";
import ModuleNext from "./module_next.vue";
import ModuleProgress from "./module_progress.vue";

const moduleListMode = ref("all"); // all, enabled, today, ready
const moduleListModeOpts = [
  { value: "all", label: "全部" },
  { value: "enabled", label: "已启用" },
  { value: "today", label: "今日" },
  { value: "ready", label: "待触发" },
];
const moduleListModeFillColorMap = {
  all: "#909399",
  enabled: "#67C23A",
  today: "#409EFF",
  ready: "#E6A23C",
};
const timer = reactive(null);
const isMgrRunning = ref(false);

const taskListData = ref([]);
const isCollapseAccordion = ref(true);
const activeTasks = ref([]);
const activeTask = ref("");

const isCmdDialogVisible = ref(false);
const isLocationDialogVisible = ref(false);
const isNextDialogVisible = ref(false);
const isProgressDialogVisible = ref(false);

const updateTaskName = ref("");
const updateModuleName = ref("");
const locationInfo = reactive({});

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
      taskListData.value = res.data.data.tasks;
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
  ElMessageBox.prompt("新任务名称(建议道号区分)", "新建任务", {
    confirmButtonText: "创建",
    cancelButtonText: "取消",
    inputPattern: /[\w]+/,
    inputErrorMessage: "任务名不能为空",
  }).then(({ value }) => {
    const loading = ElLoading.service(loadingData);
    axios
      .post(`/api/mgr/task/${value}`, {})
      .then((res) => {
        loading.close();
        refresh();
      })
      .catch((error) => onError("创建任务失败", error));
  });
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

function screen() {
  window.open("/api/screen");
}

function changeCollapseAccordion(val) {
  if (val) {
    activeTask.value = "";
    if (taskListData.value.length > 0)
      activeTask.value = taskListData.value[0].name;
  } else {
    activeTasks.value = taskListData.value.map((task) => task.name);
  }
}

function showLocationDialog(taskName, location) {
  isLocationDialogVisible.value = true;
  updateTaskName.value = taskName;
  locationInfo.value = location;
}

function showCmdDialog(taskName) {
  isCmdDialogVisible.value = true;
  updateTaskName.value = taskName;
}

function showNextDialog(taskName, moduleName) {
  isNextDialogVisible.value = true;
  updateTaskName.value = taskName;
  updateModuleName.value = moduleName;
}

function showProgressDialog(taskName, moduleName) {
  // isProgressDialogVisible.value = true;
  // updateTaskName.value = taskName;
  // updateModuleName.value = moduleName;
}

function calcDayTime(tsStr, missStr) {
  if (!tsStr) {
    return missStr;
  }
  const ts = moment.unix(parseInt(tsStr));
  const today = moment().startOf("day");
  const time = ts.format("HH:mm:ss");
  const diff = Math.trunc(moment(ts.startOf("day").diff(today, "days")));
  if (diff > 0) return diff + "天后 ";
  if (diff < 0) return diff * -1 + "天前 ";
  return time;
}

function filterModules(moduleList, mode) {
  const filteredModuleList = moduleList.filter((m) => {
    const needEnableList = ["enabled", "today", "ready"];
    const beforeToday = m.next > moment().endOf("day").unix();
    const inFuture = m.next >= moment().unix();

    if (needEnableList.includes(mode) && !m.enable) return false;
    if (mode === "today" && beforeToday) return false;
    if (mode === "ready" && inFuture) return false;

    return true;
  });
  const sortFn = (a, b) => a.priority > b.priority;
  return filteredModuleList.sort(sortFn);
}
</script>

<style scoped>
:deep(.el-table--small .el-table__cell) {
  padding: 0;
}
:deep(.el-collapse-item__content) {
  padding-bottom: 5px;
}
:deep(.el-collapse-item__header) {
  height: 30px;
}
:deep(.el-table__empty-block) {
  min-height: 30px;
}
:deep(.el-table__empty-text) {
  line-height: 20px;
  height: 20px;
}
:deep(.el-switch) {
  --el-switch-on-color: #95d475;
  --el-switch-off-color: #f89898;
}
</style>
