"""Backward-compatible entry point for econometric diagnostic tests.

The original project used src/tests.py. The enhanced project keeps this file
and delegates the implementation to src.diagnostics.
"""
from .diagnostics import main


if __name__ == "__main__":
    main()
