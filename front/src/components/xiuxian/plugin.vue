<template>
  <div>
    <el-row>
      <el-col :span="8">
        <el-switch
          v-model="isMgrRunning"
          size="large"
          inline-prompt
          active-text="自动化管理运行中"
          inactive-text="自动化管理停止"
          @change="updateMgrInfo"
        />
      </el-col>
      <el-col :span="16">
        <el-input v-model="createPluginName" placeholder="新插件名称">
          <template #append>
            <el-button @click="createPlugin">创建新插件</el-button>
          </template>
        </el-input>
      </el-col>
    </el-row>
    <el-tabs type="card">
      <el-tab-pane
        v-for="(pluginData, pluginCode) in pluginListData.value"
        :key="pluginCode"
        :label="pluginCode"
        :name="pluginCode"
      >
        <el-collapse v-model="activeProgress" accordion>
          <el-collapse-item
            v-for="(progress_profile, progress) in pluginData.progress_profile"
            :key="progress"
          >
            <template #title>
              <el-space>
                <el-tag>{{ progress_profile.type }}</el-tag>
                <span>{{ progress }}</span>
                <el-tag
                  v-if="new RegExp(progress).test(pluginData.default_cmd)"
                  type="info"
                >
                  默认状态 ({{ pluginData.default_cmd }})
                </el-tag>
                  <el-button size="small" plain type="warning"
                    @click.stop.prevent=""
                    >修改</el-button>
                  <el-button size="small" plain type="danger"
                    @click.stop.prevent=""
                    >删除</el-button>
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
                  <el-button
                    v-if="col.name in row"
                    size="small"
                    @click="updateProgress(pluginCode, progress)"
                    link
                  >
                   {{ row[col.name] }}
                  </el-button>
                  <el-tooltip
                    v-else-if="'pre' in row && col.name in row['pre']"
                  >
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

    <el-dialog
      width="90%"
      :model-value="isProgressDialogVisible"
      :title="`${updatePlugin} 的 ${updateProgress}状态 修改`"
    >
      <el-table :data="updateProgress.resp" size="small">
        <el-table-column
          v-for="col in colHeaders"
          :key="col.name"
          :label="col.label"
          :width="col.width"
          show-overflow-tooltip
        >
          <template #default="{ row }">
            <el-input
              v-if="col.name in row"
              size="small"
              @click="updateProgress(pluginCode, progress)"
              link
            >
              <template #append>
                <el-button @click="toggleValFunc()">切换方法</el-button>
              </template>
              {{ row[col.name] }}
            </el-input>
            <el-tooltip
              v-else-if="'pre' in row && col.name in row['pre']"
            >
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
    </el-dialog>
  </div>
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

const isProgressDialogVisible = ref(false);

const createPluginName = ref("");
const activeProgress = ref("");
const pluginListData = reactive({});

const loadingData = {
  lock: true,
  text: "请等待",
  background: "rgba(0, 0, 0, 0.7)",
};

onMounted(async () => {
  refreshPlugin();
});

const colHeaders = [
  { label: "回复匹配", name: "resp" },
  { label: "处理结果", name: "result" },
  { label: "等待前置", name: "wait", width: "50" },
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

const refreshPlugin = async () => {
  getPluginList();
};

const getPluginList = async () => {
  const loading = ElLoading.service(loadingData);
  axios
    .get(`/api/mgr/plugin`)
    .then((res) => {
      pluginListData.value = res.data;
      loading.close();
    })
    .catch((error) => onError("更新模块失败", error));
};

const createPlugin = async () => {
  if (!createPluginName.value) {
    onError("创建任务失败", "任务名不能为空");
    return;
  }
  const loading = ElLoading.service(loadingData);
  axios
    .post(`/api/mgr/task/${createPluginName.value}`, {})
    .then((res) => {
      createPluginName.value = "";
      loading.close();
      refresh();
    })
    .catch((error) => onError("创建任务失败", error));
};

</script>

<style scoped>
.el-switch {
  --el-switch-on-color: #95d475;
  --el-switch-off-color: #f89898;
}
</style>
