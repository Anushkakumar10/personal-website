import Image from "next/image";
import type { Metadata } from "next";
import { getProfile } from "@/app/hooks/useProfiles";
import type { ProfileRead } from "@/app/types/profile";
import { JSX } from "react";

export const metadata: Metadata = {
  title: "Profile — Details",
  description: "A clean, modern profile details page",
};

function IconExternal() {
  return (
    <svg
      className="w-4 h-4 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5"
      viewBox="0 0 24 24"
      fill="none"
      aria-hidden
    >
      <path
        d="M14 3h7v7"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M21 3L10 14"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M21 21H3V3"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconShare() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M18 8a3 3 0 1 0-3-3v.5l-6 3.5a3 3 0 1 0 0 4l6 3.5V16a3 3 0 1 0 3-3c-.18 0-.35.02-.5.05L11.45 9.5c.03-.15.05-.32.05-.5s-.02-.35-.05-.5L17.5 5.05c.15.03.32.05.5.05Z"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconEmail() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <polyline
        points="22,6 12,13 2,6"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconPhone() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconMapPin() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" aria-hidden>
      <path
        d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle
        cx="12"
        cy="10"
        r="3"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function DateRange(start?: string | null, end?: string | null) {
  if (!start && !end) return null;
  const s = start ? new Date(start).toLocaleDateString() : "—";
  const e = end ? new Date(end).toLocaleDateString() : "Present";
  return (
    <div className="text-sm text-[var(--muted-foreground)] font-medium">
      {s} — {e}
    </div>
  );
}

function SkillProficiencyBar({ proficiency }: { proficiency?: number | null }) {
  if (!proficiency) return null;

  return (
    <div className="w-full bg-[var(--muted)] rounded-full h-1.5 mt-1">
      <div
        className="bg-[var(--primary)] h-1.5 rounded-full transition-all duration-500 ease-out"
        style={{ width: `${proficiency}%` }}
      />
    </div>
  );
}

export default async function Home(): Promise<JSX.Element> {
  // fetch profiles server-side using provided helper
  const profile: ProfileRead | null = await getProfile(1).catch(() => null);

  return (
    <main className="min-h-screen bg-[var(--background)] text-[var(--foreground)]">
      {/* Header Section */}
      <header className="bg-[var(--card)] border-b border-[var(--border)] sticky top-0 z-10 backdrop-blur-sm bg-opacity-90">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center gap-6 animate-fade-in-up">
            <div className="relative flex-none">
              <div className="w-24 h-24 rounded-2xl bg-gradient-to-br from-[var(--primary)] to-blue-600 shadow-lg flex items-center justify-center transition-all duration-300 hover:shadow-xl hover:scale-105 focus-ring status-indicator">
                <Image
                  src="/next.svg"
                  alt="Profile avatar"
                  width={48}
                  height={48}
                  className="dark:invert transition-transform duration-300"
                />
              </div>
            </div>

            <div className="flex-1 min-w-0">
              <h1 className="text-4xl font-bold tracking-tight text-[var(--foreground)] mb-2">
                {profile ? profile.name : "No profile found"}
              </h1>
              <div className="flex items-center gap-4 text-[var(--muted-foreground)] mb-3">
                <span className="text-lg font-medium text-[var(--primary)]">
                  {profile?.title ?? "Software Engineer"}
                </span>
                {profile?.location && (
                  <>
                    <span className="text-[var(--border)]">•</span>
                    <div className="flex items-center gap-1.5">
                      <IconMapPin />
                      <span>{profile.location}</span>
                    </div>
                  </>
                )}
              </div>
              <p className="text-[var(--muted-foreground)] max-w-3xl leading-relaxed">
                {profile?.summary ??
                  "A passionate developer focused on creating exceptional user experiences and solving complex problems through clean, efficient code."}
              </p>
            </div>

            <div className="flex-none flex gap-3 animate-slide-in-right">
              <button className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[var(--primary)] text-[var(--primary-foreground)] font-medium shadow-lg hover:shadow-xl transition-all duration-200 hover:-translate-y-0.5 focus-ring animate-pulse-ring">
                <IconShare />
                Share Profile
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Quick Stats Cards */}
        <section className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-[var(--card)] rounded-2xl p-6 border border-[var(--border)] card-hover focus-ring">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-semibold text-[var(--muted-foreground)] uppercase tracking-wide">
                Experience
              </h3>
              <div className="w-2 h-2 bg-[var(--success)] rounded-full"></div>
            </div>
            <div className="text-2xl font-bold text-[var(--foreground)]">
              {profile?.experiences?.length ?? 0}
            </div>
            <p className="text-sm text-[var(--muted-foreground)]">Roles</p>
          </div>

          <div className="bg-[var(--card)] rounded-2xl p-6 border border-[var(--border)] card-hover focus-ring">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-semibold text-[var(--muted-foreground)] uppercase tracking-wide">
                Projects
              </h3>
              <div className="w-2 h-2 bg-[var(--primary)] rounded-full"></div>
            </div>
            <div className="text-2xl font-bold text-[var(--foreground)]">
              {profile?.projects?.length ?? 0}
            </div>
            <p className="text-sm text-[var(--muted-foreground)]">Completed</p>
          </div>

          <div className="bg-[var(--card)] rounded-2xl p-6 border border-[var(--border)] card-hover focus-ring">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-semibold text-[var(--muted-foreground)] uppercase tracking-wide">
                Skills
              </h3>
              <div className="w-2 h-2 bg-[var(--warning)] rounded-full"></div>
            </div>
            <div className="text-2xl font-bold text-[var(--foreground)]">
              {profile?.skill_items?.length ?? profile?.skills?.length ?? 0}
            </div>
            <p className="text-sm text-[var(--muted-foreground)]">
              Technologies
            </p>
          </div>

          <div className="bg-[var(--card)] rounded-2xl p-6 border border-[var(--border)] card-hover focus-ring">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-semibold text-[var(--muted-foreground)] uppercase tracking-wide">
                Education
              </h3>
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
            </div>
            <div className="text-2xl font-bold text-[var(--foreground)]">
              {profile?.educations?.length ?? 0}
            </div>
            <p className="text-sm text-[var(--muted-foreground)]">Degrees</p>
          </div>
        </section>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-3 space-y-8">
            {/* Experience Section */}
            <section className="bg-[var(--card)] rounded-2xl p-8 border border-[var(--border)] card-hover">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-[var(--foreground)]">
                  Experience
                </h2>
                <span className="text-sm text-[var(--muted-foreground)] bg-[var(--muted)] px-3 py-1 rounded-full">
                  {profile?.experiences?.length ?? 0} roles
                </span>
              </div>

              <div className="space-y-6">
                {profile?.experiences?.length ? (
                  profile.experiences.map((e) => (
                    <article
                      key={e.id}
                      className="relative p-6 rounded-xl bg-[var(--muted)] border border-[var(--border)] hover:border-[var(--primary)] transition-all duration-200 group"
                    >
                      <div className="absolute left-0 top-0 bottom-0 w-1 bg-[var(--primary)] rounded-r-full opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>

                      <div className="flex items-start justify-between gap-4 mb-4">
                        <div className="flex-1">
                          <h3 className="text-xl font-semibold text-[var(--foreground)] mb-1">
                            {e.role}
                          </h3>
                          <div className="flex items-center gap-2 text-[var(--primary)] font-medium mb-2">
                            <span>{e.company}</span>
                            {e.location && (
                              <>
                                <span className="text-[var(--border)]">•</span>
                                <span className="text-[var(--muted-foreground)]">
                                  {e.location}
                                </span>
                              </>
                            )}
                          </div>
                        </div>
                        <div className="text-right">
                          {DateRange(e.start_date, e.end_date)}
                        </div>
                      </div>

                      {e.description && (
                        <p className="text-[var(--muted-foreground)] mb-4 leading-relaxed">
                          {e.description}
                        </p>
                      )}

                      {e.skills?.length ? (
                        <div className="flex flex-wrap gap-2">
                          {e.skills.map((skill, i) => (
                            <span
                              key={i}
                              className="px-3 py-1 text-xs font-medium bg-[var(--secondary)] text-[var(--secondary-foreground)] rounded-full skill-badge transition-all duration-200 hover:bg-[var(--primary)] hover:text-[var(--primary-foreground)]"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      ) : null}
                    </article>
                  ))
                ) : (
                  <div className="text-center py-12 text-[var(--muted-foreground)]">
                    <div className="w-16 h-16 bg-[var(--muted)] rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8" viewBox="0 0 24 24" fill="none">
                        <path
                          d="M20 6L9 17l-5-5"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </div>
                    <p>No experience entries yet</p>
                  </div>
                )}
              </div>
            </section>

            {/* Projects Section */}
            <section className="bg-[var(--card)] rounded-2xl p-8 border border-[var(--border)] card-hover">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-[var(--foreground)]">
                  Projects
                </h2>
                <span className="text-sm text-[var(--muted-foreground)] bg-[var(--muted)] px-3 py-1 rounded-full">
                  {profile?.projects?.length ?? 0} projects
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {profile?.projects?.length ? (
                  profile.projects.map((p) => (
                    <div
                      key={p.id}
                      className="p-6 rounded-xl bg-[var(--muted)] border border-[var(--border)] hover:border-[var(--primary)] transition-all duration-200 group card-hover"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <h3 className="font-semibold text-[var(--foreground)] group-hover:text-[var(--primary)] transition-colors">
                          {p.title}
                        </h3>
                        {p.skills?.length ? (
                          <span className="text-xs text-[var(--muted-foreground)] bg-[var(--secondary)] px-2 py-1 rounded-md">
                            {p.skills.length} skills
                          </span>
                        ) : null}
                      </div>

                      {p.description && (
                        <p className="text-sm text-[var(--muted-foreground)] mb-4 leading-relaxed">
                          {p.description}
                        </p>
                      )}

                      {p.skills?.length ? (
                        <div className="flex flex-wrap gap-1">
                          {p.skills.slice(0, 3).map((skill, i) => (
                            <span
                              key={i}
                              className="text-xs px-2 py-1 bg-[var(--secondary)] text-[var(--secondary-foreground)] rounded-md"
                            >
                              {skill}
                            </span>
                          ))}
                          {p.skills.length > 3 && (
                            <span className="text-xs px-2 py-1 bg-[var(--muted)] text-[var(--muted-foreground)] rounded-md">
                              +{p.skills.length - 3} more
                            </span>
                          )}
                        </div>
                      ) : null}
                    </div>
                  ))
                ) : (
                  <div className="col-span-2 text-center py-12 text-[var(--muted-foreground)]">
                    <div className="w-16 h-16 bg-[var(--muted)] rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8" viewBox="0 0 24 24" fill="none">
                        <path
                          d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </div>
                    <p>No projects to showcase yet</p>
                  </div>
                )}
              </div>
            </section>

            {/* Education Section */}
            <section className="bg-[var(--card)] rounded-2xl p-8 border border-[var(--border)] card-hover">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-[var(--foreground)]">
                  Education
                </h2>
                <span className="text-sm text-[var(--muted-foreground)] bg-[var(--muted)] px-3 py-1 rounded-full">
                  {profile?.educations?.length ?? 0} degrees
                </span>
              </div>

              <div className="space-y-4">
                {profile?.educations?.length ? (
                  profile.educations.map((ed) => (
                    <div
                      key={ed.id}
                      className="p-6 rounded-xl bg-[var(--muted)] border border-[var(--border)] hover:border-[var(--primary)] transition-all duration-200"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <div>
                          <h3 className="font-semibold text-[var(--foreground)]">
                            {ed.institution}
                          </h3>
                          <p className="text-[var(--primary)] font-medium">
                            {ed.degree ?? ed.field_of_study}
                          </p>
                        </div>
                        <div className="text-right text-[var(--muted-foreground)]">
                          <div className="font-medium">
                            {ed.start_date
                              ? new Date(ed.start_date).getFullYear()
                              : ""}{" "}
                            —{" "}
                            {ed.end_date
                              ? new Date(ed.end_date).getFullYear()
                              : "Present"}
                          </div>
                        </div>
                      </div>

                      {ed.description && (
                        <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                          {ed.description}
                        </p>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="text-center py-12 text-[var(--muted-foreground)]">
                    <div className="w-16 h-16 bg-[var(--muted)] rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg className="w-8 h-8" viewBox="0 0 24 24" fill="none">
                        <path
                          d="M22 10v6M2 10l10-5 10 5-10 5z"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                        <path
                          d="M6 12v5c3 3 9 3 12 0v-5"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </div>
                    <p>No education entries</p>
                  </div>
                )}
              </div>
            </section>
          </div>

          {/* Sidebar */}
          <aside className="space-y-6">
            {/* Contact Information */}
            <div className="bg-[var(--card)] rounded-2xl p-6 border border-[var(--border)] card-hover">
              <h3 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
                Contact
              </h3>
              <div className="space-y-3">
                {profile?.contacts?.map((c) => (
                  <div key={c.id} className="group">
                    {c.email && (
                      <a
                        href={`mailto:${c.email}`}
                        className="flex items-center gap-3 p-3 rounded-lg hover:bg-[var(--muted)] transition-colors duration-200 focus-ring group"
                      >
                        <div className="w-8 h-8 bg-[var(--primary)] bg-opacity-10 rounded-lg flex items-center justify-center text-[var(--primary)]">
                          <IconEmail />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-medium text-[var(--foreground)] truncate">
                            {c.email}
                          </div>
                          <div className="text-xs text-[var(--muted-foreground)]">
                            Email
                          </div>
                        </div>
                      </a>
                    )}

                    {c.phone && (
                      <a
                        href={`tel:${c.phone}`}
                        className="flex items-center gap-3 p-3 rounded-lg hover:bg-[var(--muted)] transition-colors duration-200 focus-ring group"
                      >
                        <div className="w-8 h-8 bg-[var(--success)] bg-opacity-10 rounded-lg flex items-center justify-center text-[var(--success)]">
                          <IconPhone />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-medium text-[var(--foreground)] truncate">
                            {c.phone}
                          </div>
                          <div className="text-xs text-[var(--muted-foreground)]">
                            Phone
                          </div>
                        </div>
                      </a>
                    )}

                    {c.website && (
                      <a
                        href={c.website}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center gap-3 p-3 rounded-lg hover:bg-[var(--muted)] transition-colors duration-200 focus-ring group"
                      >
                        <div className="w-8 h-8 bg-[var(--warning)] bg-opacity-10 rounded-lg flex items-center justify-center text-[var(--warning)]">
                          <IconExternal />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="text-sm font-medium text-[var(--foreground)] truncate">
                            Website
                          </div>
                          <div className="text-xs text-[var(--muted-foreground)] truncate">
                            {c.website}
                          </div>
                        </div>
                      </a>
                    )}
                  </div>
                ))}

                {!profile?.contacts?.length && (
                  <div className="text-center py-6 text-[var(--muted-foreground)]">
                    <p className="text-sm">No contact information</p>
                  </div>
                )}
              </div>
            </div>

            {/* Skills */}
            <div className="bg-[var(--card)] rounded-2xl p-6 border border-[var(--border)] card-hover">
              <h3 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
                Skills
              </h3>
              <div className="space-y-4">
                {profile?.skill_items?.length ? (
                  profile.skill_items.map((s) => (
                    <div key={s.id} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-[var(--foreground)]">
                          {s.name}
                        </span>
                        {s.proficiency && (
                          <span className="text-xs text-[var(--muted-foreground)]">
                            {s.proficiency}%
                          </span>
                        )}
                      </div>
                      <SkillProficiencyBar proficiency={s.proficiency} />
                    </div>
                  ))
                ) : profile?.skills?.length ? (
                  <div className="flex flex-wrap gap-2">
                    {profile.skills.map((s, i) => (
                      <span
                        key={i}
                        className="px-3 py-1.5 text-sm font-medium bg-[var(--muted)] text-[var(--foreground)] rounded-lg skill-badge hover:bg-[var(--primary)] hover:text-[var(--primary-foreground)] transition-all duration-200"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-6 text-[var(--muted-foreground)]">
                    <p className="text-sm">No skills listed</p>
                  </div>
                )}
              </div>
            </div>

            {/* Social Links */}
            <div className="bg-[var(--card)] rounded-2xl p-6 border border-[var(--border)] card-hover">
              <h3 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
                Social
              </h3>
              <div className="space-y-2">
                {profile?.social_links?.map((s) => (
                  <a
                    key={s.id}
                    href={s.url ?? "#"}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-3 p-3 rounded-lg hover:bg-[var(--muted)] transition-all duration-200 focus-ring group"
                  >
                    <div className="w-8 h-8 bg-gradient-to-br from-[var(--primary)] to-blue-600 rounded-lg flex items-center justify-center text-white text-xs font-semibold">
                      {(s.platform ?? s.username ?? "L")
                        .charAt(0)
                        .toUpperCase()}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-[var(--foreground)]">
                        {s.platform ?? s.username ?? "Link"}
                      </div>
                      <div className="text-xs text-[var(--muted-foreground)] truncate">
                        {s.url}
                      </div>
                    </div>
                    <IconExternal />
                  </a>
                ))}

                {!profile?.social_links?.length && (
                  <div className="text-center py-6 text-[var(--muted-foreground)]">
                    <p className="text-sm">No social links</p>
                  </div>
                )}
              </div>
            </div>

            {/* Portfolio */}
            <div className="bg-[var(--card)] rounded-2xl p-6 border border-[var(--border)] card-hover">
              <h3 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
                Portfolio
              </h3>
              <div className="space-y-3">
                {profile?.portfolio_items?.map((item) => (
                  <a
                    key={item.id}
                    href={item.url ?? "#"}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-3 p-3 rounded-lg hover:bg-[var(--muted)] transition-all duration-200 focus-ring group"
                  >
                    <div className="w-12 h-8 rounded-lg bg-[var(--muted)] flex-none overflow-hidden flex items-center justify-center">
                      {item.screenshot_url ? (
                        <Image
                          src={item.screenshot_url}
                          alt={item.title}
                          width={48}
                          height={32}
                          className="w-full h-full object-cover rounded-lg"
                        />
                      ) : (
                        <span className="text-xs text-[var(--muted-foreground)] font-semibold">
                          {item.title?.slice(0, 2).toUpperCase()}
                        </span>
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-[var(--foreground)] truncate">
                        {item.title}
                      </div>
                      {item.description && (
                        <div className="text-xs text-[var(--muted-foreground)] truncate">
                          {item.description}
                        </div>
                      )}
                    </div>
                    <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                      <IconExternal />
                    </div>
                  </a>
                ))}

                {!profile?.portfolio_items?.length && (
                  <div className="text-center py-6 text-[var(--muted-foreground)]">
                    <p className="text-sm">No portfolio items</p>
                  </div>
                )}
              </div>
            </div>

            {/* Publications */}
            <div className="bg-[var(--card)] rounded-2xl p-6 border border-[var(--border)] card-hover">
              <h3 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
                Publications
              </h3>
              <div className="space-y-3">
                {profile?.publications?.map((pub) => (
                  <a
                    key={pub.id}
                    href={pub.url ?? "#"}
                    target="_blank"
                    rel="noreferrer"
                    className="block p-3 rounded-lg hover:bg-[var(--muted)] transition-all duration-200 focus-ring group"
                  >
                    <div className="flex items-start gap-3">
                      <div className="text-xs text-[var(--muted-foreground)] font-mono pt-1">
                        {pub.publication_date
                          ? new Date(pub.publication_date).getFullYear()
                          : "—"}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm font-medium text-[var(--foreground)] group-hover:text-[var(--primary)] transition-colors">
                          {pub.title}
                        </div>
                        {pub.publisher && (
                          <div className="text-xs text-[var(--muted-foreground)] mt-1">
                            {pub.publisher}
                          </div>
                        )}
                      </div>
                    </div>
                  </a>
                ))}

                {!profile?.publications?.length && (
                  <div className="text-center py-6 text-[var(--muted-foreground)]">
                    <p className="text-sm">No publications</p>
                  </div>
                )}
              </div>
            </div>

            {/* References */}
            <div className="bg-[var(--card)] rounded-2xl p-6 border border-[var(--border)] card-hover">
              <h3 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
                References
              </h3>
              <div className="space-y-4">
                {profile?.references?.map((r) => (
                  <div key={r.id} className="p-3 rounded-lg bg-[var(--muted)]">
                    <div className="font-medium text-[var(--foreground)] text-sm">
                      {r.name}
                    </div>
                    <div className="text-xs text-[var(--primary)] font-medium mt-1">
                      {r.relation}
                    </div>
                    {r.contact_info && (
                      <div className="text-xs text-[var(--muted-foreground)] mt-1">
                        {r.contact_info}
                      </div>
                    )}
                  </div>
                ))}

                {!profile?.references?.length && (
                  <div className="text-center py-6 text-[var(--muted-foreground)]">
                    <p className="text-sm">No references</p>
                  </div>
                )}
              </div>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
}
