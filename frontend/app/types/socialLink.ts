export interface SocialLinkBase {
  platform?: string | null;
  url?: string | null;
  username?: string | null;
}
export interface SocialLinkCreate extends SocialLinkBase {
  profile_id: number;
}
export interface SocialLinkRead extends SocialLinkBase {
  id: number;
  profile_id: number;
}
