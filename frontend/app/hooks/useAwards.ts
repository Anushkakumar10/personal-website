import type { AwardCreate, AwardRead } from "@/app/types/award";
const BASE = "/api/awards";

export const useGetAwards = async (): Promise<AwardRead[]> =>
  (await fetch(BASE)).json();
export const useGetAward = async (id: number): Promise<AwardRead> =>
  (await fetch(`${BASE}/${id}`)).json();
export const useCreateAward = async (
  payload: AwardCreate
): Promise<AwardRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useUpdateAward = async (
  id: number,
  payload: Partial<AwardCreate>
): Promise<AwardRead> =>
  (
    await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useDeleteAward = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
