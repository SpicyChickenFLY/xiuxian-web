<template lang="pug">
  <el-dialog
    v-model="dialogVisible"
    title="Tips"
    width="500"
    fullscreen
    :before-close="handleClose"
   >
     <el-input v-model="coor['i_x']" />
     <el-input v-model="coor['i_y']" />
     <el-input v-model="coor['o_x']" />
     <el-input v-model="coor['o_y']" />
   </el-dialog>
</template>
