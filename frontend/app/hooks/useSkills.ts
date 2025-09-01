import type { SkillCreate, SkillRead } from "@/app/types/skill";
const BASE = "/api/skills";

export const useGetSkills = async (): Promise<SkillRead[]> =>
  (await fetch(BASE)).json();
export const useGetSkill = async (id: number): Promise<SkillRead> =>
  (await fetch(`${BASE}/${id}`)).json();
export const useCreateSkill = async (
  payload: SkillCreate
): Promise<SkillRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useUpdateSkill = async (
  id: number,
  payload: Partial<SkillCreate>
): Promise<SkillRead> =>
  (
    await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useDeleteSkill = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
