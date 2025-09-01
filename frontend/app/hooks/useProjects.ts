import type { ProjectCreate, ProjectRead } from "@/app/types/project";

const BASE = "/api/projects";

export const useGetProjects = async (): Promise<ProjectRead[]> => {
  const res = await fetch(BASE);
  return res.json();
};

export const useGetProject = async (id: number): Promise<ProjectRead> => {
  const res = await fetch(`${BASE}/${id}`);
  return res.json();
};

export const useCreateProject = async (
  payload: ProjectCreate
): Promise<ProjectRead> => {
  const res = await fetch(BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
};

export const useUpdateProject = async (
  id: number,
  payload: Partial<ProjectCreate>
): Promise<ProjectRead> => {
  const res = await fetch(`${BASE}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
};

export const useDeleteProject = async (id: number): Promise<void> => {
  await fetch(`${BASE}/${id}`, { method: "DELETE" });
};
