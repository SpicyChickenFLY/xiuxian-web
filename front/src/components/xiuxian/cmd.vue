<template>
  <el-dialog
    :model-value="props.visible"
    @update:modelValue="emit('update:visible', $event)"
    width="400px"
    :title="`任务- ${props.taskName} 手动命令`"
  >
    <el-space>
      <el-select v-model="cmdData.type" style="width: 80px">
        <el-option label="接收" value="recv" />
        <el-option label="发送" value="send" />
      </el-select>
      <el-input v-model="cmdData.cmd" />
      <el-button :loading="cmdLoading" type="primary" @click="execTaskCmd()">运行</el-button>
    </el-space>
    <el-input
      v-model="cmdResult"
      style="width: 100%; padding-top: 20px"
      :autosize="{ minRows: 2, maxRows: 4 }"
      type="textarea"
      readonly
    />
    <el-divider />
    <el-tag
      v-for="(cmdType, cmdName) in cmdListData.value"
      :key="cmdName"
      :type="cmdTypeColorMap[cmdType]"
      @click="changeCmd(cmdName, cmdType)"
      @close="deleteCmd(cmdName)"
    >
      {{ cmdName }}
    </el-tag
    >
  </el-dialog>
</template>

<script setup>
import axios from "axios";
import { ElNotification, ElLoading } from "element-plus";
import { reactive, ref, onMounted } from "vue";

const props = defineProps({
  visible: { type: Boolean, default: false },
  taskName: { type: String, default: "" },
});

const emit = defineEmits(["update:visible", "refresh"]);

const cmdData = reactive({ cmd: "", type: "recv" });
const cmdResult = ref("");
const cmdLoading = ref(false);
const cmdListData = reactive({});
const cmdTypeColorMap = {
  recv: "success",
  send: "warning",
};

const loadingData = {
  lock: true,
  text: "请等待",
  background: "rgba(0, 0, 0, 0.7)",
};

onMounted(async () => refresh());

const onError = async (msg, error) => {
  ElNotification({
    title: "失败",
    message: `${msg} - ${error}`,
    type: "error",
  });
};

const refresh = async () => getCmdList();

const getCmdList = async () => {
  axios
    .get("/api/mgr/cmd")
    .then((res) => cmdListData.value = res.data)
    .catch((error) => onError("获取历史命令信息失败", error));
};

const deleteCmd = async (cmdName) => {
  const loading = ElLoading.service(loadingData);
  axios
    .delete(`/api/mgr/cmd/${cmdName}`)
    .then((res) => loading.close())
    .catch((error) => onError("删除历史命令失败", error));
};

const execTaskCmd = async () => {
  cmdLoading.value = true;
  cmdResult.value = ""
  axios
    .put(`/api/mgr/cmd`, { cmd: cmdData.cmd, type: cmdData.type, task: props.taskName })
    .then((res) => {
      if (res.data.success) {
        cmdResult.value = res.data.data;
      } else {
        onError("执行命令失败", res.data.msg);
      }
    })
    .catch((error) => onError("执行命令失败", error))
    .finally(() => {
      cmdLoading.value = false;
      refresh();
    });
};

function changeCmd(cmdName, cmdType) {
  cmdData.cmd = cmdName;
  cmdData.type = cmdType;
}
</script>

<style scoped></style>
