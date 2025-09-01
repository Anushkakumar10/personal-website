export interface ReferenceBase {
  name: string;
  relation?: string | null;
  contact_info?: string | null;
  testimonial?: string | null;
}
export interface ReferenceCreate extends ReferenceBase {
  profile_id: number;
}
export interface ReferenceRead extends ReferenceBase {
  id: number;
  profile_id: number;
}
