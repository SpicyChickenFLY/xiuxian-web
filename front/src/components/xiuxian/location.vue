<template>
  <el-dialog
    :model-value="props.visible"
    @update:modelValue="emit('update:visible', $event)"
    width="600px"
    :title="`任务- ${props.taskName} 自动点击坐标`"
  >
    <el-form-item label="输入框坐标" style="width: 100%">
      <el-space>
        <el-input-number v-model="coord.value['i_x']" />
        <el-input-number v-model="coord.value['i_y']" />
        <el-button type="primary" @click="recordInputCursor()">记录</el-button>
        <el-button @click="moveCursor(coord.value['i_x'], coord.value['i_y'])"
          >测试</el-button
        >
      </el-space>
    </el-form-item>
    <el-form-item label="消息框坐标">
      <el-space>
        <el-input-number v-model="coord.value['o_x']" />
        <el-input-number v-model="coord.value['o_y']" />
        <el-button type="primary" @click="recordOutputCursor()">记录</el-button>
        <el-button @click="moveCursor(coord.value['o_x'], coord.value['o_y'])"
          >测试</el-button
        >
      </el-space>
    </el-form-item>
    <el-button type="primary" @click="setTaskLocation()">更新</el-button>
  </el-dialog>
</template>

<script setup>
import axios from "axios";
import { ElNotification, ElLoading } from "element-plus";
import { reactive } from "vue";

const props = defineProps({
  visible: { type: Boolean, default: false },
  taskName: { type: String, default: "" },
  info: { type: Object, default: { i_x: 0.0, i_y: 0.0, o_x: 0.0, o_y: 0.0 } },
});

const emit = defineEmits(["update:visible", "refresh"]);

const coord = reactive(props.info);
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

const moveCursor = async (x, y) => {
  const loading = ElLoading.service(loadingData);
  axios
    .put(`/api/cursor`, { x, y })
    .then((res) => {
      loading.close();
    })
    .catch((error) => onError("移动鼠标失败", error));
};

function recordInputCursor() {
  const loading = ElLoading.service(loadingData);
  axios
    .get(`/api/cursor`)
    .then((res) => {
      coord.value["i_x"] = res.data["x"];
      coord.value["i_y"] = res.data["y"];
      loading.close();
    })
    .catch((error) => onError("记录输入框位置失败", error));
}

function recordOutputCursor() {
  const loading = ElLoading.service(loadingData);
  axios
    .get(`/api/cursor`)
    .then((res) => {
      coord.value["o_x"] = res.data["x"];
      coord.value["o_y"] = res.data["y"];
      loading.close();
    })
    .catch((error) => onError("记录回复框位置失败", error));
}

const setTaskLocation = async () => {
  const loading = ElLoading.service(loadingData);
  axios
    .put(`/api/mgr/task/${props.taskName}`, { bot: coord.value })
    .then((res) => {
      loading.close();
      emit("update:visible", false);
      emit("refresh");
    })
    .catch((error) => onError("更新位置信息失败", error));
};
</script>

<style scoped>
</style>
