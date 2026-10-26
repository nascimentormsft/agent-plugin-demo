# team-copilot-kit – a private home for your team's GitHub Copilot setup

A **template** showing how an organization can keep **everything GitHub Copilot related for its
projects in one private repository** – instructions, skills and (optionally) agents, hooks and MCP
servers – and **install it into any project repository** as an agent plugin.

> The example content targets **ASP.NET Core Web APIs (C#, .NET 8)**.
>
> This public repository is only the template. It is designed to be copied into a **private**
> repository in **Azure DevOps (Azure Repos)** or a **private GitHub** organization. All content is
> generic example content; replace it with your own standards.

## How it works

```text
Private repo (Azure Repos / GitHub)           Any project repository
┌───────────────────────────────┐            ┌──────────────────────────────┐
│ team-copilot-kit (marketplace)│  install   │ .github/copilot/settings.json│
│  └─ plugins/team-standards    │ ─────────► │  recommends team-standards   │
│      ├─ instructions (rules)  │  (git +    │ Copilot loads the plugin's   │
│      └─ skills                │  your own  │ instructions and skills      │
└───────────────────────────────┘  sign-in)  └──────────────────────────────┘
```

- The private repository is a **plugin marketplace**: a catalog (`marketplace.json`) that lists
  one or more plugins stored in `plugins/`.
- Developers register the marketplace once (or the project recommends it) and install plugins by
  name. Access is controlled by **who can read the repository** – nothing else to manage.
- Copilot clones the repository with **Git and the developer's own credentials** (for Azure DevOps:
  Git Credential Manager with Microsoft Entra ID, or SSH). No secrets are stored in this repository
  or in project settings.

## Repository layout

```text
team-copilot-kit/
├── .github/plugin/marketplace.json        # Marketplace catalog (GitHub Copilot CLI)
├── .claude-plugin/marketplace.json        # Same catalog, location read by other clients
├── plugins/
│   └── team-standards/                    # One plugin (add more folders for more plugins)
│       ├── plugin.json                    # Plugin manifest (Agent Plugins 1.0)
│       ├── skills/                        # Portable: agent skills
│       │   ├── add-structured-logging/
│       │   └── setup-project-instructions/
│       └── com.github.copilot/rules/      # Copilot-specific: the example instruction
│           └── structured-logging.instructions.md
├── examples/
│   ├── consumer-repo/.github/copilot/settings.json      # Project → private Azure Repos marketplace
│   ├── consumer-repo/.github/copilot/settings.github-private.json  # Same, private GitHub
│   ├── vscode-user-settings.json          # Per-developer VS Code settings
│   └── demo-api/                          # Small ASP.NET Core Web API (.NET 8) to try the plugin on
├── scripts/validate.py                    # Run before every release
└── docs/
    ├── PRIVATE-REPO-SETUP.md              # Azure DevOps and private GitHub setup (start here)
    └── DEMO.md                            # 15-minute demo script
```

## Quick start (Azure DevOps)

1. Create a repository in Azure Repos, push this template, tag the first release: `git tag v0.1.0`.
2. Give developers **Read** access to the repository.
3. Each developer checks they can reach it: `git ls-remote https://dev.azure.com/<organization>/<project>/_git/<repository>`
4. In each project, commit `examples/consumer-repo/.github/copilot/settings.json` as
   `.github/copilot/settings.json` (with your URL). Team members get the plugin as a recommendation.

Full steps, authentication options, version pinning and troubleshooting:
**[docs/PRIVATE-REPO-SETUP.md](docs/PRIVATE-REPO-SETUP.md)**.

## Success criteria
1. A developer with read access installs `team-standards` into a project that contains **no**
   Copilot files.
2. The skills appear in **Chat: Configure Skills** (VS Code) or the skills list (Copilot CLI).
3. Asking Copilot to "add logging to the Create endpoint" in
   `examples/demo-api/src/DemoApi/Controllers/OrdersController.cs` produces code that follows the
   instruction (`ILogger<T>`, message templates, `LogEvents`, correlation ID middleware, no body logging).
4. A change pushed to the private repository (new version tag) reaches every project through
   **Extensions: Check for Extension Updates** (VS Code) or `copilot plugin update` (CLI).
5. A person **without** access to the private repository cannot install it.

## Before every release
```bash
python scripts/validate.py
```
(Python 3 is only needed by maintainers for this check, not by developers who install the plugin.)

## References
- VS Code – Agent plugins (marketplaces, private repositories, workspace recommendations): https://code.visualstudio.com/docs/agent-customization/agent-plugins
- VS Code – Agent plugin reference: https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference
- GitHub Docs – Copilot CLI plugin reference (marketplace.json, install commands): https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference
- GitHub Docs – Adding repository custom instructions in your IDE: https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide
- GitHub Docs – About agent skills: https://docs.github.com/en/copilot/concepts/customizations/agent-skills
- Agent Plugins open standard: https://agent-plugins.org/
- Azure Repos – Git Credential Manager: https://learn.microsoft.com/azure/devops/repos/git/set-up-credential-managers
- Azure Repos – SSH keys: https://learn.microsoft.com/azure/devops/repos/git/use-ssh-keys-to-authenticate

## License
MIT
