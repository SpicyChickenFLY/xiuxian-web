<template>
  <el-dialog
    :model-value="props.visible"
    @update:modelValue="emit('update:visible', $event)"
  >
  </el-dialog>
</template>

<script setup>
import { defineProps, defineEmits, ref, reactive, onMounted, onBeforeMount } from "vue";
import axios from "axios";
import { ElNotification } from 'element-plus'

const props = defineProps({
  visible: { type: Boolean, default: false },
  taskName: { type: String, default: "" }
});

const emit = defineEmits(['update:visible']);

function hide() {
  emit('update:visible', false)
}

onMounted(async () => {
  if (taskName === "") {
    ElNotification({
      title: '加载详情异常',
      message: '识别号不应该为空',
      type: 'error',
    })
    hide();
  } else {
    getTaskDetail();
  }
});

const getTaskDetail = async () => {
  axios.get("http://127.0.0.1:8010/task/" + taskName).then((res) => {
    tableData.value = res.data;
  });
};

</script>

<style scoped>
a {
  color: #42b983;
}
</style>
