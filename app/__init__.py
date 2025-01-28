"""Health Protocol Application.

A comprehensive application for tracking and managing health protocols,
including Light Therapy (LLLT) and Mobility exercises.
"""

__version__ = "0.1.0"
__author__ = "Daniel Fugisawa"

from app.views.lllt_view import render as render_lllt
from app.views.mobility_view import render as render_mobility

__all__ = ["render_lllt", "render_mobility"] 