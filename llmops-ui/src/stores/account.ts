import { defineStore } from 'pinia'
import { ref } from 'vue'

const initAccount = {
  name: 'test',
  email: 'test@example.com',
  avatar: '',
}

export const useAccountStore = defineStore('account', () => {
  const account = ref({ ...initAccount })

  function update(params: Partial<typeof initAccount>) {
    Object.assign(account.value, params)
  }

  function clear() {
    account.value = { ...initAccount }
  }
  return {
    account,
    update,
    clear,
  }
})
