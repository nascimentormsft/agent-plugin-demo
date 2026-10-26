# Customer demo: create privately, install across projects

Goal: show how a customer creates instructions and skills in a private GitHub or
Azure Repos repository, packages them as a plugin, and installs that plugin in
separate project repositories. Allow 15-20 minutes after preparation.

## 1. Prepare

- Create a private marketplace from this template using
  [private marketplace setup](PRIVATE-REPO-SETUP.md). Choose GitHub or Azure Repos
  for the live demo; show the alternative host's configuration in the guide.
- Give the demo developer Read access and verify `git ls-remote <private-url>`.
- Have a separate ASP.NET Core application with an endpoint you can safely modify.
  It need not live beside the marketplace or use the same Git host.
- Run `python .\scripts\validate.py` from this repository.
- Build the application and run its existing tests before the demo.
- Open only the application folder in the VS Code window used for the demo.
- Remove or disable any local `chat.pluginLocations` copy for this demo.
  Install from the private repository during the presentation, not a local path.
- Prepare a published revision for the project recommendation and an optional
  second project for showing reuse.

The plugin's default instruction scope is `src/**/*.cs`. Choose a matching
application file, or use `setup-project-instructions` to adapt the scope first.
Install the .NET SDK required by your application.

## 2. Create and explain the plugin (4 minutes)

Show these files in a separate editor window:

- [Marketplace catalog](../../.github/plugin/marketplace.json): lists the plugin.
- [Plugin manifest](../../plugins/team-standards/plugin.json): identifies the plugin.
- [Logging rule](../../plugins/team-standards/com.github.copilot/rules/structured-logging.instructions.md):
  defines the C# scope and logging conventions.
- [Logging skill](../../plugins/team-standards/skills/add-structured-logging/SKILL.md):
  packages the workflow and C# templates.
- [Instruction setup skill](../../plugins/team-standards/skills/setup-project-instructions/SKILL.md):
  explicitly creates a project-local instruction when needed.

Point out that the application is not part of this repository.

Make one small, visible edit to a skill's instructions, explaining its name,
description, and template assets. Run validation, review the change, and publish
it through the private repository. Show that both catalogs point at the same
plugin directory. See the guide's authoring section for adding another plugin.

## 3. Install from the private repository (3 minutes)

In the separate application repository:

1. Add `.github/copilot/settings.json` using the GitHub or Azure Repos
   recommendation from [the setup guide](PRIVATE-REPO-SETUP.md#3-recommend-the-plugin-in-any-project).
   Use the published revision from preparation or the newly published commit.
2. Send a chat message, show the recommendation, or search
   `@agentPlugins @recommended`.
3. Install **team-standards** from **team-copilot-kit**, reviewing the trust prompt.
4. Show **Chat: Configure Skills** and confirm both skills are available.

Explain that each developer authenticates with their own account and needs Read
access. No token is committed, and no skill folders are copied to the application.
Alternatively, show user marketplace settings for installation without a
project recommendation.

## 4. Use instructions and skills (5 minutes)

Select an endpoint in the application and ask in agent mode:

> Use the add-structured-logging skill to add structured logging to this endpoint.

Review the changes against the rule and skill:

- `ILogger<T>` and named message templates, not interpolated or console logging.
- Standard `Received`, `Completed`, and `Failed` event IDs where appropriate.
- Correlation-ID middleware registered in the application.
- No request-body, credential, or personal-data logging.
- Exception logging preserves the original exception when rethrowing.

Inspect the agent's references/debug logs to confirm which customizations loaded.
Run the application's build and existing tests, then exercise the endpoint using
that project's normal workflow. Verify the actual logs; do not assume JSON output
unless the application has a JSON console formatter configured.

To explicitly demonstrate bringing a scoped instruction into the project, ask:

> Use setup-project-instructions to set up the team logging instruction here.

Show the generated project-local instruction and its `applyTo` scope. Explain
that this is an explicit copy, not an automatically synchronized plugin asset.
If you later change the plugin rule, review and update this copy separately.
Do not promise automatic plugin-rule support in every client. Confirm which
instruction loaded using references/debug logs and show the project-local
instruction as the portable fallback.

## 5. Reuse, govern, and update (3 minutes)

- The plugin repository owns the reusable workflows, templates, and catalog.
- The application repository owns its code, tests, and any explicitly generated
  project instructions.
- Open the second project, enable the installed plugin there if needed, and show
  the same skills. Team members can use a project recommendation to discover it.
- Show a reviewed plugin change and a version bump. Publish a release, move the
  consuming project's revision pin deliberately, then update through the same
  interface used initially. Follow [the release steps](PRIVATE-REPO-SETUP.md#5-release-and-update).
- Optional: demonstrate that an account without Read access cannot fetch or
  install from the private source. Use a clean profile with no cached installation;
  revoking access does not erase previously downloaded plugin content.

Close with the distinction: this template is public demo material, but the
customer's actual standards and release history live in their private repository.
