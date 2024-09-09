import axios from "axios";

const refresh = async () => getMgrInfo();

const getMgrInfo = async () => {
  axios
    .get("/api/mgr")
    .then((res) => {
      mgrData.value = res.data.data.tasks;
      isMgrRunning.value = res.data.data.is_running;
    })
    .catch((error) => onError("获取管理器信息失败", error));
};

const updateMgrInfo = async (val) => {
  const loading = ElLoading.service(loadingData);
  axios
    .put("/api/mgr", { is_running: !!val })
    .then((res) => {
      loading.close();
      refresh();
    })
    .catch((error) => onError("更新管理器状态失败", error));
};

const createTask = async () => {
  if (!createTaskName.value) {
    onError("创建任务失败", "任务名不能为空");
    return;
  }
  const loading = ElLoading.service(loadingData);
  axios
    .post(`/api/mgr/task/${createTaskName.value}`, {})
    .then((res) => {
      createTaskName.value = "";
      loading.close();
      refresh();
    })
    .catch((error) => onError("创建任务失败", error));
};

const setTaskEnable = async (taskName, enable) =>
  updateTask(taskName, { enable: enable });

const updateTask = async (taskName, taskData) => {
  if (!taskName) {
    onError("更新任务失败", "任务名不能为空");
    return;
  }
  const loading = ElLoading.service(loadingData);
  axios
    .put(`/api/mgr/task/${taskName}`, taskData)
    .then((res) => {
      loading.close();
      refresh();
    })
    .catch((error) => onError("更新任务失败", error));
};

const deleteTask = async (taskName) => {
  if (!taskName) {
    onError("删除任务失败", "任务名不能为空");
    return;
  }
  const loading = ElLoading.service(loadingData);
  axios
    .delete(`/api/mgr/task/${taskName}`, {})
    .then((res) => {
      loading.close();
      refresh();
    })
    .catch((error) => onError("删除任务失败", error));
};

const setModuleEnable = async (taskName, moduleName, enable) =>
  updateModule(taskName, moduleName, { enable: enable });

const updateModule = async (taskName, moduleName, moduleData) => {
  if (!taskName || !moduleName) {
    onError("更新模块失败", "任务名/模块名不能为空");
    return;
  }
  const loading = ElLoading.service(loadingData);
  axios
    .put(`/api/mgr/task/${taskName}/module/${moduleName}`, moduleData)
    .then((res) => {
      loading.close();
      refresh();
    })
    .catch((error) => onError("更新模块失败", error));
};
