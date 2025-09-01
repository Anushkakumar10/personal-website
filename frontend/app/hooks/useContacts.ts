import type { ContactCreate, ContactRead } from "@/app/types/contact";
const BASE = "/api/contacts";

export const useGetContacts = async (): Promise<ContactRead[]> =>
  (await fetch(BASE)).json();
export const useGetContact = async (id: number): Promise<ContactRead> =>
  (await fetch(`${BASE}/${id}`)).json();
export const useCreateContact = async (
  payload: ContactCreate
): Promise<ContactRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useUpdateContact = async (
  id: number,
  payload: Partial<ContactCreate>
): Promise<ContactRead> =>
  (
    await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useDeleteContact = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
