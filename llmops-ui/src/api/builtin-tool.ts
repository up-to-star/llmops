import { type GetCategoriesResponse, type GetBuiltinToolsResponse } from '@/models/builtin-tool'
import { request } from '@/utils/request'

// 获取内置分类列表信息
export const getCategories = async (): Promise<GetCategoriesResponse> => {
  const res = await request({
    url: '/builtin-tools/categories',
    method: 'get',
  })
  return res as GetCategoriesResponse
}

// 获取内置工具提供者列表信息
export const getBuiltinTools = async (): Promise<GetBuiltinToolsResponse> => {
  const res = await request({
    url: '/builtin-tools',
    method: 'get',
  })
  return res as GetBuiltinToolsResponse
}
