<script setup lang="ts">
import { useAccountStore } from '@/stores/account'
import { debugApp } from '@/api'

const accountStore = useAccountStore()

function updateName() {
  accountStore.update({ name: 'new name' })
}

const handleDebugApp = async () => {
  const res = await debugApp('550e8400-e29b-41d4-a716-446655440000', '你好，你是？')
  console.log(res)
}
</script>

<template>
  <p>首页</p>
  <p>当前用户：{{ accountStore.account.name }}</p>
  <p>当前邮箱：{{ accountStore.account.email }}</p>
  <p>当前头像：{{ accountStore.account.avatar }}</p>
  <a-button type="primary" @click="updateName">更新名字</a-button>
  <a-button type="primary" @click="accountStore.clear">清除账号</a-button>
  <a-button type="primary" @click="handleDebugApp">调试应用</a-button>
</template>

<style scoped></style>
