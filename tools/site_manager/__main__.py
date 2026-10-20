from __future__ import annotations

import argparse
import os
from pathlib import Path

from .web import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Sadoghi local Jekyll content manager")
    parser.add_argument("--repo", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    suppress_browser = args.no_browser or os.environ.get("SITE_MANAGER_NO_BROWSER") == "1"
    run(args.repo, open_browser=not suppress_browser)


if __name__ == "__main__":
    main()
