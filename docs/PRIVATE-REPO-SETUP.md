# Set up the plugin repository as a private marketplace

This guide uses **Azure DevOps (Azure Repos)** as the main example and lists the differences for a
**private GitHub** repository at the end. Replace every `<placeholder>`.

| Placeholder | Example meaning |
|---|---|
| `<organization>` | Azure DevOps organization |
| `<project>` | Azure DevOps project |
| `<repository>` | Name of the private repository holding this template |

HTTPS URL: `https://dev.azure.com/<organization>/<project>/_git/<repository>`
SSH URL: `git@ssh.dev.azure.com:v3/<organization>/<project>/<repository>`

---

## 1. Create the private repository (maintainers, once)

1. In Azure DevOps: **Repos → New repository** in the project that owns your engineering standards.
2. Push this template:
   ```bash
   git remote add origin https://dev.azure.com/<organization>/<project>/_git/<repository>
   git push -u origin main
   ```
3. Run `python scripts/validate.py` and tag the first release:
   ```bash
   git tag v0.1.0 && git push origin v0.1.0
   ```
4. Protect `main`: **Project settings → Repositories → Policies** – require a pull request and at
   least one reviewer. Every change to instructions and skills is then reviewed like code.

## 2. Control who can use it

Access to the plugin = **Read** access to the repository.

| Role | Azure DevOps permission |
|---|---|
| Developers who install the plugin | **Read** on the repository (e.g. the project's *Readers* group, or a dedicated group) |
| Maintainers of the standards | **Contribute** + **Contribute to pull requests** |

Developers in other projects need Read access to this repository too (add their group under
**Repository settings → Security**).

## 3. Authentication on developer machines

Copilot (VS Code and CLI) clones the marketplace with **Git**, so it uses whatever Git
authentication already works on the machine. Nothing is stored in this repository.

Pick one:

| Option | When | Setup |
|---|---|---|
| **Git Credential Manager (recommended)** | Windows / macOS with Microsoft Entra ID sign-in | Included with Git for Windows. The first `git` command against `dev.azure.com` opens a browser sign-in. To use Microsoft Entra ID tokens: `git config --global credential.azreposCredentialType oauth` |
| **SSH key** | Linux, or where browser sign-in is not possible | Add the public key in **User settings → SSH public keys**; use the SSH URL. |
| **Personal access token (PAT)** | Last resort (build agents, containers) | Scope **Code (Read)** only, short expiry. Store it in the Git credential store – **never** in `settings.json` or in this repository. |

**Test before installing:**
```bash
git ls-remote https://dev.azure.com/<organization>/<project>/_git/<repository>
```
If this prints references (for example `refs/heads/main`), Copilot can reach the repository too.

## 4. Install the plugin

### Option A – Project recommendation (recommended)
Commit this file to each project as `.github/copilot/settings.json`
(template: `examples/consumer-repo/.github/copilot/settings.json`):

```json
{
  "extraKnownMarketplaces": {
    "team-copilot-kit": {
      "source": {
        "source": "git",
        "url": "https://dev.azure.com/<organization>/<project>/_git/<repository>",
        "ref": "v0.1.0"
      }
    }
  },
  "enabledPlugins": {
    "team-standards@team-copilot-kit": true
  }
}
```
- **VS Code:** after the first chat message, a notification shows the recommended plugin; it is also
  listed under **Extensions → `@agentPlugins @recommended`**.
- **Copilot CLI:** reads the same file when it runs in the project folder.
- `ref` pins the project to a released version. Change it to roll the project forward.

### Option B – VS Code, per developer
1. Settings (JSON) – template: `examples/vscode-user-settings.json`:
   ```json
   {
     "chat.plugins.enabled": true,
     "chat.plugins.marketplaces": [
       "git@ssh.dev.azure.com:v3/<organization>/<project>/<repository>"
     ]
   }
   ```
   VS Code accepts an SSH-style remote, an HTTPS remote, or a `file:///` path to a local clone. If
   the public lookup fails, VS Code clones the repository directly with your Git credentials.
2. **Extensions** view → search `@agentPlugins` → install **team-standards**.
3. Check **Chat: Open Customizations → Plugins**.

### Option C – GitHub Copilot CLI
```bash
copilot plugin marketplace add https://dev.azure.com/<organization>/<project>/_git/<repository>
copilot plugin install team-standards@team-copilot-kit
copilot plugin list
```
If HTTPS authentication fails, use the SSH URL or check step 3.

## 5. Release and update

1. Change instructions or skills in a pull request.
2. Bump `version` in `plugins/team-standards/plugin.json` **and** in both `marketplace.json` files.
3. Run `python scripts/validate.py`, merge, tag (`v0.2.0`) and push the tag.
4. Projects pinned with `ref` move when you update `ref` in their `.github/copilot/settings.json`.
   Developers update with **Extensions: Check for Extension Updates** (VS Code) or
   `copilot plugin update team-standards` (CLI).

For fully reproducible installs, pin `ref` to a full 40-character commit SHA instead of a tag.

## 6. Organization-wide control (optional)

Administrators can centrally allow or block marketplaces and plugins (for example, allow only
`dev.azure.com` sources from your organization). See *Manage agent plugins and marketplaces* in the
VS Code documentation and your device-management policies.

## 7. Private GitHub instead of Azure DevOps

| Topic | Private GitHub |
|---|---|
| Access | Repository **Read** permission (organization team) |
| Authentication | GitHub sign-in in VS Code / `gh auth login`; the CLI retries HTTPS with your signed-in GitHub token |
| Project settings | `examples/consumer-repo/.github/copilot/settings.github-private.json` (`"source": "github"`, `"repo": "<your-org>/<repository>"`) |
| CLI | `copilot plugin marketplace add <your-org>/<repository>` |

## 8. Troubleshooting

| Symptom | Check |
|---|---|
| Marketplace or plugin not found | Run the `git ls-remote` test in step 3 with the exact URL. Check Read permission. |
| Authentication prompt loops / 401 / 403 | Sign in again with Git Credential Manager, or switch to the SSH URL. Expired PAT? |
| Plugin not listed in VS Code | `chat.plugins.enabled` is `true`; the plugin `name` in `plugin.json` matches the marketplace entry. |
| Skill not listed | Folder name equals the `name` in `SKILL.md` (lowercase, hyphens). |
| Instruction not applied | `applyTo` (default `src/**/*.cs`) matches the file path in the project; run **Developer: Open Agent Debug Logs**; or use the `setup-project-instructions` skill to place it in `.github/instructions/`. |
| Old version still used | Check `ref` in the project settings; run the update command. |

> Plugin rules (`com.github.copilot/rules/`) are a Copilot-specific capability and support can vary
> between clients and versions. For instructions that must always apply, use the
> `setup-project-instructions` skill so the instruction is committed to the project itself.
