"""
gradio_crystal3d - Gradio component for interactive 3D crystal structure
visualization.

Provides:
    - Crystal3D: Full Gradio Custom Component class
    - create_crystal3d_viewer: Simplified function returning gr.HTML

Usage:
    >>> from gradio_crystal3d import create_crystal3d_viewer
    >>> viewer = create_crystal3d_viewer(value="path/to/structure.cif")
"""

from .crystal3d import Crystal3D, create_crystal3d_viewer

__all__ = ["Crystal3D", "create_crystal3d_viewer"]
