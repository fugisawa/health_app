"""
Health Protocol App package.
"""

__version__ = "0.1.0"
__author__ = "Daniel Fugisawa"

from app.views.lllt_view import render as render_lllt
from app.views.mobility_view import render as render_mobility

__all__ = ["render_lllt", "render_mobility"] 