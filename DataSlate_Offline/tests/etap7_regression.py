#!/usr/bin/env python3
"""Automated static/regression checks for DataSlate_Offline Stage 7.

The script intentionally uses only Python's standard library plus the local Node
binary when available. It does not install browser/test dependencies and does not
modify application files.
"""
from __future__ import annotations

import argparse
import difflib
import html.parser
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_ROOT = REPO_ROOT / "DataSlate_Offline"
ACTIVE_FILES = [
    MODULE_ROOT / "index.html",
    MODULE_ROOT / "index_backup.html",
    MODULE_ROOT / "index_test.html",
    MODULE_ROOT / "tools" / "update_embedded_data.py",
    MODULE_ROOT / "assets" / "data" / "data.json",
]
INDEX_FILES = [MODULE_ROOT / "index.html", MODULE_ROOT / "index_backup.html", MODULE_ROOT / "index_test.html"]
DATA_FILE = MODULE_ROOT / "assets" / "data" / "data.json"
TOOL_FILE = MODULE_ROOT / "tools" / "update_embedded_data.py"


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str = ""


class BasicHTMLParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[str] = []
        self.start_tags: list[tuple[str, list[tuple[str, str | None]]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.start_tags.append((tag, attrs))

    def error(self, message: str) -> None:  # pragma: no cover - legacy API hook
        self.errors.append(message)


def run_command(args: list[str], cwd: Path = REPO_ROOT, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=timeout, check=False)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fail(message: str) -> None:
    raise AssertionError(message)


def extract_embedded_json(html_text: str) -> dict:
    match = re.search(
        r'<script\s+type="application/json"\s+id="embeddedDataSlateData"\s*>\s*(.*?)\s*</script>',
        html_text,
        flags=re.DOTALL,
    )
    if not match:
        fail("embeddedDataSlateData script tag not found")
    return json.loads(match.group(1))


def extract_main_script(html_text: str) -> str:
    scripts = re.findall(r"<script(?![^>]*application/json)[^>]*>(.*?)</script>", html_text, flags=re.DOTALL)
    if not scripts:
        fail("main JavaScript <script> block not found")
    return scripts[-1]


def canonical_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def assert_relative_local_asset(path_value: str, context: str) -> None:
    if not isinstance(path_value, str) or not path_value:
        fail(f"{context}: file path is missing")
    lowered = path_value.lower()
    if re.match(r"^[a-z][a-z0-9+.-]*://", lowered) or lowered.startswith("//"):
        fail(f"{context}: external URL is not allowed: {path_value}")
    if os.path.isabs(path_value) or ".." in Path(path_value).parts:
        fail(f"{context}: path must stay relative inside DataSlate_Offline: {path_value}")


def get_content_rect_ids(index_text: str) -> set[int]:
    match = re.search(r"const\s+CONTENT_RECTS_BY_BACKGROUND_ID\s*=\s*\{(.*?)\n\s*\};", index_text, re.DOTALL)
    if not match:
        fail("CONTENT_RECTS_BY_BACKGROUND_ID not found")
    return {int(value) for value in re.findall(r"(?:^|\n)\s*(\d+)\s*:\s*\{", match.group(1))}


def check_data_and_assets(data: dict, index_text: str) -> str:
    counts = []
    for key in ["backgrounds", "logos", "audios", "fonts", "fillers"]:
        if key not in data or not isinstance(data[key], list):
            fail(f"data.json missing list: {key}")
        counts.append(f"{key}={len(data[key])}")

    for section in ["backgrounds", "logos", "audios"]:
        for item in data[section]:
            asset = item.get("file")
            assert_relative_local_asset(asset, f"{section} id={item.get('id')}")
            if not (MODULE_ROOT / asset).is_file():
                fail(f"missing asset for {section} id={item.get('id')}: {asset}")

    for font in data["fonts"]:
        for field in ["id", "name", "font"]:
            if field not in font:
                fail(f"font entry missing {field}: {font}")
        if not isinstance(font["font"], str) or not font["font"].strip():
            fail(f"font entry has invalid font value: {font}")

    for filler in data["fillers"]:
        if not isinstance(filler.get("prefixes"), list) or not isinstance(filler.get("suffixes"), list):
            fail(f"filler prefixes/suffixes must be arrays: {filler.get('id')}")

    rect_ids = get_content_rect_ids(index_text)
    bg_ids = {int(item["id"]) for item in data["backgrounds"]}
    if "const DEFAULT_CONTENT_RECT" not in index_text:
        fail("DEFAULT_CONTENT_RECT fallback not found")
    missing = sorted(bg_ids - rect_ids)
    if missing:
        return ", ".join(counts) + f"; backgrounds without explicit rect use DEFAULT_CONTENT_RECT: {missing}"
    return ", ".join(counts) + "; all backgrounds have explicit content rects"


def check_forbidden_mechanisms() -> str:
    # These are active-mechanism signatures. The generated data may still contain
    # an audios list, so plain words like "audios" and asset names are not errors.
    forbidden = [
        (r"firebase-config\.js", "firebase-config.js"),
        (r"config/firebase-config\.js", "config/firebase-config.js"),
        (r"\binitializeApp\b", "initializeApp"),
        (r"\bgetFirestore\b", "getFirestore"),
        (r"dataslate/current", "dataslate/current"),
        (r"currentRef\.set\s*\(", "currentRef.set"),
        (r"onSnapshot\s*\(", "onSnapshot"),
        (r"new\s+Audio\s*\(", "new Audio"),
        (r"\.play\s*\(", ".play()"),
        (r"\baudioEnabled\b", "audioEnabled"),
        (r"\bmessageAudioId\b", "messageAudioId"),
        (r"\bmessageAudioFile\b", "messageAudioFile"),
        (r"odblok\w*\s+audio|unlock\w*\s+audio", "audio unlock"),
        (r"\blocalStorage\b", "localStorage"),
        (r"\bsessionStorage\b", "sessionStorage"),
        (r"\bpostMessage\b", "postMessage"),
        (r"location\.hash", "location.hash"),
        (r"location\.search", "location.search"),
        (r"\bURLSearchParams\b", "URLSearchParams"),
        (r"\bSheetJS\b", "SheetJS"),
        (r"\bXLSX\.(?:read|utils|write)", "runtime XLSX parsing"),
    ]
    ui_forbidden = [
        (r"<button[^>]*>\s*(?:Send|Wyślij|Wyslij)\s*</button>", "Send/Wyślij button"),
        (r"<button[^>]*>\s*Ping\s*</button>", "Ping button"),
    ]
    problems: list[str] = []
    for path in ACTIVE_FILES:
        text = read(path)
        checks = forbidden + (ui_forbidden if path.suffix.lower() == ".html" else [])
        for pattern, label in checks:
            for m in re.finditer(pattern, text, flags=re.IGNORECASE):
                line = text.count("\n", 0, m.start()) + 1
                problems.append(f"{path.relative_to(REPO_ROOT)}:{line}: {label}")
    if problems:
        fail("forbidden active mechanisms found:\n" + "\n".join(problems))
    return "no active Firebase/Firestore/Send/Ping/audio/storage/postMessage/query/hash/SheetJS mechanisms found"


def check_external_dependencies(index_text: str, data: dict) -> str:
    external_patterns = [
        r"<script[^>]+src=[\"']https?://",
        r"<link[^>]+href=[\"']https?://",
        r"<img[^>]+src=[\"']https?://",
        r"@import\s+url\([\"']?https?://",
        r"fetch\s*\(\s*[\"']https?://",
    ]
    for pattern in external_patterns:
        match = re.search(pattern, index_text, flags=re.IGNORECASE)
        if match:
            fail(f"external dependency pattern found: {pattern}")
    for section in ["backgrounds", "logos", "audios"]:
        for item in data.get(section, []):
            assert_relative_local_asset(item.get("file"), f"{section} id={item.get('id')}")
    return "active index uses local scripts/styles/assets/data only; Google font names remain non-blocking data values"


def check_index_structure(index_text: str) -> str:
    checks = {
        "html lang en": r"<html\s+lang=\"en\"",
        "default currentLanguage en": r"let\s+currentLanguage\s*=\s*'en'",
        "I18N pl": r"const\s+I18N\s*=\s*\{[\s\S]*?\bpl\s*:",
        "I18N en": r"const\s+I18N\s*=\s*\{[\s\S]*?\ben\s*:",
        "DATA_URL local data": r"const\s+DATA_URL\s*=\s*'assets/data/data\.json'",
        "fetch no-store": r"fetch\s*\(\s*DATA_URL\s*,\s*\{\s*cache\s*:\s*'no-store'\s*\}\s*\)",
        "parseEmbeddedManifest": r"function\s+parseEmbeddedManifest\s*\(\s*\)",
        "buildPayload": r"function\s+buildPayload\s*\(\s*\)",
        "buildOfflineSlateHTML": r"function\s+buildOfflineSlateHTML\s*\(\s*payload\s*\)",
        "openOfflineSlate": r"function\s+openOfflineSlate\s*\(\s*payload\s*\)",
        "handleGenerate": r"function\s+handleGenerate\s*\(\s*\)",
        "handleGenerate opens lastPayload": r"openOfflineSlate\s*\(\s*lastPayload\s*\)",
        "full generated document": r"return\s+`<!doctype html>[\s\S]*<html\s+lang=",
        "background image in generated HTML": r"<img\s+id=\"bg\"\s+class=\"bg\"\s+src=\"\$\{escapeAttribute\(payload\.backgroundFile",
        "overlay in generated HTML": r"id=\"overlay\"",
        "content rect serialized": r"PAYLOAD_CONTENT_RECT\s*=\s*\$\{serializeForScript\(rect\)\}",
        "prefix/suffix rendered": r"prefixText|suffixText|prefixes|suffixes",
        "message rendered": r"<div\s+id=\"msg\"\s+class=\"msg\">\$\{escapeHtml\(message\)\}</div>",
        "optional logo": r"payload\.showLogo[\s\S]*logoFile",
        "embedded fallback tag": r"id=\"embeddedDataSlateData\"",
    }
    missing = [name for name, pattern in checks.items() if not re.search(pattern, index_text)]
    if missing:
        fail("missing expected index structure: " + ", ".join(missing))

    lang_match = re.search(r"<select[^>]+id=\"languageSelect\"[\s\S]*?</select>", index_text)
    if not lang_match:
        fail("languageSelect not found")
    options = re.findall(r"<option\s+value=\"([^\"]+)\">([^<]+)</option>", lang_match.group(0))
    if options[:2] != [("en", "English"), ("pl", "Polski")]:
        fail(f"language options are not English then Polski: {options[:2]}")

    load_manifest = re.search(r"async\s+function\s+loadManifest\s*\(\s*\)\s*\{([\s\S]*?)\n\s*\}\n\s*function\s+buildOfflineSlateHTML", index_text)
    if not load_manifest:
        fail("loadManifest body not found")
    body = load_manifest.group(1)
    if "try" not in body or "catch" not in body or "parseEmbeddedManifest()" not in body:
        fail("loadManifest must use try/catch and parseEmbeddedManifest() fallback")
    return "index structure, language defaults, fetch path, embedded fallback, generator functions and generated document markers verified"


def check_html_files() -> str:
    for path in INDEX_FILES:
        parser = BasicHTMLParser()
        parser.feed(read(path))
        parser.close()
        if parser.errors:
            fail(f"HTML parser errors in {path.name}: {parser.errors}")
        if not parser.start_tags or parser.start_tags[0][0] != "html":
            fail(f"first start tag is not <html> in {path.name}")
    return "Python html.parser accepted index.html/index_backup.html/index_test.html"


def check_dynamic_node(index_text: str, data: dict) -> str:
    node = shutil.which("node")
    if not node:
        return "NOT AVAILABLE: node binary is not available"
    main_script = extract_main_script(index_text)
    embedded = json.dumps(data, ensure_ascii=False)
    harness = f"""
const vm = require('vm');
const code = {json.dumps(main_script)};
const embeddedJson = {json.dumps(embedded)};
function makeNode(id) {{
  const node = {{
    id, value: '', checked: false, textContent: '', innerHTML: '', src: '', alt: '', hidden: false,
    className: '', style: {{ setProperty(){{}} }}, classList: {{ add(){{}}, remove(){{}}, toggle(){{}}, contains(){{ return false; }} }}, dataset: {{}}, children: [],
    addEventListener(){{}}, appendChild(child){{ this.children.push(child); return child; }}, replaceChildren(...kids){{ this.children = kids; }},
    focus(){{}}, setAttribute(name, value){{ this[name] = value; }}, removeAttribute(name){{ delete this[name]; }},
    querySelectorAll(){{ return []; }}
  }};
  return node;
}}
const nodes = new Map();
function getNode(id) {{
  if (!nodes.has(id)) nodes.set(id, makeNode(id));
  return nodes.get(id);
}}
const documentStub = {{
  documentElement: {{ lang: 'en', clientWidth: 1280, clientHeight: 720, style: {{ setProperty(){{}} }} }},
  body: makeNode('body'),
  getElementById(id) {{
    if (id === 'embeddedDataSlateData') return {{ textContent: embeddedJson }};
    return getNode(id);
  }},
  querySelectorAll() {{ return []; }},
  createElement(tag) {{ const node = makeNode(tag); node.tagName = tag.toUpperCase(); return node; }}
}};
const context = {{
  console: {{ log(){{}}, warn(){{}}, error(){{}} }},
  document: documentStub,
  window: {{
    innerWidth: 1280, innerHeight: 720, visualViewport: null,
    open() {{ return {{ document: {{ open(){{}}, write(html){{ this.html = html; }}, close(){{}} }} }}; }},
    addEventListener(){{}}
  }},
  alert(){{}}, fetch: async () => ({{ ok: false }}), setTimeout, clearTimeout,
  requestAnimationFrame(cb) {{ return setTimeout(cb, 0); }}, cancelAnimationFrame(id) {{ clearTimeout(id); }}
}};
vm.createContext(context);
vm.runInContext(code, context, {{ filename: 'index-main-script.js' }});
const testCode = `
(function() {{
  const sample = {{
    backgroundId: 10,
    backgroundFile: 'assets/backgrounds/WnG.png',
    logoId: 3,
    logoFile: 'assets/logos/Aquila.png',
    showLogo: true,
    fillersEnabled: true,
    prefixLines: ['+++'],
    suffixLines: ['---'],
    text: 'Stage 7 test message\\\\nSecond line',
    messageColor: '#00ff66',
    prefixSuffixColor: '#ffffff',
    logoColor: '#d4af37',
    fontPreset: 'Orbitron',
    msgFontSize: 22,
    psFontSize: 12,
    contentRect: {{ x: 0.12, y: 0.09, w: 0.74, h: 0.80 }}
  }};
  const variants = [
    sample,
    {{ ...sample, showLogo: false }},
    {{ ...sample, fillersEnabled: false }},
    {{ ...sample, text: '' }},
    {{ ...sample, fontPreset: null }},
    {{ ...sample, contentRect: {{ x: -9, y: 4, w: 99, h: null }} }},
    {{ ...sample, backgroundId: 1, backgroundFile: 'assets/backgrounds/DataSlate_01.png', contentRect: {{ x: 0.0642, y: 0.0762, w: 0.8707, h: 0.8124 }} }}
  ];
  for (const payload of variants) {{
    const html = buildOfflineSlateHTML(payload);
    if (!html.startsWith('<!doctype html>')) throw new Error('generated HTML is not a full document');
    for (const token of [payload.backgroundFile, 'id="overlay"', 'PAYLOAD_CONTENT_RECT', 'Stage 7 test message']) {{
      if (payload.text === '' && token === 'Stage 7 test message') continue;
      if (!html.includes(token)) throw new Error('generated HTML missing token: ' + token);
    }}
    if (payload.showLogo && !html.includes(payload.logoFile)) throw new Error('logo-enabled HTML misses logo file');
    if (!payload.showLogo && html.includes('class="slate-logo"')) throw new Error('logo-disabled HTML still renders logo element');
    if (payload.fillersEnabled && !html.includes('+++')) throw new Error('fillers-enabled HTML misses prefix');
    if (!payload.fillersEnabled && html.includes('<div id="prefix" class="prefix">+++')) throw new Error('fillers-disabled HTML still renders visible prefix text');
    for (const forbidden of ['firebase', 'Firestore', 'postMessage', 'localStorage', 'sessionStorage', 'new Audio', '.play(']) {{
      if (html.includes(forbidden)) throw new Error('generated HTML contains forbidden token: ' + forbidden);
    }}
  }}
  const parsed = parseEmbeddedManifest();
  if (!parsed.backgrounds || parsed.backgrounds.length !== {len(data.get('backgrounds', []))}) throw new Error('embedded fallback parse failed');
}})();
`;
vm.runInContext(testCode, context, {{ filename: 'stage7-dynamic-test.js' }});
"""
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as temp:
        temp.write(harness)
        temp_path = Path(temp.name)
    try:
        proc = run_command([node, str(temp_path)], timeout=30)
        if proc.returncode != 0:
            fail("Node dynamic generated-HTML test failed:\nSTDOUT:\n" + proc.stdout + "\nSTDERR:\n" + proc.stderr)
    finally:
        temp_path.unlink(missing_ok=True)
    return "Node VM generated HTML test passed for logo/filler/message/font/contentRect payload variants and embedded fallback parsing"


def check_node_syntax(index_text: str) -> str:
    node = shutil.which("node")
    if not node:
        return "NOT AVAILABLE: node binary is not available"
    main_script = extract_main_script(index_text)
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as temp:
        temp.write(main_script)
        temp_path = Path(temp.name)
    try:
        proc = run_command([node, "--check", str(temp_path)], timeout=30)
        if proc.returncode != 0:
            fail("node --check failed:\n" + proc.stdout + proc.stderr)
    finally:
        temp_path.unlink(missing_ok=True)
    return "node --check accepted extracted index.html script"


def check_git_clean_baseline() -> str:
    proc = run_command(["git", "status", "--short"])
    detail = proc.stdout.strip() or "clean"
    if proc.returncode != 0:
        fail(proc.stderr.strip() or "git status failed")
    return detail


def check_protected_dataslate_unchanged() -> str:
    proc = run_command(["git", "diff", "--name-only", "--", "DataSlate"])
    if proc.returncode != 0:
        fail(proc.stderr.strip() or "git diff DataSlate failed")
    if proc.stdout.strip():
        fail("protected DataSlate/ folder has changes:\n" + proc.stdout)
    return "no git diff under protected DataSlate/ folder"


def collect_checks() -> list[tuple[str, callable[[], str]]]:
    index_text = read(MODULE_ROOT / "index.html")
    data = json.loads(read(DATA_FILE))
    return [
        ("git status snapshot", check_git_clean_baseline),
        ("data.json parses as JSON", lambda: f"top-level keys={', '.join(data.keys())}"),
        ("embedded data parses and matches data.json", lambda: check_embedded_all(data)),
        ("index backup/test synchronized", check_index_sync),
        ("static HTML parser validation", check_html_files),
        ("index JavaScript syntax", lambda: check_node_syntax(index_text)),
        ("update_embedded_data.py compiles", check_py_compile_tool),
        ("forbidden active mechanisms scan", check_forbidden_mechanisms),
        ("index structure and generator function scan", lambda: check_index_structure(index_text)),
        ("data and local asset integrity", lambda: check_data_and_assets(data, index_text)),
        ("external dependency scan", lambda: check_external_dependencies(index_text, data)),
        ("Node VM generated HTML and fallback behavior", lambda: check_dynamic_node(index_text, data)),
        ("protected DataSlate folder unchanged", check_protected_dataslate_unchanged),
    ]


def check_embedded_all(data: dict) -> str:
    expected = canonical_json(data)
    for path in INDEX_FILES:
        embedded = extract_embedded_json(read(path))
        if canonical_json(embedded) != expected:
            diff = "\n".join(difflib.unified_diff(
                expected.splitlines(), canonical_json(embedded).splitlines(),
                fromfile="data.json", tofile=path.name, lineterm=""
            ))
            fail(f"embedded data mismatch in {path.name}:\n{diff[:4000]}")
    return "embeddedDataSlateData in all index files matches assets/data/data.json"


def check_index_sync() -> str:
    base = (MODULE_ROOT / "index.html").read_bytes()
    for path in [MODULE_ROOT / "index_backup.html", MODULE_ROOT / "index_test.html"]:
        if path.read_bytes() != base:
            fail(f"{path.name} is not byte-identical to index.html")
    return "index_backup.html and index_test.html are byte-identical to index.html"


def check_py_compile_tool() -> str:
    proc = run_command([sys.executable, "-m", "py_compile", str(TOOL_FILE)])
    pycache = TOOL_FILE.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if proc.returncode != 0:
        fail(proc.stdout + proc.stderr)
    return "python3 -m py_compile accepted update_embedded_data.py"


def render_markdown(results: list[CheckResult]) -> str:
    lines = ["| Check | Result | Details |", "| --- | --- | --- |"]
    for item in results:
        detail = item.detail.replace("\n", "<br>").replace("|", "\\|")
        lines.append(f"| {item.name} | {item.status} | {detail} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", action="store_true", help="Print a Markdown table instead of plain text")
    args = parser.parse_args()

    results: list[CheckResult] = []
    exit_code = 0
    for name, check in collect_checks():
        try:
            detail = check()
            status = "PASS"
            if isinstance(detail, str) and detail.startswith("NOT AVAILABLE"):
                status = "NOT AVAILABLE"
        except AssertionError as exc:
            status = "FAIL"
            detail = str(exc)
            exit_code = 1
        results.append(CheckResult(name, status, detail))

    if args.markdown:
        print(render_markdown(results))
    else:
        for result in results:
            print(f"{result.status}: {result.name} — {result.detail}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
