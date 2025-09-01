import type { ReferenceCreate, ReferenceRead } from "@/app/types/reference";
const API_ROOT = (process.env.NEXT_PUBLIC_API_URL ?? "").replace(/\/$/, "");
const BASE = `${API_ROOT}/api/references`;

export const useGetReferences = async (): Promise<ReferenceRead[]> =>
  (await fetch(BASE)).json();
export const useGetReference = async (id: number): Promise<ReferenceRead> =>
  (await fetch(`${BASE}/${id}`)).json();
export const useCreateReference = async (
  payload: ReferenceCreate
): Promise<ReferenceRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useUpdateReference = async (
  id: number,
  payload: Partial<ReferenceCreate>
): Promise<ReferenceRead> =>
  (
    await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useDeleteReference = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
