import { type BaseResponse } from '@/models/base'

export type GetCategoriesResponse = BaseResponse<
  Array<{
    catetory: string
    icon: string
    name: string
  }>
>

export type GetBuiltinToolsResponse = BaseResponse<
  Array<{
    background: string
    category: string
    create_at: number
    description: string
    label: string
    name: string
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    tools: Array<any>
  }>
>
