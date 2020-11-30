<template>
 <v-container>
    <v-flex>
      <v-spacer></v-spacer>
      <v-app-bar
        elevation="3"
        class="pa-1"
        max-width="500px"
        >
        <v-layout row align-center>
                <v-avatar
                    class="elevation-4 mr-2"
                    color="orange"
                >
                  <v-icon dark>mdi-earth</v-icon>
                </v-avatar>
                <v-select
                    :items="regions"
                    item-text="region"
                    item-value="areacode"
                    label="region"
                    solo
                    class="mt-7"
                    v-model="areacode"
                ></v-select>
                <v-btn class="ml-2" depressed color="orange lighten-1 grey--text text--darken-4" @click="onSubmit">검색</v-btn>
        </v-layout>
      </v-app-bar>
      <v-spacer></v-spacer>
    </v-flex>
    <div
        v-infinite-scroll="loadMore"
        infinite-scroll-disabled="loading"
        infinite-scroll-distance="10"
    >
        <v-flex>
        <v-layout row>
            <v-card
                class="ma-1 pa-1"
                max-width="300"
                max-height="400"
                v-for="re in recommends" :key="re.contentid"
            >
                <v-img
                    v-if="re.first_image2 == undefined"
                    class="white--text align-end"
                    height="200px"
                    width="290px"
                    src="../assets/img/imageNotFound.png"
                >
                </v-img>
                <v-img
                    v-else
                    class="white--text align-end"
                    height="200px"
                    width="290px"
                    :src="re.first_image2"
                >
                </v-img>
                <div style="height:100px">
                  <v-card-title v-if="re.title == null" class="font-weight-bold" style="font-size:1.2em">제목이 없습니다.</v-card-title>
                  <v-card-title v-else class="font-weight-bold" style="font-size:1.2em">{{re.title}}</v-card-title>
                  <v-card-text>지역:{{re.areacode}}</v-card-text>
                </div>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        outlined
                        color="orange"
                        @click="getDetail(re.content_id, re.title)"
                    >
                        자세히보기
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-layout>
        </v-flex>
          <p style="text-align: center; margin-top:20px;" v-if="noNext">더 이상 항목이 없습니다.</p>
   
    </div>
  <app-my-modal
    :title="modaltitle"
    :visible.sync="modalVisible">
    <div>
      <v-timeline dense>
        <v-row
          v-for="(item, i) in modaldata"
          :key="i"
        >
          <v-timeline-item
            color="orange lighten-1"
            class="ml-3"
            :icon="getNumberIcon(i)"
          >
            <v-card
              color="amber lighten-4"
              style="margin:6px 6px;"
              light
              dense
              class="justify-center elevation-4"
            >
              <div class="d-flex flex-no-wrap justify-space-between">
                <v-layout col wrap align-center>
                <v-flex>
                <v-img
                  class="elevation-2"
                  width="300px"
                  height="200px"
                  v-if="item.subdetailimg === ''"
                  src="../assets/img/imageNotFound2.png">
                </v-img>
                <v-img
                  class="elevation-2"
                  width="300px"
                  height="200px"
                  v-else
                  :src="item.subdetailimg">
                </v-img>
                </v-flex>
                <v-flex>
                <v-layout row>
                <v-flex>
                <v-card-title
                  v-text="item.subname"
                  class="font-weight-bold grey--text text--darken-3"
                  size="10"
                ></v-card-title>
                </v-flex>
                <v-flex>
                <v-card-text
                  v-html="item.subdetailoverview" style="font-size:18px;">
                </v-card-text>
                </v-flex>
                </v-layout>
                </v-flex>
                </v-layout>
              </div>
            </v-card>
          </v-timeline-item>
        </v-row>
      </v-timeline>
    </div>
  </app-my-modal>
 </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";
import axios from "axios"
import Modal from '../components/Modal'

const resourceHost = process.env.VUE_APP_BACK_URL;
export default {
  components:{
    appMyModal:Modal
  },
  data: () => ({
    loading: true,
    areacode:'',
    noNext:false,
    regions:[
      {region:'전체', areacode:''},
      {region:'서울', areacode:'서울'},
      {region:'인천', areacode:'인천'},
      {region:'대전', areacode:'대전'},
      {region:'대구', areacode:'대구'},
      {region:'광주', areacode:'광주'},
      {region:'부산', areacode:'부산'},
      {region:'울산', areacode:'울산'},
      {region:'세종', areacode:'세종'},
      {region:'경기', areacode:'경기'},
      {region:'강원', areacode:'강원'},
      {region:'충북', areacode:'충북'},
      {region:'충남', areacode:'충남'},
      {region:'경북', areacode:'경북'},
      {region:'경남', areacode:'경남'},
      {region:'전북', areacode:'전북'},
      {region:'전남', areacode:'전남'},
      {region:'제주', areacode:'제주'},
    ],
    recom:[],
    modalVisible:false,
    modaldata:[],
    modaltitle:"",
    numberIcon:["mdi-numeric-1",
                "mdi-numeric-2",
                "mdi-numeric-3",
                "mdi-numeric-4",
                "mdi-numeric-5",
                "mdi-numeric-6",
                "mdi-numeric-7",
                "mdi-numeric-8",
                "mdi-numeric-9",
                "mdi-numeric-9-plus"
                ],
  }),
  computed: {
    ...mapState({
      userData : state => state.userData,
      recommends: state => state.data.recommendSearchList,
      page: state => state.data.recommendSearchPage
    }) 
  },
   mounted(){
    this.init();
  },
   destroyed(){
    this.init();
  },
  methods: {
    ...mapActions("data", ["getRecommends","setInitRecommand"]),
    onSubmit: async function() {
    const params = {
      areacode: this.areacode,
      page: 1,
      append: false
    };
    this.noNext=false
    await this.getRecommends(params);
    this.loading = false;
  },
  init: async function(){
    this.setInitRecommand();
    
  },
  async init2(){

  },
  addCart: async function(contentid){
    if(this.userData!=null){
      axios.post(`${resourceHost}api/`)
    }
  },
    loadMore: async function() {
      this.loading = true;
      if(this.page == 0 ){
        this.loading = false
        this.noNext = true
        return
      }else{
      const params = {
        areacode: this.areacode,
        page: this.page,
        append: true
      };
      await this.getRecommends(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
      }
    },
    getDetail(contentid, title){
      axios
        .get(`${resourceHost}api/recommandspots`, {params:{contentid:contentid}})
        .then(
          ({ data }) => {
            ((this.modaldata = data.results))
            console.log(this.modaldata)
          })
      
      this.modalVisible = !this.modalVisible
      this.modaltitle = title
    },
    getNumberIcon(i){
      if(i < 10){
        return this.numberIcon[i]
      }else{
        return this.numberIcon[9]
      }
    }
  },
};
</script>
<style scoped>
  .v-btn{
    font-size : 20px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
  .v-select {
    font-size : 20px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
   .v-select >>> .item{
    font-size : 25px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
</style>