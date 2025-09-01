export interface SkillBase {
  name: string;
  proficiency?: number | null;
  years?: number | null;
}
export interface SkillCreate extends SkillBase {
  profile_id: number;
}
export interface SkillRead extends SkillBase {
  id: number;
  profile_id: number;
}
