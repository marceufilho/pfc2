"""Standalone entry point: `uv run --locked python -m pfc2` from the repository root."""

import sys

from pfc2.cli import main

sys.exit(main())
