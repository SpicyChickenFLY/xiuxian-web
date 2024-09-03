<template>
  <el-dialog
    top="15px"
    width="90%"
    :model-value="props.visible"
    @update:modelValue="emit('update:visible', $event)"
    :title="`任务 - ${taskName} 的 模块列表`"
  >
    <el-table
      :data="tableData[taskIdx].modules"
      size="small"
      :row-style="{ height: '20px' }"
      :cell-style="{ padding: '0px' }"
      style="width: 100%"
    >
      <el-table-column label="模块" width="150">
        <template #default="{ row }">
          <el-space>
            <el-switch
              v-model="row.enable"
              size="large"
              inline-prompt
              :active-text="row.name"
              :inactive-text="row.name"
              @change="(val) => setModuleEnable(val, row.name)"
            />
          </el-space>
        </template>
      </el-table-column>
      <el-table-column label="上次触发" width="140">
        <template #default="{ row }">
          <el-space>
            {{ calcDayTime(row.prev) }}
          </el-space>
        </template>
      </el-table-column>
      <el-table-column label="下次触发">
        <template #default="{ row, $index }">
          <el-space>
            {{ calcDayTime(row.next) }}
            <el-button
              type="primary"
              size="small"
              link
              @click="showNextDialog($index)"
              >设置</el-button
            >
          </el-space>
        </template>
      </el-table-column>
      <el-table-column label="当前状态" width="120">
        <template #default="{ row }">
          {{ !!row.progress ? row.progress : "未开始" }}
        </template>
      </el-table-column>
      <el-table-column label="当前等待" width="70">
        <template #default="{ row }">
          {{ !!row.wait ? row.wait : "无" }}
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
  taskIdx: { type: Number, default: 0 },
  tableData: { type: Object, default: {} },
});

const emit = defineEmits(["update:visible", "refresh"]);

const taskName = computed(() => {
  return props.tableData[props.taskIdx].name;
});

const isNextDialogVisible = ref(false);
const nextTaskName = ref("");
const nextModuleName = ref("");

onMounted(async () => {});

const postReq = async (url, data = null, callback = null) => {
  const loading = ElLoading.service({
    lock: true,
    text: "请等待",
    background: "rgba(0, 0, 0, 0.7)",
  });
  axios
    .post(`/api/${url}`, data)
    .then((res) => {
      ElNotification({ title: "成功", message: "成功", type: "success" });
      if (callback !== null) {
        callback(res);
      }
      loading.close();
      emit("refresh");
      return res;
    })
    .catch((error) => {
      ElNotification({ title: "失败", message: "程序异常", type: "error" });
    });
};

function setModuleEnable(val, module) {
  postReq(
    !!val
      ? `module/enable/${taskName.value}/${module}`
      : `module/disable/${taskName.value}/${module}`,
  );
}

function showNextDialog(moduleIdx) {
  isNextDialogVisible.value = true;
  nextTaskName.value = taskName.value;
  nextModuleName.value = props.tableData[props.taskIdx].modules[moduleIdx].name;
}

function calcDayTime(tsStr) {
  if (!tsStr) {
    return "未知"
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

const refreshModule = async () => {
  emit("refresh");
};
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
