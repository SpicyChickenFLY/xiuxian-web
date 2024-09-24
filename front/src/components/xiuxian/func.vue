<template>
  <el-collapse v-model="activeProgress" @change="collapseChange" accordion>
    <el-collapse-item
      v-for="(funcData, funcName) in funcsData.value"
      :key="funcName"
      :title="funcName"
      :name="funcName"
    >
      <codemirror
        v-model:value="funcsData.value[funcName]"
        :options="options"
        @ready="(val) => onReady(funcName, val)"
        class="code"
      />
    </el-collapse-item>
  </el-collapse>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { ElNotification, ElLoading, ElMessageBox } from "element-plus";
import axios from "axios";
import Codemirror from "codemirror-editor-vue3";
import "codemirror/mode/python/python";
import "codemirror/addon/display/autorefresh";
import "codemirror/theme/duotone-light.css";

const props = defineProps({
  visible: { type: Boolean, default: false },
});

const cmMap = reactive({});

const activeProgress = ref("");
const funcsData = reactive({});

const code = "import re";

const options = {
  autorefresh: true, // 自动刷新
  smartIndent: true, // 自动缩进
  tabSize: 4, // 缩进单元格为 4 个空格
  mode: "python", //编辑器的编程语言，比如：'javascript'
  theme: "duotone-light", // 主题，使用主体需要引入相应的 css 文件
  line: true, // 是否显示行数
  viewportMargin: Infinity, // 高度自适应
  autofocus: false,
  indentUnit: 2,
  showCursorWhenSelecting: true,
  firstLineNumber: 1,
  matchBrackets: true, //括号匹配
};

const loadingData = {
  lock: true,
  text: "请等待",
  background: "rgba(0, 0, 0, 0.7)",
};

onMounted(async () => {
  refreshFunc();
});

const onError = async (msg, error) => {
  ElNotification({
    title: "失败",
    message: `${msg} - ${error}`,
    type: "error",
  });
};

const refreshFunc = async () => {
  getFuncList();
};

const getFuncList = async () => {
  const loading = ElLoading.service(loadingData);
  axios
    .get(`/api/mgr/func`)
    .then((res) => {
      funcsData.value = res.data;
      loading.close();
    })
    .catch((error) => onError("获取自定义方法失败", error));
};

const onReady = async (funcName, cm) => {
  cm.refresh();
  cmMap[funcName] = cm;
};

const collapseChange = async () => {
  if (!activeProgress.value) {
    return;
  }
  setTimeout(() => {
    cmMap[activeProgress.value].refresh();
  }, 1);
};
</script>

<style scoped>
.code {
  text-align: left;
  min-height: 200px;
}

:deep(.el-switch){
  --el-switch-on-color: #95d475;
  --el-switch-off-color: #f89898;
}
</style>
