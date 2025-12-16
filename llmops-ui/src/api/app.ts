import service from '@/utils/request'

export function debugApp(appId: string, query: string) {
  return service({
    url: `/apps/${appId}/debug`,
    method: 'post',
    data: {
      query,
    },
  })
}
