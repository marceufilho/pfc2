"""Standalone entry point: `uv run --locked python -m pfc2_eval` from the repository root."""

import sys

from pfc2_eval.cli import main

sys.exit(main())
