import type { ExperienceCreate, ExperienceRead } from "@/app/types/experience";
const BASE = "/api/experiences";

export const useGetExperiences = async (): Promise<ExperienceRead[]> => {
  const res = await fetch(BASE);
  return res.json();
};

export const useGetExperience = async (id: number): Promise<ExperienceRead> => {
  const res = await fetch(`${BASE}/${id}`);
  return res.json();
};

export const useCreateExperience = async (
  payload: ExperienceCreate
): Promise<ExperienceRead> => {
  const res = await fetch(BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
};

export const useUpdateExperience = async (
  id: number,
  payload: Partial<ExperienceCreate>
): Promise<ExperienceRead> => {
  const res = await fetch(`${BASE}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
};

export const useDeleteExperience = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
