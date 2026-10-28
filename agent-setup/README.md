# Agent setup (one-time)

These files belong in `.claude/`, but they couldn't be written there directly. Move them once.

**Windows (Command Prompt, in the repo folder):**

```
mkdir .claude\agents
move agent-setup\agents\*.md .claude\agents\
move agent-setup\settings.json .claude\settings.json
rmdir /s /q agent-setup
```

Or open Claude Code in the repo and say: *"Move agent-setup/agents/* to .claude/agents/ and agent-setup/settings.json to .claude/settings.json, then delete agent-setup."*

Commit the result in GitHub Desktop: `chore: add Claude agents and permissions`.

| File | Becomes | What it does |
|---|---|---|
| `agents/builder.md` | `.claude/agents/builder.md` | Implements approved backlog items on a branch, with tests |
| `agents/qa-reviewer.md` | `.claude/agents/qa-reviewer.md` | Reviews branches and PRs. Read-only, apart from running the tests. |
| `agents/docs-keeper.md` | `.claude/agents/docs-keeper.md` | Keeps the docs in step with the code |
| `settings.json` | `.claude/settings.json` | Lets agents run the tests and commit on branches. Blocks pushing to `main`, force-pushes, and reading spreadsheets. |
