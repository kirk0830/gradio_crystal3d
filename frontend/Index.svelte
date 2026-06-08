<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import { BlockLabel } from "@gradio/atoms";
  import { StatusTracker } from "@gradio/statustracker";
  import type { LoadingStatus } from "@gradio/statustracker";
  import * as $3Dmol from "3dmol/build/3Dmol.js";

  export let value: string | null = null;
  export let label = "Crystal Structure";
  export let show_label = true;
  export let container = true;
  export let style_type: "sphere" | "stick" | "ball+stick" = "ball+stick";
  export let show_unit_cell = true;
  export let show_hydrogen = true;
  export let loading_status: LoadingStatus;

  let viewer_div: HTMLDivElement;
  let viewer: any = null;
  let is_initialized = false;

  onMount(() => {
    if (value && viewer_div && !is_initialized) {
      initViewer();
    }
  });

  onDestroy(() => {
    if (viewer) {
      viewer.removeAllModels();
      viewer = null;
    }
  });

  $: if (value && viewer_div && is_initialized) {
    updateModel();
  }

  function initViewer(): void {
    if (!viewer_div || viewer) return;

    viewer = $3Dmol.createViewer(viewer_div, {
      defaultcolors: $3Dmol.elementColors.rasmol,
      backgroundColor: "white"
    });

    is_initialized = true;

    if (value) {
      updateModel();
    }
  }

  function updateModel(): void {
    if (!viewer || !value) return;

    viewer.clear();

    viewer.addModel(value, "cif", { doAssembly: true });

    if (show_unit_cell) {
      viewer.addUnitCell();
    }

    applyStyles();

    viewer.zoomTo();
    viewer.render();
  }

  function applyStyles(): void {
    const baseStyle: any = {};

    if (style_type === "sphere" || style_type === "ball+stick") {
      baseStyle.sphere = { scale: 0.3 };
    }
    if (style_type === "stick" || style_type === "ball+stick") {
      baseStyle.stick = { radius: 0.15 };
    }

    viewer.setStyle({}, baseStyle);

    if (show_hydrogen) {
      viewer.setStyle({ elem: "H" }, {
        sphere: { scale: 0.15 },
        stick: { radius: 0.1 }
      });
    } else {
      viewer.setStyle({ elem: "H" }, { hide: true });
    }
  }
</script>

<BlockLabel {show_label} {label} />
<StatusTracker {...loading_status} />

<div
  bind:this={viewer_div}
  class="crystal-viewer"
  style="width: 100%; height: 400px; position: relative;"
></div>

<style>
  .crystal-viewer {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    overflow: hidden;
  }
  .crystal-viewer :global(canvas) {
    width: 100% !important;
    height: 100% !important;
  }
</style>