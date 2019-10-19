<template>
  <div>
    <div class="container">
      <div
        v-bind:style="`height: ${radius_max*2}px; width:${radius_max*2}px; justify-content: center; align-items: center; display: flex;`"
      >
        <div
          v-bind:style="`height: ${radius*2}px; width:${radius*2}px;border-radius: ${radius}px;background-color:${color};border-radius:${shape==='circle'?radius*2:0}px;`"
        ></div>
      </div>

      <input
        class="float-left"
        v-model="radius"
        type="range"
        min="5"
        max="40"
        v-on:change="$emit('change', radius)"
      />
    </div>
    <div class="container">
      <picker v-on:pick="select"></picker>
    </div>
  </div>
</template>

<script>
import Picker from "../components/Picker";

export default {
  components: {
    picker: Picker
  },
  methods: {
    select(texture){this.$emit('select', texture)}
  },
  data() {
    return {
      color: "black",
      radius: 10,
      shape: "circle",
      radius_max: 40
    };
  }
};
</script>

<style scoped>
.container {
  border: 1px solid lightgray;
  padding: 0.5rem;
  border-radius: 0.25rem;
  overflow: hidden;

  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
