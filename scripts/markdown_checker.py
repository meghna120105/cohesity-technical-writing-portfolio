"""
Markdown Documentation Checker
==============================

A small command-line tool that checks Markdown (.md) files for basic
quality problems.

What it checks:
    1. Is the file empty?
    2. Does the file have a heading (a line starting with #)?
    3. Are there lines with trailing whitespace (extra spaces at the end)?
    4. Do relative links (like [Guide](docs/guide.md)) point to files that exist?

How to run it (from the project folder):
    python scripts/markdown_checker.py README.md
    python scripts/markdown_checker.py docs/
    python scripts/markdown_checker.py README.md docs/user-guide.md

Exit codes (useful for automation):
    0 = every file checked was clean
    1 = at least one issue was found
    2 = a path was missing or a file could not be read
"""

# --- Imports -----------------------------------------------------------
# These are all part of Python's standard library, so nothing extra
# needs to be installed.
import argparse                      # reads command-line arguments
import re                            # regular expressions (pattern matching)
import sys                           # lets us exit with a status code
from dataclasses import dataclass    # a short way to define a simple data class
from pathlib import Path             # a clean way to work with file paths
from urllib.parse import unquote     # turns "my%20file.md" into "my file.md"


# --- Settings ----------------------------------------------------------

# A heading in Markdown looks like "# Title" or "## Section".
# Pattern meaning: start of line, 1 to 6 '#' characters, a space, then text.
HEADING_PATTERN = re.compile(r"^#{1,6}\s+\S")

# A top-level title is a single '#' followed by a space: "# My Title".
TITLE_PATTERN = re.compile(r"^#\s+\S")

# A Markdown link looks like [text](target) or ![alt](image.png).
# Group 1 captures the target (the part inside the round brackets).
LINK_PATTERN = re.compile(r'!?\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')

# Links starting with these are NOT local files, so we skip them.
EXTERNAL_PREFIXES = ("http://", "https://", "ftp://", "mailto:", "tel:", "#")


# --- Data structure ----------------------------------------------------

@dataclass
class Issue:
    """One problem found in a file."""
    line: int        # line number (0 means the problem is about the whole file)
    severity: str    # "ERROR" or "WARNING"
    message: str     # human-readable description


# --- Helper functions --------------------------------------------------

def read_markdown_file(file_path: Path) -> str:
    """Read a file and return its text.

    'utf-8-sig' reads normal UTF-8 and also safely ignores the invisible
    marker (BOM) that some Windows editors add at the start of a file.
    Errors are NOT handled here; the caller handles them (see check_file).
    """
    return file_path.read_text(encoding="utf-8-sig")


def lines_outside_code_blocks(lines):
    """Yield (line_number, text) for lines that are NOT inside a code block.

    Code blocks are fenced with ``` or ~~~. Text inside them is example
    code, so we do not want to treat '# comment' as a heading or
    '[x](y)' as a real link.
    """
    inside_code_block = False
    for number, line in enumerate(lines, start=1):
        if line.lstrip().startswith(("```", "~~~")):
            inside_code_block = not inside_code_block   # flip on/off
            continue
        if not inside_code_block:
            yield number, line


# --- The four checks ---------------------------------------------------
# Each check receives data and returns a list of Issue objects.
# An empty list means "no problems found".

def check_empty(content: str) -> list:
    """Check 1: is the file empty or only whitespace?"""
    if content.strip() == "":
        return [Issue(0, "ERROR", "File is empty (or contains only whitespace).")]
    return []


def check_heading(lines: list) -> list:
    """Check 2: does the file have a heading, and a top-level title?"""
    headings = [
        (number, line)
        for number, line in lines_outside_code_blocks(lines)
        if HEADING_PATTERN.match(line)
    ]

    if not headings:
        return [Issue(0, "ERROR", "No heading found (expected a line like '# Title').")]

    has_title = any(TITLE_PATTERN.match(line) for _, line in headings)
    if not has_title:
        return [Issue(0, "WARNING",
                      "Headings exist, but there is no top-level title ('# Title').")]
    return []


def check_trailing_whitespace(lines: list) -> list:
    """Check 3: find lines that end with spaces or tabs.

    Note: in Markdown, two trailing spaces can be used on purpose to force
    a line break. This tool still reports them so you can decide.
    """
    issues = []
    for number, line in enumerate(lines, start=1):
        if line != line.rstrip():     # rstrip() removes whitespace at the end
            issues.append(Issue(number, "WARNING", "Trailing whitespace."))
    return issues


