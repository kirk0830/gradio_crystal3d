# gradio_crystal3d

[![PyPI version](https://badge.fury.io/py/gradio_crystal3d.svg)](https://badge.fury.io/py/gradio_crystal3d)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Gradio Custom Component for interactive 3D crystal structure visualization from CIF files.

## Overview

`gradio_crystal3d` is a Gradio custom component that visualizes crystal structures from Crystallographic Information File (CIF) format. It is built on top of **3Dmol.js**, a powerful WebGL-based molecular visualization library.

> **Note**: This component was implemented through **vibe coding** - a collaborative AI-assisted development approach that combines human creativity with AI capabilities to rapidly prototype and build functional software.

## Features

- **Native CIF format support** - Directly load and parse `.cif` files
- **Interactive 3D visualization** - Rotate, zoom, and pan crystal structures with mouse controls
- **Multiple rendering styles** - Ball-and-stick, sphere, and stick representations
- **Unit cell display** - Show/hide crystal unit cell boundaries
- **Hydrogen atom control** - Toggle hydrogen atom visibility
- **Seamless Gradio integration** - Works like any standard Gradio component
- **WebGL acceleration** - Smooth rendering powered by 3Dmol.js

## Installation

### From source (recommended for development)

```bash
# Clone the repository
git clone https://github.com/kirk0830/gradio_crystal3d.git
cd gradio_crystal3d

# Create and activate conda environment
conda create -n gradio_crystal3d python=3.12
conda activate gradio_crystal3d

# Install dependencies
pip install gradio>=5.0

# Build the component
gradio cc build

# Install the built package
pip install dist/gradio_crystal3d-0.0.1-py3-none-any.whl
```

### From PyPI (coming soon)

```bash
pip install gradio_crystal3d
```

## Quick Start

### Simple example

```python
import gradio as gr
from gradio_crystal3d import create_crystal3d_viewer
from pathlib import Path

# Create a viewer from a CIF file
viewer = create_crystal3d_viewer(
    value=Path("demo/Si_mp-149.cif"),
    label="Silicon Crystal",
    style_type="ball+stick",
    show_unit_cell=True,
    show_hydrogen=True,
)

# Use in a Gradio Blocks application
with gr.Blocks() as demo:
    gr.Markdown("# Crystal Structure Viewer")
    viewer.render()

demo.launch()
```

### File upload example

```python
import gradio as gr
from gradio_crystal3d import create_crystal3d_viewer
from pathlib import Path
from typing import Optional

def load_structure(file: Optional[gr.File]) -> gr.HTML:
    """Load CIF file and return crystal3d viewer component."""
    if file is None:
        return gr.HTML("")
    return create_crystal3d_viewer(
        value=Path(file.name),
        style_type="ball+stick",
        show_unit_cell=True,
        show_hydrogen=True,
    )

with gr.Blocks() as demo:
    gr.Markdown("# Crystal Structure Viewer")
    gr.Markdown("Upload a CIF file to visualize the crystal structure.")

    cif_file = gr.File(label="Upload CIF", file_types=[".cif"])
    viewer = gr.HTML(label="Crystal Structure")

    cif_file.upload(fn=load_structure, inputs=cif_file, outputs=viewer)

demo.launch()
```

## API Reference

### `create_crystal3d_viewer()` function

Simplified function that returns a `gr.HTML` component with embedded 3D viewer.

```python
def create_crystal3d_viewer(
    value: Optional[str | Path] = None,
    label: Optional[str] = "Crystal Structure",
    show_label: bool = True,
    style_type: str = "ball+stick",
    show_unit_cell: bool = True,
    show_hydrogen: bool = True,
    container: bool = True,
    **kwargs
) -> gr.HTML
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `str \| Path \| None` | `None` | Path to CIF file (string or Path object) |
| `label` | `str \| None` | `"Crystal Structure"` | Component display label |
| `show_label` | `bool` | `True` | Whether to display the label |
| `style_type` | `str` | `"ball+stick"` | Rendering style: `"ball+stick"`, `"sphere"`, or `"stick"` |
| `show_unit_cell` | `bool` | `True` | Whether to show unit cell boundary |
| `show_hydrogen` | `bool` | `True` | Whether to show hydrogen atoms |
| `container` | `bool` | `True` | Whether to wrap in Gradio container |

**Returns:** `gr.HTML` - Gradio HTML component with embedded 3Dmol.js viewer.

**Raises:** `FileNotFoundError` if the specified CIF file does not exist.

### `Crystal3D` class

Full Gradio Custom Component class. Provides the same functionality as the `create_crystal3d_viewer()` function but as a proper Gradio Component class.

```python
from gradio_crystal3d import Crystal3D

component = Crystal3D(
    value=Path("path/to/structure.cif"),
    label="My Crystal",
    style_type="ball+stick",
    show_unit_cell=True,
    show_hydrogen=True,
)
```

## Configuration Options

### Rendering Styles

| Style | Description |
|-------|-------------|
| `"ball+stick"` | Atoms as scaled spheres connected by bonds (default) |
| `"sphere"` | Atoms as full-size spheres (CPK style) |
| `"stick"` | Bonds only, without atomic spheres |

### Unit Cell Display

When `show_unit_cell=True`, the crystal unit cell boundary is displayed as a box outline, helping to visualize the periodic structure.

### Hydrogen Atoms

When `show_hydrogen=False`, hydrogen atoms are hidden, useful for simplifying the view of structures with many hydrogen atoms.

## Interactive Controls

The viewer provides interactive controls via mouse:

- **Left click + drag**: Rotate the structure
- **Right click + drag**: Pan the view
- **Scroll wheel**: Zoom in/out

## Running the Demo

### Interactive demo with file upload

```bash
cd gradio_crystal3d
python demo/app.py
```

Visit `http://localhost:7860` in your browser to see the demo with a default silicon crystal structure and file upload capability.

### Full example application

```bash
python examples/example_crystal3d.py
```

Visit `http://localhost:8002` for a more comprehensive example with style selection and toggles.

## Development

### Local development with hot reload

```bash
# Start development server
gradio cc dev
```

This launches a development server at `http://localhost:7861` with hot reload enabled.

### Building the component

```bash
# Build Python package
gradio cc build
```

This creates `.whl` and `.tar.gz` files in the `dist/` directory.

### Running tests

```bash
# Run unit tests
python -m unittest tests/test_component.py
```

Expected output: 18 tests passing.

## Project Structure

```
gradio_crystal3d/
├── backend/
│   └── gradio_crystal3d/
│       ├── __init__.py            # Package exports
│       ├── crystal3d.py           # Core component implementation
│       └── templates/             # Frontend build artifacts
├── frontend/
│   ├── Index.svelte               # Main Svelte component
│   ├── Example.svelte             # Example display component
│   ├── package.json               # Frontend dependencies
│   └── gradio.config.js           # Gradio frontend config
├── demo/
│   ├── app.py                     # Demo application
│   └── Si_mp-149.cif              # Default example CIF file
├── examples/
│   ├── example_crystal3d.py       # Full example application
│   └── Si_mp-149.cif              # Example CIF file
├── tests/
│   ├── test_component.py          # Unit tests
│   └── test_crystal3d.py          # Integration tests
├── pyproject.toml                 # Python package configuration
└── README.md                      # This file
```

## Dependencies

### Python

- **Python** >= 3.10
- **gradio** >= 5.0

### JavaScript (bundled)

- **3Dmol.js** >= 2.0.0 (bundled in the component)
- **@gradio/atoms**, **@gradio/statustracker**, **@gradio/utils** (Gradio frontend dependencies)

## Technology Stack

This component is built using:

- **Backend**: Python with Gradio Custom Component framework
- **Frontend**: Svelte + Vite
- **3D Visualization**: [3Dmol.js](https://3dmol.csb.pitt.edu/) - WebGL-based molecular visualization library

## Acknowledgments

- **3Dmol.js** - The core visualization engine that makes this component possible
- **Gradio** - The excellent framework for building interactive ML demos

## License

GNU General Public License v3.0 (GPL-3.0)

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0) for details.

## Contributing

Contributions are welcome! Please ensure:

1. All Python files follow the style guidelines (PEP8, type hints, docstrings)
2. All functions have complete type annotations
3. Unit tests are added or updated for new functionality
4. Examples are provided for new features

## Links

- **GitHub Repository**: https://github.com/kirk0830/gradio_crystal3d
- **Issue Tracker**: https://github.com/kirk0830/gradio_crystal3d/issues
- **3Dmol.js Documentation**: https://3dmol.csb.pitt.edu/doc/
- **Gradio Custom Components Guide**: https://www.gradio.app/guides/custom-components-in-five-minutes/