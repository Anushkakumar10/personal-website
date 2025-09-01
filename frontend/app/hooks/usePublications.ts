import type {
  PublicationCreate,
  PublicationRead,
} from "@/app/types/publication";
const API_ROOT = (process.env.NEXT_PUBLIC_API_URL ?? "").replace(/\/$/, "");
const BASE = `${API_ROOT}/api/publications`;

export const useGetPublications = async (): Promise<PublicationRead[]> =>
  (await fetch(BASE)).json();
export const useGetPublication = async (id: number): Promise<PublicationRead> =>
  (await fetch(`${BASE}/${id}`)).json();
export const useCreatePublication = async (
  payload: PublicationCreate
): Promise<PublicationRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useUpdatePublication = async (
  id: number,
  payload: Partial<PublicationCreate>
): Promise<PublicationRead> =>
  (
    await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useDeletePublication = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
