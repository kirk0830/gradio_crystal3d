<script lang="ts">
  import Crystal3D from "./Index.svelte";

  const test_cif = `data_test
_cell_length_a 5.431
_cell_length_b 5.431
_cell_length_c 5.431
_cell_angle_alpha 90.0
_cell_angle_beta 90.0
_cell_angle_gamma 90.0
_symmetry_space_group_name_H-M 'F d -3 m'
_symmetry_Int_Tables_number 227
loop_
_atom_site_label
_atom_site_type_symbol
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
Si1 Si 0.0 0.0 0.0
O1 O 0.25 0.25 0.25`;
</script>

<div class="example-container">
  <Crystal3D
    value={test_cif}
    label="Crystal Structure (SiO2)"
    style_type="ball+stick"
    show_unit_cell={true}
    show_hydrogen={true}
  />
</div>

<style>
  .example-container {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
  }
</style>