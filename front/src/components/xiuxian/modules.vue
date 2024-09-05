<template>
  <el-dialog
    top="15px"
    width="90%"
    :model-value="props.visible"
    @update:modelValue="emit('update:visible', $event)"
    :title="`任务 - ${taskName} 的 模块列表`"
  >
    <el-table
      :data="props.taskData.modules"
      size="small"
      :row-style="{ height: '20px' }"
      :cell-style="{ padding: '0px' }"
      style="width: 100%"
    >
      <el-table-column label="模块" width="120">
        <template #default="{ row }">
          <el-space>
            <el-switch
              v-model="row.enable"
              size="large"
              inline-prompt
              :active-text="row.name"
              :inactive-text="row.name"
              @change="(val) => setModuleEnable(taskName, row.name, val)"
            />
          </el-space>
        </template>
      </el-table-column>
      <el-table-column label="上次触发" width="140">
        <template #default="{ row }">
          {{ calcDayTime(row.prev, "尚未触发") }}
        </template>
      </el-table-column>
      <el-table-column label="下次触发" width="140">
        <template #default="{ row, $index }">
          <el-button
            type="primary"
            size="small"
            link
            @click="showNextDialog($index)"
            >{{ calcDayTime(row.next, "随时可以") }}</el-button
          >
        </template>
      </el-table-column>
      <el-table-column label="当前状态" width="120">
        <template #default="{ row }">
          {{ !!row.progress ? row.progress : "未开始" }}
        </template>
      </el-table-column>
      <el-table-column label="当前等待" width="120">
        <template #default="{ row }">
          {{ !!row.wait ? row.wait : "无" }}
        </template>
      </el-table-column>
      <el-table-column label="执行结果">
        <template #default="{ row }">
          {{ !!row.log ? row.log : "无" }}
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>

  <next
    v-if="isNextDialogVisible"
    v-model:visible="isNextDialogVisible"
    :taskName="nextTaskName"
    :moduleName="nextModuleName"
    @refreshModule="refreshModule"
  />
</template>

<script setup>
import axios from "axios";
import { ElNotification, ElLoading, ElMessageBox } from "element-plus";
import { ref, reactive, onMounted, watch, computed } from "vue";
import Next from "./module_next.vue";
import moment from "moment";

const props = defineProps({
  visible: { type: Boolean, default: false },
  taskData: { type: Object, default: {} },
});

const emit = defineEmits(["update:visible", "refresh"]);

const taskName = computed(() => {
  return props.taskData.name;
});

const isNextDialogVisible = ref(false);
const nextTaskName = ref("");
const nextModuleName = ref("");

const loadingData = {
  lock: true,
  text: "请等待",
  background: "rgba(0, 0, 0, 0.7)",
};

const onError = async (msg, error) => {
  ElNotification({
    title: "失败",
    message: `${msg} - ${error}`,
    type: "error",
  });
};

const refreshModule = async () => {
  emit("refresh");
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
      refreshModule();
    })
    .catch((error) => onError("更新模块失败", error));
};

function showNextDialog(moduleIdx) {
  isNextDialogVisible.value = true;
  nextTaskName.value = taskName.value;
  nextModuleName.value = props.taskData.modules[moduleIdx].name;
}

function calcDayTime(tsStr, missStr) {
  if (!tsStr) {
    return missStr
  }
  const ts = moment.unix(parseInt(tsStr))
  const today = moment().startOf('day');
  let prefix = ""
  const time = ts.format("HH:mm:ss")
  const diff = Math.trunc(moment(ts.diff(today, 'days')));
  if (diff > 0) {
    prefix = diff + "天后 "
  }
  if (diff < 0) {
    prefix = (diff * -1) + "天前 "
  }
  return prefix + time
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
