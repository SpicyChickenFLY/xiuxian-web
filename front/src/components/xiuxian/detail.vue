<template>
  <el-dialog>
  </el-dialog>
</template>

<script setup>
import { defineProps, ref, reactive, onMounted, onBeforeMount } from "vue";
import axios from "axios";
import { ElNotification } from 'element-plus'


defineProps({
  msg: String,
});


onMounted(async () => {
});

</script>

<style scoped>
a {
  color: #42b983;
}
</style>
