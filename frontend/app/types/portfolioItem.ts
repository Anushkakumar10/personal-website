export interface PortfolioItemBase {
  title: string;
  description?: string | null;
  url?: string | null;
  screenshot_url?: string | null;
  skills?: string[];
  display_order?: number | null;
}
export interface PortfolioItemCreate extends PortfolioItemBase {
  profile_id: number;
}
export interface PortfolioItemRead extends PortfolioItemBase {
  id: number;
  profile_id: number;
}
