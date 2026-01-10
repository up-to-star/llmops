<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getApiToolProvidersWithPage } from '@/api/api-tool'
import moment from 'moment'

const providers = reactive<Array<any>>([])
const loading = ref<boolean>(false)
const showIdx = ref<number>(-1)
const paginator = reactive({
  current_page: 1,
  page_size: 20,
  total_page: 0,
  total_record: 0,
})
const route = useRoute()

const loadMoreData = async (init: boolean = false) => {
  if (!init && paginator.current_page >= paginator.total_page) {
    return
  }
  try {
    loading.value = true
    const resp = await getApiToolProvidersWithPage(
      paginator.current_page,
      paginator.page_size,
      (route.query?.search_word as string | undefined) ?? '',
    )
    const data = resp.data
    paginator.current_page = data.paginator.current_page
    paginator.page_size = data.paginator.page_size
    paginator.total_page = data.paginator.total_page
    paginator.total_record = data.paginator.total_record
    if (paginator.current_page <= paginator.total_page) {
      paginator.current_page += 1
    }
    if (init) {
      providers.splice(0, providers.length, ...data.data)
    } else {
      providers.push(...data.data)
    }
  } finally {
    loading.value = false
  }
}

const handleScroll = async (event: UIEvent) => {
  const { scrollTop, scrollHeight, clientHeight } = event.target as HTMLElement
  if (scrollTop + clientHeight >= scrollHeight - 10) {
    if (loading.value) {
      return
    }
    await loadMoreData(false)
  }
}
onMounted(async () => {
  await loadMoreData(true)
})
watch(
  () => route.query?.search_word,
  async () => {
    paginator.current_page = 1
    paginator.page_size = 20
    paginator.total_page = 0
    paginator.total_record = 0
    await loadMoreData(true)
  },
)
</script>

