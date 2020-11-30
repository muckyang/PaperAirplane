<template>
  <v-card elevation="0"
    class="my-1 pa-1 text-center"
    max-width="100%"
    height="500">
    <v-col align-center>
      <!-- <v-row> -->
        <!-- <v-flex> -->
        <v-img
          class="align-center"
          max-height="250px"
          max-width="100%"
          v-if="this.image==null"
          src="../assets/img/imageNotFound2.png">
        </v-img>
        <v-img
          class="align-center"
          max-height="250px"
          max-width="100%"
          v-else
          :src="image">
        </v-img>
        <!-- </v-flex> -->
      <!-- </v-row> -->
      <v-row>
        <v-card-text class="text-center" style="width:100%">
          <p class="headline font-weight-bold text-center">{{ name }}</p>
          <p class="subtitle-1 font-italic">{{ content }}</p>
        </v-card-text>
      </v-row>
      <!-- <v-row> -->
        <v-footer color="white">
          <v-col class="text-center">
            <span class="grey--text caption font-italic">({{areacode}}) {{ address }}/ 📞 {{ tel }}</span>
          </v-col>
        </v-footer>
      <!-- </v-row> -->
    </v-col>
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
      type: Number,
      default: ""
    },
    address: {
      type: String,
      default: ""
    },
    tel: {
      type: String,
      default: ""
    },
    areacode:{
      type: String,
      default: ""
    },
    image:{
      type: String,
      default: ""
    }
  },
  computed: {
    content: function() {
      if(this.categories == 12){
        return "관광지"
      }else if(this.categories == 14){
        return  "문화시설"
      }else if(this.categories == 15){
        return  "축제/공연/행사"
      }else if(this.categories == 25){
        return  "여행코스"
      }else if(this.categories == 28){
        return  "레포츠"
      }else if(this.categories == 32){
        return  "숙박"
      }else if(this.categories == 38){
        return  "쇼핑"
      }else if(this.categories == 39){
        return  "음식"
      }
    }
  }
};
</script>
