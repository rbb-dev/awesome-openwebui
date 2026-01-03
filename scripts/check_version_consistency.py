#!/usr/bin/env python3
"""
Script to check and enforce version consistency across OpenWebUI plugins and documentation.
用于检查并强制 OpenWebUI 插件和文档之间版本一致性的脚本。

Usage:
    python scripts/check_version_consistency.py          # Check only
    python scripts/check_version_consistency.py --fix    # Check and fix
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Optional, List, Dict, Tuple

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def log_info(msg):
    print(f"{BLUE}[INFO]{RESET} {msg}")


def log_success(msg):
    print(f"{GREEN}[OK]{RESET} {msg}")


def log_warning(msg):
    print(f"{YELLOW}[WARN]{RESET} {msg}")


def log_error(msg):
    print(f"{RED}[ERR]{RESET} {msg}")


class VersionChecker:
    def __init__(self, root_dir: str, fix: bool = False):
        self.root_dir = Path(root_dir)
        self.plugins_dir = self.root_dir / "plugins"
        self.docs_dir = self.root_dir / "docs" / "plugins"
        self.fix = fix
        self.issues_found = 0
        self.fixed_count = 0

    def extract_version_from_py(self, file_path: Path) -> Optional[str]:
        """Extract version from Python docstring."""
        try:
            content = file_path.read_text(encoding="utf-8")
            match = re.search(r"version:\s*([\d\.]+)", content)
            if match:
                return match.group(1)
        except Exception as e:
            log_error(f"Failed to read {file_path}: {e}")
        return None

    def update_file_content(
        self, file_path: Path, pattern: str, replacement: str, version: str
    ) -> bool:
        """Update file content with new version."""
        try:
            content = file_path.read_text(encoding="utf-8")
            new_content = re.sub(pattern, replacement, content)

            if content != new_content:
                if self.fix:
                    file_path.write_text(new_content, encoding="utf-8")
                    log_success(
                        f"Fixed {file_path.relative_to(self.root_dir)}: -> {version}"
                    )
                    self.fixed_count += 1
                    return True
                else:
                    log_error(
                        f"Mismatch in {file_path.relative_to(self.root_dir)}: Expected {version}"
                    )
                    self.issues_found += 1
                    return False
            return True
        except Exception as e:
            log_error(f"Failed to update {file_path}: {e}")
            return False

    def check_plugin(self, plugin_type: str, plugin_dir: Path):
        """Check consistency for a single plugin."""
        plugin_name = plugin_dir.name

        # 1. Identify Source of Truth (English .py file)
        py_file = plugin_dir / f"{plugin_name}.py"
        if not py_file.exists():
            # Try finding any .py file that matches the directory name pattern or is the main file
            py_files = list(plugin_dir.glob("*.py"))
            # Filter out _cn.py, templates, etc.
            candidates = [
                f
                for f in py_files
                if not f.name.endswith("_cn.py") and "TEMPLATE" not in f.name
            ]
            if candidates:
                py_file = candidates[0]
            else:
                return  # Not a valid plugin dir

        true_version = self.extract_version_from_py(py_file)
        if not true_version:
            log_warning(f"Skipping {plugin_name}: No version found in {py_file.name}")
            return

        log_info(f"Checking {plugin_name} (v{true_version})...")

        # 2. Check Chinese .py file
        cn_py_files = list(plugin_dir.glob("*_cn.py")) + list(
            plugin_dir.glob("*中文*.py")
        )
        # Also check for files that are not the main file but might be the CN version
        for f in plugin_dir.glob("*.py"):
            if f != py_file and "TEMPLATE" not in f.name and f not in cn_py_files:
                # Heuristic: if it has Chinese characters or ends in _cn
                if re.search(r"[\u4e00-\u9fff]", f.name) or f.name.endswith("_cn.py"):
                    cn_py_files.append(f)

        for cn_py in set(cn_py_files):
            self.update_file_content(
                cn_py, r"(version:\s*)([\d\.]+)", rf"\g<1>{true_version}", true_version
            )

        # 3. Check README.md (English)
        readme = plugin_dir / "README.md"
        if readme.exists():
            # Pattern 1: **Version:** 1.0.0
            self.update_file_content(
                readme,
                r"(\*\*Version:?\*\*\s*)([\d\.]+)",
                rf"\g<1>{true_version}",
                true_version,
            )
            # Pattern 2: | **Version:** 1.0.0 |
            self.update_file_content(
                readme,
                r"(\|\s*\*\*Version:\*\*\s*)([\d\.]+)",
                rf"\g<1>{true_version}",
                true_version,
            )

        # 4. Check README_CN.md (Chinese)
        readme_cn = plugin_dir / "README_CN.md"
        if readme_cn.exists():
            # Pattern: **版本：** 1.0.0
            self.update_file_content(
                readme_cn,
                r"(\*\*版本：?\*\*\s*)([\d\.]+)",
                rf"\g<1>{true_version}",
                true_version,
            )

        # 5. Check Global Docs Index (docs/plugins/{type}/index.md)
        index_md = self.docs_dir / plugin_type / "index.md"
        if index_md.exists():
            # Need to find the specific block for this plugin.
            # This is harder with regex on the whole file.
            # We assume the format: **Version:** X.Y.Z
            # But we need to make sure we are updating the RIGHT plugin's version.
            # Strategy: Look for the plugin title or link, then the version nearby.

            # Extract title from py file to help search
            title = self.extract_title(py_file)
            if title:
                self.update_version_in_index(index_md, title, true_version)

        # 6. Check Global Docs Index CN (docs/plugins/{type}/index.zh.md)
        index_zh = self.docs_dir / plugin_type / "index.zh.md"
        if index_zh.exists():
            # Try to find Chinese title? Or just use English title if listed?
            # Often Chinese index uses English title or Chinese title.
            # Let's try to extract Chinese title from cn_py if available
            cn_title = None
            if cn_py_files:
                cn_title = self.extract_title(cn_py_files[0])

            target_title = cn_title if cn_title else title
            if target_title:
                self.update_version_in_index(
                    index_zh, target_title, true_version, is_zh=True
                )

        # 7. Check Global Detail Page (docs/plugins/{type}/{name}.md)
        # The doc filename usually matches the plugin directory name
        detail_md = self.docs_dir / plugin_type / f"{plugin_name}.md"
        if detail_md.exists():
            self.update_file_content(
                detail_md,
                r'(<span class="version-badge">v)([\d\.]+)(</span>)',
                rf"\g<1>{true_version}\g<3>",
                true_version,
            )

        # 8. Check Global Detail Page CN (docs/plugins/{type}/{name}.zh.md)
        detail_zh = self.docs_dir / plugin_type / f"{plugin_name}.zh.md"
        if detail_zh.exists():
            self.update_file_content(
                detail_zh,
                r'(<span class="version-badge">v)([\d\.]+)(</span>)',
                rf"\g<1>{true_version}\g<3>",
                true_version,
            )

    def extract_title(self, file_path: Path) -> Optional[str]:
        try:
            content = file_path.read_text(encoding="utf-8")
            match = re.search(r"title:\s*(.+)", content)
            if match:
                return match.group(1).strip()
        except:
            pass
        return None

    def update_version_in_index(
        self, file_path: Path, title: str, version: str, is_zh: bool = False
    ):
        """
        Update version in index file.
        Look for:
        - ... **Title** ...
        - ...
        - **Version:** X.Y.Z
        """
        try:
            content = file_path.read_text(encoding="utf-8")

            # Escape title for regex
            safe_title = re.escape(title)

            # Regex to find the plugin block and its version
            # We look for the title, then non-greedy match until we find Version line
            if is_zh:
                ver_label = r"\*\*版本：\*\*"
            else:
                ver_label = r"\*\*Version:\*\*"

            # Pattern: (Title ...)(Version: )(\d+\.\d+\.\d+)
            # We allow some lines between title and version
            pattern = rf"(\*\*{safe_title}\*\*[\s\S]*?{ver_label}\s*)([\d\.]+)"

            match = re.search(pattern, content)
            if match:
                current_ver = match.group(2)
                if current_ver != version:
                    if self.fix:
                        new_content = content.replace(
                            match.group(0), f"{match.group(1)}{version}"
                        )
                        file_path.write_text(new_content, encoding="utf-8")
                        log_success(
                            f"Fixed index for {title}: {current_ver} -> {version}"
                        )
                        self.fixed_count += 1
                    else:
                        log_error(
                            f"Mismatch in index for {title}: Found {current_ver}, Expected {version}"
                        )
                        self.issues_found += 1
            else:
                # log_warning(f"Could not find entry for '{title}' in {file_path.name}")
                pass

        except Exception as e:
            log_error(f"Failed to check index {file_path}: {e}")

    def run(self):
        if not self.plugins_dir.exists():
            log_error(f"Plugins directory not found: {self.plugins_dir}")
            return

        # Scan actions, filters, pipes
        for type_dir in self.plugins_dir.iterdir():
            if type_dir.is_dir() and type_dir.name in ["actions", "filters", "pipes"]:
                for plugin_dir in type_dir.iterdir():
                    if plugin_dir.is_dir():
                        self.check_plugin(type_dir.name, plugin_dir)

        print("-" * 40)
        if self.issues_found > 0:
            if self.fix:
                print(f"Fixed {self.fixed_count} issues.")
            else:
                print(f"Found {self.issues_found} version inconsistencies.")
                print(f"Run with --fix to automatically resolve them.")
                sys.exit(1)
        else:
            print("All versions are consistent! ✨")


def main():
    parser = argparse.ArgumentParser(description="Check version consistency.")
    parser.add_argument("--fix", action="store_true", help="Fix inconsistencies")
    args = parser.parse_args()

    # Assume script is run from root or scripts dir
    root = Path.cwd()
    if (root / "scripts").exists():
        pass
    elif root.name == "scripts":
        root = root.parent

    checker = VersionChecker(str(root), fix=args.fix)
    checker.run()


if __name__ == "__main__":
    main()
