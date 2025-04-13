<template>
  <div>
    <!-- The component will be rendered by ipyleaflet -->
  </div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/image_service.html
export default {
  name: 'VlImageService',
  props: {
    // URL to the image service
    url: {
      type: String,
      required: true,
      default: '',
      validator: (value) => value.startsWith('http') || value.startsWith('https')
    },
    // response format (use "image" to stream as bytes)
    f: {
      type: String,
      default: 'image'
    },
    // Name of the layer
    name: {
      type: String,
      default: ''
    },
    // format of exported image
    format: {
      type: String,
      default: 'jpgpng',
      validator: (value) => ["jpgpng" ,"png" ,"png8" ,"png24" ,"jpg" ,"bmp" ,"gif" ,"tiff" ,"png32" ,"bip" ,"bsq" ,"lerc"].includes(value)
    },
    // data type of the raster image
    pixel_type: {
      type: String,
      default: 'UNKNOWN',
      validator: (value) => ["C128" ,"C64" ,"F32" ,"F64" ,"S16" ,"S32" ,"S8" ,"U1" ,"U16" ,"U2" ,"U32" ,"U4" ,"U8" ,"UNKNOWN"].includes(value)
    },
    // pixel values representing no data
    no_data: {
      type: Array,
      default: [],
    },
    // how to interpret no data values
    no_data_interpretation: {
      type: String,
      default: '',
      validator: (value) => ["esriNoDataMatchAny", "esriNoDataMatchAll"].includes(value)
    },
    // resampling process for interpolating the pixel values
    interpolation: {
      type: String,
      default: '',
      validator: (value) => ["RSP_BilinearInterpolation", "RSP_CubicConvolution", "RSP_Majority", "RSP_NearestNeighbor"].includes(value)
    },
    // lossy quality for image compression
    compression_quality: {
      type: Number,
      default: 100
    },
    // order of bands to export for multiple band images
    band_ids: {
      type: Array,
      default: [],
    },
    // time range for image
    time: {
      type: Array,
      default: [],
    },
    // rules for rendering
    rendering_rule: {
      type: Object,
      default: {}
    },
    // rules for mosaicking
    mosaic_Rule: {
      type: Object,
      default: {}
    },
    // endpoint format for building the export image URL
    endpoint: {
      type: String,
      default: 'Esri',
      validator: (value) => ['Esri'].includes(value)
    },
    // resampling process for interpolating the pixel values
    interpolation: {
      type: String,
      default: '',
      validator: (value) => ["RSP_BilinearInterpolation", "RSP_CubicConvolution", "RSP_Majority", "RSP_NearestNeighbor"].includes(value)
    },
    // include image service attribution
    attribution: {
      type: String,
      default: '',
    },
    // projection used for this image service.
    crs: {
      type: String,
      default: 'EPSG3857',
      validator: (value) => ['Earth', 'EPSG3395', 'EPSG3857', 'EPSG4326', 'Base', 'Simple'].includes(value)
    },
    // emit when clicked for registered callback
    interactive: {
      type: bool,
      default: false
    },
    // minimum time interval to query for updates when panning (ms)
    update_interval: {
      type: Number,
      default: 200
    },
  },
}
</script>