from tools.site_manager.bibliography import parse_records, validate_bibliography


def test_nested_braces_are_parsed() -> None:
    text = "@article{x, title={{A {Nested} Title}}, year={2024}, doi={10.1/x}}"
    records = parse_records(text)
    assert len(records) == 1
    assert records[0].key == "x"


def test_duplicate_title_year_is_detected() -> None:
    text = "@article{a,title={Same Work},year={2024}}\n@inproceedings{b,title={Same {Work}},year={2024}}"
    issues = validate_bibliography(text)
    assert any("عنوان/سال تکراری" in issue for issue in issues)
