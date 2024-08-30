<template>
  <el-dialog
    width="90%"
    :model-value="props.visible"
    @update:modelValue="emit('update:visible', $event)"
    :title="`${taskName} 的 ${moduleName}模块 下次触发时间`"
  >
    <el-radio-group
      v-model="triggerType"
      size="large"
      style="margin-bottom: 20px"
    >
      <el-radio-button label="延迟触发" value="delay" />
      <el-radio-button label="指定触发" value="set" />
    </el-radio-group>

    <div v-if="triggerType === 'delay'">
      <el-input v-model="delayDuration" size="large">
        <template #prepend> 当前时间延迟 </template>
        <template #append>
          <el-select
            v-model="delayUnit"
            placeholder="单位"
            style="width: 100px"
            size="large"
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
        size="large"
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

const emit = defineEmits(["update:visible", "refreshModule"]);

const triggerType = ref("delay");
const delayDuration = ref(0);
const delayUnit = ref("second");
const setTime = ref(moment().format("YYYY/MM/DD HH:mm:ss"));
onMounted(async () => {});

const postReq = async (url, data = null, callback = null) => {
  const loading = ElLoading.service({
    lock: true,
    text: "请等待",
    background: "rgba(0, 0, 0, 0.7)",
  });
  axios
    .post(`http://127.0.0.1:8010/${url}`, data)
    .then((res) => {
      ElNotification({ title: "成功", message: "成功", type: "success" });
      if (callback !== null) {
        callback(res);
      }
      loading.close();
      return res;
    })
    .catch((error) => {
      ElNotification({ title: "失败", message: "程序异常", type: "error" });
    });
};

const setModuleNext = async (next) => {
  await postReq(`module/${props.taskName}/${props.moduleName}/setNext/${next}`);
  emit("update:visible", false);
  emit("refreshModule");
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
