<template>
  <div class="my-modal"
    v-if="visible" @click.self="handleWrapperClick">
    <div class="my-modal__dialog">
      <header class="my-modal__header">
        <v-layout>
        <span>{{title}}</span>
        <v-spacer></v-spacer>
        <v-btn fab small @click="$emit('update:visible', !visible)">
          <v-icon x-large>mdi-close-outline</v-icon>
        </v-btn>
        </v-layout>
      </header>
      <div class="my-modal__body scroll-t">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'my-modal',
  props: {
    visible: {
      type: Boolean,
      require: true,
      default: false
    },
    title: {
      type: String,
      require: false,
    },
  },
  methods: {
    handleWrapperClick(){
      this.$emit('update:visible', false)
    },
  },
}
</script>

<style lang="scss">
$module: 'my-modal';
.#{$module} {
  // This is modal bg
  background-color: rgba(0,0,0,0.7);
  top: 0; right: 0; bottom: 0; left: 0;
  position: fixed;
  overflow: auto;
  margin: 0;
  //This is modal layer
  &__dialog{
    left: 18%;
    top: 5%;
    width: 64%;
    height: 90%;
    position: absolute;
    background: #fff;
    border-radius: 10px;
  }

  &__header {
    font-size: 28px;
    font-weight: bold;
    line-height: 1.29;
    padding: 16px 16px 0 25px;
    position: relative;
    padding-bottom: 10px;
  }
  &__body {
    padding-right: 25px;
    padding-left: 25px;
    padding-top: 10px;
    padding-bottom: 10px;
    min-height: 150px;
    max-height: 85%;
    overflow-y: scroll;
  }
}
.scroll-t::-webkit-scrollbar {
  width: 7px;
}
.scroll-t::-webkit-scrollbar-track {
  background-color: transparent;
}
.scroll-t::-webkit-scrollbar-thumb {
  border-radius: 4px;
  background-color: gray;
}
.scroll-t::-webkit-scrollbar-button {
  width: 0;
  height: 0;
}
</style>