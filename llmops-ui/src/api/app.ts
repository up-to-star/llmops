import { request } from '@/utils/request'
import { type DebugAppResponse } from '@/models/app'

export const debugApp = async (appId: string, query: string): Promise<DebugAppResponse> => {
  const res = await request({
    url: `/apps/${appId}/debug`,
    method: 'post',
    data: {
      query,
    },
  })
  return res as DebugAppResponse
}
