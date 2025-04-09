<template>
  <div></div>
</template>
<script>
export default {
  name: 'VlMeasureControl',
  props: {
    position: {
      type: String,
      default: 'topleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // Possible values are ‘feet’, ‘meters’, ‘miles’, ‘kilometers’ or any user defined unit.
    primary_length_unit: {
      type: String,
      default: 'meters',
      validator: (value) => ['feet', 'meters', 'miles', 'kilometers'].includes(value)
    },
    // Possible values are ‘feet’, ‘meters’, ‘miles’, ‘kilometers’ or any user defined unit.
    secondary_length_unit: {
      type: String,
      default: null,
      validator: (value) => ['feet', 'meters', 'miles', 'kilometers'].includes(value)
    },
    // Possible values are ‘acres’, ‘hectares’, ‘sqfeet’, ‘sqmeters’, ‘sqmiles’ or any user defined unit.
    primary_area_unit: {
      type: String,
      default: 'sqmeters',
      validator: (value) => ['acres', 'hectares', 'sqfeet', 'sqmeters', 'sqmiles'].includes(value)
    },
    // Possible values are ‘acres’, ‘hectares’, ‘sqfeet’, ‘sqmeters’, ‘sqmiles’ or any user defined unit.
    secondary_area_unit: {
      type: String,
      default: null,
      validator: (value) => ['acres', 'hectares', 'sqfeet', 'sqmeters', 'sqmiles'].includes(value)
    },
    // The color used for current measurements.
    active_color: {
      type: String,
      default: '#ABE67E'
    },
    // The color used for the completed measurements.
    completed_color: {
      type: String,
      default: '#C8F2BE'
    }
  }
}
</script> 