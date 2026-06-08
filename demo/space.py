
import gradio as gr
from app import demo as app
import os

_docs = {'Crystal3D': {'description': 'Interactive 3D crystal structure viewer for Gradio.\n\nVisualizes crystal structures from CIF format files or strings using\n3Dmol.js WebGL rendering engine. Supports unit cell display, hydrogen\natom control, and multiple rendering styles.', 'members': {'__init__': {'value': {'type': 'typing.Union[str, pathlib.Path, NoneType][str,pathlib.Path,None]', 'default': 'value = None', 'description': 'CIF content string or file path. If Path, reads file content.'}, 'label': {'type': 'typing.Optional[str][str,None]', 'default': 'value = "Crystal Structure"', 'description': 'Component label displayed in UI.'}, 'show_label': {'type': 'bool', 'default': 'value = True', 'description': 'Whether to display the label.'}, 'style_type': {'type': 'str', 'default': 'value = "ball+stick"', 'description': 'Rendering style - "ball+stick", "sphere", or "stick".'}, 'show_unit_cell': {'type': 'bool', 'default': 'value = True', 'description': 'Whether to display unit cell boundary.'}, 'show_hydrogen': {'type': 'bool', 'default': 'value = True', 'description': 'Whether to display hydrogen atoms.'}, 'scale': {'type': 'float', 'default': 'value = 1.0', 'description': 'Atom size scale factor.'}, 'container': {'type': 'bool', 'default': 'value = True', 'description': 'Whether to wrap in Gradio container.'}, 'every': {'type': 'typing.Optional[float][float,None]', 'default': 'value = None', 'description': 'Auto-update interval for Gradio streaming.'}, 'visible': {'type': 'bool', 'default': 'value = True', 'description': 'Initial visibility state.'}, 'elem_id': {'type': 'typing.Optional[str][str,None]', 'default': 'value = None', 'description': 'HTML element ID for CSS targeting.'}, 'elem_classes': {'type': 'typing.Optional[typing.List[str]][typing.List[str][str],None]', 'default': 'value = None', 'description': 'Additional CSS classes.'}, 'render': {'type': 'bool', 'default': 'value = True', 'description': 'Whether to render in Blocks context.'}, 'key': {'type': 'typing.Union[int, str, NoneType][int,str,None]', 'default': 'value = None', 'description': 'Unique key for component identity.'}}, 'postprocess': {'x': {'type': 'typing.Union[str, pathlib.Path, NoneType][str,pathlib.Path,None]', 'description': None}, 'value': {'type': 'typing.Union[str, pathlib.Path, NoneType][str,pathlib.Path,None]', 'description': None}}, 'preprocess': {'return': {'type': 'typing.Optional[str][str,None]', 'description': None}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': ''}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'Crystal3D': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_crystal3d`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Gradio Custom Component for interactive 3D crystal structure visualization from CIF files
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_crystal3d
```

## Usage

```python
\"\"\"
Demo application for gradio_crystal3d.
\"\"\"

import gradio as gr
from gradio_crystal3d import Crystal3D
from pathlib import Path
from typing import Optional


def load_cif(file: Optional[gr.File]) -> Optional[str]:
    \"\"\"Load CIF file content from uploaded file.\"\"\"
    if file is None:
        return None
    return Path(file.name).read_text()


with gr.Blocks(title="Crystal3D Demo") as demo:
    gr.Markdown("# gradio_crystal3d Demo")
    gr.Markdown("Upload a CIF file to visualize the crystal structure.")

    with gr.Row():
        with gr.Column(scale=1):
            cif_file = gr.File(
                label="Upload CIF",
                file_types=[".cif"],
            )
            style_type = gr.Dropdown(
                choices=["ball+stick", "sphere", "stick"],
                value="ball+stick",
                label="Render Style",
            )
            show_unit_cell = gr.Checkbox(
                value=True,
                label="Show Unit Cell",
            )
            show_hydrogen = gr.Checkbox(
                value=True,
                label="Show Hydrogen Atoms",
            )

        with gr.Column(scale=2):
            viewer = Crystal3D(
                label="Crystal Structure",
                style_type="ball+stick",
                show_unit_cell=True,
                show_hydrogen=True,
            )

    cif_file.upload(
        fn=load_cif,
        inputs=cif_file,
        outputs=viewer,
    )

    style_type.change(
        fn=lambda s, v: v,
        inputs=[style_type, viewer],
        outputs=viewer,
    )

    show_unit_cell.change(
        fn=lambda u, v: v,
        inputs=[show_unit_cell, viewer],
        outputs=viewer,
    )

    show_hydrogen.change(
        fn=lambda h, v: v,
        inputs=[show_hydrogen, viewer],
        outputs=viewer,
    )


if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `Crystal3D`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["Crystal3D"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["Crystal3D"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.



 ```python
def predict(
    value: typing.Optional[str][str,None]
) -> typing.Union[str, pathlib.Path, NoneType][str,pathlib.Path,None]:
    return value
```
""", elem_classes=["md-custom", "Crystal3D-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          Crystal3D: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
