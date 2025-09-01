export interface ProjectBase {
  title: string;
  description?: string | null;
  skills?: string[];
}
export interface ProjectCreate extends ProjectBase {
  profile_id?: number | null;
}
export interface ProjectRead extends ProjectBase {
  id: number;
  profile_id?: number | null;
}