<template>
  <a-spin
    :loading="loading"
    class="block h-full w-full scrollbar-w-none overflow-scroll"
    @scroll="handleScroll"
  >
    <!-- 插件列表 -->
    <a-row :gutter="[20, 20]" class="flex-1">
      <!-- 有数据 -->
      <a-col v-for="(provider, idx) in providers" :key="provider.name" :span="6">
        <a-card hoverable class="!cursor-pointer !rounded-lg" @click="showIdx = idx">
          <div class="flex items-center !gap-3 !mb-3">
            <a-avatar :size="40" shape="square" :image-url="provider.icon"> </a-avatar>
            <div class="flex flex-col">
              <div class="!text-base !font-bold !text-gray-900">{{ provider.name }}</div>
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
              慕小课 · 编辑时间 {{ moment(provider.createTime).format('YYYY-MM-DD HH:mm') }}
            </div>
          </div>
        </a-card>
      </a-col>
      <!-- 没有数据 -->
      <a-col v-if="providers.length === 0" :span="24">
        <a-empty
          description="没有可用的API插件"
          class="!h-[400px] flex flex-col items-center justify-center"
        ></a-empty>
      </a-col>
    </a-row>
    <!-- 加载器 -->
    <a-row v-if="providers.length > 0">
      <a-col v-if="paginator.current_page <= paginator.total_page" :span="24" align="center">
        <a-space class="my-4">
          <a-spin></a-spin>
          <div class="!text-gray-400">加载中</div>
        </a-space>
      </a-col>
      <a-col v-else :span="24" align="center">
        <div class="!text-gray-400 my-4">数据已加载完成</div>
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
          <a-avatar :size="40" shape="square" :image-url="providers[showIdx].icon"> </a-avatar>
          <div class="flex flex-col">
            <div class="!text-base !font-bold !text-gray-900">
              {{ providers[showIdx].name }}
            </div>
            <div class="!text-xs !text-gray-500 !line-clamp-1">
              提供商 {{ providers[showIdx].name }} · {{ providers[showIdx].tools.length }} 插件
            </div>
          </div>
        </div>
        <div class="leading-[18px] !text-gray-500 !mb-4">
          {{ providers[showIdx].description }}
        </div>
        <!-- 编辑按钮 -->
        <a-button type="dashed" long class="!mb-2 !rounded-lg">
          <template #icon>
            <icon-settings></icon-settings>
          </template>
          编辑工具</a-button
        >
        <hr class="my-4" />
        <div class="flex flex-col gap-2">
          <div class="text-xs !text-gray-500">
            包含 {{ providers[showIdx].tools.length }} 个工具
          </div>
          <a-card
            v-for="tool in providers[showIdx].tools"
            :key="tool.name"
            class="cursor-pointer flex flex-col !rounded-xl"
          >
            <div class="mb-2 !font-bold !text-gray-900">{{ tool.name }}</div>
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
    <!-- 新建/修改模态窗 -->
    <a-modal :width="630" :visible="false" hide-title :footer="false" modal-class="rounded-xl">
      <div class="flex items-center justify-between">
        <div class="text-lg font-bold text-gray-700">新建插件</div>
        <a-button type="text" class="!text-gray-700" size="small">
          <template #icon>
            <icon-close></icon-close>
          </template>
        </a-button>
      </div>
      <!-- 中间表单 -->
      <div class="pt-6">
        <a-form layout="vertical">
          <a-form-item
            field="icon"
            hide-label
            :rules="[{ required: true, message: '插件图标不能为空' }]"
          >
            <a-upload
              :limit="1"
              list-type="picture-card"
              accept="image/png, image/jpeg"
              class="!w-auto mx-auto"
            ></a-upload>
          </a-form-item>
          <a-form-item
            field="name"
            label="插件名称"
            asterisk-position="end"
            :rules="[{ required: true, message: '插件名称不能为空' }]"
          >
            <a-input placeholder="请输入插件名称" show-word-limit :max-length="60"></a-input>
          </a-form-item>
          <a-form-item
            field="openapi_schema"
            label="OpenAPI Schema"
            asterisk-position="end"
            :rules="[{ required: true, message: 'OpenAPI Schema不能为空' }]"
          >
            <a-textarea
              :auto-size="{ minRows: 4, maxRows: 6 }"
              placeholder="在此处输入您的OpenAPI Schema"
            ></a-textarea>
          </a-form-item>
          <a-form-item label="可用工具">
            <div class="!rounded-lg border !border-gray-200 w-full overflow-x-auto">
              <table class="w-full leading-[18px] text-xs !text-grap-700 font-normal">
                <thead class="!text-gray-500">
                  <tr class="border-b !border-gray-200">
                    <th class="!pl-3 !p-2 font-medium">名称</th>
                    <th class="!pl-3 !p-2 font-medium w-[236px]">描述</th>
                    <th class="!pl-3 !p-2 font-medium">方法</th>
                    <th class="!pl-3 !p-2 font-medium">路径</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="border-b last:border-0 !border-gray-200 !text-gray-700">
                    <td class="!pl-3 !p-2">getxxx</td>
                    <td class="!pl-3 !p-2 w-[236px]">xxxxx</td>
                    <td class="!pl-3 !p-2">get</td>
                    <td class="!pl-3 !p-2 w-[62px]">xxxxx</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </a-form-item>
          <a-form-item label="Headers">
            <div class="!rounded-lg !border !border-gray-200 !w-full !overflow-x-auto">
              <table class="w-full leading-[18px] text-xs !text-grap-700 font-normal !mb-3">
                <thead class="!text-gray-500">
                  <tr class="border-b !border-gray-200">
                    <th class="!pl-3 !p-2 font-medium">Key</th>
                    <th class="!pl-3 !p-2 font-medium">Value</th>
                    <th class="!pl-3 !p-2 font-medium w-[50px]">操作</th>
                  </tr>
                </thead>
                <tbody class="border-b !border-gray-200">
                  <tr class="border-b last:!border-0 !border-gray-200">
                    <td class="!pl-3 !p-2">
                      <a-form-item class="!m-0" hide-label>
                        <a-input placeholder="请输入请求头键名"></a-input>
                      </a-form-item>
                    </td>
                    <td class="!pl-3 !p-2">
                      <a-form-item class="!m-0" hide-label>
                        <a-input placeholder="请输入请求头键值"></a-input>
                      </a-form-item>
                    </td>
                    <td class="!pl-3 !p-2">
                      <a-button type="text" class="!text-gray-700" size="mini">
                        <template #icon>
                          <icon-delete />
                        </template>
                      </a-button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <a-button size="mini" class="!rounded !ml-3 !mb-3 !text-gray-700">
                <template #icon>
                  <icon-plus></icon-plus>
                </template>
                增加参数</a-button
              >
            </div>
          </a-form-item>
          <!-- 底部按钮 -->
          <div class="flex items-center justify-between">
            <div>
              <a-button class="!rounded-lg !text-red-700">删除</a-button>
            </div>
            <a-space :size="16">
              <a-button class="!rounded-lg">取消</a-button>
              <a-button type="primary" html-type="submit" class="!rounded-lg">保存</a-button>
            </a-space>
          </div>
        </a-form>
      </div>
    </a-modal>
  </a-spin>
</template>

<style scoped></style>
