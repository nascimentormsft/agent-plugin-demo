# Copilot skills: a quick guide and reusable template

A **skill** packages a repeatable task as a folder with a required `SKILL.md` file and optional supporting files. Copilot can load it when its description matches the task, or you can invoke it by typing `/` and choosing the skill.

## Instructions, skills, templates or scripts?

| Item | Purpose | Logging example |
|---|---|---|
| **Instruction** | Rules for relevant work, scoped by file patterns and task relevance. | "Use `ILogger<T>` and never log sensitive payloads." |
| **Skill** | An on-demand procedure with steps and checks. | "Add logging to this service and verify the build." |
| **Template inside a skill** | A starting file the procedure tells Copilot to copy or adapt. | A C# file defining shared event IDs. |
| **Script inside a skill** | Executable code the procedure tells Copilot to run for a repeatable operation. | A PowerShell script that checks logging conventions and reports violations. |

Use an **instruction** for a convention, a **skill** for a repeatable task, and **both** when the task must follow that convention. Templates are optional: they do not run, install themselves or enforce rules. See the [instructions guide and reusable template](CUSTOM-INSTRUCTIONS-EXAMPLE.md).

## Create a skill

1. Create `.github/skills/add-service-logging/` in the application repository.
2. Add the `SKILL.md` below. Its `name` must match the folder: use lowercase letters, numbers and hyphens.
3. Add the template shown below under `templates/`. This is a conventional folder name, not a special mechanism; link to each asset from the procedure.
4. Adapt paths and prerequisites, then test in a sample project.

```text
.github/skills/add-service-logging/
|-- SKILL.md                  # When to use it, steps and completion checks
`-- templates/
    `-- LogEvents.cs          # Starting code, copied only when needed
```

Other optional folders: `references/` for supporting documentation and `scripts/` for executable helpers. Include only what the task needs; keep secrets out of all assets.

## Copy-ready example: SKILL.md

```markdown
---
name: add-service-logging
description: 'Add structured logging to a C# service. Use when asked to add logging or instrument a service under src/.'
---

# Add structured logging to a service

## Prerequisites
- An ASP.NET Core project with dependency injection and logging configured.
- The user identifies the service or operation to change.
- Follow the project's logging instruction if present; report conflicting rules.

## Steps
1. Read the target service and nearby logging code. Reuse existing helpers.
2. If no shared event constants exist, adapt [LogEvents.cs](./templates/LogEvents.cs)
   into the application's Logging folder. Match its namespace; do not overwrite
   existing files or introduce duplicate constants.
3. Inject ILogger<T> using the project's existing dependency injection pattern.
4. Log Received at entry and Completed on success using named message fields.
   In the error path, log Failed with the exception and preserve existing error
   handling. If rethrowing, use throw;, not throw ex;.
5. Never log full payloads, personal data, credentials or keys.
6. Run the target project's dotnet build and relevant existing tests.
   Report failures or missing prerequisites; do not claim unrun checks passed.

## Done when
- The changed operation logs receipt and the appropriate outcome.
- Existing logging infrastructure is reused; no sensitive data is logged.
- Report changed files, validation results and any unmet requirements.
```

## Template asset: templates/LogEvents.cs

Place this file **inside the skill folder**, not in the application yet:

```csharp
using Microsoft.Extensions.Logging;

namespace SampleApi.Logging;

public static class LogEvents
{
    public static readonly EventId Received = new(1000, nameof(Received));
    public static readonly EventId Completed = new(1001, nameof(Completed));
    public static readonly EventId Failed = new(1002, nameof(Failed));
}
```

The skill tells Copilot **when and where** to use this template and what to adapt. `SampleApi` is an example namespace, not a customer name. A copied file belongs to the application; updating the skill's template does not automatically update existing copies.

## What are scripts inside a skill?

Scripts are optional executable helpers, usually stored in `scripts/`. Use them for repeatable checks, data processing or file generation that should follow the same logic each time. They can be PowerShell, Python, JavaScript or another language available in the target environment.

- **Template:** starting content to copy or adapt into the application.
- **Script:** code to execute against specified inputs; it normally stays with the skill.
- **Skill:** explains when to use either resource, in what order and how to check the result.

For example, you could add `scripts/Validate-Logging.ps1` to check for prohibited logging calls. This is an optional extension, not a script included in the example above. In `SKILL.md`, link to the script and specify:

1. **Requirements:** the runtime and tools it needs, such as PowerShell 7.
2. **Invocation:** the exact command, working directory and arguments. Resolve the script path from the skill's location and pass the application path explicitly; do not assume they share a root.
3. **Effects:** whether it only reads files or changes them. Review scripts before running them and get approval for destructive actions.
4. **Results:** what output means success, how failures are reported and which nonzero exit codes indicate failure.

Placing a script in the folder does **not** run it automatically. Copilot must invoke it through an available execution tool, subject to permissions. Prefer an existing build, test or lint command when it already covers the check; add a script only for a missing, repeatable operation.

## Reusable SKILL.md template

Save under `.github/skills/<skill-name>/SKILL.md` and replace every bracketed placeholder.

```markdown
---
name: replace-with-skill-name
description: '[What this accomplishes]. Use when [specific requests or trigger phrases].'
---

# [Task name]

## Prerequisites
- [Required tools, project type, inputs and applicable instructions.]
- [When not to use this skill; what to clarify before proceeding.]

## Steps
1. [Inspect the target and identify existing patterns to reuse.]
2. [Describe the action. Link any asset, e.g. ./templates/example.txt.
   Specify its destination, substitutions and handling of existing files.]
3. [Run the relevant validation command; report errors and blockers.
   If using a bundled script, link it and specify its runtime, exact command,
   working directory, inputs, side effects and success/failure signals.]

## Done when
- [Observable result that proves the task is complete.]
- [Checks to report, including anything not run or not satisfied.]
```

**Fields at a glance:** `name` identifies the skill and must match its folder; `description` explains what it does and when to load it. Unlike scoped instructions, skills do not use `applyTo`; put task boundaries in the description and prerequisites.

## Check before sharing

- **Discovery:** Open **Chat: Configure Skills** and confirm the skill appears.
- **Positive test:** Invoke `/add-service-logging` in a sample project. Check the changed code, template adaptation and validation results.
- **Negative test:** Request an unrelated task; the skill should not be selected automatically.
- **Safety test:** Run it again where helpers already exist; confirm it reuses them without overwriting or duplicating them.
- **Script test (if included):** Check valid and invalid inputs; verify failure exit codes, clear errors and that only intended files can change.

For shared distribution through a plugin, use the existing [logging skill](../../plugins/team-standards/skills/add-structured-logging/SKILL.md) as a working example.

## References

- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [VS Code custom instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
