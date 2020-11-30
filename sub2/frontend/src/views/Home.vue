<template>
  <v-container class="mt-5" bg fill-height grid-list-md text-xs-center>
    <v-layout row wrap align-center>
      <v-flex>
        <v-card-text class="text-center">
          <img src="../assets/img/logo.png">
          <p class="pa-5" style=" font-size:60px; ">종이비행기</p>
          <v-btn large color="blue lighten-1 white--text ma-5" style="font-size:20px" rounded to="/toursearch">관광지 검색</v-btn>
          <v-btn large color="blue lighten-1 white--text ma-5" style="font-size:20px" rounded to="/foodsearch">음식점 검색</v-btn>
        </v-card-text>
      </v-flex>
      <v-flex>
        <v-layout row>
          <v-flex xs12 sm10 md10 lg9 xl4>
            <p class="text-center mt-8 mx-9" style="font-size:25px;">이런 여행지는 어떠세요?</p>
            <v-carousel v-model="tourspotmodel" height="300px" class="mx-9">
              <v-carousel-item
                v-for="(spot, i) in tourspots"
                :key="i"
              >
                <v-sheet
                  :color="colors[i]"
                  height="100%"
                  width="100%"
                  tile
                >
                  <v-col
                    class="fill-height grey--text text--darken-3"
                    align="center"
                    justify="center"
                  >
                    <v-row align="center" justify="center">
                      <div class="mb-3" style="margin-top:10%; max-width:350px; font-size:30px; line-height:30px">
                        {{ spot.title }}
                      </div>
                    </v-row>
                    <v-row align="center" justify="center">
                      <div class="my-3">
                        [{{ spot.addr1 }}]
                      </div>
                    </v-row>
                    <v-row align="center" justify="center">
                      <div class="my-3">
                        📞 {{ spot.tel }} 
                      </div>
                    </v-row>
                  </v-col>
                </v-sheet>
              </v-carousel-item>
            </v-carousel>
          </v-flex>
          <div style="width:100%"></div>
          <v-flex xs12 sm10 md10 lg9 xl4>
            <p class="text-center mt-8 mx-9" style="font-size:25px;">나와 비슷한 연령대가 가는 맛집</p>
            <v-carousel v-model="storemodel" height="300px" class="mx-9">
              <v-carousel-item
                v-for="(store, i) in stores"
                :key="i"
              >
                <v-sheet
                  :color="colors2[i]"
                  height="100%"
                  width="100%"
                  tile
                >
                  <v-col
                    class="fill-height grey--text text--darken-3"
                    align="center"
                    justify="center"
                  >
                    <v-row align="center" justify="center">
                      <div class="mb-3" style="margin-top:10%; max-width:350px; font-size:30px; line-height:30px">
                        {{ store.store_name }}
                      </div>
                    </v-row>
                    <v-row align="center" justify="center">
                      <div class=" my-3">
                        [{{ store.address }}]
                      </div>
                    </v-row>
                    <v-row align="center" justify="center">
                      <div class=" my-3">
                        📞 {{ store.tel }} 
                      </div>
                    </v-row>
                  </v-col>
                </v-sheet>
              </v-carousel-item>
            </v-carousel>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import axios from "axios"
  const resourceHost = process.env.VUE_APP_BACK_URL;
  export default {
    data: () => ({
      storemodel: 0,
      tourspotmodel:0,
      colors: [
        'purple lighten-4',
        'cyan lighten-4',
        'blue-grey lighten-4',
        'amber lighten-3',
        'teal lighten-4',
      ],
      colors2: [
        'teal lighten-4',
        'amber lighten-3',
        'blue-grey lighten-4',
        'cyan lighten-4',
        'purple lighten-4',
      ],
      stores:[],
      tourspots:[],
    }),
    mounted(){
      axios
        .get(`${resourceHost}api/recommendAuto`, {params: {rec:5}})
        .then(
          ({ data }) => {
            this.tourspots = data.results
          })
        .catch(
          this.tourspots = [{title:'추천 관광지를 불러오는 중이에요!', address:'조금만 기다려주세요❤💕💖', tel:''},
          ],
        )

      axios
        .get(`${resourceHost}api/userrecommad`)
        .then(
          ({ data }) => {
            this.stores = data.results
          })
        .catch(
          this.stores = [{store_name:'추천 음식점을 불러오는 중이에요!', address:'조금만 기다려주세요❤💕💖', tel:''},
          ],
        )
    },
  }

   
</script>
<style scoped>
p{
  font-family: 'Gamja Flower', 'Hi Melody', cursive;
}
</style>
