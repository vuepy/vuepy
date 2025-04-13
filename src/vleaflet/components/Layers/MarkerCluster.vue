<template>
  <div>
    <!-- markers: List of markers to include in the cluster. -->
    <slot name="default"></slot>
  </div>
</template>

<script>
export default {
  name: 'VlMarkerCluster',
  props: {
    // layer name
    name: {
      type: String,
      default: ''
    },
    // The maximum radius that a cluster will cover from the central marker (in pixels). Decreasing will make more, smaller clusters.
    max_cluster_radius: {
      type: Number,
      default: 80
    },
    /*
    When you click a cluster at the bottom zoom level, spiderfy it so you can see all of its markers. 
    (Note: the spiderfy occurs at the current zoom level if all items within the cluster 
    are still clustered at the maximum zoom level or at zoom specified by disableClusteringAtZoom option)
    */
    spiderfy_on_max_zoom: {
      type: Boolean,
      default: true
    },
    // Mouse over a cluster to show the bounds of its markers.
    show_coverage_on_hover: {
      type: Boolean,
      default: true
    },
    // Click a cluster to zoom in to its bounds.
    zoom_to_bounds_on_click: {
      type: Boolean,
      default: true
    },
    /*
     Markers will not be clustered at or below this zoom level.
     Note: you may be interested in disabling spiderfyOnMaxZoom option when using disableClusteringAtZoom.
     */
    disable_clustering_at_zoom: {
      type: Number,
      default: 18
    },
    // Clusters and markers too far from the viewport are removed from the map for performance.
    remove_outside_visible_bounds: {
      type: Boolean,
      default: true
    },
    // Smoothly split / merge cluster children when zooming and spiderfying. If L.DomUtil.TRANSITION is false, this option has no effect (no animation is possible).
    animate: {
      type: Boolean,
      default: true
    },
    /*
    If set to true (and animate option is also true) then adding individual markers to the MarkerClusterGroup after it has been added to the map will add the marker and animate it into the cluster.
    Defaults to false as this gives better performance when bulk adding markers.
    */
    animate_adding_markers: {
      type: Boolean,
      default: false
    },
    // Allows you to specify PolylineOptions to style spider legs.
    spider_leg_polyline_options: {
      type: Object,
      default:  {"weight": 1.5, "color": "#222", "opacity": 0.5}
    },
    // Scale the distance away from the center that spiderfied markers are placed. Use if you are using big marker icons.
    spiderfy_distance_multiplier: {
      type: Number,
      default: 1
    },
  }
}
</script> 