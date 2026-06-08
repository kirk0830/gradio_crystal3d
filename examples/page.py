"""
Example application for gradio_crystal3d component.

Complete example demonstrating how to use the Crystal3D component
for interactive crystal structure visualization. Includes:
    - CIF file upload
    - Multiple rendering styles
    - Unit cell toggle
    - Hydrogen atom toggle

Features:
    - Native CIF format support
    - Interactive 3D rotation and zoom
    - Multiple rendering styles (ball+stick, sphere, stick)
    - Unit cell boundary display
    - Hydrogen atom visibility control

Usage:
    python examples/example_crystal3d.py
"""

import sys
from pathlib import Path
from typing import Optional

import gradio as gr

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from gradio_crystal3d import Crystal3D, create_crystal3d_viewer

here = Path(__file__).parent


def update_viewer(
    file: Optional[gr.File],
    style: str,
    unit_cell: bool,
    hydrogen: bool,
    ) -> gr.HTML:
    """
    Update the crystal viewer based on user inputs.

    Parameters
    ----------
    file : Optional[gr.File]
        Uploaded CIF file from Gradio file input
    style : str
        Rendering style: 'ball+stick', 'sphere', or 'stick'
    unit_cell : bool
        Whether to show unit cell boundary
    hydrogen : bool
        Whether to show hydrogen atoms

    Returns
    -------
    gr.HTML
        Updated Crystal3D viewer component
    """
    if isinstance(file, str):
        file = Path(file)
    if file is None:
        file = here / "Si_mp-149.cif"
    if isinstance(file, gr.File):
        file = file.name

    return create_crystal3d_viewer(
        value=file,
        style_type=style,
        show_unit_cell=unit_cell,
        show_hydrogen=hydrogen,
    )


with gr.Blocks(title="Crystal3D Example") as demo:
    gr.Markdown("# Crystal3D Component Example")
    gr.Markdown("""
        This example demonstrates the **gradio_crystal3d** component
        for interactive 3D crystal structure visualization. Upload a CIF
        file or view the default silicon crystal example.

        **Features:**
        - Native CIF format support
        - Interactive 3D rotation and zoom
        - Multiple rendering styles
        - Unit cell boundary display
        - Hydrogen atom visibility control
    """)

    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            gr.Markdown("### Upload CIF File")
            cif_file = gr.File(
                label="Choose CIF file",
                file_types=[".cif"],
            )

            gr.Markdown("### Visualization Settings")
            style_type = gr.Dropdown(
                choices=[
                    ("Ball and Stick", "ball+stick"),
                    ("Sphere Only", "sphere"),
                    ("Stick Only", "stick"),
                ],
                value="ball+stick",
                label="Rendering Style",
                info="Choose how atoms are displayed",
            )

            show_unit_cell = gr.Checkbox(
                value=True,
                label="Show Unit Cell",
                info="Display crystal unit cell boundary",
            )

            show_hydrogen = gr.Checkbox(
                value=True,
                label="Show Hydrogen Atoms",
                info="Display hydrogen atoms in the structure",
            )

            load_default = gr.Button("Load Default (Si)")

        with gr.Column(scale=2):
            gr.Markdown("### Crystal Structure Viewer")
            default_cif = here / "Si_mp-149.cif"
            viewer = gr.HTML(label="3D Visualization")

            if default_cif.exists():
                initial_viewer = create_crystal3d_viewer(
                    value=default_cif,
                    style_type="ball+stick",
                    show_unit_cell=True,
                    show_hydrogen=True,
                )
                viewer = initial_viewer

    cif_file.change(
        fn=update_viewer,
        inputs=[cif_file, style_type, show_unit_cell, show_hydrogen],
        outputs=viewer,
    )

    style_type.change(
        fn=update_viewer,
        inputs=[cif_file, style_type, show_unit_cell, show_hydrogen],
        outputs=viewer,
    )

    show_unit_cell.change(
        fn=update_viewer,
        inputs=[cif_file, style_type, show_unit_cell, show_hydrogen],
        outputs=viewer,
    )

    show_hydrogen.change(
        fn=update_viewer,
        inputs=[cif_file, style_type, show_unit_cell, show_hydrogen],
        outputs=viewer,
    )

    load_default.click(
        fn=lambda: create_crystal3d_viewer(
            value=default_cif if default_cif.exists() else None,
            style_type="ball+stick",
            show_unit_cell=True,
            show_hydrogen=True,
        ),
        outputs=viewer,
    )

    gr.Markdown("---")
    gr.Markdown("""
        **Usage Tips:**
        - **Left click + drag**: Rotate the structure
        - **Right click + drag**: Pan the view
        - **Scroll**: Zoom in/out
        - **Upload**: Upload any CIF file to visualize your own structures
    """)


if __name__ == "__main__":
    print("Starting Crystal3D Example Application...")
    print("Visit http://localhost:7860 to use the application.")
    demo.launch(server_name="localhost", server_port=7860)
