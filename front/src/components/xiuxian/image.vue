<template>
  <el-dialog
    :model-value="props.visible"
    @update:modelValue="emit('update:visible', $event)"
    fullscreen
    center
    :title="`任务- ${props.taskName} 自动点击坐标`"
  >
    <template #title>
      任务- {{props.taskName}} 自动点击坐标
      <el-button type="primary" @click="setTaskLocation()">更新</el-button>
    </template>
    <div class="container">
      <div class="aside">
        <el-slider v-model="value" :show-tooltip="false" vertical height="90%" />
      </div>
      <div class="canvas">
        <div class="cursor">
        </div>
        <div class="image-container">
          <img src="/api/screen" class="image" />
        </div>
      </div>
      <div class="footer">
        <el-slider v-model="value" height="100%" />
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import axios from "axios";
import { ElNotification, ElLoading } from "element-plus";
import { TopLeft } from '@element-plus/icons-vue'
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

<style lang="scss" scoped>
.container {
  height: 100%;
  width: 100%;
  display: flex;

  .aside {
    width: 50px;
    height: 100%;
  }

  .canvas {
    flex-grow: 1;
    .cursor {
      position: absolute;
      height: 5px;
      width: 5px;
      background-color: #FF0000;
      z-index: 2;
    }
    .image-container {
      width: 100%;
      .image {
        width: 100%;
      }
      z-index: 1;
    }
  }
}
</style>
