export interface ContactBase {
  email?: string | null;
  phone?: string | null;
  website?: string | null;
  address?: string | null;
}
export interface ContactCreate extends ContactBase {
  profile_id: number;
}
export interface ContactRead extends ContactBase {
  id: number;
  profile_id: number;
}
