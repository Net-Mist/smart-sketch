<template>
  <div class="container">
    <div class="float-left" v-bind:style="`height: ${radius*2}px; width:${radius*2}px;border-radius: ${radius}px;background-color:${color};border-radius:${shape==='circle'?radius*2:0}px;`"></div>
    <input v-model="radius" type="range" min="5" max="40" v-on:change="$emit('change', radius)">
  </div>
</template>

<script>
export default {
  data() {
    return {
      color: "black",
      radius: 10,
      shape: "circle",
    };
  },
}
</script>

<style scoped>
.container {
  border: 1px solid lightgray;
  padding: 0.5rem;
  vertical-align: middle;
  border-radius: 0.25rem;
  overflow: hidden;
}
</style>
