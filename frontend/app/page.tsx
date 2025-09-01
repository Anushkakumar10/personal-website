import Image from "next/image";
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { getProfile } from "@/app/hooks/useProfiles";
import type { ProfileRead } from "@/app/types/profile";
import { JSX } from "react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Profile — Details",
  description: "A clean, modern profile details page",
};

function IconExternal() {
  return (
    <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" aria-hidden>
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

function DateRange(start?: string | null, end?: string | null) {
  if (!start && !end) return null;
  const s = start ? new Date(start).toLocaleDateString() : "—";
  const e = end ? new Date(end).toLocaleDateString() : "Present";
  return (
    <div className="text-sm text-muted-foreground">
      {s} — {e}
    </div>
  );
}

export default async function Home(): Promise<JSX.Element> {
  // fetch profiles server-side using provided helper
  const profile: ProfileRead | null = await getProfile(1).catch(() => null);

  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-[var(--background)] text-[var(--foreground)]`}
      >
        <main className="min-h-screen max-w-6xl mx-auto p-8 sm:p-12">
          <header className="mb-8">
            <div className="flex items-center gap-4">
              <div className="flex-none w-20 h-20 rounded-2xl bg-gradient-to-br from-gray-900 to-gray-700 dark:from-gray-200 dark:to-gray-400 shadow-lg flex items-center justify-center transform transition-transform duration-300 hover:scale-105">
                <Image
                  src="/next.svg"
                  alt="logo"
                  width={56}
                  height={56}
                  className="dark:invert"
                />
              </div>
              <div className="flex-1">
                <h1 className="text-3xl font-semibold tracking-tight">
                  {profile ? profile.name : "No profile found"}
                </h1>
                <p className="mt-1 text-sm text-muted-foreground">
                  {profile?.title ?? "—"}{" "}
                  {profile?.location ? `· ${profile.location}` : ""}
                </p>
              </div>
              <div className="flex-none">
                <a
                  className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-foreground text-background text-sm font-medium shadow hover:shadow-lg transition-shadow"
                  href="#"
                >
                  Share
                </a>
              </div>
            </div>
            <p className="mt-6 text-gray-600 dark:text-gray-300 max-w-3xl leading-relaxed">
              {profile?.summary ??
                "A refined profile layout that prioritizes clarity and simplicity. Small, intentional animations and cohesive spacing make the information easy to consume."}
            </p>
          </header>

          {/* Top cards */}
          <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="col-span-1 md:col-span-1 bg-white dark:bg-[#0b0b0b] rounded-2xl p-5 shadow-sm border border-transparent hover:border-gray-200 dark:hover:border-white/5 transition-all transform hover:-translate-y-1">
              <h3 className="text-sm font-semibold mb-3">Contact</h3>
              <div className="space-y-2 text-sm">
                {profile?.contacts?.map((c) => (
                  <div key={c.id} className="flex items-center justify-between">
                    <div className="truncate">
                      {c.email && (
                        <div className="text-foreground">{c.email}</div>
                      )}
                      {c.phone && (
                        <div className="text-muted-foreground text-xs">
                          {c.phone}
                        </div>
                      )}
                      {!c.email && !c.phone && (
                        <div className="text-xs text-muted-foreground">
                          No contact info
                        </div>
                      )}
                    </div>
                    {c.website && (
                      <a
                        href={c.website}
                        target="_blank"
                        rel="noreferrer"
                        className="text-muted-foreground hover:text-foreground"
                      >
                        <IconExternal />
                      </a>
                    )}
                  </div>
                ))}
                {!profile?.contacts?.length && (
                  <div className="text-sm text-muted-foreground">
                    No contacts yet
                  </div>
                )}
              </div>
            </div>

            <div className="bg-white dark:bg-[#0b0b0b] rounded-2xl p-5 shadow-sm border border-transparent hover:border-gray-200 dark:hover:border-white/5 transition-all transform hover:-translate-y-1">
              <h3 className="text-sm font-semibold mb-3">Skills</h3>
              <div className="flex flex-wrap gap-2">
                {profile?.skill_items?.length
                  ? profile.skill_items.map((s) => (
                      <span
                        key={s.id}
                        className="px-3 py-1 rounded-full bg-gray-100 dark:bg-white/6 text-sm text-foreground/90 transition-colors"
                      >
                        {s.name} {s.proficiency ? `· ${s.proficiency}%` : ""}
                      </span>
                    ))
                  : (profile?.skills ?? []).map((s, i) => (
                      <span
                        key={i}
                        className="px-3 py-1 rounded-full bg-gray-100 dark:bg-white/6 text-sm text-foreground/90"
                      >
                        {s}
                      </span>
                    ))}
              </div>
            </div>

            <div className="bg-white dark:bg-[#0b0b0b] rounded-2xl p-5 shadow-sm border border-transparent hover:border-gray-200 dark:hover:border-white/5 transition-all transform hover:-translate-y-1">
              <h3 className="text-sm font-semibold mb-3">Social</h3>
              <div className="flex flex-col gap-2">
                {profile?.social_links?.map((s) => (
                  <a
                    key={s.id}
                    href={s.url ?? "#"}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center justify-between px-3 py-2 rounded-lg hover:bg-gray-50 dark:hover:bg-white/6 transition"
                  >
                    <div className="truncate">
                      <div className="text-sm font-medium">
                        {s.platform ?? s.username ?? "Link"}
                      </div>
                      <div className="text-xs text-muted-foreground truncate">
                        {s.url}
                      </div>
                    </div>
                    <IconExternal />
                  </a>
                ))}

                {!profile?.social_links?.length && (
                  <div className="text-sm text-muted-foreground">
                    No social links
                  </div>
                )}
              </div>
            </div>
          </section>

          {/* Section lists */}
          <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <div>
                <h2 className="text-lg font-semibold mb-4">Experience</h2>
                <div className="space-y-4">
                  {profile?.experiences?.length ? (
                    profile.experiences.map((e) => (
                      <article
                        key={e.id}
                        className="p-4 rounded-xl bg-white dark:bg-[#0b0b0b] shadow-sm border border-transparent hover:shadow-lg transition-shadow transform hover:-translate-y-0.5"
                      >
                        <div className="flex items-start justify-between gap-4">
                          <div>
                            <div className="text-sm font-semibold">
                              {e.role}{" "}
                              <span className="text-muted-foreground text-sm">
                                at {e.company}
                              </span>
                            </div>
                            <div className="text-xs text-muted-foreground mt-1">
                              {e.location ?? ""}
                            </div>
                          </div>
                          <div className="text-right">
                            {DateRange(e.start_date, e.end_date)}
                          </div>
                        </div>
                        {e.description && (
                          <p className="mt-3 text-sm text-muted-foreground">
                            {e.description}
                          </p>
                        )}
                        {e.skills?.length ? (
                          <div className="mt-3 flex flex-wrap gap-2">
                            {e.skills.map((sk, i) => (
                              <span
                                key={i}
                                className="text-xs px-2 py-1 rounded-md bg-gray-100 dark:bg-white/6"
                              >
                                {sk}
                              </span>
                            ))}
                          </div>
                        ) : null}
                      </article>
                    ))
                  ) : (
                    <div className="text-sm text-muted-foreground">
                      No experiences recorded
                    </div>
                  )}
                </div>
              </div>

              <div>
                <h2 className="text-lg font-semibold mb-4">Projects</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {profile?.projects?.length ? (
                    profile.projects.map((p) => (
                      <div
                        key={p.id}
                        className="p-4 rounded-xl bg-white dark:bg-[#0b0b0b] shadow-sm hover:shadow-lg transition-shadow"
                      >
                        <div className="flex items-center justify-between">
                          <h3 className="font-medium">{p.title}</h3>
                          <div className="text-xs text-muted-foreground">
                            {p.skills?.slice(0, 3).join(", ")}
                          </div>
                        </div>
                        {p.description && (
                          <p className="mt-2 text-sm text-muted-foreground">
                            {p.description}
                          </p>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="text-sm text-muted-foreground">
                      No projects yet
                    </div>
                  )}
                </div>
              </div>

              <div>
                <h2 className="text-lg font-semibold mb-4">Education</h2>
                <div className="space-y-3">
                  {profile?.educations?.length ? (
                    profile.educations.map((ed) => (
                      <div
                        key={ed.id}
                        className="p-3 rounded-lg bg-white dark:bg-[#0b0b0b] shadow-sm"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-medium">{ed.institution}</div>
                            <div className="text-sm text-muted-foreground">
                              {ed.degree ?? ed.field_of_study}
                            </div>
                          </div>
                          <div className="text-sm text-muted-foreground">
                            {ed.start_date
                              ? new Date(ed.start_date).getFullYear()
                              : ""}{" "}
                            —{" "}
                            {ed.end_date
                              ? new Date(ed.end_date).getFullYear()
                              : "Present"}
                          </div>
                        </div>
                        {ed.description && (
                          <p className="mt-2 text-sm text-muted-foreground">
                            {ed.description}
                          </p>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="text-sm text-muted-foreground">
                      No education entries
                    </div>
                  )}
                </div>
              </div>
            </div>

            <aside className="space-y-6">
              <div className="p-4 rounded-2xl bg-white dark:bg-[#0b0b0b] shadow-sm">
                <h3 className="text-sm font-semibold mb-3">Publications</h3>
                <div className="flex flex-col gap-3">
                  {profile?.publications?.length ? (
                    profile.publications.map((pub) => (
                      <a
                        key={pub.id}
                        href={pub.url ?? "#"}
                        target="_blank"
                        rel="noreferrer"
                        className="text-sm hover:underline flex items-start gap-3"
                      >
                        <div className="text-xs text-muted-foreground">
                          {pub.publication_date
                            ? new Date(pub.publication_date).getFullYear()
                            : ""}
                        </div>
                        <div className="truncate">
                          <div className="font-medium">{pub.title}</div>
                          {pub.publisher && (
                            <div className="text-xs text-muted-foreground">
                              {pub.publisher}
                            </div>
                          )}
                        </div>
                      </a>
                    ))
                  ) : (
                    <div className="text-sm text-muted-foreground">
                      No publications
                    </div>
                  )}
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-white dark:bg-[#0b0b0b] shadow-sm">
                <h3 className="text-sm font-semibold mb-3">Portfolio</h3>
                <div className="flex flex-col gap-3">
                  {profile?.portfolio_items?.length ? (
                    profile.portfolio_items.map((item) => (
                      <a
                        key={item.id}
                        href={item.url ?? "#"}
                        target="_blank"
                        rel="noreferrer"
                        className="group flex items-center gap-3"
                      >
                        <div className="w-12 h-8 rounded-md bg-gray-100 dark:bg-white/6 flex-none overflow-hidden flex items-center justify-center text-xs">
                          {item.screenshot_url ? (
                            <Image
                              src={item.screenshot_url}
                              alt={item.title}
                              width={48}
                              height={32}
                              className="w-full h-full object-cover"
                            />
                          ) : (
                            <span className="text-xs">
                              {item.title?.slice(0, 2)}
                            </span>
                          )}
                        </div>
                        <div className="flex-1">
                          <div className="text-sm font-medium">
                            {item.title}
                          </div>
                          {item.description && (
                            <div className="text-xs text-muted-foreground">
                              {item.description}
                            </div>
                          )}
                        </div>
                        <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                          <IconExternal />
                        </div>
                      </a>
                    ))
                  ) : (
                    <div className="text-sm text-muted-foreground">
                      No portfolio items
                    </div>
                  )}
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-white dark:bg-[#0b0b0b] shadow-sm">
                <h3 className="text-sm font-semibold mb-3">References</h3>
                <div className="space-y-3 text-sm text-muted-foreground">
                  {profile?.references?.length ? (
                    profile.references.map((r) => (
                      <div key={r.id}>
                        <div className="font-medium text-foreground">
                          {r.name}{" "}
                          <span className="text-xs text-muted-foreground">
                            · {r.relation}
                          </span>
                        </div>
                        {r.contact_info && (
                          <div className="text-xs">{r.contact_info}</div>
                        )}
                      </div>
                    ))
                  ) : (
                    <div>No references</div>
                  )}
                </div>
              </div>
            </aside>
          </section>

          <footer className="mt-12 text-center text-sm text-muted-foreground">
            Built with intention.
          </footer>
        </main>
      </body>
    </html>
  );
}
