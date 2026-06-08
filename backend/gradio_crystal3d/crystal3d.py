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
            if "\n" not in x and Path(x).exists():
                return Path(x).read_text(encoding="utf-8")
            return x
        return str(x)

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
    **kwargs
    ) -> gr.HTML:
    """
    Create a crystal structure viewer using gr.HTML.

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
    import base64

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

    cif_b64 = base64.b64encode(cif_content.encode()).decode()

    unit_cell_code = (
        "viewer.addUnitCell();" if show_unit_cell else ""
    )
    sphere_code = (
        "style.sphere = {scale: 0.3};"
        if style_type == "ball+stick" or style_type == "sphere"
        else ""
    )
    stick_code = (
        "style.stick = {radius: 0.15};"
        if style_type == "ball+stick" or style_type == "stick"
        else ""
    )
    hydrogen_code = "true" if show_hydrogen else "false"

    html_content = f"""
    <div style="width: 100%; height: 400px; border: 1px solid #e5e7eb;
    border-radius: 8px; overflow: hidden;">
        <script src="https://cdn.jsdelivr.net/npm/3dmol@2.0.0/build/3Dmol-min.js"></script>
        <div id="crystal_viewer_{hash(cif_content) % 10000}"
        style="width: 100%; height: 100%;"></div>
        <script>
            (function() {{
                let viewer = $3Dmol.createViewer(
                    'crystal_viewer_{hash(cif_content) % 10000}',
                    {{
                        defaultcolors: $3Dmol.elementColors.rasmol,
                        backgroundColor: 'white'
                    }}
                );

                let cifData = atob("{cif_b64}");
                viewer.addModel(cifData, 'cif', {{doAssembly: true}});

                {unit_cell_code}

                let style = {{}};
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

    return gr.HTML(
        html_content,
        label=label,
        show_label=show_label,
        container=container,
        **kwargs
    )
