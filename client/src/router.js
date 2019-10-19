import Vue from "vue";
import Router from "vue-router";
import Paint from "./views/Paint.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Paint",
      component: Paint,
    }
  ],
});
