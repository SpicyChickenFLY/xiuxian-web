<template>
  <el-collapse v-model="activeProgress" accordion>
    <el-collapse-item
      v-for="(miscJson, miscName) in miscData.value"
      :key="miscName"
      :title="miscName"
    >
      <JsonEditorVue
        v-model="miscData.value[miscName]"
        class="json"
      />
    </el-collapse-item>
  </el-collapse>
</template>

<script setup>
import axios from "axios";
import { ElNotification, ElLoading, ElMessageBox } from "element-plus";
import { ref, reactive, onMounted } from "vue";
import Next from "./module_next.vue";
import moment from "moment";
import JsonEditorVue from 'json-editor-vue';

const props = defineProps({
  visible: { type: Boolean, default: false },
});

const activeProgress = ref("");
const miscData = reactive({});

const loadingData = {
  lock: true,
  text: "请等待",
  background: "rgba(0, 0, 0, 0.7)",
};

onMounted(async () => {
  refreshMisc();
});

const onError = async (msg, error) => {
  ElNotification({
    title: "失败",
    message: `${msg} - ${error}`,
    type: "error",
  });
};

const refreshMisc = async () => {
  getMiscList();
};

const getMiscList = async () => {
  const loading = ElLoading.service(loadingData);
  axios
    .get(`/api/mgr/misc`)
    .then((res) => {
      miscData.value = res.data;
      loading.close();
    })
    .catch((error) => onError("获取自定义方法失败", error));
};
</script>

<style scoped>
.json {
  text-align: left;
}

:deep(.el-switch){
  --el-switch-on-color: #95d475;
  --el-switch-off-color: #f89898;
}
</style>
