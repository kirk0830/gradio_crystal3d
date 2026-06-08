"""Test script to verify the Crystal3D class and generate_html method."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from gradio_crystal3d import Crystal3D, create_crystal3d_viewer

# Test with example CIF file
cif_path = Path(__file__).parent / "examples" / "Si_mp-149.cif"

if cif_path.exists():
    print(f"Testing Crystal3D class with CIF file: {cif_path}")

    # Test Crystal3D class directly
    crystal = Crystal3D(
        value=str(cif_path),
        style_type="ball+stick",
        show_unit_cell=True,
        show_hydrogen=True,
    )

    print("\n1. Testing Crystal3D.generate_html():")
    html_content = crystal.generate_html()
    print(f"   HTML generated successfully, length: {len(html_content)} chars")

    # Test create_crystal3d_viewer convenience function
    print("\n2. Testing create_crystal3d_viewer():")
    viewer = create_crystal3d_viewer(
        value=cif_path,
        style_type="ball+stick",
        show_unit_cell=True,
        show_hydrogen=True,
    )
    print(f"   Viewer created successfully, HTML length: {len(viewer.value)} chars")

    # Save as complete HTML file for browser testing
    output_file = Path(__file__).parent / "test_class_output.html"
    complete_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Crystal3D Class Method</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
    </style>
</head>
<body>
    <h1>Crystal3D Class Method Test</h1>
{viewer.value}
</body>
</html>"""

    with open(output_file, "w") as f:
        f.write(complete_html)

    print(f"\n3. Test HTML file saved to: {output_file}")
    print("   Open this file in a browser to verify 3D visualization.")
else:
    print(f"CIF file not found: {cif_path}")
