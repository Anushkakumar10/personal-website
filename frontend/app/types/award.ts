export interface AwardBase {
  title: string;
  issuer?: string | null;
  date?: string | null;
  description?: string | null;
}
export interface AwardCreate extends AwardBase {
  profile_id: number;
}
export interface AwardRead extends AwardBase {
  id: number;
  profile_id: number;
}
