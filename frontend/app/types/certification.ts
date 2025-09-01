export interface CertificationBase {
  name: string;
  issuer?: string | null;
  issue_date?: string | null;
  expiration_date?: string | null;
  credential_id?: string | null;
  credential_url?: string | null;
}
export interface CertificationCreate extends CertificationBase {
  profile_id: number;
}
export interface CertificationRead extends CertificationBase {
  id: number;
  profile_id: number;
}
