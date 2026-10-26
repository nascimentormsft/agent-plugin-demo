# Demo script (15–20 minutes)

Goal: show that an organization can keep its GitHub Copilot setup in **one private repository**
(Azure DevOps) and install it into any project.

## 0. Prepare (before the session)
- Create a **private** Azure Repos repository in a demo organization/project and push this template
  (see `docs/PRIVATE-REPO-SETUP.md`, steps 1–2). Tag `v0.1.0`.
- Run `python scripts/validate.py` – it must pass.
- Confirm `git ls-remote <your Azure Repos URL>` works on the demo machine.
- Create a second project repository (no `.github/` folder) and copy `examples/demo-api/` into it
  (`src/DemoApi/...` plus `requests.http`). Check it builds: `dotnet build src/DemoApi`.
- .NET 8 SDK installed; the C# Dev Kit extension is optional.
- VS Code: `chat.plugins.enabled` is `true`.
- Optional negative test: a second user/profile **without** access to the private repository.

## 1. The problem (2 min)
Every project copies instructions and skills by hand; versions drift, and there is no review or
access control over what Copilot is told to do.

## 2. Tour of the private repository (4 min)
- Azure Repos: branch policy on `main`, pull requests for every change, version tags.
- `marketplace.json` – the catalog; `plugins/team-standards/plugin.json` – one plugin.
- `com.github.copilot/rules/structured-logging.instructions.md` – a scoped instruction
  (`applyTo`, `description`, scope guard, Why, Rules, examples, Done when).
- `skills/` – one skill that uses the instruction, one that installs it into a project.

## 3. Install into the project (4 min)
- Commit `.github/copilot/settings.json` (from `examples/consumer-repo/`) with the real URL.
- Send a chat message → VS Code shows the recommended plugin → install.
  (Alternative: CLI `copilot plugin marketplace add <url>` then `copilot plugin install team-standards@team-copilot-kit`.)
- Show **Chat: Open Customizations → Plugins** and **Chat: Configure Skills**.

## 4. Use it (5 min)
1. Open `src/DemoApi/Controllers/OrdersController.cs`, agent mode:
   *"Add logging to the Create endpoint."*
   Expected: `ILogger<OrdersController>` injected; `LogEvents.cs` and `CorrelationIdMiddleware.cs`
   added and the middleware registered in `Program.cs`; `Received`/`Completed`/`Failed` logged with
   message templates; `Console.WriteLine` removed; the request body (with customer name and email)
   is no longer logged; `catch` ends with `throw;`. Expand **References** to show the instruction/skill.
   Run `dotnet run --project src/DemoApi` and send `requests.http` to show the JSON log with `CorrelationId`.
2. *"Set up the team instructions in this repository."*
   Expected: `.github/instructions/structured-logging.instructions.md` created.
3. Negative check: *"Update the README."* – the logging instruction is not referenced.

## 5. Govern and update (3 min)
- Open a pull request that changes one rule, bump the version, merge, tag `v0.2.0`.
- In the project, change `ref` to `v0.2.0` → update the plugin → show the new rule.
- Optional: show that the user without repository access cannot install the plugin.
