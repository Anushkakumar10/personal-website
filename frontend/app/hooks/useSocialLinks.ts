import type { SocialLinkCreate, SocialLinkRead } from "@/app/types/socialLink";
const BASE = "/api/social-links";

export const useGetSocialLinks = async (): Promise<SocialLinkRead[]> =>
  (await fetch(BASE)).json();
export const useGetSocialLink = async (id: number): Promise<SocialLinkRead> =>
  (await fetch(`${BASE}/${id}`)).json();
export const useCreateSocialLink = async (
  payload: SocialLinkCreate
): Promise<SocialLinkRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useUpdateSocialLink = async (
  id: number,
  payload: Partial<SocialLinkCreate>
): Promise<SocialLinkRead> =>
  (
    await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useDeleteSocialLink = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
