# Scoped Copilot instructions: custom logging example

Use a repository-level instruction to apply your logging standard to an ASP.NET Core API, without affecting unrelated projects.

## Instructions or skills?

| Use an instruction for... | Use a skill for... |
|---|---|
| Rules that should guide relevant work: "Use structured logging." | A repeatable task: "Add structured logging to this service." |
| Conventions scoped by file patterns and task relevance. | A procedure loaded on demand or invoked by its slash command. |
| What the result must follow. | How to produce and verify that result, optionally using bundled templates or scripts. |

Use both together: the instruction defines the logging standard; the skill applies it step by step. A template inside a skill is a starting file, not a rule or an automatically installed component. See the [skills guide and reusable template](SKILLS-EXAMPLE.md).

## Quick setup

1. Save the example below as `.github/instructions/custom-logging.instructions.md` in the application repository, not in your personal instructions.
2. Adjust `src/Api/` to match the application folder. Keep `applyTo` narrow; avoid `**`.
3. Confirm the logging contract and adapt the event names and correlation ID handling to your application.

`applyTo` attaches instructions for matching files; `description` supports discovery for relevant tasks. The scope guard reinforces the intended boundary, but instructions are guidance, not an enforcement mechanism.

## Copy-ready example

````markdown
---
name: 'API - custom logging'
description: 'Use when changing logging, tracing or error handling in the ASP.NET Core API under src/Api/.'
applyTo: 'src/Api/**/*.cs'
---

# Custom logging for the API

**Scope:** Apply only to application code under `src/Api/`.
Ignore these rules for unrelated work.

## Why
Use structured logs so support teams can trace requests and business events
consistently across services.

## Rules
1. Use injected `ILogger<T>`, not `Console.WriteLine`, `Trace` or a separate sink.
2. Use message templates with named fields, not string interpolation.
3. Log `Received` (1000), `Completed` (1001) and `Failed` (1002) using the shared
   `LogEvents` constants for the appropriate outcome.
4. Use the existing correlation ID middleware and logging scope. Do not create
   a second correlation mechanism.
5. On error, include the exception in the `Failed` event and preserve the
   existing error handling. When rethrowing, use `throw;`, not `throw ex;`.
6. Never log full payloads, personal data, credentials or keys. Use only approved
   identifiers and status values.

## Example
Assumes the shared `LogEvents` constants and injected logger are available:

```csharp
logger.LogInformation(LogEvents.Received, "Order {OrderId} received", orderId);
```

## Done when
- Changed operations log receipt and the appropriate success or failure outcome.
- Logs use message templates and the existing correlation scope.
- No sensitive payload logging or separate logging sinks are introduced.
- Report any rules that could not be applied and why.
````

## Reusable template

Save as `.github/instructions/<topic>.instructions.md`. Replace every bracketed placeholder; keep one topic per file.

````markdown
---
name: '[Project or component] - [topic]'
description: 'Use when [specific tasks] in [project or technology].'
applyTo: 'src/[component]/**/*.[extension]'
---

# [Topic] for [project or component]

**Scope:** Apply only to [included code or folder].
Ignore these rules for [excluded tasks or files].

## Why
[Explain the problem this prevents or the outcome it enables in 1-2 sentences.]

## Rules
1. [State one specific, testable action. Name the required API or convention.]
2. [Identify the existing helper or pattern to reuse, with its relative path.]
3. Never [prohibited behavior]. Instead, [approved alternative].

## Example
[Add a short, realistic code snippet showing the preferred approach.
Name any dependencies it assumes; optionally show what to avoid and why.]

## Done when
- [Observable result or check that proves the rules were followed.]
- [Relevant test, lint or build command passes, if applicable.]
- Report any rule that could not be applied and why.
````

**Fields at a glance:** `name` is a readable label; `description` says **when** to use the instruction; `applyTo` says **which files** it targets. Replace the example glob with your actual folder and file type, such as `src/Web/**/*.tsx`. Use comma-separated globs for multiple patterns.

## Check before sharing

- **Discovery:** Open **Chat: Open Customizations** and confirm the instruction is listed.
- **Positive test:** Add logging to an API operation. Check the chat's references and verify the result against **Done when**.
- **Negative test:** Try an unrelated task and a separate repository. Confirm the API logging rules are not applied.
- **Troubleshooting:** Check **Developer: Open Agent Debug Logs** and the actual application paths. If the instruction is not loaded, attach it to the request explicitly.

Keep one topic per instruction file. Use a **skill** instead for a reusable procedure with templates or scripts. Resolve conflicting instructions rather than relying on load order.

## References

- [VS Code custom instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
