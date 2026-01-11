/* eslint-disable @typescript-eslint/no-explicit-any */
import { type BasePaginatorResponse } from '@/models/base'

export type GetApiToolProvidersWithPageResponse = BasePaginatorResponse<{
  id: string
  name: string
  icon: string
  description: string
  headers: Array<any>
  tools: Array<any>
  create_at: number
}>

export type CreateApiToolProviderRequest = {
  name: string
  icon: string
  openapi_schema: string
  headers: Array<any>
}

export type UpdateApiToolProviderRequest = {
  name: string
  icon: string
  openapi_schema: string
  headers: Array<any>
}

export type GetApiToolProviderResponse = {
  id: string
  name: string
  icon: string
  openapi_schema: string
  headers: Array<any>
  create_at: number
}
