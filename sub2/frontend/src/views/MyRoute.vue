<template>
  <v-container>
    <div
      v-infinite-scroll="loadMore"
      infinite-scroll-disabled="loading"
      infinite-scroll-distance="10"
    >
      <v-flex>
        <v-layout row>
          <v-card
            v-for="route in routeList" :key="route.id"
            class="ma-1 pa-1"
            max-width="300"
            max-height="400"
          >
            <v-img
              v-if="route.img == undefined"
              class="white--text align-end"
              height="200px"
              width="290px"
              src="../assets/img/imageNotFound.png"
            />
            <v-img
              v-else
              class="white--text align-end"
              height="200px"
              width="290px"
              :src="route.img"
            />
            <div style="height:100px">
              <v-card-title v-if="route.title == null" class="font-weight-bold" style="font-size:1.2em">제목이 없습니다.</v-card-title>
              <v-card-title v-else class="font-weight-bold" style="font-size:1.2em">{{ route.title }}</v-card-title>
              <!-- <v-card-text class="font-weight-bold">조회수 : {{ route.click }}회</v-card-text> -->
            </div>
            <v-card-actions>
              <v-spacer />
              <v-btn
                outlined
                color="orange"
                text
                @click="getDetail(route.id, route.title)"
              >자세히보기
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-layout>
      </v-flex>
    <p style="text-align: center; margin-top:20px;" v-if="noNext">더 이상 항목이 없습니다.</p>
    </div>
    <app-my-modal
      :title="modaltitle"
      :visible.sync="modalVisible"
    >
      <div>
        <v-timeline dense>
          <v-row
            v-for="(item, i) in modaldata"
            :key="i"
          >
            <v-timeline-item
              :color="getIconColor(i)"
              class="ml-3"
              :icon="getNumberIcon(item.rdtype)"
              fill-dot
            >
              <v-card
                :color="getColor(i)"
                light
                class="justify-center elevation-4 px-2 ma-1"
              >
                <div class="d-flex justify-space-between">
                  <v-layout style="min-width:100%" col align-center >
                    <v-layout row style="width:100%">
                      <div style="min-width:100%">
                        <v-flex>
                          <v-img
                            v-if="item.rdimg === '' || item.rdimg== null"
                            class="elevation-2"
                            width="300px"
                            height="200px"
                            src="../assets/img/imageNotFound2.png"
                          />
                          <v-img
                            v-else
                            :src="item.rdimg"
                            class="elevation-2"
                            width="300px"
                            height="200px"
                          />
                        </v-flex>
                      </div>
                      <v-flex>
                        <v-flex>
                          <v-card-title
                            size="10"
                            class="font-weight-bold body-1 grey--text text--darken-3"
                            v-text="item.rdtitle"
                          />
                        </v-flex>
                        <v-flex>
                          <v-card-text
                            v-if="item.rdtype === 'T'"
                            v-html="item.rdoverview"
                            style="font-size:18px;"
                          ></v-card-text>
                          <v-card-text
                            v-else
                            v-html="getSplit(item.rdoverview)"
                            style="font-size:18px;"
                            ></v-card-text>
                        </v-flex>
                      </v-flex>
                    </v-layout>
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
    routeitems:[],
    routeView:[],
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
    modalVisible:false,
    modaldata:[],
    modaltitle:"",
    numberIcon:['mdi-eiffel-tower', 'mdi-rice'],
    colorPull: ['light-blue lighten-4','deep-orange lighten-4','green lighten-4','deep-purple lighten-4',],
    iconColorPull: ['indigo','deep-orange darken-1','green darken-1', 'deep-purple darken-1', ],
  }), 
    computed: {
    ...mapState({
      userData: state => state.userData,
      routeList: state => state.data.routeList,
      page: state => state.data.routePage
    }) 
  },
  mounted(){
    this.init()
  },
  destroyed(){
    this.clear();
  },

  methods : {
    ...mapActions("data", ["getRoutes","setInitRoutes","clearRoutes"]),
      onSubmit: async function() {
      const parameter = {
        areacode: this.areacode,
        page: 1,
        append: false
      };
      
      await this.getRoutes(parameter);
      this.loading = false;
    },
    
    init: async function(){
      await this.setInitRoutes();
      const params = {
        page: 1,
        append: false,        
        username : this.userData.username,
      };
      this.noNext =false
      await this.getRoutes(params);
      
      console.log(this.routeList)
      this.loading = false;
      this.inprogress = false
    },
    clear: async function(){
      await this.clearRoutes();
    },
    loadMore: async function() {
      this.loading = true;
        if(this.page == 0 ){
        this.loading = false
        this.noNext =true
      }else{
      const params = {
        page: this.page,
        append: true,
        username : this.userData.username,
      };
      await this.getRoutes(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
      }
    },
     getSplit(text){
      var answer = ""
      var list = []
      list = text.split("|")
      for(var k in list){
        answer += list[k]+"<br/>"
      }
      return answer
     },
    getDetail(contentid, title){
        console.log(contentid)
      axios
        .get(`${resourceHost}api/routeDetailRead`, {params:{routeid:contentid, username: this.userData.username}})
        .then( ( {data} ) => {
            (this.modaldata = data.results)
        })
      this.modalVisible = !this.modalVisible
      this.modaltitle = title
    },
      getNumberIcon(type){
      if(type=="T"){
        return this.numberIcon[0]
      }else{
        return this.numberIcon[1]
      }
    },getColor(i){
      var k = i%4
      return this.colorPull[k]
      
    },getIconColor(i){
      var k = i%4
      return this.iconColorPull[k]
      
    },

    
  },
}
</script>