def check_relative_links(lines: list, file_path: Path) -> list:
    """Check 4: do relative links point to files that exist?

    A relative link is resolved from the folder that contains the Markdown
    file. Web links, email links and '#section' links are skipped.
    """
    issues = []
    base_folder = file_path.parent

    for number, line in lines_outside_code_blocks(lines):
        for match in LINK_PATTERN.finditer(line):
            target = match.group(1).strip("<>")

            # Skip web links, mailto links and in-page anchors.
            if target.lower().startswith(EXTERNAL_PREFIXES):
                continue
            # Skip links starting with '/': on GitHub they mean "from the
            # repository root", which this simple tool cannot know.
            if target.startswith("/"):
                continue

            # Remove '#section' and '?query' parts, then decode '%20'.
            path_part = target.split("#")[0].split("?")[0]
            path_part = unquote(path_part)
            if path_part == "":
                continue

            if not (base_folder / path_part).exists():
                issues.append(Issue(number, "ERROR",
                                    f"Broken relative link: '{target}'"))
    return issues


# --- Putting the checks together ---------------------------------------

def check_file(file_path: Path):
    """Run all checks on one file.

    Returns (issues, error_message):
        - issues: list of Issue objects (may be empty)
        - error_message: None if the file was read, otherwise text
          explaining why it could not be read
    """
    try:
        content = read_markdown_file(file_path)
    except FileNotFoundError:
        return [], "File not found."
    except PermissionError:
        return [], "Permission denied (the file cannot be opened)."
    except IsADirectoryError:
        return [], "This path is a folder, not a file."
    except UnicodeDecodeError:
        return [], "Could not read the file as UTF-8 text."
    except OSError as error:
        return [], f"Could not read the file: {error}"

    # If the file is empty, the other checks would add nothing useful.
    empty_issues = check_empty(content)
    if empty_issues:
        return empty_issues, None

    lines = content.splitlines()   # split the text into a list of lines
    issues = []
    issues += check_heading(lines)
    issues += check_trailing_whitespace(lines)
    issues += check_relative_links(lines, file_path)

    issues.sort(key=lambda issue: issue.line)   # show in line order
    return issues, None


def collect_markdown_files(paths: list):
    """Turn the paths given by the user into a list of .md files.

    Returns (files, problems) where 'problems' lists paths we could not use.
    """
    files = []
    problems = []

    for raw_path in paths:
        path = Path(raw_path)
        if not path.exists():
            problems.append(f"{raw_path}: path does not exist.")
        elif path.is_dir():
            # rglob searches the folder and all subfolders for .md files.
            found = sorted(path.rglob("*.md"))
            if not found:
                problems.append(f"{raw_path}: no .md files found in this folder.")
            files.extend(found)
        elif path.suffix.lower() != ".md":
            problems.append(f"{raw_path}: not a Markdown (.md) file, skipped.")
        else:
            files.append(path)

    return files, problems


# --- Report ------------------------------------------------------------

def print_report(results: list, problems: list) -> None:
    """Print a readable report.

    'results' is a list of (file_path, issues, error_message) tuples.
    """
    print("=" * 60)
    print("MARKDOWN DOCUMENTATION CHECK REPORT")
    print("=" * 60)

    error_count = 0
    warning_count = 0
    files_with_issues = 0
    unreadable_count = 0

    for file_path, issues, error_message in results:
        print(f"\nFile: {file_path}")

        if error_message:
            print(f"  [COULD NOT CHECK] {error_message}")
            unreadable_count += 1
            continue

        if not issues:
            print("  [OK] No issues found.")
            continue

        files_with_issues += 1
        for issue in issues:
            location = f"line {issue.line}" if issue.line > 0 else "file"
            print(f"  [{issue.severity}] {location}: {issue.message}")
            if issue.severity == "ERROR":
                error_count += 1
            else:
                warning_count += 1

    if problems:
        print("\nPaths that could not be used:")
        for problem in problems:
            print(f"  - {problem}")

    print("\n" + "-" * 60)
    print("SUMMARY")
    print(f"  Files checked     : {len(results)}")
    print(f"  Files with issues : {files_with_issues}")
    print(f"  Errors            : {error_count}")
    print(f"  Warnings          : {warning_count}")
    if unreadable_count:
        print(f"  Unreadable files  : {unreadable_count}")
    print("-" * 60)


# --- Main program ------------------------------------------------------

def main() -> int:
    """Read command-line input, run the checks, print the report."""
    parser = argparse.ArgumentParser(
        description="Check Markdown files for common documentation problems."
    )
    parser.add_argument(
        "paths",
        nargs="+",   # one or more paths
        help="One or more .md files or folders to check.",
    )
    args = parser.parse_args()

    files, problems = collect_markdown_files(args.paths)

    results = []
    for file_path in files:
        issues, error_message = check_file(file_path)
        results.append((file_path, issues, error_message))

    print_report(results, problems)

    # Decide the exit code (see the top of this file).
    if problems or any(error for _, _, error in results):
        return 2
    if any(issues for _, issues, _ in results):
        return 1
    return 0


# This block runs only when the file is executed directly
# (not when it is imported by another Python file).
if __name__ == "__main__":
    sys.exit(main())