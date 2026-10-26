---
name: setup-project-instructions
description: Copies the team's Copilot instruction files from this plugin into the current repository's .github/instructions folder. Use when asked to "set up team instructions" or "apply our Copilot standards", or when the plugin's rules are not being picked up in this editor.
---

# Set up project instructions

Places the team's instruction files directly in the repository you are working on, so they are
versioned with the code and apply in every tool that reads `.github/instructions/`.

## Steps
1. Create `.github/instructions/` in the current repository if it does not exist.
2. Copy [templates/structured-logging.instructions.md](templates/structured-logging.instructions.md)
   to `.github/instructions/structured-logging.instructions.md`.
   If a file with that name already exists, show the differences and ask before overwriting.
3. Ask the user whether the `applyTo` glob matches this repository's source folder
   (default `src/**/*.cs`). Adjust it if needed.
4. Tell the user how to verify: run **Chat: Open Customizations** and check *Instructions*, or ask
   Copilot to change a `.cs` file under `src/` and check that the instruction appears under **References**.
