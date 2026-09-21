#!/usr/bin/env python3
"""Insert the V2.1 detailed expansions after matching project-book headings.

The operation is intentionally one-shot.  It fails when the marker is already
present so an accidental second invocation cannot duplicate the content.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "01_project_book" / "1nm晶圆IPD量测设备_整机项目书.md"
EXPANSIONS = ROOT / "01_project_book" / "项目书扩写内容_V2.1.md"
MARKER = "<!-- V2.1_DETAILED_EXPANSION -->"


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## ") or line.startswith("# "):
            current = line
            if current in sections:
                raise RuntimeError(f"duplicate expansion heading: {current}")
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return {heading: "\n".join(lines).strip() for heading, lines in sections.items()}


def main() -> None:
    source = BOOK.read_text(encoding="utf-8")
    if MARKER in source:
        raise RuntimeError("V2.1 expansions have already been merged")

    sections = parse_sections(EXPANSIONS.read_text(encoding="utf-8"))
    lines = source.splitlines()
    output: list[str] = []
    used: set[str] = set()

    for line in lines:
        output.append(line)
        if line in sections:
            output.extend(["", MARKER, "", sections[line]])
            used.add(line)

    unused = sorted(set(sections) - used)
    if unused:
        raise RuntimeError("unmatched expansion headings: " + ", ".join(unused))

    result = "\n".join(output) + "\n"
    result = result.replace(
        "<!-- 文档版本：V2.0；状态：方案设计与证据闭环基线 -->",
        "<!-- 文档版本：V2.1；状态：详细设计与证据闭环基线 -->",
        1,
    )
    BOOK.write_text(result, encoding="utf-8")
    print(f"merged {len(used)} sections into {BOOK}")


if __name__ == "__main__":
    main()
