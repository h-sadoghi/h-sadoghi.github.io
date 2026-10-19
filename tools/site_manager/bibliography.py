from __future__ import annotations

import re
from dataclasses import dataclass

from .utils import SiteManagerError


@dataclass(frozen=True)
class BibRecord:
    entry_type: str
    key: str
    raw: str
    fields: dict[str, str]


def _balanced_entries(text: str) -> list[str]:
    entries: list[str] = []
    index = 0
    while True:
        match = re.search(r"@[A-Za-z]+\s*[({]", text[index:])
        if not match:
            break
        start = index + match.start()
        opener = text[index + match.end() - 1]
        closer = "}" if opener == "{" else ")"
        depth = 0
        quoted = False
        escaped = False
        end = None
        for pos in range(index + match.end() - 1, len(text)):
            char = text[pos]
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                quoted = not quoted
            if quoted:
                continue
            if char == opener:
                depth += 1
            elif char == closer:
                depth -= 1
                if depth == 0:
                    end = pos + 1
                    break
        if end is None:
            raise SiteManagerError("یک رکورد BibTeX بسته نشده است.")
        entries.append(text[start:end])
        index = end
    return entries


def _field(entry: str, name: str) -> str:
    match = re.search(rf"(?is),\s*{re.escape(name)}\s*=\s*", entry)
    if not match:
        return ""
    start = match.end()
    if start >= len(entry):
        return ""
    opener = entry[start]
    if opener in "{\"":
        closer = "}" if opener == "{" else '"'
        depth = 0
        escaped = False
        value_start = start + 1
        for pos in range(start, len(entry)):
            char = entry[pos]
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if opener == '"':
                if pos > start and char == closer:
                    return entry[value_start:pos].strip()
            else:
                if char == opener:
                    depth += 1
                elif char == closer:
                    depth -= 1
                    if depth == 0:
                        return entry[value_start:pos].strip()
        return entry[value_start:].strip()
    end = re.search(r"[,)}]", entry[start:])
    return entry[start : start + end.start() if end else len(entry)].strip()


def parse_records(text: str) -> list[BibRecord]:
    records: list[BibRecord] = []
    for raw in _balanced_entries(text):
        header = re.match(r"@([A-Za-z]+)\s*[({]\s*([^,\s]+)\s*,", raw)
        if not header:
            continue
        fields = {name: _field(raw, name) for name in ("title", "year", "doi", "author")}
        records.append(BibRecord(header.group(1).lower(), header.group(2), raw, fields))
    return records


def normalize_doi(value: str) -> str:
    return re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value.strip().lower()).rstrip("/.,")


def normalize_title(value: str) -> str:
    value = re.sub(r"[{}\\]", "", value).casefold()
    return re.sub(r"[^\w]+", " ", value).strip()


def duplicate_messages(existing: str, candidate: str) -> list[str]:
    old = parse_records(existing)
    new = parse_records(candidate)
    if len(new) != 1:
        return ["ورودی باید دقیقاً یک رکورد BibTeX داشته باشد."]
    item = new[0]
    issues: list[str] = []
    for record in old:
        if record.key.casefold() == item.key.casefold():
            issues.append(f"کلید BibTeX تکراری است: {item.key}")
        old_doi, new_doi = normalize_doi(record.fields["doi"]), normalize_doi(item.fields["doi"])
        if new_doi and old_doi == new_doi:
            issues.append(f"DOI تکراری است: {new_doi} (کلید موجود: {record.key})")
        old_title, new_title = normalize_title(record.fields["title"]), normalize_title(item.fields["title"])
        if new_title and old_title == new_title and record.fields["year"] == item.fields["year"]:
            issues.append(f"عنوان و سال احتمالاً تکراری است (کلید موجود: {record.key}).")
    return sorted(set(issues))


def validate_bibliography(text: str) -> list[str]:
    records = parse_records(text)
    issues: list[str] = []
    seen_keys: dict[str, str] = {}
    seen_dois: dict[str, str] = {}
    seen_title_year: dict[tuple[str, str], str] = {}
    for record in records:
        key = record.key.casefold()
        if key in seen_keys:
            issues.append(f"کلید تکراری: {record.key} و {seen_keys[key]}")
        seen_keys[key] = record.key
        doi = normalize_doi(record.fields["doi"])
        if doi and doi in seen_dois:
            issues.append(f"DOI تکراری: {doi} در {record.key} و {seen_dois[doi]}")
        if doi:
            seen_dois[doi] = record.key
        title_year = (normalize_title(record.fields["title"]), record.fields["year"])
        if title_year[0] and title_year in seen_title_year:
            issues.append(f"عنوان/سال تکراری: {record.key} و {seen_title_year[title_year]}")
        if title_year[0]:
            seen_title_year[title_year] = record.key
    return sorted(set(issues))
