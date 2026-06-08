"""
Unit tests for gradio_crystal3d component.

Tests:
    - Component creation
    - File path handling
    - Content processing
    - API information
    - Configuration options

Usage:
    python -m pytest tests/test_component.py
    python tests/test_component.py
"""

import sys
import tempfile
from pathlib import Path
from typing import Dict
import unittest

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "backend")
)

from gradio_crystal3d import Crystal3D, create_crystal3d_viewer

here = Path(__file__).parent

SAMPLE_CIF = """data_test
_cell_length_a 5.431
_cell_length_b 5.431
_cell_length_c 5.431
_cell_angle_alpha 90
_cell_angle_beta 90
_cell_angle_gamma 90
_symmetry_space_group_name_H-M 'P 1'
loop_
_atom_site_label
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
Si1 0.0 0.0 0.0
"""


class TestCrystal3D(unittest.TestCase):
    """Test suite for Crystal3D component."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.cif_file = self.temp_path / "test.cif"
        self.cif_file.write_text(SAMPLE_CIF, encoding="utf-8")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_component_creation(self) -> None:
        """Test basic Crystal3D component creation."""
        component = Crystal3D(
            style_type="ball+stick",
            show_unit_cell=True,
            show_hydrogen=True,
        )
        self.assertIsNotNone(component)
        self.assertEqual(component.style_type, "ball+stick")
        self.assertTrue(component.show_unit_cell)
        self.assertTrue(component.show_hydrogen)

    def test_component_with_file_path(self) -> None:
        """Test component creation with CIF file path."""
        component = Crystal3D(value=str(self.cif_file))
        self.assertIsNotNone(component.value)
        self.assertIn("data_test", component.value)
        self.assertIn("Si1", component.value)

    def test_component_with_path_object(self) -> None:
        """Test component creation with Path object."""
        component = Crystal3D(value=self.cif_file)
        self.assertIsNotNone(component.value)
        self.assertIn("data_test", component.value)

    def test_component_no_value(self) -> None:
        """Test component creation without value."""
        component = Crystal3D()
        self.assertIsNone(component.value)

    def test_invalid_style_type(self) -> None:
        """Test that invalid style_type raises AssertionError."""
        with self.assertRaises(AssertionError):
            Crystal3D(style_type="invalid_style")

    def test_example_inputs(self) -> None:
        """Test example_inputs returns valid dictionary."""
        component = Crystal3D()
        examples: Dict = component.example_inputs()

        self.assertIsInstance(examples, dict)
        self.assertIn("value", examples)
        self.assertIn("style_type", examples)
        self.assertIn("show_unit_cell", examples)
        self.assertIn("show_hydrogen", examples)
        self.assertEqual(examples["style_type"], "ball+stick")
        self.assertTrue(examples["show_unit_cell"])
        self.assertTrue(examples["show_hydrogen"])

    def test_postprocess_none(self) -> None:
        """Test postprocess handles None correctly."""
        component = Crystal3D()
        result = component.postprocess(None)
        self.assertIsNone(result)

    def test_postprocess_file_path(self) -> None:
        """Test postprocess reads file content from path."""
        component = Crystal3D()
        result = component.postprocess(str(self.cif_file))
        self.assertIsNotNone(result)
        self.assertIn("data_test", result)

    def test_postprocess_path_object(self) -> None:
        """Test postprocess reads file content from Path object."""
        component = Crystal3D()
        result = component.postprocess(self.cif_file)
        self.assertIsNotNone(result)
        self.assertIn("data_test", result)

    def test_postprocess_content_string(self) -> None:
        """Test postprocess passes through content string."""
        component = Crystal3D()
        result = component.postprocess(SAMPLE_CIF)
        self.assertEqual(result, SAMPLE_CIF)

    def test_preprocess(self) -> None:
        """Test preprocess passes through content unchanged."""
        component = Crystal3D()
        result = component.preprocess(SAMPLE_CIF)
        self.assertEqual(result, SAMPLE_CIF)

    def test_api_info(self) -> None:
        """Test api_info returns correct structure."""
        component = Crystal3D()
        info = component.api_info()

        self.assertIn("input", info)
        self.assertIn("output", info)
        self.assertEqual(info["input"]["type"], "string")
        self.assertEqual(info["output"]["type"], "string")

    def test_component_different_styles(self) -> None:
        """Test component creation with different style types."""
        for style in ("ball+stick", "sphere", "stick"):
            component = Crystal3D(
                style_type=style,
                show_unit_cell=False,
                show_hydrogen=False,
            )
            self.assertEqual(component.style_type, style)
            self.assertFalse(component.show_unit_cell)
            self.assertFalse(component.show_hydrogen)

    def test_create_crystal3d_viewer_function(self) -> None:
        """Test the simplified create_crystal3d_viewer function."""
        import gradio as gr

        result = create_crystal3d_viewer(
            value=self.cif_file,
            style_type="ball+stick",
            show_unit_cell=True,
            show_hydrogen=True,
        )
        self.assertIsInstance(result, gr.HTML)

    def test_create_crystal3d_viewer_function_file_not_found(self) -> None:
        """Test create_crystal3d_viewer function raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            create_crystal3d_viewer(value="nonexistent_file.cif")

    def test_create_crystal3d_viewer_function_no_value(self) -> None:
        """Test create_crystal3d_viewer function with no value."""
        import gradio as gr

        result = create_crystal3d_viewer()
        self.assertIsInstance(result, gr.HTML)

    def test_component_with_custom_label(self) -> None:
        """Test component with custom label."""
        component = Crystal3D(label="My Custom Label")
        self.assertEqual(component.label, "My Custom Label")

    def test_component_hidden(self) -> None:
        """Test component with hidden visibility."""
        component = Crystal3D(visible=False)
        self.assertFalse(component.visible)


if __name__ == "__main__":
    unittest.main()
