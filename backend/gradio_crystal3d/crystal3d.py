"""
Crystal3D - Gradio Custom Component for crystal structure visualization.

This module provides an interactive 3D crystal structure viewer for Gradio
applications. It uses 3Dmol.js WebGL rendering engine to visualize crystal
structures from CIF format files.

Features:
    - Native CIF format support
    - Unit cell boundary display
    - Hydrogen atom visibility control
    - Multiple rendering styles (ball+stick, sphere, stick)
    - Interactive 3D rotation and zoom
"""

import base64
from pathlib import Path
from typing import Dict, List, Optional

import gradio as gr
from gradio.components.base import Component
from gradio_client.documentation import document, set_documentation_group

set_documentation_group("component")

here = Path(__file__).parent


@document()
class Crystal3D(Component):
    """
    Interactive 3D crystal structure viewer for Gradio.

    Visualizes crystal structures from CIF format files using 3Dmol.js WebGL
    rendering engine. Supports unit cell display, hydrogen atom control,
    and multiple rendering styles.

    Attributes:
        style_type (str): Rendering style ('ball+stick', 'sphere', or 'stick')
        show_unit_cell (bool): Whether to display unit cell boundary
        show_hydrogen (bool): Whether to display hydrogen atoms

    Example:
        >>> import gradio as gr
        >>> from gradio_crystal3d import Crystal3D
        >>> demo = gr.Blocks()
        >>> with demo:
        ...     crystal = Crystal3D(
        ...         value="path/to/structure.cif",
        ...         style_type="ball+stick",
        ...         show_unit_cell=True,
        ...         show_hydrogen=True,
        ...     )
        >>> demo.launch()
    """

    EVENTS = ["change"]

    def __init__(
        self,
        value: Optional[str | Path] = None,
        label: Optional[str] = "Crystal Structure",
        show_label: bool = True,
        style_type: str = "ball+stick",
        show_unit_cell: bool = True,
        show_hydrogen: bool = True,
        container: bool = True,
        every: Optional[float] = None,
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[List[str]] = None,
        render: bool = True,
        key: Optional[int | str] = None,
    ):
        """
        Initialize Crystal3D component.

        Parameters
        ----------
        value : Optional[str | Path]
            Path to CIF file. If Path object or string pointing to existing
            file, reads file content. Default: None
        label : Optional[str]
            Component label displayed in UI. Default: "Crystal Structure"
        show_label : bool
            Whether to display the label. Default: True
        style_type : str
            Rendering style: 'ball+stick', 'sphere', or 'stick'.
            Default: 'ball+stick'
        show_unit_cell : bool
            Whether to display unit cell boundary. Default: True
        show_hydrogen : bool
            Whether to display hydrogen atoms. Default: True
        container : bool
            Whether to wrap in Gradio container. Default: True
        every : Optional[float]
            Auto-update interval for Gradio streaming. Default: None
        visible : bool
            Initial visibility state. Default: True
        elem_id : Optional[str]
            HTML element ID for CSS targeting. Default: None
        elem_classes : Optional[List[str]]
            Additional CSS classes. Default: None
        render : bool
            Whether to render in Blocks context. Default: True
        key : Optional[int | str]
            Component key for Gradio reconciliation. Default: None
        """
        assert style_type in ("ball+stick", "sphere", "stick"), (
            f"style_type must be 'ball+stick', 'sphere', or 'stick', "
            f"got '{style_type}'"
        )

        self.style_type = style_type
        self.show_unit_cell = show_unit_cell
        self.show_hydrogen = show_hydrogen

        if isinstance(value, (str | Path)) and Path(value).exists():
            value = Path(value).read_text(encoding="utf-8")

        super().__init__(
            value=value,
            label=label,
            show_label=show_label,
            container=container,
            every=every,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
        )

    def generate_html(self, cif_content: Optional[str] = None) -> str:
        """
        Generate HTML content with embedded 3Dmol.js viewer.

        Parameters
        ----------
        cif_content : Optional[str]
            CIF file content string. If None, uses the component's value.

        Returns
        -------
        str
            HTML string containing the 3Dmol.js viewer
        """
        content = cif_content if cif_content is not None else self.value

        if content is None:
            content = ""

        viewer_id = hash(content) % 10000

        unit_cell_code = (
            "viewer.addUnitCell();" if self.show_unit_cell else ""
        )
        sphere_code = (
            "style.sphere = {scale: 0.3};"
            if self.style_type == "ball+stick" or self.style_type == "sphere"
            else ""
        )
        stick_code = (
            "style.stick = {radius: 0.15};"
            if self.style_type == "ball+stick" or self.style_type == "stick"
            else ""
        )
        hydrogen_code = "true" if self.show_hydrogen else "false"

        html_content = f"""
    <div style="width: 100%; height: 400px; border: 1px solid #e5e7eb;
    border-radius: 8px; overflow: hidden; position: relative;">
        <div id="crystal_viewer_{viewer_id}"
        style="width: 100%; height: 100%;"></div>
        <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
        <script>
            (function() {{
                var viewer = $3Dmol.createViewer('crystal_viewer_{viewer_id}', {{
                    defaultcolors: $3Dmol.elementColors.Jmol,
                    backgroundColor: 'white'
                }});

                var cifData = `{content}`;
                viewer.addModel(cifData, 'cif', {{doAssembly: true}});

                {unit_cell_code}

                var style = {{}};
                {sphere_code}
                {stick_code}
                viewer.setStyle({{}}, style);

                if ({hydrogen_code}) {{
                    viewer.setStyle(
                        {{elem: 'H'}},
                        {{sphere: {{scale: 0.15}}, stick: {{radius: 0.1}}}}
                    );
                }} else {{
                    viewer.setStyle({{elem: 'H'}}, {{hide: true}});
                }}

                viewer.zoomTo();
                viewer.render();
            }})();
        </script>
    </div>
    """
        return html_content

    def preprocess(self, x: Optional[str]) -> Optional[str]:
        """
        Pass through CIF string from frontend.

        Parameters
        ----------
        x : Optional[str]
            CIF content string from frontend

        Returns
        -------
        Optional[str]
            CIF content string unchanged
        """
        return x

    def postprocess(self, x: Optional[str | Path]) -> Optional[str]:
        """
        Convert file path to CIF string content.

        Parameters
        ----------
        x : Optional[str | Path]
            CIF file path or content string

        Returns
        -------
        Optional[str]
            CIF content string, or None if input is None
        """
        if x is None:
            return None
        if isinstance(x, Path):
            return x.read_text(encoding="utf-8")
        if isinstance(x, str):
            if "\n" not in x:
                path = Path(x)
                if path.exists():
                    return path.read_text(encoding="utf-8")
            return x
        raise TypeError(f"Expected str, Path, or None, got {type(x).__name__}")

    def example_inputs(self) -> Dict[str, str | bool]:
        """
        Return example inputs for documentation.

        Returns
        -------
        Dict[str, str | bool]
            Dictionary with example input values
        """
        return {
            "value": (
                "data_test\n"
                "_cell_length_a 5.431\n"
                "_cell_length_b 5.431\n"
                "_cell_length_c 5.431\n"
                "_cell_angle_alpha 90\n"
                "_cell_angle_beta 90\n"
                "_cell_angle_gamma 90\n"
                "_symmetry_space_group_name_H-M 'P 1'\n"
                "loop_\n"
                "_atom_site_label\n"
                "_atom_site_fract_x\n"
                "_atom_site_fract_y\n"
                "_atom_site_fract_z\n"
                "Si1 0.0 0.0 0.0\n"
            ),
            "style_type": "ball+stick",
            "show_unit_cell": True,
            "show_hydrogen": True,
        }

    def api_info(self) -> Dict[str, Dict[str, str]]:
        """
        Return API info for the component.

        Returns
        -------
        Dict[str, Dict[str, str]]
            Dictionary with input and output type information
        """
        return {
            "input": {"type": "string"},
            "output": {"type": "string"},
        }


