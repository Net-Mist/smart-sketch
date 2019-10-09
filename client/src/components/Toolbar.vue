<template>
  <div class="btn-group" role="toolbar">
    <template v-for="(button, i) in buttons">
      <button v-if="typeof button==='string'"
              type="button"
              class="btn btn-light"
              v-bind:class="{active: selection===i}"
              v-on:click="select(button, i)">
        <font-awesome-icon v-bind:icon="button"/>
      </button>
      <div v-if="Array.isArray(button)" class="btn-group" role="group">
        <button
          v-on:click="dropDownIndex=(dropDownIndex===undefined?i:undefined)"
          type="button" class="btn btn-secondary dropdown-toggle"
          data-toggle="dropdown"
          v-text="button[0]">
        </button>
        <div class="dropdown-menu" v-bind:class="{show: i===dropDownIndex}">
          <a
            v-for="subButton in button.slice(1)"
            class="dropdown-item"
            href="#"
            v-text="subButton"
            v-on:click="select(subButton);button[0]=subButton;"></a>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
export default {
  name: "Toolbar",
  props: {
    buttonList: Array,
  },
  data() {
    return {
      selection: 0,
      dropDownIndex: undefined,
      buttons: this.buttonList,
    };
  },
  methods: {
    select(button, index) {
      this.selection = index;
      this.dropDownIndex = undefined;
      this.$emit("select", button);
    },
  },
}
</script>

<style scoped>

</style>
