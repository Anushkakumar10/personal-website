import { ProjectRead } from "./project";
import { ExperienceRead } from "./experience";
import { EducationRead } from "./education";
import { CertificationRead } from "./certification";
import { AwardRead } from "./award";
import { PublicationRead } from "./publication";
import { ContactRead } from "./contact";
import { SocialLinkRead } from "./socialLink";
import { PortfolioItemRead } from "./portfolioItem";
import { ReferenceRead } from "./reference";
import { SkillRead } from "./skill";

export interface ProfileBase {
  name: string;
  title?: string | null;
  location?: string | null;
  summary?: string | null;
  skills?: string[];
}

export interface ProfileRead extends ProfileBase {
  id: number;
  projects: ProjectRead[];
  experiences: ExperienceRead[];
  educations: EducationRead[];
  certifications: CertificationRead[];
  awards: AwardRead[];
  publications: PublicationRead[];
  contacts: ContactRead[];
  social_links: SocialLinkRead[];
  portfolio_items: PortfolioItemRead[];
  references: ReferenceRead[];
  skill_items: SkillRead[];
}
