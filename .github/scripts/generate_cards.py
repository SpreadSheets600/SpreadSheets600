"""Backwards-compatible entry point.

Delegates to the organised :mod:`cards` package. Invocation path and flags
are unchanged: ``python3 .github/scripts/generate_cards.py [--only ...]``
"""

from cards.generate import main

import sys

if __name__ == "__main__":
    sys.exit(main())
