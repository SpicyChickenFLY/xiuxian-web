<template>
  <!-- <el-tabs tab-position="left"> -->
  <el-tabs>
    <el-tab-pane
      v-for="(config, code) in configData.value"
      :key="code"
      :label="code"
      :name="code"
    >
      <el-collapse v-model="activeProgress" accordion>
        <el-collapse-item
          v-for="(progress_profile, progress) in config.progress_profile"
          :key="progress"
          :title="progress + progress_profile.type"
        >
          <template #title>
            <el-space>
             <el-tag>{{ progress_profile.type }}</el-tag>
             <span>{{ progress }}</span>
             <el-tag v-if="new RegExp(progress).test(config.default_cmd)" type="info">
                默认状态 ({{ config.default_cmd }})
             </el-tag>
            </el-space>
          </template>
          <el-table :data="progress_profile.resp" size="small">
            <el-table-column
              v-for="col in colHeaders"
              :key="col.name"
              :label="col.label"
              :width="col.width"
              show-overflow-tooltip
            >
              <template #default="{ row }">
                <span v-if="col.name in row">{{ row[col.name] }}</span>
                <el-tooltip v-else-if="'pre' in row && col.name in row['pre']">
                  <template #content>
                    {{ row.pre[col.name].func_name }}
                    <br />
                    {{ row.pre[col.name].args }}
                  </template>
                  <el-tag type="info" size="small">方法</el-tag>
                </el-tooltip>
                <span v-else>/</span>
              </template>
            </el-table-column>
          </el-table>
        </el-collapse-item>
      </el-collapse>
    </el-tab-pane>
  </el-tabs>
</template>

<script setup>
import axios from "axios";
import { ElNotification, ElLoading, ElMessageBox } from "element-plus";
import { ref, reactive, onMounted, watch, computed } from "vue";
import Next from "./module_next.vue";
import moment from "moment";

const props = defineProps({
  visible: { type: Boolean, default: false },
});

const emit = defineEmits(["update:visible"]);

const activeProgress = ref("");
const configData = reactive({});

const loadingData = {
  lock: true,
  text: "请等待",
  background: "rgba(0, 0, 0, 0.7)",
};

onMounted(async () => {
  refreshConfig();
});

const colHeaders = [
  { label: "回复匹配", name: "resp" },
  { label: "处理结果", name: "result" },
  { label: "等待前置", name: "wait" },
  { label: "触发类型", name: "next_type", width: "50" },
  { label: "延迟量", name: "next_duration", width: "50" },
  { label: "延迟单位", name: "next_unit", width: "50" },
  { label: "时", name: "next_hour", width: "30" },
  { label: "分", name: "next_minute", width: "30" },
  { label: "秒", name: "next_second", width: "30" },
  { label: "后续命令", name: "progress" },
];

const onError = async (msg, error) => {
  ElNotification({
    title: "失败",
    message: `${msg} - ${error}`,
    type: "error",
  });
};

const refreshConfig = async () => {
  getConfigs();
};

const getConfigs = async () => {
  const loading = ElLoading.service(loadingData);
  axios
    .get(`/api/mgr/plugin`)
    .then((res) => {
      configData.value = res.data;
      loading.close();
    })
    .catch((error) => onError("更新模块失败", error));
};
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
