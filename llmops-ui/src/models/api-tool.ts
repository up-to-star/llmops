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
