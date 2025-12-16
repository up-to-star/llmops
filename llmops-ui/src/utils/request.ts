import axios from 'axios'
import { BASE_URL, TIMEOUT } from '@/config'

const service = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL || BASE_URL,
  timeout: TIMEOUT,
})

service.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

service.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code !== 200) {
      if (res.code === 401) {
        // 未登录
      }
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    return res.data
  },
  (error) => {
    const { response } = error
    if (response) {
      return Promise.reject(new Error(response.data.message || '请求失败'))
    }
    return Promise.reject(error)
  },
)

export default service
