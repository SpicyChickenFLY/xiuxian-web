<template>
  <div>
    <!-- <el-row> -->
    <!--   <el-col :span="8"> -->
    <!--     <el-switch -->
    <!--       v-model="isMgrRunning" -->
    <!--       size="large" -->
    <!--       inline-prompt -->
    <!--       active-text="自动化管理运行中" -->
    <!--       inactive-text="自动化管理停止" -->
    <!--       @change="updateMgrInfo" -->
    <!--     /> -->
    <!--   </el-col> -->
    <!--   <el-col :span="16"> -->
    <!--     <el-input v-model="createPluginName" placeholder="新插件名称"> -->
    <!--       <template #append> -->
    <!--         <el-button @click="createPlugin">创建新插件</el-button> -->
    <!--       </template> -->
    <!--     </el-input> -->
    <!--   </el-col> -->
    <!-- </el-row> -->
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
                <el-tag>{{
                  progress_type_label_map[progress_profile.type]
                }}</el-tag>
                <span>步骤 - {{ progress }}</span>
                <el-tag
                  v-if="new RegExp(progress).test(pluginData.default_cmd)"
                  type="info"
                >
                  初始命令 - {{ pluginData.default_cmd }}
                </el-tag>
                <!-- <el-button -->
                <!--   size="small" -->
                <!--   plain -->
                <!--   type="danger" -->
                <!--   @click.stop.prevent="" -->
                <!--   >删除</el-button -->
                <!-- > -->
              </el-space>
            </template>
            <el-table :data="progress_profile.resp" size="small">
              <el-table-column label="回复结果" show-overflow-tooltip>
                <template #default="{ row }">
                  <el-button
                    size="small"
                    type="primary"
                    @click="showRespDialog(pluginCode, progress, row)"
                    link
                  >
                    {{ row["resp"] }}
                  </el-button>
                </template>
              </el-table-column>
              <el-table-column
                v-for="col in colHeaders"
                :key="col.name"
                :label="col.label"
                :width="col.width"
                show-overflow-tooltip
              >
                <template #default="{ row }">
                  <span v-if="col.name in row"> {{ row[col.name] }} </span>
                  <el-tooltip
                    v-else-if="'pre' in row && col.name in row['pre']"
                  >
                    <template #content>
                      {{ row.pre[col.name].func_name }} <br />
                      {{ row.pre[col.name].args }}
                    </template>
                    <el-tag type="info" size="small">方法</el-tag>
                  </el-tooltip>
                  <span v-else>/</span>
                </template>
              </el-table-column>
            </el-table>
            <!-- <el-button size="small" plain type="info">新增匹配项</el-button> -->
          </el-collapse-item>
        </el-collapse>
      </el-tab-pane>
    </el-tabs>

    <el-dialog
      width="90%"
      v-model="isRespDialogVisible"
      :title="`插件:${updatePlugin} 步骤:${updateProgress} 回复项: ${updateResp} 修改`"
    >
      <JsonEditorVue
        v-model="updateResp.value"
        class="json"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import axios from "axios";
import { ElNotification, ElLoading, ElMessageBox } from "element-plus";
import JsonEditorVue from 'json-editor-vue';
import { ref, reactive, onMounted } from "vue";
import Next from "./module_next.vue";
import moment from "moment";

const props = defineProps({
  visible: { type: Boolean, default: false },
});

const isRespDialogVisible = ref(false);
const updatePlugin = ref("");
const updateProgress = ref("");
const updateResp = reactive({});

const createPluginName = ref("");
const activeProgress = ref("");
const pluginListData = reactive({});

const progress_type_label_map = {
  send: "发送类",
  recv: "回复类",
  listen: "监听类",
};
const delay_type_label_map = {
  set: "设置触发周期",
  delay: "延迟触发时间",
};

const loadingData = {
  lock: true,
  text: "请等待",
  background: "rgba(0, 0, 0, 0.7)",
};

onMounted(async () => refreshPlugin());

const colHeaders = [
  { label: "处理结果", name: "result" },
  { label: "等待前置", name: "wait", width: "70" },
  { label: "下次触发类型", name: "next_type", width: "90" },
  { label: "延迟量", name: "next_duration", width: "60" },
  { label: "延迟单位", name: "next_unit", width: "70" },
  { label: "时", name: "next_hour", width: "30" },
  { label: "分", name: "next_minute", width: "30" },
  { label: "秒", name: "next_second", width: "30" },
  { label: "下个命令", name: "progress" },
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
    onError("创建插件失败", "插件名不能为空");
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

function showRespDialog(pluginName, progressName, respData) {
  // isRespDialogVisible.value = true;
  // updatePlugin.value = pluginName;
  // updateProgress.value = progressName;
  // updateResp.value = respData;
}
</script>

<style scoped>
.json {
  text-align: left;
}

.row {
  width: 100%;
  display: flex;
  align-items: baseline;
}

:deep(.el-dialog){
  --el-dialog-margin-top: 5vh;
  height: 90vh;
  overflow: scroll;
}

:deep(.el-switch){
  --el-switch-on-color: #95d475;
  --el-switch-off-color: #f89898;
}
</style>
