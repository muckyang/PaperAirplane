<template>
  <v-card elevation="0"
    class="my-1 pa-1"
    height="280"
  >
    <v-card-text class="text-center">
      <p class="display-1 font-weight-bold">{{ name }}</p>
      <p class="subtitle-1 font-italic">{{ tags }}</p>
    </v-card-text>
    <v-footer color="white">
      <v-col class="text-center">
        <p class="grey--text caption font-italic">{{ address }}</p>
        <p class="grey--text caption font-italic"> 📞 {{ tel }}</p>
      </v-col>
    </v-footer>
  </v-card>
</template>

<script>
export default {
  props: {
    id: {
      type: Number,
      default: ""
    },
    name: {
      type: String,
      default: ""
    },
    categories: {
      type: Array,
      default: () => new Array()
    },
    address: {
      type: String,
      default: ""
    },
    tel: {
      type: String,
      default: ""
    },
    lat: {
      type: Number,
      default: ""
    },
    lng: {
      type: Number,
      default: ""
    },
  },
  computed: {
    tags: function() {
      return this.categories.reduce((acc, v) => {
        return `${acc} #${v}`;
      }, "");
    },
  },
};
</script>
