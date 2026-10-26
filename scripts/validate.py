#!/usr/bin/env python3
"""Validate the marketplace and its plugins before a release (standard library only)."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?$")
SECRET_PATTERNS = {
    "e-mail address": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "credential value": re.compile(r"(?i)(api[_-]?key|secret|password|token|pat)\s*[:=]\s*['\"][^'\"<>]{8,}"),
    "connection string": re.compile(r"(?i)(AccountKey|SharedAccessKey|Password)=[^;<>\s]+"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "credentials in URL": re.compile(r"https://[^/\s:@<>]+:[^/\s@<>]+@"),
    "real Azure DevOps organization": re.compile(r"dev\.azure\.com/(?!<)[A-Za-z0-9-]+"),
}
ALLOWED_EMAIL_LIKE = ("git@ssh.dev.azure.com",)
errors = []


def error(msg):
    errors.append(msg)
    print(f"ERROR  {msg}")


def ok(msg):
    print(f"ok     {msg}")


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        error(f"{path.relative_to(ROOT)}: {exc}")
        return None


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("'\"")
    return fields


# 1. Every JSON file parses
for path in ROOT.rglob("*.json"):
    load_json(path)

# 2. Marketplace catalogs
catalogs = [ROOT / ".github/plugin/marketplace.json", ROOT / ".claude-plugin/marketplace.json"]
data = [load_json(p) for p in catalogs if p.exists()]
if not data or data[0] is None:
    error("no marketplace.json found")
    sys.exit(1)
if len(data) == 2 and data[0] != data[1]:
    error("the two marketplace.json files differ – keep them identical")
market = data[0]
ok(f"marketplace '{market.get('name')}' with {len(market.get('plugins', []))} plugin(s)")

# 3. Each plugin
for entry in market.get("plugins", []):
    src = entry.get("source")
    if not isinstance(src, str) or not src.startswith("./") or ".." in src:
        error(f"plugin '{entry.get('name')}': source must be a relative path starting with ./")
        continue
    pdir = ROOT / src[2:]
    manifest = load_json(pdir / "plugin.json") if (pdir / "plugin.json").exists() else None
    if manifest is None:
        error(f"plugin '{entry.get('name')}': {src}/plugin.json missing or invalid")
        continue
    name = manifest.get("name", "")
    if manifest.get("$schema") != SCHEMA:
        error(f"{src}/plugin.json: $schema must be the Agent Plugins 1.0 schema URL")
    if not NAME_RE.match(name) or "--" in name:
        error(f"{src}/plugin.json: invalid name '{name}'")
    if name != entry.get("name"):
        error(f"plugin entry '{entry.get('name')}' differs from manifest name '{name}'")
    if manifest.get("version") != entry.get("version"):
        error(f"plugin '{name}': version {manifest.get('version')} in plugin.json, {entry.get('version')} in marketplace.json")
    ok(f"plugin '{name}' {manifest.get('version')}")
    for skill in sorted(p for p in (pdir / "skills").iterdir() if p.is_dir()):
        fm = frontmatter(skill / "SKILL.md") if (skill / "SKILL.md").exists() else {}
        if fm.get("name") != skill.name or not fm.get("description"):
            error(f"{src}/skills/{skill.name}: SKILL.md needs name '{skill.name}' and a description")
        else:
            ok(f"  skill '{skill.name}'")
    for rule in sorted(pdir.rglob("*.instructions.md")):
        fm = frontmatter(rule)
        rel = rule.relative_to(pdir)
        if not fm.get("description"):
            error(f"{src}/{rel}: missing description")
        else:
            ok(f"  instruction {rel} (applyTo: {fm.get('applyTo', 'manual only')})")

# 4. No secrets, personal data or real organization names
for path in ROOT.rglob("*"):
    if not path.is_file() or path.name == "validate.py" or ".git" in path.parts:
        continue
    if path.suffix not in {".md", ".json", ".py", ".ts", ".cs", ".txt", ".yml", ".yaml"}:
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for label, pattern in SECRET_PATTERNS.items():
        for match in pattern.finditer(text):
            if any(match.group(0) in allowed for allowed in ALLOWED_EMAIL_LIKE):
                continue
            error(f"{path.relative_to(ROOT)}: possible {label}: '{match.group(0)[:50]}'")

print()
if errors:
    print(f"FAILED – {len(errors)} problem(s)")
    sys.exit(1)
print("PASSED – ready to release")
