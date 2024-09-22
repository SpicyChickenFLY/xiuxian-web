<template>
  <el-dialog
    :model-value="props.visible"
    @update:modelValue="emit('update:visible', $event)"
    width="100%"
    title="截图"
  >
    <el-image style="width: 100px; height: 100px" :src="url" fit="scale-down">
      <template #error>
        <div class="image-slot">
          <el-icon><icon-picture /></el-icon>
        </div>
       </template>
    </el-image>
  </el-dialog>
</template>

<script setup>
import axios from "axios";
import { ElNotification, ElLoading } from "element-plus";
import { Picture as IconPicture } from '@element-plus/icons-vue'
import { reactive } from "vue";

const props = defineProps({
  visible: { type: Boolean, default: false },
  taskName: { type: String, default: "" },
  info: { type: Object, default: { i_x: 0.0, i_y: 0.0, o_x: 0.0, o_y: 0.0 } },
});

const emit = defineEmits(["update:visible", "refresh"]);

const url = ref('/api/screen/');

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

function getScreenShot() {
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
</script>

<style scoped>
</style>
