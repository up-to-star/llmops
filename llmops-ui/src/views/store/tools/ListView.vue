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

const showIdx = ref<number>(-1)

onMounted(async () => {
  const resp = await getCategories()
  categories.push(...resp.data)
})

onMounted(async () => {
  try {
    loading.value = true
    const resp = await getBuiltinTools()
    providers.push(...resp.data)
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
        <a-col v-for="(provider, idx) in filterProviders" :key="provider.name" :span="6">
          <a-card hoverable class="!cursor-pointer !rounded-lg" @click="showIdx = idx">
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

      <!-- 卡片抽屉 -->
      <a-drawer
        :visible="showIdx !== -1"
        :width="350"
        :footer="false"
        title="工具详情"
        :drawer-style="{ background: '#F9FAFB' }"
        @cancel="showIdx = -1"
      >
        <div v-if="showIdx !== -1" class="px-6">
          <div class="flex items-center !gap-3 !mb-3">
            <a-avatar :size="40" shape="square" :style="{ backgroundColor: 'white' }">
              <img
                :src="`${BASE_URL}/builtin-tools/${filterProviders[showIdx].name}/icon`"
                :alt="filterProviders[showIdx].name"
              />
            </a-avatar>
            <div class="flex flex-col">
              <div class="!text-base !font-bold !text-gray-900">
                {{ filterProviders[showIdx].label }}
              </div>
              <div class="!text-xs !text-gray-500 !line-clamp-1">
                提供商 {{ filterProviders[showIdx].name }} ·
                {{ filterProviders[showIdx].tools.length }} 插件
              </div>
            </div>
          </div>
          <div class="!leading-[18px] !text-gray-500 !mb-2">
            {{ filterProviders[showIdx].description }}
          </div>
          <hr class="my-4" />
          <div class="flex flex-col gap-2">
            <div class="text-xs !text-gray-500">
              包含 {{ filterProviders[showIdx].tools.length }} 个工具
            </div>
            <a-card
              v-for="tool in filterProviders[showIdx].tools"
              :key="tool.name"
              class="cursor-pointer flex flex-col !rounded-xl"
            >
              <div class="mb-2 !font-bold !text-gray-900">{{ tool.label }}</div>
              <div class="!text-xs !text-gray-500">{{ tool.description }}</div>
              <div v-if="tool.inputs.length > 0" class="">
                <div class="flex items-center gap-2 my-4">
                  <div class="!text-xs !text-gray-500 !font-bold">参数</div>
                  <hr class="flex-1" />
                </div>
                <div class="flex flex-col gap-4">
                  <div v-for="input in tool.inputs" :key="input.name" class="flex flex-col gap-2">
                    <div class="flex items-center gap-2 !text-xs">
                      <div class="!text-gray-900 !font-bold">{{ input.name }}</div>
                      <div class="!text-gray-500">{{ input.type }}</div>
                      <div v-if="input.required" class="!text-red-700">必填</div>
                    </div>
                    <div class="!text-xs !text-gray-500">{{ input.description }}</div>
                  </div>
                </div>
              </div>
            </a-card>
          </div>
        </div>
      </a-drawer>
    </div>
  </a-spin>
</template>

<style scoped></style>
