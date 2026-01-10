<script setup lang="ts">
import { onMounted, reactive, ref, computed } from 'vue'
import { getCategories, getBuiltinTools } from '@/api/builtin-tool'
import { BASE_URL } from '@/config/index'
import moment from 'moment'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const categories = reactive<Array<any>>([])
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const providers = reactive<Array<any>>([])
const loading = ref<boolean>(false)

const category = ref<string>('all')
const search_word = ref<string>('')
const filterProviders = computed(() => {
  return providers.filter((provider) => {
    const matchCategory = category.value === 'all' || provider.category === category.value
    const matchSearch =
      search_word.value === '' ||
      provider.label.toLowerCase().includes(search_word.value.toLowerCase())
    return matchCategory && matchSearch
  })
})

onMounted(async () => {
  const resp = await getCategories()
  Object.assign(categories, resp.data)
})

onMounted(async () => {
  try {
    loading.value = true
    const resp = await getBuiltinTools()
    Object.assign(providers, resp.data)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <a-spin :loading="loading" class="block h-full w-full">
    <div class="p-6 flex flex-col">
      <!-- 顶层标题，创建按钮 -->
      <div class="flex items-center justify-between mb-6">
        <!-- 左侧标题 -->
        <div class="flex items-center gap-2">
          <a-avatar :size="32" class="!bg-blue-700">
            <icon-common :size="18"></icon-common>
          </a-avatar>
          <div class="text-lg font-medium !text-gray-900">插件广场</div>
        </div>

        <!-- 创建按钮 -->
        <a-button type="primary" class="!rounded-lg">创建自定义插件</a-button>
      </div>

      <!-- 插件分类，搜索框 -->
      <div class="flex items-center justify-between mb-6">
        <!-- 插件分类 -->
        <div class="flex items-center gap-2">
          <a-button
            :type="category === 'all' ? 'outline' : 'text'"
            class="!rounded-lg !text-gray-700 px-3"
            @click="category = 'all'"
            >全部</a-button
          >
          <a-button
            v-for="item in categories"
            :key="item.category"
            :type="category === item.category ? 'outline' : 'text'"
            class="!rounded-lg !text-gray-700 px-3"
            @click="category = item.category"
            >{{ item.name }}</a-button
          >
        </div>
        <!-- 搜索框 -->
        <div class="flex items-center gap-2">
          <a-input-search
            v-model="search_word"
            placeholder="搜索插件"
            class="!w-[240px] !bg-white !rounded-lg !border !border-gray-300"
          ></a-input-search>
        </div>
      </div>
      <!-- 插件列表 -->
      <a-row :gutter="[20, 20]" class="flex-1">
        <!-- 有数据 -->
        <a-col v-for="provider in filterProviders" :key="provider.name" :span="6">
          <a-card hoverable class="!cursor-pointer !rounded-lg">
            <div class="flex items-center !gap-3 !mb-3">
              <a-avatar :size="40" shape="square" :style="{ backgroundColor: 'white' }">
                <img
                  :src="`${BASE_URL}/builtin-tools/${provider.name}/icon`"
                  :alt="provider.name"
                />
              </a-avatar>
              <div class="flex flex-col">
                <div class="!text-base !font-bold !text-gray-900">{{ provider.label }}</div>
                <div class="!text-xs !text-gray-500 !line-clamp-1">
                  提供商 {{ provider.name }} · {{ provider.tools.length }} 插件
                </div>
              </div>
            </div>
            <div class="!leading-[18px] !text-gray-500 h-[72px] !line-clamp-4 !mb-2">
              {{ provider.description }}
            </div>
            <div class="flex items-center gap-1.5">
              <a-avatar :size="18" class="!bg-blue-700">
                <icon-user></icon-user>
              </a-avatar>
              <div class="!text-xs !text-gray-400">
                慕课 · 发布时间 {{ moment(provider.createTime).format('YYYY-MM-DD HH:mm') }}
              </div>
            </div>
          </a-card>
        </a-col>
        <!-- 没有数据 -->
        <a-col v-if="providers.length === 0" :span="24">
          <a-empty
            description="没有可用的内置插件"
            class="!h-[400px] flex flex-col items-center justify-center"
          ></a-empty>
        </a-col>
      </a-row>
    </div>
  </a-spin>
</template>

<style scoped></style>
