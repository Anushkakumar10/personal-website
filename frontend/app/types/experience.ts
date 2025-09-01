export interface ExperienceBase {
  company: string;
  role: string;
  start_date?: string | null; // ISO date
  end_date?: string | null;
  location?: string | null;
  description?: string | null;
  currently?: boolean | null;
  skills?: string[];
}
export interface ExperienceCreate extends ExperienceBase {
  profile_id: number;
}
export interface ExperienceRead extends ExperienceBase {
  id: number;
  profile_id: number;
}
