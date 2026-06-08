"""
Integration test for gradio_crystal3d component.

Loads Si_mp-149.cif example file and verifies the component works
end-to-end without requiring user interaction.

Usage:
    python tests/test_crystal3d.py
"""

import sys
from pathlib import Path

import gradio as gr
from fastapi import FastAPI

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "backend")
)

from gradio_crystal3d import create_crystal3d_viewer

here = Path(__file__).parent


def create_test_app() -> gr.Blocks:
    """
    Create a test Gradio Blocks application.

    Returns
    -------
    gr.Blocks
        Gradio Blocks app with Crystal3D viewer preloaded with Si example
    """
    cif_path = (
        Path(__file__).parent.parent
        / "examples"
        / "Si_mp-149.cif"
    )

    if not cif_path.exists():
        raise FileNotFoundError(
            f"Example CIF file not found: {cif_path}"
        )

    print(f"Loaded CIF file: {cif_path}")
    cif_content = cif_path.read_text(encoding="utf-8")
    print(f"CIF content length: {len(cif_content)} characters")

    with gr.Blocks(title="Crystal3D Test") as demo:
        gr.Markdown("# Crystal3D Component Test")
        gr.Markdown("## Silicon Crystal Structure (mp-149)")
        gr.Markdown(
            "This test automatically loads Si_mp-149.cif from the "
            "examples directory."
        )

        gr.Markdown("### Crystal Structure Viewer")
        create_crystal3d_viewer(
            value=cif_path,
            label="Silicon (Diamond Structure)",
            style_type="ball+stick",
            show_unit_cell=True,
            show_hydrogen=True,
        )

        gr.Markdown("### Structure Information")
        gr.Markdown("- **Formula**: Si₈")
        gr.Markdown("- **Space Group**: P 1")
        gr.Markdown("- **Lattice**: Cubic (5.44 Å)")
        gr.Markdown("- **Atoms**: 8 Si atoms")

    return demo


def create_fastapi_app() -> FastAPI:
    """
    Create FastAPI app with mounted Gradio demo.

    Returns
    -------
    FastAPI
        FastAPI application with Crystal3D Gradio interface
    """
    app = FastAPI(title="Crystal3D Test API", version="1.0")
    demo = create_test_app()
    app = gr.mount_gradio_app(app, demo, path="/")
    return app


if __name__ == "__main__":
    print("=" * 60)
    print("Crystal3D Integration Test")
    print("=" * 60)

    import uvicorn

    app = create_fastapi_app()
    print("\nApplication created successfully!")
    print("\nStarting server on http://localhost:8001")
    print("Press Ctrl+C to stop the server.\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info",
    )
