"""Views package for the Health Protocol Application."""

from .lllt_view import render as render_lllt
from .mobility_view import render as render_mobility

__all__ = ['render_lllt', 'render_mobility'] 