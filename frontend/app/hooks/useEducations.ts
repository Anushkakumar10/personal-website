import type { EducationCreate, EducationRead } from "@/app/types/education";
const BASE = "/api/educations";

export const useGetEducations = async (): Promise<EducationRead[]> =>
  (await fetch(BASE)).json();
export const useGetEducation = async (id: number): Promise<EducationRead> =>
  (await fetch(`${BASE}/${id}`)).json();
export const useCreateEducation = async (
  payload: EducationCreate
): Promise<EducationRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useUpdateEducation = async (
  id: number,
  payload: Partial<EducationCreate>
): Promise<EducationRead> =>
  (
    await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useDeleteEducation = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
