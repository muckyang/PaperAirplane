<template>
  <v-container class="ml-n9 mt-5" fill-height>
    <v-content>
      <section id="hero">
        <v-row no-gutters>
          <v-img
            :min-height="'100px'"
            src="../assets/img/info_sky.jpg"
          >
            <!-- <v-theme-provider dark> -->
              <v-container fill-height>
                <v-row
                  align="center"
                  class="white--text mx-auto"
                  justify="center"
                >
                  <v-col
                    class="grey--text text--darken-3 text-center"
                    cols="12"
                    tag="h1"
                  >
                    <span
                      class="font-weight-light"
                      style="font-size:110px"
                    >
                      WELCOME TO
                    </span>

                    <br><br><br>

                    <span
                      class="font-weight-black"
                      style="font-size:110px"
                    >
                    
                      종이비행기
                    </span>

                  </v-col>

                  <v-btn
                    class="align-self-end"
                    fab
                    outlined
                    @click="$vuetify.goTo('#features')"
                  >
                    <v-icon>mdi-chevron-double-down</v-icon>
                  </v-btn>
                </v-row>
              </v-container>
            <!-- </v-theme-provider> -->
          </v-img>
        </v-row>
      </section>

      <section
        id="features"
        class="grey lighten-3"
      >
        <div class="py-12"></div>

        <v-container class="text-center">
          <h2 class="font-weight-bold mb-3" style="font-size:70px">PROJECT FEATURES</h2>

          <v-responsive
            class="mx-auto mb-12"
            width="56"
          >
            <v-divider class="mb-1"></v-divider>
              
            <v-divider></v-divider>
          </v-responsive>

          <v-row>
            <v-col
              v-for="({ icon, title, text, text2 }, i) in features"
              :key="i"
              cols="12"
              md="4"
            >
              <v-card
                class="py-12 px-4"
                color="grey lighten-5"
                flat
              >
                <!-- <v-theme-provider dark> -->
                  <div>
                    <v-avatar
                      color="indigo darken-3"
                      size="88"
                    >
                      <v-icon
                        large
                        v-text="icon"
                        dark
                      ></v-icon>
                    </v-avatar>
                  </div>
                <!-- </v-theme-provider> -->

                <v-card-title
                  class="justify-center font-weight-black text-uppercase"
                  v-text="title"
                  style="font-size:35px"
                ></v-card-title>

                <v-card-text
                  v-text="text"
                  style="font-size:20px"
                >
                </v-card-text>

                <v-card-text
                  style="font-size:20px;"
                  v-text="text2"
                >
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-container>

        <div class="py-12"></div>
      </section>

      <section id="stats">
        <v-parallax
          :height="$vuetify.breakpoint.smAndDown ? 700 : 500"
          src="../assets/img/info_night.jpg"
        >
          <v-container fill-height>
            <v-row class="mx-auto">
              <v-col
                v-for="[value, title, ] of stats"
                :key="title"
                cols="12"
                md="3"
              >
                <div class="text-center">
                  <div
                    class="font-weight-black mb-4"
                    v-text="value"
                    style="font-size:75px"
                  ></div>

                  <div
                    class="font-weight-regular text-uppercase"
                    v-text="title"
                    style="font-size:40px"
                  ></div>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-parallax>
          <div style="height:100px"></div>
      </section>

      <section id="about-us">
        <div class="py-12"></div>

        <v-container class="text-center">
          <h2 class="font-weight-bold mb-3" style="font-size:70px">ABOUT US</h2>

          <v-responsive
            class="mx-auto mb-8"
            width="56"
          >
            <v-divider class="mb-1"></v-divider>

            <v-divider></v-divider>
          </v-responsive>

          <v-responsive
            class="mx-auto font-weight-light mb-8"
            max-width="720"
            style="font-size:25px"
          >
            <p v-for="it in team" :key="it">{{it}}</p>
          </v-responsive>
          
          <v-row justify="space-around">
          <v-spacer></v-spacer>
          <v-avatar
            class="elevation-12 mb-12"
            size="100"
          >
            <v-img src="../assets/img/yeji.png"></v-img>
          </v-avatar>
          <v-spacer></v-spacer>
          <v-avatar
            class="elevation-12 mb-12"
            size="100"
          >
            <v-img src="../assets/img/nam.png"></v-img>
          </v-avatar>
          <v-spacer></v-spacer>
          <v-avatar
            class="elevation-12 mb-12"
            size="100"
          >
            <v-img src="../assets/img/ho.png"></v-img>
          </v-avatar>
          <v-spacer></v-spacer>
          <v-avatar
            class="elevation-12 mb-12"
            size="100"
          >
            <v-img src="../assets/img/bok.png"></v-img>
          </v-avatar>
          <v-spacer></v-spacer>
          <v-avatar
            class="elevation-12 mb-12"
            size="100"
          >
            <v-img src="../assets/img/dong.png"></v-img>
          </v-avatar>
          <v-spacer></v-spacer>
          </v-row>

          <div></div>
        </v-container>

        <div class="py-12"></div>
      </section>
    </v-content>
  </v-container>
</template>

<script>
import axios from "axios"
const resourceHost = process.env.VUE_APP_BACK_URL;
export default {
    data () {
      return {
        team: [
          "[팀장]손예지 : front-end",
            "김영남 : front-end",
            "김영호 : back-end",
            "송복민 : back-end",
            "이동현 : back-end",
        ],
        features: [
          {
            icon: 'mdi-account-heart-outline',
            title: 'PICK MYSELF',
            text: '사용자 친화적인 검색 시스템과 사용자가 직접 선택하는 본인만의 리스트를 제공합니다.',
            text2: 'Provides a user-friendly search system and your own personal list of choices.',
          },
          {
            icon: 'mdi-map-search',
            title: 'EASY VIEW',
            text: '선택한 리스트를 바로 지도에서 확인할 수 있습니다.',
            text2: 'You can view the selected list directly on the map.'
          },
          {
            icon: 'mdi-account-group-outline',
            title: 'RANK AND RECOMMEND',
            text: '다른 사용자가 만든 경로와 기본적으로 제공하는 추천 경로를 볼 수 있습니다.',
            text2: 'You can view paths created by other users and recommended paths provided by default.'
          },
        ],
        stats: [
          ['459k', '맛집'],
          ['25k', '관광지'],
          ['9m', '추천경로'],
        ],
      }
    },
    mounted(){
      axios.get(`${resourceHost}api/routeRankRead`)
      .then((data)=>{
        this.stats.push([data.data.count, '유저 커스텀 경로'])
      })
  },
};
</script>