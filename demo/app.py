"""
Demo application for gradio_crystal3d component.

Shows a simple example of using the crystal3d function with file upload.
Also displays a default silicon crystal structure.
"""

import sys
from pathlib import Path
from typing import Optional

import gradio as gr

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from gradio_crystal3d import create_crystal3d_viewer

here = Path(__file__).parent


def load_cif(file: Optional[gr.File]) -> gr.HTML:
    """
    Load CIF file and return crystal3d viewer component.

    Parameters
    ----------
    file : Optional[gr.File]
        Uploaded CIF file object from Gradio

    Returns
    -------
    gr.HTML
        Crystal3D viewer component with loaded structure, or default
        silicon crystal if no file uploaded
    """
    if file is None:
        # Use default silicon crystal example
        default_cif = here / "Si_mp-149.cif"
        if default_cif.exists():
            return create_crystal3d_viewer(
                value=default_cif,
                label="Silicon Crystal (Default)",
                style_type="ball+stick",
                show_unit_cell=True,
                show_hydrogen=True,
            )
        return gr.HTML("")
    return create_crystal3d_viewer(
        value=Path(file.name),
        label="Crystal Structure",
        style_type="ball+stick",
        show_unit_cell=True,
        show_hydrogen=True,
    )


with gr.Blocks(title="Crystal3D Demo") as demo:
    gr.Markdown("# gradio_crystal3d Demo")
    gr.Markdown(
        "Upload a CIF file to visualize the crystal structure in 3D.\n"
        "By default, a silicon crystal structure is displayed."
    )

    # Default viewer with silicon crystal
    default_viewer = create_crystal3d_viewer(
        value=here / "Si_mp-149.cif",
        label="Silicon Crystal (Diamond Structure)",
        style_type="ball+stick",
        show_unit_cell=True,
        show_hydrogen=True,
    )

    gr.Markdown("---")
    gr.Markdown("### Upload your own CIF file")

    cif_file = gr.File(
        label="Upload CIF",
        file_types=[".cif"],
    )
    uploaded_viewer = gr.HTML(label="Uploaded Crystal Structure")

    cif_file.upload(
        fn=load_cif,
        inputs=cif_file,
        outputs=uploaded_viewer,
    )


if __name__ == "__main__":
    demo.launch()
