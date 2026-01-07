<script setup lang="ts">
import IconHomeFill from '@/components/icons/IconHomeFill.vue'
import IconUserFill from '@/components/icons/IconUserFill.vue'
import IconRobotFill from '@/components/icons/IconRobotFill.vue'
import IconCommonFill from '@/components/icons/IconCommonFill.vue'
import IconShareFill from '@/components/icons/IconShareFill.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <a-layout has-sider>
    <!-- 侧边栏 -->
    <a-layout-sider :width="240" class="min-h-screen bg-gray-50 p-2 shadow-none">
      <div class="bg-white h-full rounded-lg px-2 py-4 flex flex-col justify-between">
        <!-- 上半部分 -->
        <div class="">
          <router-link
            to="/home"
            class="block h-9 w-[110px] mb-5 !bg-gray-200 hover:!bg-gray-300 transition-all rounded-lg"
          />
          <a-button type="primary" long class="!rounded-lg !mb-4">
            <template #icon>
              <icon-plus></icon-plus>
            </template>
            创建AI应用
          </a-button>
          <!-- 侧边栏导航 -->
          <div class="flex flex-col gap-2">
            <router-link
              to="/home"
              class="flex items-center gap-2 h-8 leading-8 rounded-lg transition-all px-2 text-gray-700 hover:text-gray-900 hover:!bg-gray-200"
              active-class="!bg-gray-200 !text-gray-900"
            >
              <icon-home-fill v-if="route.path.startsWith('/home')" />
              <icon-home :style="{ fontSize: '18' }" v-else />
              主页
            </router-link>
            <router-link
              to="/space/apps"
              :class="`flex items-center gap-2 h-8 leading-8 rounded-lg transition-all px-2 text-gray-700 hover:text-gray-900 hover:!bg-gray-200 ${route.path.startsWith('/space') ? '!bg-gray-100' : ''}`"
              active-class="!bg-gray-200 !text-gray-900"
            >
              <icon-user-fill v-if="route.path.startsWith('/space')" />
              <icon-user :style="{ fontSize: '18' }" v-else />
              个人空间
            </router-link>
            <div class="text-gray-500 text-sm px-2">探索</div>
            <router-link
              to="/store/apps"
              class="flex items-center gap-2 h-8 leading-8 rounded-lg transition-all px-2 text-gray-700 hover:text-gray-900 hover:!bg-gray-200"
              active-class="!bg-gray-200 !text-gray-900"
            >
              <icon-robot-fill v-if="route.path.startsWith('/store/apps')" />
              <icon-robot :style="{ fontSize: '18' }" v-else />
              应用广场
            </router-link>
            <router-link
              to="/store/tools"
              class="flex items-center gap-2 h-8 leading-8 rounded-lg transition-all px-2 text-gray-700 hover:text-gray-900 hover:!bg-gray-200"
              active-class="!bg-gray-200 !text-gray-900"
            >
              <icon-common-fill v-if="route.path.startsWith('/store/tools')" />
              <icon-common :style="{ fontSize: '18' }" v-else />
              插件广场
            </router-link>
            <router-link
              to="/open"
              class="flex items-center gap-2 h-8 leading-8 rounded-lg transition-all px-2 text-gray-700 hover:text-gray-900 hover:!bg-gray-200"
              active-class="!bg-gray-200 !text-gray-900"
            >
              <icon-share-fill v-if="route.path.startsWith('/open')" />
              <icon-share-alt :style="{ fontSize: '18' }" :rotate="180" v-else />
              开放API
            </router-link>
          </div>
        </div>
        <!-- 账号设置 -->
        <a-dropdown position="tl">
          <div
            class="flex items-center p-2 gap-2 transition-all rounded-lg cursor-pointer hover:!bg-gray-100"
          >
            <!-- 头像 -->
            <a-avatar :size="32" class="text-sm !bg-blue-700">陈</a-avatar>
            <!-- 个人信息 -->
            <div class="flex flex-col">
              <div class="text-sm text-gray-900">陈小课</div>
              <div class="text-xs text-gray-500">chenyujie@example.com</div>
            </div>
          </div>
          <template #content>
            <a-doption>
              <template #icon>
                <icon-settings></icon-settings>
              </template>
              账号设置
            </a-doption>
            <a-doption>
              <template #icon>
                <icon-poweroff></icon-poweroff>
              </template>
              退出登录
            </a-doption>
          </template>
        </a-dropdown>
      </div>
    </a-layout-sider>
    <!-- 右侧内容 -->
    <a-layout-content>
      <router-view />
    </a-layout-content>
  </a-layout>
</template>

<style scoped></style>
