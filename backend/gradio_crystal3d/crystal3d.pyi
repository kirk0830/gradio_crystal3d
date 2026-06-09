"""Type stubs for gradio_crystal3d module."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from gradio.components.base import Component


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

    def generate_html(self, cif_content: Optional[str] = None) -> Tuple[str, str]:
        """
        Generate HTML content with embedded 3Dmol.js viewer.

        Parameters
        ----------
        cif_content : Optional[str]
            CIF file content string. If None, uses the component's value.

        Returns
        -------
        Tuple[str, str]
            Tuple containing the HTML string and the scripts should be loaded
            when the component is rendered (should be passed to the `js_on_load`
            parameter of `gr.HTML`)
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

        html = f"""
<div style="width: 100%; 
            height: 400px; 
            border: 1px solid #e5e7eb;
            border-radius: 8px; 
            overflow: hidden; 
            position: relative;">
<div id="crystal_viewer_{viewer_id}"
     style="width: 100%; height: 100%;"></div>
</div>
"""

        js = f"""let myViewer = function() {{
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
}};
myViewer();"""
        return html, js

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
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer
        from gradio.components.base import Component

    
    def change(self,
        fn: Callable[..., Any] | None = None,
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | None = None,
        api_name: str | None = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        show_progress_on: Component | Sequence[Component] | None = None,
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: Timer | float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | Literal[True] | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        api_visibility: Literal["public", "private", "undocumented"] = "public",
        key: int | str | tuple[int | str, ...] | None = None,
        api_description: str | None | Literal[False] = None,
        validator: Callable[..., Any] | None = None,
    
        ) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: list of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: list of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: defines how the endpoint appears in the API docs. Can be a string or None. If set to a string, the endpoint will be exposed in the API docs with the given name. If None (default), the name of the function will be used as the API endpoint.
            scroll_to_output: if True, will scroll to output component on completion
            show_progress: how to show the progress animation while event is running: "full" shows a spinner which covers the output component area as well as a runtime display in the upper right corner, "minimal" only shows the runtime display, "hidden" shows no progress animation at all
            show_progress_on: Component or list of components to show the progress animation on. If None, will show the progress animation on all of the output components.
            queue: if True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: if True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: if False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: if False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: a list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: continuously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            trigger_mode: if "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: if set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: if set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            api_visibility: controls the visibility and accessibility of this endpoint. Can be "public" (shown in API docs and callable by clients), "private" (hidden from API docs and not callable by the Gradio client libraries), or "undocumented" (hidden from API docs but callable by clients and via gr.load). If fn is None, api_visibility will automatically be set to "private".
            key: A unique key for this event listener to be used in @gr.render(). If set, this value identifies an event as identical across re-renders when the key is identical.
            api_description: Description of the API endpoint. Can be a string, None, or False. If set to a string, the endpoint will be exposed in the API docs with the given description. If None, the function's docstring will be used as the API endpoint description. If False, then no description will be displayed in the API docs.
            validator: Optional validation function to run before the main function. If provided, this function will be executed first with queue=False, and only if it completes successfully will the main function be called. The validator receives the same inputs as the main function.
        
        """
        ...


def create_crystal3d_viewer(
    value: Optional[str | Path] = None,
    label: Optional[str] = "Crystal Structure",
    show_label: bool = True,
    style_type: str = "ball+stick",
    show_unit_cell: bool = True,
    show_hydrogen: bool = True,
    container: bool = True,
    **kwargs: Any,
) -> Any:
    ...
