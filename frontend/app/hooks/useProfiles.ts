import type { ProfileBase, ProfileRead } from "@/app/types/profile";
const BASE = "/api/profiles";

export const useGetProfiles = async (): Promise<ProfileRead[]> =>
  (await fetch(BASE)).json();
export const useGetProfile = async (id: number): Promise<ProfileRead> =>
  (await fetch(`${BASE}/${id}`)).json();
export const useCreateProfile = async (
  payload: ProfileBase
): Promise<ProfileRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useUpdateProfile = async (
  id: number,
  payload: Partial<ProfileBase>
): Promise<ProfileRead> =>
  (
    await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useDeleteProfile = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
