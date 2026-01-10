import { request } from '@/utils/request'
import { type GetApiToolProvidersWithPageResponse } from '@/models/api-tool'

// 获取 API 工具提供者列表信息
export const getApiToolProvidersWithPage = async (
  current_page: number = 1,
  page_size: number = 20,
  search_word: string = '',
): Promise<GetApiToolProvidersWithPageResponse> => {
  const res = await request({
    url: '/api-tools/pages',
    method: 'post',
    data: {
      current_page,
      page_size,
      search_word,
    },
  })
  return res as GetApiToolProvidersWithPageResponse
}
