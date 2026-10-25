from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from .manager import BookManager, ManagerError, Plan, find_repo


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="مدیریت امن Jupyter Book در مخزن اصلی سایت")
    root.add_argument("--repo", type=Path, default=Path.cwd(), help="ریشه یا مسیری داخل مخزن اصلی")
    sub = root.add_subparsers(dest="command")

    sub.add_parser("books", help="نمایش کتاب‌های ثبت‌شده")
    tree = sub.add_parser("tree", help="نمایش ساختار TOC")
    tree.add_argument("--book", default="image-processing")
    validate = sub.add_parser("validate", help="اعتبارسنجی کتاب بدون اجرا")
    validate.add_argument("--book", default="image-processing")

    add = sub.add_parser("add", help="پیش‌نمایش افزودن فایل Markdown یا Notebook")
    add.add_argument("--book", default="image-processing")
    add.add_argument("--file", type=Path, required=True)
    add.add_argument("--destination", help="مسیر نسبی مقصد در پوشهٔ کتاب")
    add.add_argument("--parent", help="file فصل والد در _toc.yml؛ برای فصل اصلی خالی بگذارید")
    add.add_argument("--position", type=int, help="موقعیت یک‌مبنایی")
    add.add_argument("--title", help="عنوان نمایشی اختیاری")
    add.add_argument("--description", help="توضیح کوتاه اختیاری برای مالک")
    add.add_argument("--apply", action="store_true", help="نوشتن پس از مشاهدهٔ Preview")

    move = sub.add_parser("move", help="تغییر عنوان یا ترتیب در همان بخش")
    move.add_argument("--book", default="image-processing")
    move.add_argument("--file", required=True, help="file موجود در _toc.yml")
    move.add_argument("--position", type=int, required=True)
    move.add_argument("--title", help="عنوان جدید؛ رشتهٔ خالی عنوان سفارشی را حذف می‌کند")
    move.add_argument("--apply", action="store_true")

    asset = sub.add_parser("asset", help="افزودن تصویر/PDF/ZIP و لینک آن به Markdown")
    asset.add_argument("--book", default="image-processing")
    asset.add_argument("--file", type=Path, required=True)
    asset.add_argument("--page", required=True, help="صفحهٔ Markdown ثبت‌شده در TOC")
    asset.add_argument("--label", help="متن لینک یا alt تصویر")
    asset.add_argument("--apply", action="store_true")

    build = sub.add_parser("build", help="ساخت کتاب بدون اجرای Notebook")
    build.add_argument("--book", default="image-processing")
    build.add_argument("--clean", action="store_true")
    execute = sub.add_parser("execute-copy", help="اجرای صریح یک کپی از Notebook؛ هرگز در Build عادی اجرا نمی‌شود")
    execute.add_argument("--book", default="image-processing")
    execute.add_argument("--file", required=True, help="file مربوط به Notebook در TOC")
    execute.add_argument("--acknowledge-risk", required=True, help="برای تأیید آگاهانه دقیقاً EXECUTE")
    stage = sub.add_parser("stage", help="کپی خروجی ساخته‌شده بعد از Build Jekyll")
    stage.add_argument("--book", default="image-processing")
    stage.add_argument("--site-dir", type=Path, default=Path("_site"))
    preview = sub.add_parser("preview", help="ساخت و نمایش محلی در پورت 4100")
    preview.add_argument("--book", default="image-processing")
    preview.add_argument("--port", type=int, default=4100)
    preview.add_argument("--no-browser", action="store_true")
    sub.add_parser("stop", help="توقف Preview کتاب")
    return root


def show_plan(plan: Plan) -> None:
    print(f"\nپیش‌نمایش: {plan.summary}")
    for warning in plan.warnings:
        print(f"هشدار: {warning}")
    print("\nفایل‌های درگیر:")
    for change in plan.changes:
        print(f"- {change.path}")
    print("\nDiff:")
    print(plan.diff or "(تفاوت متنی وجود ندارد)")


def apply_or_preview(manager: BookManager, plan: Plan, apply: bool) -> None:
    show_plan(plan)
    if not apply:
        print("\nDry-run کامل شد؛ هیچ فایلی نوشته نشد. برای ذخیره همین دستور را با --apply اجرا کنید.")
        return
    backup = manager.apply(plan)
    print(f"\nذخیره شد. پشتیبان: {backup}")


