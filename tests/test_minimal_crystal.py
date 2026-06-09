'''this script is to test whether the minimal example can work. if not,
please check the installation of the package.

Reference
---------
https://gradio.app/guides/custom-HTML-components
https://3dmol.csb.pitt.edu/doc/tutorial-embeddable.html
'''

import gradio as gr

head = '<script src="https://3Dmol.org/build/3Dmol-min.js"></script>'
viewerjs = '''let viewer = function() {
    var viewer = $3Dmol.createViewer('crystal_viewer', {
        defaultcolors: $3Dmol.elementColors.Jmol,
        backgroundColor: 'white'
    });
    var cifData = `# generated using pymatgen
data_Si
_symmetry_space_group_name_H-M   'P 1'
_cell_length_a   3.86755226
_cell_length_b   3.86755226
_cell_length_c   3.86755226
_cell_angle_alpha   60.00000002
_cell_angle_beta   60.00000002
_cell_angle_gamma   60.00000002
_symmetry_Int_Tables_number   1
_chemical_formula_structural   Si
_chemical_formula_sum   Si2
_cell_volume   40.90661800
_cell_formula_units_Z   2
loop_
_symmetry_equiv_pos_site_id
_symmetry_equiv_pos_as_xyz
1  'x, y, z'
loop_
_atom_site_type_symbol
_atom_site_label
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Si  Si0  1  0.000000  0.000000  0.000000  1
Si  Si1  1  0.250000  0.250000  0.250000  1`;
            viewer.addModel(cifData, 'cif', {doAssembly: true});
            viewer.addUnitCell();
            
            var style = {};
            style.sphere = {scale: 0.3};
            style.stick = {radius: 0.15};
            viewer.setStyle({}, style);

            viewer.zoomTo();
            viewer.render();
        };
    viewer();
'''

html = """
<div style="width: 100%; 
            height: 400px; 
            border: 1px solid #e5e7eb; 
            border-radius: 8px; 
            overflow: hidden; 
            position: relative;">
<div id="crystal_viewer" 
     style="width: 100%; height: 100%;">
</div>
"""

with gr.Blocks() as demo:
    viewer = gr.HTML(
        value=html,
        label='Silicon crystal visualization',
        head=head,
        js_on_load=viewerjs+'\n$3Dmol.autoload();'
    )

if __name__ == '__main__':
    demo.launch()