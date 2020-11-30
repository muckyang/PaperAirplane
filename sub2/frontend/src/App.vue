<template>
  <v-app id="app">
    <drawer />
    <route-view/>
    <go-top />
  </v-app>
</template>

<script>
import Drawer from "@/components/Drawer";
import RouteView from "@/components/RouteView";
import GoTop from "@/components/GoTop";

export default {
  components: {
    Drawer,
    RouteView,
    GoTop
  },
};
</script>

<style>
#app{
  background-image: linear-gradient(rgba(255, 255, 255, 0.7)), url(assets/img/newsky.jpg);
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
  font-family: 'Gamja Flower', 'Hi Melody', cursive;
  font-size:1.2em;
  line-height: 0.7;
}
.v-label{
  font-size:25px;
}  
.v-text-field , .v-card title{
    font-size : 20px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
   .v-text-field >>> label {
    font-size : 24px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
  .v-btn, .v-radio >>> label {
    font-size : 30px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
</style>