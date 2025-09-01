import type {
  CertificationCreate,
  CertificationRead,
} from "@/app/types/certification";
const API_ROOT = (process.env.NEXT_PUBLIC_API_URL ?? "").replace(/\/$/, "");
const BASE = `${API_ROOT}/api/certifications`;

export const useGetCertifications = async (): Promise<CertificationRead[]> =>
  (await fetch(BASE)).json();
export const useGetCertification = async (
  id: number
): Promise<CertificationRead> => (await fetch(`${BASE}/${id}`)).json();
export const useCreateCertification = async (
  payload: CertificationCreate
): Promise<CertificationRead> =>
  (
    await fetch(BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useUpdateCertification = async (
  id: number,
  payload: Partial<CertificationCreate>
): Promise<CertificationRead> =>
  (
    await fetch(`${BASE}/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
  ).json();
export const useDeleteCertification = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
