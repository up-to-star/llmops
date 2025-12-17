import axios from 'axios'
import { BASE_URL, TIMEOUT } from '@/config'
import { type AxiosResponse, type AxiosRequestConfig } from 'axios'
import { type BaseResponse, type BasePaginatorResponse } from '@/models/base'

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
  (response: AxiosResponse) => {
    const { data } = response
    if (data.code !== 200) {
      if (data.code === 401) {
        // 未登录
      }
      throw new Error(data.message || '请求失败')
    }
    return data
  },
  (error) => {
    console.error('API 请求错误', error)
    throw error
  },
)

export const request = async <T>(config: AxiosRequestConfig): Promise<BaseResponse<T>> => {
  const res = await service(config)
  return res as unknown as BaseResponse<T>
}

export const requestPaginator = async <T>(
  config: AxiosRequestConfig,
): Promise<BasePaginatorResponse<T>> => {
  const res = await service(config)
  return res as unknown as BasePaginatorResponse<T>
}

export default service
