chatStore.ts
    ↓
single source of truth

ChatWorkspace.tsx
    ↓
renders messages

ChatMessage.tsx
    ↓
renders:
- markdown
- streaming
- human review controls


// User: "delete registry.py"
// Assistant:
// [empty message placeholder]
// human_review_required arrives
// Assistant:
// ⚠ Human approval required
// [Approve] [Reject]