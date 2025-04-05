export interface FormItem {
    type: 'input' | 'select' | 'datepicker' | 'textarea'
    label: string
    prop: string
    placeholder?: string
    options?: Array<{ label: string; value: string | number }>
    rules?: Array<{ required?: boolean; message: string }>
    rows?: number
}

export interface TableColumn {
    prop: string
    label: string
    width?: string
    render?: (row: any) => {
        type: string
        buttons?: Array<{
            type: string
            text: string
            onClick: () => void
        }>
    }
}

export interface Pagination {
    current: number
    pageSize: number
    total: number
}

export interface TableData {
    id?: number
    name: string
    status: string
    createDate?: string
    description?: string
} 