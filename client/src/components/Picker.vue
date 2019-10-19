<template>
  <div>
    <button
      v-for="texture in textures"
      v-bind:style="'background-color:'+texture.color"
      class="btn btn-default rounded-4 shadow-sm border-light float-left"
      v-bind:class="texture.text==='light' ? 'text-white' : 'text-dark'"
      v-text="texture.title"
      v-on:click="pick(texture)">
    </button>
  </div>
</template>

<script>
export default {
  name: "Picker",
  data() {
    return {
      textures: [
        { color: "#384f83", title: "mer", text: "light" },
        { color: "#efefef", title: "nuage", text: "dark" },
        { color: "#2c1e16", title: "terre", text: "light" },
        { color: "#5d6e32", title: "buisson", text: "light" },
        { color: "#b7d24e", title: "herbe", text: "dark" },
        { color: "#3c3b4b", title: "montagne", text: "light" },
        { color: "#987e6a", title: "route", text: "light" },
        { color: "#759edf", title: "ciel", text: "light" },
        { color: "#352613", title: "forêt", text: "light" },
        { color: "#636363", title: "pavé", text: "light" },
        { color: "#e670b6", title: "fleur", text: "dark" },
        { color: "#c1c3c9", title: "brouillard", text: "dark" },
        { color: "#776c2d", title: "colline", text: "light" },
        { color: "#bf602c", title: "feuilles", text: "light" },
        { color: "#32604d", title: "rivière", text: "light" },
        { color: "#fafafa", title: "neige", text: "dark" },
        { color: "#7CFC00", title: "avion", text: "dark" },
        { color: "#D2D2D2", title: "bateau", text: "dark" },
        { color: "#D2691E", title: "pont", text: "light" },
        { color: "#8B0000", title: "toit", text: "light" },
        { color: "#DEB887", title: "maison", text: "dark" },
        { color: "#00CED1", title: "fenêtre", text: "dark" },
        { color: "#B22222", title: "mur", text: "light" },
        { color: "#8B4513", title: "branche", text: "light" },
        // { color: "#FF3232", title: "fire" }
      ],
    }
  },
  methods: {
    /**
     * @param {{color:String, title:String}} texture
     */
    pick(texture) {
      this.$emit("pick", texture);
    },
  },
}
</script>

<style scoped>

</style>
