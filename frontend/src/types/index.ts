export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Receipt {
  id: number;
  shop_name: string | null;
  transaction_date: string | null;
  transaction_total_amount: string | null;
  receipt_image_url: string | null;
  created_at: string;
}

export interface MonthlyStat {
  month: string;
  total: string;
}

export interface Stats {
  total_expenses: string;
  receipt_count: number;
  monthly_summary: MonthlyStat[];
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface TokenPair {
  access: string;
  refresh: string;
}
