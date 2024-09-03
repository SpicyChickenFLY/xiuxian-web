<template>
  <el-dialog
    :model-value="props.visible"
    @update:modelValue="emit('update:visible', $event)"
    width="600px"
    :title="`任务- ${task} 自动点击坐标`"
  >
    <el-form-item label="输入框横坐标" style="width: 100%">
      <el-space>
        <el-input-number v-model="coord.value['i_x']" />
        <el-input-number v-model="coord.value['i_y']" />
        <el-button type="primary" @click="recordInputCursor()">记录</el-button>
        <el-button @click="moveCursor(coord.value['i_x'], coord.value['i_y'])"
          >测试</el-button
        >
      </el-space>
    </el-form-item>
    <el-form-item label="消息框横坐标">
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
  task: { type: String, default: "" },
  info: { type: Object, default: { i_x: 0.0, i_y: 0.0, o_x: 0.0, o_y: 0.0 } },
});

const emit = defineEmits(["update:visible", "refresh"]);

const coord = reactive(props.info);

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
      return res;
    })
    .catch((error) => {
      ElNotification({ title: "失败", message: "程序异常", type: "error" });
    });
};
function moveCursor(x, y) {
  postReq(`moveCursor`, { x: x, y: y });
}

function recordInputCursor() {
  ElNotification({
    title: "注意",
    message: "请在8秒内将鼠标移至目标位置",
    type: "warning",
  });
  postReq(`recordCursor`, null, (res) => {
    coord.value["i_x"] = res.data["x"];
    coord.value["i_y"] = res.data["y"];
  });
}

function recordOutputCursor() {
  ElNotification({
    title: "注意",
    message: "请在8秒内将鼠标移至目标位置",
    type: "warning",
  });
  postReq(`recordCursor`, null, (res) => {
    coord.value["o_x"] = res.data["x"];
    coord.value["o_y"] = res.data["y"];
  });
}

const setTaskLocation = async () => {
  await postReq(`task/setBot/${props.task}`, coord.value, () => {
    emit("update:visible", false);
    emit("refresh");
  });
};
</script>

<style scoped>
a {
  color: #42b983;
}
</style>
