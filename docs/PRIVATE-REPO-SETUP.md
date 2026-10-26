# Share the plugin as a private marketplace

Use this guide to create a customer-owned private repository, author a plugin,
and install it in separate projects. GitHub and Azure Repos are alternative hosts;
you do not need both.

## 1. Publish and grant access

Create an empty **private** repository in GitHub, or an Azure Repos repository in
a private Azure DevOps project. Copy this template's contents, including hidden
catalog directories, into a new local folder. From that folder:

```powershell
git init -b main
git add .
git commit -m "Create private agent plugin marketplace"
git remote add origin <private-remote-url>
git push -u origin main
```

Replace `<private-remote-url>` with one of the URLs below before running the
commands. This creates a separate customer repository without changing this
template's origin or visibility. Review the staged content before committing.

Developers need **Read** access; maintainers need permission to contribute.
Protect the default branch with pull requests. In Azure DevOps, explicitly grant
Read access to developers in other projects who need the plugin.

Use an authenticated Git remote, never credentials embedded in a URL or settings:

| Host | HTTPS remote |
|---|---|
| GitHub | `https://github.com/<owner>/<repository>.git` |
| Azure Repos | `https://dev.azure.com/<organization>/<project>/_git/<repository>` |

For GitHub, authenticate with `gh auth login` and configure Git with
`gh auth setup-git`. For Azure Repos, use Git Credential Manager or an SSH key
registered with Azure DevOps.

Before installation, run `git ls-remote <remote-url>` with the same remote you
will configure. Fix authentication or repository permissions if this fails.

### Author the customer's plugin

Start with `team-standards`, then replace its example content with team standards:

1. Edit the [logging rule](../plugins/team-standards/com.github.copilot/rules/structured-logging.instructions.md).
   Keep a meaningful description and an `applyTo` glob that matches consumer
   files. This plugin rule location is Copilot-specific.
2. Edit the [logging skill](../plugins/team-standards/skills/add-structured-logging/SKILL.md)
   and its templates, or add `skills/<skill-name>/SKILL.md`. Each skill needs
   frontmatter with a matching kebab-case `name` and a description explaining
   when to use it.
3. Keep the [instruction setup template](../plugins/team-standards/skills/setup-project-instructions/templates/structured-logging.instructions.md)
   aligned with the plugin rule when changing logging standards. It supports an
   explicit project-local instruction copy for clients that need one.
4. Set the customer/team owner and marketplace description in both catalogs.
   To rename the plugin, update its directory, manifest name, catalog names and
   source paths, and the installation examples together.
5. Run `python .\scripts\validate.py` from the repository root. Test the plugin in
   a separate application, review the output, and push the changes.

For another plugin, add a directory under `plugins/` with its own `plugin.json`
and skills, then add a matching relative source entry to **both** catalogs.
Use [the existing manifest](../plugins/team-standards/plugin.json) and
[catalog](../.github/plugin/marketplace.json) as the working examples.
The application stays outside the marketplace repository.

## 2. Install in VS Code

In each developer's VS Code user Settings (JSON), enable plugins and register the
marketplace. For GitHub:

```json
{
  "chat.plugins.enabled": true,
  "chat.plugins.marketplaces": [
    "https://github.com/<owner>/<repository>.git"
  ]
}
```

For Azure Repos, replace the entry with:

```text
https://dev.azure.com/<organization>/<project>/_git/<repository>
```

Then:

1. Open the separate application repository.
2. In Extensions, search `@agentPlugins`.
3. Install **team-standards** from **team-copilot-kit** and review the trust prompt.
4. Confirm the skills appear in **Chat: Configure Skills**.

Do not also register the same plugin with `chat.pluginLocations`.
For a reproducible VS Code installation, append `#<full-40-character-commit-sha>`
to the marketplace URL. A branch or tag can also select a revision, but is not
immutable.

## 3. Recommend the plugin in any project

For repeatable team onboarding, commit `.github/copilot/settings.json` in each
consuming project. This small configuration references the private marketplace;
it does not copy its instructions or skills.

For **private GitHub**:

```json
{
  "extraKnownMarketplaces": {
    "team-copilot-kit": {
      "source": {
        "source": "github",
        "repo": "<owner>/<repository>",
        "ref": "<release-tag-or-full-commit-sha>"
      }
    }
  },
  "enabledPlugins": {
    "team-standards@team-copilot-kit": true
  }
}
```

For **Azure Repos**, use this configuration instead:

```json
{
  "extraKnownMarketplaces": {
    "team-copilot-kit": {
      "source": {
        "source": "git",
        "url": "https://dev.azure.com/<organization>/<project>/_git/<repository>",
        "ref": "<release-tag-or-full-commit-sha>"
      }
    }
  },
  "enabledPlugins": {
    "team-standards@team-copilot-kit": true
  }
}
```

Replace the placeholders with the actual private repository and a published
revision. The marketplace key must match the catalog's `name`; the qualified
plugin identity must match the plugin and marketplace names.

After a developer sends the first chat message in VS Code, the project can show a
plugin recommendation. They can also search `@agentPlugins @recommended` and
install it after reviewing the source. Each developer still needs their own Git
authentication and repository Read permission. This is **not** silent installation,
an access grant, or a way to enforce standards.

User marketplace settings from step 2 are an alternative to project
recommendations, not an extra file every project must contain.

## 4. Install with Copilot CLI

Use the remote URL for your host:

```text
copilot plugin marketplace add <remote-url>
copilot plugin install team-standards@team-copilot-kit
copilot plugin list
```

Run Copilot in the application repository to use the installed plugin. Manage
the plugin through the interface used to install it; VS Code's `/plugin` commands
and its customization UI can maintain separate inventories.

## 5. Release and update

1. Change the plugin through a pull request.
2. Update its version in [the manifest](../plugins/team-standards/plugin.json)
   and the matching entry in both catalogs:
   [Copilot catalog](../.github/plugin/marketplace.json) and
   [compatible catalog](../.claude-plugin/marketplace.json).
   Keep the catalogs identical and update their marketplace metadata version
   when publishing a new marketplace release.
3. Run `python .\scripts\validate.py` from the repository root.
4. Merge, then tag the release and push the tag, for example:

   ```powershell
   git tag v0.2.0
   git push origin v0.2.0
   ```

5. If the marketplace URL pins a revision, update that pin deliberately.
   For project recommendations, update `source.ref` in the consuming project's
   settings. Use a full commit SHA when immutability is required.
   In VS Code, use **Extensions: Check for Extension Updates**. For a CLI install,
   use `copilot plugin update team-standards@team-copilot-kit`.

Review any instructions previously copied into application repositories by
`setup-project-instructions` separately: plugin updates do not update those files.
New releases are not forced into every project; consumers update according to
their configured revisions and client update settings.

## Troubleshooting

| Symptom | Check |
|---|---|
| Cannot fetch marketplace | Test the exact URL with `git ls-remote`; check sign-in and Read permission. |
| Plugin missing | Enable `chat.plugins.enabled`; check the configured marketplace and installed/enabled state. |
| Duplicate skills | Use either local loading or marketplace installation, not both. |
| Logging rule not applied | Check `src/**/*.cs` against the application layout and inspect agent debug logs. Client support for `com.github.copilot/rules` can vary; use `setup-project-instructions` if needed. |
| Old rules still used | Check revision pins, update through the original installation interface, and inspect project-local instruction copies. |

See the [official VS Code plugin documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins)
for current settings and client support.
