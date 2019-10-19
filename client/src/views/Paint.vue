<template>
  <div>
    <div class="row">
      <div class="col">
        <div class="card border-success rounded-1">
          <div class="card-header p-2 bg-success text-white rounded-1">Dessinez</div>
          <div class="card-body p-2">
            <div class="row">
              <div class="col">
                <pen-selector
                  ref="penSelector"
                  class="text-right"
                  :color="penInfo.color"
                  v-on:change="penChange"
                  v-on:select="select"
                ></pen-selector>
              </div>
            </div>

            <!-- <div class="card-body p-2">
              <picker v-on:pick="select"></picker>
            </div> -->

            <hr />
            <painter ref="paint" v-on:mouseup="mouseUp" v-on:mousedown="mouseDown"></painter>
          </div>
          <div class="card-footer" v-bind:style="`background-color: ${texture.color};`">
            <div v-bind:class="texture.text==='light'?'text-light':'text-dark'">
              Selection:
              <span v-text="texture.title"></span>
            </div>
          </div>
        </div>
      </div>
      <div class="col-1 m-0 p-0">
        <button class="btn btn-dark pl-0 pr-0 h-100" v-on:click="convert">
          <span style="font-size: 500%">&rarr;</span>
        </button>
      </div>
      <div class="col">
        <div class="card border-info h-100 rounded-1">
          <div class="card-header p-2 bg-info text-white rounded-1">Image générée</div>
          <div class="card-body p-2 d-flex h-100 mx-auto">
            <h1
              v-show="!image"
              class="w-100 justify-content-center align-self-center"
            >Pas encore d'image</h1>
            <img
              v-show="image"
              class="border border-light justify-content-center align-self-center"
              :src="image"
              height="400"
              width="400"
            />
            <busy ref="busy"></busy>
          </div>
        </div>
      </div>
    </div>
    <!-- <div class="row mt-2">
      <div class="col">
        <div class="card border-primary rounded-1">
          <div class="card-header rounded-1 p-2 bg-primary text-white text-left">Textures</div>
          <div class="card-body p-2">
            <picker v-on:pick="select"></picker>
          </div>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script>
import Picker from "../components/Picker";
import Painter from "../components/Painter";
import PenSelector from "../components/PenSelector";
import Toolbar from "../components/Toolbar";
import Busy from "../components/Busy";

export default {
  name: "paint",
  components: {
    picker: Picker,
    painter: Painter,
    "pen-selector": PenSelector,
    toolbar: Toolbar,
    busy: Busy
  },
  data() {
    return {
      image: false,
      buttons: [
        "pen",
        "eraser",
        "fill-drip",
        "undo",
        "redo",
        "trash",
        ["Shape", "Circle", "Square"]
      ],
      penInfo: { color: "black" },
      toolbar: { selection: "" },
      texture: { title: "None", color: "", text: "dark" },
      // Beware that each item is pixel data stored in RAM (stored onmouseup).
      stack: {
        undo: [],
        redo: []
      },
      snapshot: undefined
    };
  },
  watch: {
    busy(val) {
      this.$refs.busy.work = val;
    }
  },
  methods: {
    select(texture) {
      this.texture = texture;
      this.$refs.paint.pen = texture.color;
      this.$refs.penSelector.color = texture.color;
    },
    pen() {
      this.$refs.paint.pen = this.texture.color;
      this.$refs.paint.mode = "draw";
      this.$log.info(this.$refs.paint.mode);
    },
    trash() {
      this.$refs.paint.clear();
    },
    undo() {
      if (this.stack.undo.length > 0) {
        const data = this.stack.undo.pop();
        this.stack.redo.push(data);
        this.$refs.paint.putData(data);
      }
    },
    redo() {
      if (this.stack.redo.length > 0) {
        const data = this.stack.redo.pop();
        this.stack.undo.push(data);
        this.$refs.paint.putData(data);
      }
    },
    eraser() {
      this.$refs.paint.pen = "white";
      this.$refs.paint.mode = "draw";
    },
    circle() {
      this.$refs.paint.shape = "circle";
      this.$refs.penSelector.shape = "circle";
    },
    square() {
      this.$refs.paint.shape = "square";
      this.$refs.penSelector.shape = "square";
    },
    filldrip() {
      this.$refs.paint.mode = "fill";
    },
    toolbarSelect(selection) {
      const method = selection.toLowerCase().replace(/[^a-z]/g, "");
      this[method]();
    },
    penChange(val) {
      // Triger each time a user change the size of the pen
      this.$refs.paint.radius = val;
    },
    mouseUp() {
      this.stack.undo.push(this.snapshot);
      this.stack.redo = [];
    },
    mouseDown() {
      this.snapshot = this.$refs.paint.getData();
    },
    convert() {
      this.busy = true;

      const dataURL = this.$refs.paint.toPNG();
      fetch("/upload", {
        method: "POST",
        body: dataURL
      })
        .then(response => response.json())
        .then(r => {
          this.image = `${this.$baseUrl}${r.location}`;
          this.busy = false;
        });
    }
  }
};
</script>

<style scoped>
.keep-bottom {
  bottom: 1rem;
  position: absolute;
}
</style>
