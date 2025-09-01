import type { ProfileBase, ProfileRead } from "@/app/types/profile";
const API_ROOT = (process.env.NEXT_PUBLIC_API_URL ?? "").replace(/\/$/, "");
const BASE = `${API_ROOT}/api/profiles`;

export const getProfiles = async (): Promise<ProfileRead[]> =>
  (await fetch(BASE)).json();
export const getProfile = async (id: number): Promise<ProfileRead> =>
  (await fetch(`${BASE}/${id}`)).json();
export const createProfile = async (
  payload: ProfileBase
): Promise<ProfileRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const updateProfile = async (
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
export const deleteProfile = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
