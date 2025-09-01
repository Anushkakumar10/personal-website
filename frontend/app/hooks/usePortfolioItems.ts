import type {
  PortfolioItemCreate,
  PortfolioItemRead,
} from "@/app/types/portfolioItem";
const API_ROOT = (process.env.NEXT_PUBLIC_API_URL ?? "").replace(/\/$/, "");
const BASE = `${API_ROOT}/api/portfolio-items`;

export const useGetPortfolioItems = async (): Promise<PortfolioItemRead[]> =>
  (await fetch(BASE)).json();
export const useGetPortfolioItem = async (
  id: number
): Promise<PortfolioItemRead> => (await fetch(`${BASE}/${id}`)).json();
export const useCreatePortfolioItem = async (
  payload: PortfolioItemCreate
): Promise<PortfolioItemRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useUpdatePortfolioItem = async (
  id: number,
  payload: Partial<PortfolioItemCreate>
): Promise<PortfolioItemRead> =>
  (
    await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useDeletePortfolioItem = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