def create_crystal3d_viewer(
    value: Optional[str | Path] = None,
    label: Optional[str] = "Crystal Structure",
    show_label: bool = True,
    style_type: str = "ball+stick",
    show_unit_cell: bool = True,
    show_hydrogen: bool = True,
    container: bool = True,
    **kwargs,
) -> gr.HTML:
    """
    Create a crystal structure viewer using gr.HTML.

    This is a convenience function that creates a Crystal3D instance
    and generates the corresponding HTML for visualization.

    Parameters
    ----------
    value : Optional[str | Path]
        Path to CIF file. Must be a valid file path (str or Path object)
    label : Optional[str]
        Component label. Default: "Crystal Structure"
    show_label : bool
        Whether to display label. Default: True
    style_type : str
        Rendering style: 'ball+stick', 'sphere', or 'stick'.
        Default: 'ball+stick'
    show_unit_cell : bool
        Whether to show unit cell boundary. Default: True
    show_hydrogen : bool
        Whether to show hydrogen atoms. Default: True
    container : bool
        Whether to wrap in container. Default: True
    **kwargs
        Additional keyword arguments passed to gr.HTML

    Returns
    -------
    gr.HTML
        Gradio HTML component with embedded 3Dmol.js viewer

    Raises
    ------
    FileNotFoundError
        If the specified CIF file does not exist
    ValueError
        If style_type is not a valid option
    """
    assert style_type in ("ball+stick", "sphere", "stick"), (
        f"style_type must be 'ball+stick', 'sphere', or 'stick', "
        f"got '{style_type}'"
    )

    cif_content = ""
    if value is not None:
        cif_path = Path(value) if isinstance(value, str) else value
        if not cif_path.exists():
            raise FileNotFoundError(f"CIF file not found: {cif_path}")
        cif_content = cif_path.read_text(encoding="utf-8")

    crystal = Crystal3D(
        style_type=style_type,
        show_unit_cell=show_unit_cell,
        show_hydrogen=show_hydrogen,
    )

    html_content = crystal.generate_html(cif_content)

    return gr.HTML(
        html_content,
        label=label,
        show_label=show_label,
        container=container,
        **kwargs,
    )
