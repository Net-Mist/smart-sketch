<template>
  <div id="app">
    <!-- <nav class="navbar navbar-expand-lg navbar-dark static-top bg-primary">
      <div class="container-fluid">
        <div class="navbar-brand rubik branding">GAN-Sketcher</div>
      </div>
    </nav> -->

    <div class="main container-fluid p-2">
      <router-view/>
    </div>
  </div>
</template>

<style>
.bg-primary {
  background-color: #2c3e50 !important;
}

.border-primary {
    border-color: #2c3e50 !important;
}

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #28369c;
}

#nav {
  padding: 30px;
  color: #28369c;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.main {
  padding: 2rem;
}

body {
  background: #2b2b2b;
  overflow: hidden;
}
</style>
