export type BaseResponse<T> = {
  code: number
  message: string
  data: T
}

export type BasePaginatorResponse<T> = BaseResponse<{
  list: Array<T>
  paginator: {
    total_page: number
    total_record: number
    current_page: number
    page_size: number
  }
}>
