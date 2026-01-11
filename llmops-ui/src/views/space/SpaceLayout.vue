<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const route = useRoute()
const router = useRouter()
const createType = ref<string>('')

// 搜索词的响应式变量
const searchWord = ref(route.query?.search_word || '')

const handleSearch = (word: string) => {
  searchWord.value = word
  router.push({
    path: route.path,
    query: {
      search_word: word,
    },
  })
}

watch(
  () => route.query?.search_word,
  () => {
    searchWord.value = route.query?.search_word || ''
  },
)

const updateCreateType = (value: string) => {
  createType.value = value
}
</script>

<template>
  <div class="px-6 flex flex-col overflow-hidden h-full">
    <div class="pt-6 sticky top-0 !bg-gray-50 z-20">
      <!-- 顶层标题，创建按钮 -->
      <div class="flex items-center justify-between mb-6">
        <!-- 左侧标题 -->
        <div class="flex items-center gap-2">
          <a-avatar :size="32" class="!bg-blue-700">
            <icon-user :size="18"></icon-user>
          </a-avatar>
          <div class="text-lg font-medium !text-gray-900">个人空间</div>
        </div>

        <!-- 创建按钮 -->
        <a-button v-if="route.path.startsWith('/space/apps')" type="primary" class="!rounded-lg"
          >创建 AI 应用</a-button
        >
        <a-button
          v-if="route.path.startsWith('/space/tools')"
          type="primary"
          class="!rounded-lg"
          @click="createType = 'tool'"
          >创建自定义插件</a-button
        >
        <a-button
          v-if="route.path.startsWith('/space/workflows')"
          type="primary"
          class="!rounded-lg"
          >创建工作流</a-button
        >
        <a-button v-if="route.path.startsWith('/space/datasets')" type="primary" class="!rounded-lg"
          >创建知识库</a-button
        >
      </div>

      <!-- 导航按钮，搜索框 -->
      <div class="flex items-center justify-between mb-6">
        <!-- 导航按钮 -->
        <div class="flex items-center gap-2">
          <router-link
            to="/space/apps"
            class="!rounded-lg !text-gray-700 px-3 h-8 !leading-8 hover:!bg-gray-200 active:!bg-gray-300 transition-all"
            active-class="!bg-gray-200"
            >AI应用</router-link
          >
          <router-link
            to="/space/tools"
            class="!rounded-lg !text-gray-700 px-3 h-8 !leading-8 hover:!bg-gray-200 active:!bg-gray-300 transition-all"
            active-class="!bg-gray-200"
            >插件</router-link
          >
          <router-link
            to="/space/workflows"
            class="!rounded-lg !text-gray-700 px-3 h-8 !leading-8 hover:!bg-gray-200 active:!bg-gray-300 transition-all"
            active-class="!bg-gray-200"
            >工作流</router-link
          >
          <router-link
            to="/space/datasets"
            class="!rounded-lg !text-gray-700 px-3 h-8 !leading-8 hover:!bg-gray-200 active:!bg-gray-300 transition-all"
            active-class="!bg-gray-200"
            >知识库</router-link
          >
        </div>
        <!-- 搜索框 -->
        <div class="flex items-center gap-2">
          <a-input-search
            v-model="searchWord"
            placeholder="输入搜索词"
            class="!w-[240px] !bg-white !rounded-lg !border !border-gray-300"
            @search="handleSearch"
            @keyup.enter="handleSearch(String(searchWord))"
          ></a-input-search>
        </div>
      </div>
    </div>

    <!-- 中间内容 -->
    <router-view :create-type="createType" @update-create-type="updateCreateType"></router-view>
  </div>
</template>

<style scoped></style>
