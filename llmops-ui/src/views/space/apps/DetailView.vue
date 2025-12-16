<script setup lang="ts">

</script>

<template>
  <!-- 最外层容器，高度撑满整个浏览器屏幕 -->
   <div class="min-h-screen">
    <!-- 顶部导航 -->
     <header class="flex items-center h-[74px] bg-gray-100 border-b border-gray-200 px-4">顶部导航</header>

     <!-- 底部内容区 -->
      <div class="flex flex-row h-[calc(100vh-74px)]">
        <!-- 左侧编排 -->
        <div class="w-2/3 bg-gray-50 h-full">
          <header class="flex items-center h-16 border-b border-gray-200 px-7 text-xl text-gray-700">应用编排</header>
          <div class="flex flex-row h-full">
            <div class="flex-1 border-r border-gray-200 p-6">人设与回复逻辑</div>
            <div class="flex-1 p-6">应用能力</div>
          </div>
        </div>
        <!-- 右侧调试预览 -->
        <div class="flex flex-col w-1/3 bg-white h-full">
          <header class="flex items-center h-16  px-4 text-xl bg-white border-b border-gray-200">
            调试与预览
          </header>
          
        </div>
      </div>
   </div>
</template>

<style scoped>

</style>
