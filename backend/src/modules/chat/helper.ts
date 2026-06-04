export function selectWorkflowType(
  query: string,
): string {

  const normalized =
    query.toLowerCase();

  const ragKeywords = [
    ".py",
    "repository",
    "workflow",
    "architecture",
    "codebase",
    "service",
    "module",
    "explain",
    "project",
    "direction",
    "history",
    "evolution",
    "commit",
    "release",
    "technical debt",
    "microservice",
    "deployment",
  ];

  const requiresRag =
    ragKeywords.some(
      (keyword) =>
        normalized.includes(
          keyword,
        ),
    );

  return requiresRag
    ? "agentic_rag"
    : "core_chat";
}