def interactive(manager: BookManager) -> int:
    while True:
        print("\nمدیر Jupyter Book — همهٔ فایل‌ها در همین مخزن اصلی")
        print("1) مشاهده کتاب‌ها  2) ساختار فصل‌ها  3) اعتبارسنجی  4) افزودن فایل")
        print("5) Build  6) Preview  7) توقف Preview  0) خروج")
        choice = input("انتخاب: ").strip()
        if choice == "0":
            return 0
        if choice == "1":
            for item in manager.books():
                print(f"- {item['id']}: {item['title']} ({item['source']})")
        elif choice == "2":
            for depth, file, title in manager.tree("image-processing"):
                suffix = f" — {title}" if title else ""
                print(f"{'  ' * depth}- {file}{suffix}")
        elif choice == "3":
            report = manager.validate("image-processing")
            print("کتاب معتبر است." if report.ok else "خطا:\n- " + "\n- ".join(report.errors))
            for warning in report.warnings:
                print(f"هشدار: {warning}")
        elif choice == "4":
            source = Path(input("مسیر فایل موجود .md یا .ipynb: ").strip().strip('"'))
            destination = input("مسیر مقصد داخل کتاب (Enter = chapters/نام فایل): ").strip() or None
            parent = input("فصل والد مثل gonzalez/index (Enter = فصل اصلی): ").strip() or None
            title = input("عنوان نمایشی اختیاری (Enter = عنوان داخل فایل): ").strip() or None
            description = input("توضیح کوتاه اختیاری: ").strip() or None
            plan = manager.plan_add(
                "image-processing", source, destination, parent, title=title, description=description
            )
            show_plan(plan)
            if input("برای نوشتن دقیقاً YES وارد کنید: ").strip() == "YES":
                print(f"ذخیره شد. پشتیبان: {manager.apply(plan)}")
            else:
                print("لغو شد؛ فایلی تغییر نکرد.")
        elif choice == "5":
            print(f"خروجی: {manager.build('image-processing', clean=True)}")
        elif choice == "6":
            print(f"آدرس: {manager.preview('image-processing')}")
        elif choice == "7":
            print(manager.stop_preview())
        else:
            print("گزینه معتبر نیست.")


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    args = parser().parse_args(argv)
    try:
        repo = find_repo(args.repo.resolve())
        manager = BookManager(repo)
        if args.command is None:
            return interactive(manager)
        if args.command == "books":
            for item in manager.books():
                print(f"{item['id']}\t{item['title']}\t{item['source']}\t{item['public_path']}")
        elif args.command == "tree":
            for depth, file, title in manager.tree(args.book):
                print(f"{'  ' * depth}{file}{' — ' + title if title else ''}")
        elif args.command == "validate":
            report = manager.validate(args.book)
            for file in report.files:
                print(f"OK  {file}")
            for warning in report.warnings:
                print(f"WARN  {warning}")
            for error in report.errors:
                print(f"ERROR  {error}")
            return 0 if report.ok else 1
        elif args.command == "add":
            apply_or_preview(
                manager,
                manager.plan_add(
                    args.book,
                    args.file,
                    args.destination,
                    args.parent,
                    args.position,
                    args.title,
                    args.description,
                ),
                args.apply,
            )
        elif args.command == "move":
            apply_or_preview(manager, manager.plan_move(args.book, args.file, args.position, args.title), args.apply)
        elif args.command == "asset":
            apply_or_preview(manager, manager.plan_asset(args.book, args.file, args.page, args.label), args.apply)
        elif args.command == "build":
            print(manager.build(args.book, args.clean))
        elif args.command == "execute-copy":
            print(manager.execute_copy(args.book, args.file, args.acknowledge_risk))
        elif args.command == "stage":
            site_dir = args.site_dir if args.site_dir.is_absolute() else repo / args.site_dir
            print(manager.stage(args.book, site_dir))
        elif args.command == "preview":
            print(manager.preview(args.book, args.port, not args.no_browser))
        elif args.command == "stop":
            print(manager.stop_preview())
        return 0
    except (ManagerError, OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"خطا: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
