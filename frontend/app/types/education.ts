export interface EducationBase {
  institution: string;
  degree?: string | null;
  field_of_study?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  grade?: string | null;
  description?: string | null;
}
export interface EducationCreate extends EducationBase {
  profile_id: number;
}
export interface EducationRead extends EducationBase {
  id: number;
  profile_id: number;
}
