/* eslint-disable @typescript-eslint/no-explicit-any */
import { request } from '@/utils/request'
import { type GetApiToolProvidersWithPageResponse } from '@/models/api-tool'
import { type BaseResponse } from '@/models/base'
import {
  type CreateApiToolProviderRequest,
  type UpdateApiToolProviderRequest,
  type GetApiToolProviderResponse,
} from '@/models/api-tool'

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

export const validateOpenAPISchema = async (openapi_schema: string): Promise<BaseResponse<any>> => {
  const res = await request({
    url: '/api-tools/validate-openapi-schema',
    method: 'post',
    data: {
      openapi_schema,
    },
  })
  return res as BaseResponse<any>
}

export const createApiToolProvider = async (
  req: CreateApiToolProviderRequest,
): Promise<BaseResponse<any>> => {
  const res = await request({
    url: '/api-tools',
    method: 'post',
    data: req,
  })
  return res as BaseResponse<any>
}

export const deleteApiToolProvider = async (provider_id: string): Promise<BaseResponse<any>> => {
  const res = await request({
    url: `/api-tools/${provider_id}/delete`,
    method: 'post',
  })
  return res as BaseResponse<any>
}

export const updateApiToolProvider = async (
  provider_id: string,
  req: UpdateApiToolProviderRequest,
): Promise<BaseResponse<any>> => {
  const res = await request({
    url: `/api-tools/${provider_id}/update`,
    method: 'post',
    data: req,
  })
  return res as BaseResponse<any>
}

export const getApiToolProvider = async (provider_id: string): Promise<BaseResponse<GetApiToolProviderResponse>> => {
  const res = await request({
    url: `/api-tools/${provider_id}`,
    method: 'get',
  })
  return res as BaseResponse<GetApiToolProviderResponse>
}
