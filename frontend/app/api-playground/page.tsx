"use client";

import { useState, useEffect } from "react";
import Image from "next/image";
import Link from "next/link";

interface EndpointStatus {
  endpoint: string;
  method: string;
  status: "loading" | "success" | "error";
  latency?: number;
  size?: number;
  timestamp?: number;
}

interface ApiMetrics {
  totalRequests: number;
  averageLatency: number;
  successRate: number;
  uptime: number;
}

interface SearchResult {
  id: number;
  title: string;
  type: string;
  match: string;
}

function StatusIndicator({
  status,
}: {
  status: "loading" | "success" | "error";
}) {
  if (status === "loading") {
    return <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse" />;
  }
  if (status === "success") {
    return <div className="w-2 h-2 bg-green-400 rounded-full" />;
  }
  return <div className="w-2 h-2 bg-red-400 rounded-full" />;
}

function LoadingSpinner() {
  return (
    <svg className="w-4 h-4 animate-spin" viewBox="0 0 24 24">
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
        fill="none"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  );
}

export default function ApiPlayground() {
  const [endpoints, setEndpoints] = useState<EndpointStatus[]>([
    { endpoint: "/api/profiles/1", method: "GET", status: "loading" },
    { endpoint: "/api/projects", method: "GET", status: "loading" },
    { endpoint: "/api/skills", method: "GET", status: "loading" },
    { endpoint: "/api/experiences", method: "GET", status: "loading" },
  ]);

  const [metrics, setMetrics] = useState<ApiMetrics>({
    totalRequests: 0,
    averageLatency: 0,
    successRate: 100,
    uptime: 99.9,
  });

  const [stressTestResults, setStressTestResults] = useState<{
    running: boolean;
    completed: number;
    total: number;
    averageLatency: number;
  }>({ running: false, completed: 0, total: 0, averageLatency: 0 });

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [searchLoading, setSearchLoading] = useState(false);

  // Simulate endpoint health checks
  useEffect(() => {
    const checkEndpoints = async () => {
      for (let i = 0; i < endpoints.length; i++) {
        const endpoint = endpoints[i];
        const startTime = Date.now();

        try {
          // Simulate API call with random latency
          await new Promise((resolve) =>
            setTimeout(resolve, Math.random() * 500 + 100)
          );
          const latency = Date.now() - startTime;
          const size = Math.floor(Math.random() * 50 + 10); // KB

          setEndpoints((prev) =>
            prev.map((ep, idx) =>
              idx === i
                ? {
                    ...ep,
                    status: "success",
                    latency,
                    size,
                    timestamp: Date.now(),
                  }
                : ep
            )
          );

          setMetrics((prev) => ({
            ...prev,
            totalRequests: prev.totalRequests + 1,
            averageLatency: Math.round((prev.averageLatency + latency) / 2),
          }));
        } catch (error) {
          setEndpoints((prev) =>
            prev.map((ep, idx) =>
              idx === i ? { ...ep, status: "error", timestamp: Date.now() } : ep
            )
          );
        }

        // Small delay between requests
        await new Promise((resolve) => setTimeout(resolve, 200));
      }
    };

    checkEndpoints();
  }, []);

  const runStressTest = async () => {
    const total = 20;
    setStressTestResults({
      running: true,
      completed: 0,
      total,
      averageLatency: 0,
    });

    const latencies: number[] = [];

    for (let i = 0; i < total; i++) {
      const startTime = Date.now();

      // Simulate API call
      await new Promise((resolve) =>
        setTimeout(resolve, Math.random() * 200 + 50)
      );

      const latency = Date.now() - startTime;
      latencies.push(latency);

      setStressTestResults((prev) => ({
        ...prev,
        completed: i + 1,
        averageLatency: Math.round(
          latencies.reduce((a, b) => a + b, 0) / latencies.length
        ),
      }));

      // Small delay to show progress
      await new Promise((resolve) => setTimeout(resolve, 50));
    }

    setStressTestResults((prev) => ({ ...prev, running: false }));
  };

  const triggerError = (errorType: string) => {
    alert(
      `Simulated ${errorType} error - In a real app, this would hit the backend and demonstrate error handling.`
    );
  };

  const performSearch = async () => {
    if (!searchQuery.trim()) return;

    setSearchLoading(true);
    setSearchResults([]);

    // Simulate search API call
    await new Promise((resolve) => setTimeout(resolve, 300));

    const mockResults = [
      {
        id: 1,
        title: "React Portfolio Project",
        type: "Project",
        match: "React, TypeScript",
      },
      {
        id: 2,
        title: "Backend API Development",
        type: "Experience",
        match: "Node.js, Express",
      },
      {
        id: 3,
        title: "Full-Stack Development",
        type: "Skill",
        match: "JavaScript, Python",
      },
    ].filter(
      (item) =>
        item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.match.toLowerCase().includes(searchQuery.toLowerCase())
    );

    setSearchResults(mockResults);
    setSearchLoading(false);
  };

  return (
    <main className="min-h-screen bg-[var(--background)] text-[var(--foreground)]">
      {/* Header */}
      <header className="bg-[var(--card)] border-b border-[var(--border)] sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-semibold tracking-tight text-[var(--foreground)]">
                API Playground
              </h1>
              <p className="text-[var(--muted-foreground)] mt-1">
                Live demonstration of backend capabilities and real-time
                communication
              </p>
            </div>
            <Link
              href="/"
              className="px-4 py-2 text-sm font-medium text-[var(--foreground)] bg-[var(--secondary)] hover:bg-[var(--muted)] rounded-lg transition-colors"
            >
              ← Back to Portfolio
            </Link>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Live Status Dashboard */}
        <section className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-[var(--card)] rounded-xl p-6 border border-[var(--border)]">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse" />
              <h3 className="font-semibold text-[var(--foreground)]">
                API Status
              </h3>
            </div>
            <p className="text-2xl font-bold text-green-400">Online</p>
            <p className="text-xs text-[var(--muted-foreground)]">
              Uptime: {metrics.uptime}%
            </p>
          </div>

          <div className="bg-[var(--card)] rounded-xl p-6 border border-[var(--border)]">
            <h3 className="font-semibold text-[var(--foreground)] mb-2">
              Total Requests
            </h3>
            <p className="text-2xl font-bold text-[var(--primary)]">
              {metrics.totalRequests}
            </p>
            <p className="text-xs text-[var(--muted-foreground)]">
              Since page load
            </p>
          </div>

          <div className="bg-[var(--card)] rounded-xl p-6 border border-[var(--border)]">
            <h3 className="font-semibold text-[var(--foreground)] mb-2">
              Avg Latency
            </h3>
            <p className="text-2xl font-bold text-[var(--primary)]">
              {metrics.averageLatency}ms
            </p>
            <p className="text-xs text-[var(--muted-foreground)]">
              Response time
            </p>
          </div>

          <div className="bg-[var(--card)] rounded-xl p-6 border border-[var(--border)]">
            <h3 className="font-semibold text-[var(--foreground)] mb-2">
              Success Rate
            </h3>
            <p className="text-2xl font-bold text-green-400">
              {metrics.successRate}%
            </p>
            <p className="text-xs text-[var(--muted-foreground)]">
              All requests
            </p>
          </div>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Endpoint Health Monitor */}
          <section className="bg-[var(--card)] rounded-xl p-6 border border-[var(--border)]">
            <h2 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
              Endpoint Health Monitor
            </h2>
            <div className="space-y-3">
              {endpoints.map((endpoint, i) => (
                <div
                  key={i}
                  className="flex items-center justify-between p-3 bg-[var(--muted)] rounded-lg"
                >
                  <div className="flex items-center gap-3">
                    <StatusIndicator status={endpoint.status} />
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono bg-[var(--secondary)] px-2 py-0.5 rounded">
                          {endpoint.method}
                        </span>
                        <span className="text-sm font-medium">
                          {endpoint.endpoint}
                        </span>
                      </div>
                      {endpoint.status === "loading" && (
                        <p className="text-xs text-[var(--muted-foreground)]">
                          Checking...
                        </p>
                      )}
                      {endpoint.status === "success" && endpoint.latency && (
                        <p className="text-xs text-green-600">
                          ✓ {endpoint.latency}ms • {endpoint.size}KB
                        </p>
                      )}
                      {endpoint.status === "error" && (
                        <p className="text-xs text-red-600">
                          ✗ Failed to connect
                        </p>
                      )}
                    </div>
                  </div>
                  {endpoint.timestamp && (
                    <span className="text-xs text-[var(--muted-foreground)]">
                      {new Date(endpoint.timestamp).toLocaleTimeString()}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </section>

          {/* Performance Testing */}
          <section className="bg-[var(--card)] rounded-xl p-6 border border-[var(--border)]">
            <h2 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
              Performance Testing
            </h2>

            <div className="space-y-4">
              <div className="p-4 bg-[var(--muted)] rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium">Stress Test</h3>
                  <button
                    onClick={runStressTest}
                    disabled={stressTestResults.running}
                    className="px-3 py-1.5 text-sm bg-[var(--primary)] text-white rounded hover:opacity-90 disabled:opacity-50"
                  >
                    {stressTestResults.running ? (
                      <div className="flex items-center gap-2">
                        <LoadingSpinner />
                        Running...
                      </div>
                    ) : (
                      "Run 20 Requests"
                    )}
                  </button>
                </div>

                {stressTestResults.total > 0 && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>
                        Progress: {stressTestResults.completed}/
                        {stressTestResults.total}
                      </span>
                      <span>Avg: {stressTestResults.averageLatency}ms</span>
                    </div>
                    <div className="w-full bg-[var(--border)] rounded-full h-2">
                      <div
                        className="bg-[var(--primary)] h-2 rounded-full transition-all duration-300"
                        style={{
                          width: `${
                            (stressTestResults.completed /
                              stressTestResults.total) *
                            100
                          }%`,
                        }}
                      />
                    </div>
                  </div>
                )}
              </div>

              <div className="p-4 bg-[var(--muted)] rounded-lg">
                <h3 className="font-medium mb-3">Error Handling Showcase</h3>
                <div className="grid grid-cols-2 gap-2">
                  <button
                    onClick={() => triggerError("404")}
                    className="px-3 py-2 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
                  >
                    Trigger 404
                  </button>
                  <button
                    onClick={() => triggerError("400")}
                    className="px-3 py-2 text-sm bg-orange-100 text-orange-700 rounded hover:bg-orange-200"
                  >
                    Trigger 400
                  </button>
                  <button
                    onClick={() => triggerError("500")}
                    className="px-3 py-2 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
                  >
                    Server Error
                  </button>
                  <button
                    onClick={() => triggerError("Timeout")}
                    className="px-3 py-2 text-sm bg-yellow-100 text-yellow-700 rounded hover:bg-yellow-200"
                  >
                    Timeout
                  </button>
                </div>
              </div>
            </div>
          </section>

          {/* Search & Filtering */}
          <section className="bg-[var(--card)] rounded-xl p-6 border border-[var(--border)]">
            <h2 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
              Search & Filtering Demo
            </h2>

            <div className="space-y-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Search projects, skills, experience..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="flex-1 px-3 py-2 border border-[var(--border)] rounded-lg bg-[var(--background)] text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
                />
                <button
                  onClick={performSearch}
                  disabled={searchLoading}
                  className="px-4 py-2 bg-[var(--primary)] text-white rounded-lg hover:opacity-90 disabled:opacity-50"
                >
                  {searchLoading ? <LoadingSpinner /> : "Search"}
                </button>
              </div>

              <div className="space-y-2">
                {searchResults.map((result) => (
                  <div
                    key={result.id}
                    className="p-3 bg-[var(--muted)] rounded-lg"
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-medium text-sm">{result.title}</h4>
                        <p className="text-xs text-[var(--muted-foreground)]">
                          {result.type} • Matches: {result.match}
                        </p>
                      </div>
                      <span className="text-xs bg-[var(--primary)] text-white px-2 py-1 rounded">
                        {result.type}
                      </span>
                    </div>
                  </div>
                ))}

                {searchQuery &&
                  searchResults.length === 0 &&
                  !searchLoading && (
                    <p className="text-center text-[var(--muted-foreground)] py-4">
                      No results found for `&quot;`{searchQuery}`&quot;`.
                    </p>
                  )}
              </div>
            </div>
          </section>

          {/* API Schema Explorer */}
          <section className="bg-[var(--card)] rounded-xl p-6 border border-[var(--border)]">
            <h2 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
              API Schema Explorer
            </h2>

            <div className="space-y-3">
              {[
                {
                  endpoint: "/api/profiles",
                  methods: ["GET", "POST"],
                  description: "User profile management",
                },
                {
                  endpoint: "/api/projects",
                  methods: ["GET", "POST", "PUT", "DELETE"],
                  description: "Project portfolio",
                },
                {
                  endpoint: "/api/skills",
                  methods: ["GET", "POST"],
                  description: "Skills and proficiency",
                },
                {
                  endpoint: "/api/experiences",
                  methods: ["GET", "POST", "PUT"],
                  description: "Work experience",
                },
              ].map((api, i) => (
                <div key={i} className="p-3 bg-[var(--muted)] rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <code className="text-sm font-mono text-[var(--primary)]">
                      {api.endpoint}
                    </code>
                    <div className="flex gap-1">
                      {api.methods.map((method) => (
                        <span
                          key={method}
                          className={`text-xs px-2 py-0.5 rounded font-medium ${
                            method === "GET"
                              ? "bg-green-100 text-green-700"
                              : method === "POST"
                              ? "bg-blue-100 text-blue-700"
                              : method === "PUT"
                              ? "bg-orange-100 text-orange-700"
                              : "bg-red-100 text-red-700"
                          }`}
                        >
                          {method}
                        </span>
                      ))}
                    </div>
                  </div>
                  <p className="text-xs text-[var(--muted-foreground)]">
                    {api.description}
                  </p>
                </div>
              ))}
            </div>
          </section>
        </div>

        {/* Real-time Activity Feed */}
        <section className="mt-8 bg-[var(--card)] rounded-xl p-6 border border-[var(--border)]">
          <h2 className="text-lg font-semibold mb-4 text-[var(--foreground)]">
            Real-time Activity Feed
          </h2>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {endpoints
              .filter((e) => e.timestamp)
              .reverse()
              .map((endpoint, i) => (
                <div
                  key={i}
                  className="flex items-center gap-3 text-sm p-2 hover:bg-[var(--muted)] rounded"
                >
                  <StatusIndicator status={endpoint.status} />
                  <span className="text-xs font-mono text-[var(--muted-foreground)]">
                    {endpoint.timestamp
                      ? new Date(endpoint.timestamp).toLocaleTimeString()
                      : ""}
                  </span>
                  <span className="text-xs bg-[var(--secondary)] px-2 py-0.5 rounded">
                    {endpoint.method}
                  </span>
                  <span>{endpoint.endpoint}</span>
                  {endpoint.latency && (
                    <span className="text-xs text-green-600 ml-auto">
                      {endpoint.latency}ms
                    </span>
                  )}
                </div>
              ))}
          </div>
        </section>
      </div>
    </main>
  );
}
