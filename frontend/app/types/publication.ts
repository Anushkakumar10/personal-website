export interface PublicationBase {
  title: string;
  publisher?: string | null;
  publication_date?: string | null;
  url?: string | null;
  description?: string | null;
}
export interface PublicationCreate extends PublicationBase {
  profile_id: number;
}
export interface PublicationRead extends PublicationBase {
  id: number;
  profile_id: number;
}
