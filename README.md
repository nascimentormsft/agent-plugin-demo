# Private agent plugin marketplace demo

A customer demo and template for keeping team instructions and skills in a
**private GitHub or Azure DevOps repository**, packaging them as agent plugins,
and installing them in separate project repositories.

The customer owns the private repository and controls access through its existing
repository permissions. No public marketplace publication is required.

```text
Private GitHub / Azure Repos           Any consuming project
marketplace + plugins                 install plugin
  instructions + skills  ---------->  use team workflows in Copilot
```

This repository contains the plugin, not the application it modifies.

The example plugin, **team-standards**, teaches structured logging for ASP.NET Core
Web APIs. Its C# templates are plugin assets, not a standalone application.

## Repository layout

```text
agent-plugin-demo/
|-- .github/plugin/marketplace.json     # Copilot marketplace catalog
|-- .claude-plugin/marketplace.json     # Compatible catalog for other clients
|-- plugins/team-standards/
|   |-- plugin.json
|   |-- com.github.copilot/rules/
|   |   `-- structured-logging.instructions.md
|   `-- skills/
|       |-- add-structured-logging/     # Workflow and C# templates
|       `-- setup-project-instructions/ # Workflow and instruction template
|-- scripts/validate.py                # Maintainer checks; Python standard library
`-- docs/
    |-- DEMO.md
    `-- PRIVATE-REPO-SETUP.md
```

There is intentionally no sample application, consumer configuration folder,
application build, or dependency installation step here.

## Customer quick start

1. Create an **empty private repository** in GitHub or Azure Repos and push a copy
   of this template there. Do not change this public template's visibility.
2. Adapt the plugin's rules and skills to the customer's standards, validate them,
   and publish the changes.
3. Give consuming developers **Read** access and verify Git authentication.
4. Register the private marketplace, install **team-standards**, and open any
   project where you want to use it.
5. For team onboarding, commit a plugin recommendation in each consuming project.
   This recommends installation; it does not silently install or grant access.

In VS Code **user Settings (JSON)**, register the customer's private marketplace.
For private GitHub:

```json
{
  "chat.plugins.enabled": true,
  "chat.plugins.marketplaces": [
    "https://github.com/<owner>/<repository>.git"
  ]
}
```

For **Azure DevOps**, replace the marketplace entry with:

```text
https://dev.azure.com/<organization>/<project>/_git/<repository>
```

Open Extensions, search `@agentPlugins`, and install **team-standards** from
**team-copilot-kit**. Review the trust prompt. In the separate project, confirm
both skills appear in **Chat: Configure Skills**.

The plugin is installed for the developer and can be enabled or disabled globally
or per workspace. Projects do not need to copy the plugin or clone its source
alongside their application.

Full steps for **creating the private repo, authoring a plugin, authentication,
project recommendations, and updates**:
[private marketplace setup](docs/PRIVATE-REPO-SETUP.md).
For the customer presentation, follow [the demo guide](docs/DEMO.md).

## What the plugin brings to a project

| Component | Purpose |
|---|---|
| Scoped logging instruction | Team standards for matching C# files; client support for plugin rules can vary. |
| `add-structured-logging` skill | Reusable workflow with C# templates; invoke it on an ASP.NET Core endpoint. |
| `setup-project-instructions` skill | Explicitly creates a project-local instruction when needed and adapts its scope. |

The marketplace mechanism works across projects; these particular logging assets
target **ASP.NET Core**, not every language. Customers can replace or extend them
with their own stack-specific instructions and skills.

The logging rule defaults to `src/**/*.cs`. For other layouts or clients without
plugin-rule support, run `setup-project-instructions` and inspect its output.
That generated instruction belongs to the consuming project and does **not**
automatically change when the plugin is updated.

## Optional: local authoring preview

Before publishing, open a separate test application and register the local plugin
directory in that workspace's Settings (JSON):

```json
{
  "chat.plugins.enabled": true,
  "chat.pluginLocations": {
    "C:\\path\\to\\agent-plugin-demo\\plugins\\team-standards": true
  }
}
```

Use the plugin directory, not the marketplace root. Keep machine-specific paths
out of shared configuration and disable the local copy before demonstrating
private marketplace installation. Local loading does not demonstrate private
repository authentication or distribution.

## Maintain the plugin

From this repository's root:

```powershell
python .\scripts\validate.py
```

Python 3 is needed only for this maintainer check. Consumers need the tools used
by their application; the logging skill uses `dotnet build`.

Keep both marketplace catalogs identical. When releasing, update the plugin
version in its manifest and both catalog entries, validate, and publish a tag.
The validator checks JSON, catalog consistency, plugin metadata, customization
frontmatter, and common credential patterns; it does not test agent behavior.

## References

- [VS Code agent plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins)
- [VS Code plugin reference](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference)
- [Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
- [Agent Plugins standard](https://agent-plugins.org/)

## License

[MIT](LICENSE)
