<template>
  <el-dialog
    width="90%"
    :model-value="props.visible"
    @update:modelValue="emit('update:visible', $event)"
    :title="`${taskName} 的 ${moduleName}模块 下次触发时间`"
  >
    <el-radio-group
      v-model="triggerType"
      style="margin-bottom: 20px"
    >
      <el-radio-button label="延迟触发" value="delay" />
      <el-radio-button label="指定触发" value="set" />
    </el-radio-group>

    <div v-if="triggerType === 'delay'">
      <el-input v-model="delayDuration">
        <template #prepend> 当前时间延迟 </template>
        <template #append>
          <el-select
            v-model="delayUnit"
            placeholder="单位"
            style="width: 100px"
          >
            <el-option label="秒" value="second" />
            <el-option label="分钟" value="minute" />
            <el-option label="小时" value="hour" />
            <el-option label="天" value="day" />
          </el-select>
        </template>
      </el-input>

      <el-button
        type="primary"
        style="margin-top: 20px"
        @click="setModuleNext(moment().add(delayDuration, delayUnit).unix())"
        >设置下次触发时间为
        {{
          moment().add(delayDuration, delayUnit).format("YYYY/MM/DD HH:mm:ss")
        }}</el-button
      >
    </div>
    <div v-else>
      <el-space>
        <span> 设置下次触发时间</span>
        <el-date-picker
          v-model="setTime"
          type="datetime"
          format="YYYY/MM/DD hh:mm:ss"
          value-format="x"
          size="large"
          style="width: 100%"
        />
      </el-space>
      <div style="width: 100%">
        <el-button
          type="primary"
          size="large"
          style="margin-top: 20px"
          @click="setModuleNext(moment(setTime).unix())"
          >设置下次触发时间为
          {{ moment(setTime).format("YYYY/MM/DD HH:mm:ss") }}</el-button
        >
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import axios from "axios";
import moment from "moment";
import { ElNotification, ElLoading, ElMessageBox } from "element-plus";
import { ref, reactive, onMounted } from "vue";

const props = defineProps({
  visible: { type: Boolean, default: false },
  taskName: { type: String, default: "" },
  moduleName: { type: String, default: "" },
});

const emit = defineEmits(["update:visible", "refresh"]);

const triggerType = ref("delay");
const delayDuration = ref(0);
const delayUnit = ref("second");
const setTime = ref(moment().format("YYYY/MM/DD HH:mm:ss"));

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

const setModuleNext = async (next) =>
  updateModule(props.taskName, props.moduleName, { next: next });

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
      emit("refresh");
      emit("update:visible", false);
    })
    .catch((error) => onError("更新模块失败", error));
};
</script>

<style scoped>

:deep(.el-dialog){
  --el-dialog-margin-top: 5vh;
  height: 90vh;
  overflow: scroll;
}
:deep(.el-switch){
  --el-switch-on-color: #95d475;
  --el-switch-off-color: #f89898;
}
</style>
