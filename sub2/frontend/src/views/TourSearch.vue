<template>
  <v-container fluid grid-list-xl>
    <v-layout col>
      <v-col cols="3">
        <v-btn
          class="mt-n3 ml-n3"
          outlined
          x-small
          fab
          style="position: fixed;"
          color="grey darken-2"
          @click="openinfo()"
        >
          <v-icon large>mdi-information-variant</v-icon>
        </v-btn>

        <v-sheet
          elevation="3"
          style="width:20%; position: fixed; top: 7%; left: 90px; "
          left
          absolute
          class="float-left"
        >
          <v-avatar
            class="elevation-4"
            color="orange"
          >
            <v-icon dark>mdi-earth</v-icon>
          </v-avatar>
          지역 선택
          <v-row justify="center" style="width:85%">
            <v-select
              v-model="searchRegion" 
              :items="regions"
              item-text="region"
              item-value="areacode"
              label="전체"
              solo
              style="left:25px; margin-top:10px; margin-bottom:-10px"
            /> 
          </v-row>
        </v-sheet>
        <v-sheet
          elevation="3"
          style="width:20%; position: fixed; top: 200px; left: 90px; "
          left
          absolute
          class="float-left pb-3"
        >
          <v-avatar
            class="elevation-4"
            color="orange"
          >
            <v-icon dark>mdi-basket-plus</v-icon>
          </v-avatar>
          장바구니
          <div
            class="scroll-t"
            style="overflow-x:hidden; overflow-y:auto; width:100%; height:230px; margin:0px; padding-bottom:10px"
          >
            <v-row justify="center">
              <v-flex>
                <v-col
                  v-for="(item, i) in items"
                  :key="i"
                >
                  <v-sheet
                    elevation="3"
                    :color="getColor(item.type)"
                    class="my-n3 mx-2"
                  >
                    <v-radio-group v-model="selected">
                      <v-radio
                        class="mb-n6 ml-1"
                        :label="item.title"
                        :value="i"
                        color="orange"
                        height="55px"
                        line-height="55px"
                        @change="getContentRecommend(item.id, item.type)"
                      />    
                    </v-radio-group>
                  </v-sheet>
                </v-col>
              </v-flex>
            </v-row>
          </div>
          <div>
            <v-btn class="mx-1 mb-n2" style="width:48%;" depressed small dark color="orange" @click="radioCheck()">선택 해제</v-btn>
            <v-btn class="mr-1 mb-n2" style="width:48%;" depressed small dark color="orange" @click="cartDelete()">선택 삭제</v-btn>
          </div>
        </v-sheet>
        <v-sheet
          elevation="3"
          style="width:20%; position: fixed; top: 530px; left: 90px; "
          left
          absolute
          class="float-left pb-3"
        >
          <v-avatar
            class="elevation-4"
            color="orange"
          >
            <v-icon dark>mdi-chart-box-outline</v-icon>
          </v-avatar>
          유사항목 추천
          <div
            class="scroll-t"
            style="overflow-x:hidden; overflow-y:auto; width:100%; height:210px; margin:0px; padding-bottom:10px"
          >
            <v-row justify="center">
              <v-flex>
                <v-col
                  v-for="(item, i) in contentRecommendItem"
                  :key="i"
                >
                  <v-sheet
                    elevation="2"
                    color="light-blue lighten-5"
                    class="my-n2 mx-2 ml-1 grey--text text--darken-2"
                    style="padding:1px"
                  >{{ item.title }}</v-sheet>
                </v-col>
              </v-flex>
            </v-row>
          </div>
        </v-sheet>
      </v-col>
      <v-col cols="9" style="margin-left:5%">    
        <div
          v-infinite-scroll="loadMore"
          infinite-scroll-disabled="loading"
          infinite-scroll-distance="10"
        >
          <v-layout justify-center wrap mt-5>
            <v-flex xs12 md10>
              <card title="관광지 검색">
                <!-- enter 입력시 새로고침 방지-->
                <v-form onsubmit="return false;">
                  <v-container py-0>
                    <v-layout wrap>
                      <v-flex xs12 md12>
                        <!-- 반응형 검색 -->
                        <!-- <v-text-field v-model="tourspotName" v-on:keyup="onSubmit" label="관광지 이름" /> -->
                        <!-- 반응형 검색 미적용-->
                        <v-text-field v-model="tourspotName" label="관광지 이름" />
                      </v-flex>
                      <v-flex xs12 text-center>
                        <v-btn
                          large
                          class="indigo white--text ma-5"
                          rounded
                          color="blue lighten-2"
                          @click="onSubmit"
                        >GO!</v-btn>
                      </v-flex>
                    </v-layout>
                  </v-container>
                </v-form>
              </card>
              <v-divider class="mx-4" />
            </v-flex>
            <v-flex xs12 md10>
              <v-row>
                <v-flex v-for="spot in tourspots" :key="spot.id" pa-4>
                  <v-sheet elevation="4" class="my-1 mr-n3 pa-1" max-width="430p" height="565px">
                    <div fill>
                      <v-btn icon color="blue lighten-2" x-small class="ma-2">
                        <v-icon v-if="isPick(spot.content_id, 'T')" large title="임시저장" @click="toggle(spot.content_id, spot.title, 'T', spot.mapy, spot.mapx)">mdi-star</v-icon>
                        <v-icon v-else title="임시저장" large @click="toggle(spot.content_id, spot.title, 'T', spot.mapy, spot.mapx)">mdi-star-outline</v-icon>
                      </v-btn>
                      <v-btn style="float:right" icon color="blue lighten-2" x-small class="ma-2" title="상세정보" @click="getDetail(spot.content_id, spot.title, spot.first_image)">
                        <v-icon large class="float-right">mdi-information-outline</v-icon>
                      </v-btn>
                    </div>
                    <spot-list-card
                      :id="spot.id"
                      :content_id="spot.content_id"
                      :name="spot.title"
                      :categories="spot.content_type_id"
                      :address="spot.addr1"
                      :tel="spot.tel"
                      :areacode="spot.areacode"
                      :image="spot.first_image"
                      :mapx="spot.mapx"
                      :mapy="spot.mapy"
                    />
                  </v-sheet>
                </v-flex>
              </v-row>
              <div v-if="inprogress" class="text-center mx-2">
                <v-progress-circular
                  :size="50"
                  :width="6"
                  color="purple"
                  indeterminate
                  class="mx-2"
                />
                <v-progress-circular
                  :width="3"
                  color="red"
                  indeterminate
                  class="mx-2"
                />
                <v-progress-circular
                  :size="70"
                  :width="10"
                  color="blue lighten-1"
                  indeterminate
                  class="mx-2"
                />
                <v-progress-circular
                  :width="3"
                  color="green"
                  indeterminate
                  class="mx-2"
                />
                <v-progress-circular
                  :size="50"
                  :width="6"
                  color="orange"
                  indeterminate
                  class="mx-2"
                />
              </div>
            </v-flex>
          </v-layout>
        </div>
      </v-col>
    </v-layout>
    <app-my-modal
      :title="modaltitle"
      :visible.sync="modalVisible"
    >
      <div>
        <v-img v-if="modaldata.image==null" class="align-center mx-1" max-width="99%" src="../assets/img/imageNotFound2.png" />
        <v-img v-else :src="modaldata.image" class="align-center mx-1" max-width="99%" />
        <v-card
          color="amber lighten-4"
          style="margin:6px 6px; padding-bottom:6px"
          light
          dense
          class="justify-center elevation-4"
        >
          <div class="d-flex flex-no-wrap justify-space-between">
            <v-layout col wrap align-center>
              <v-flex>
                <v-layout row>
                  <v-flex>
                    <v-card-title
                      class="font-weight-bold body-1 grey--text text--darken-3"
                      size="10"
                    >홈페이지</v-card-title>
                  </v-flex>
                  <v-flex>
                    <v-card-text class="mb-n5 black--text" v-html="modaldata.homepage" />
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
          </div>
        </v-card>
        <v-card
          color="amber lighten-4"
          style="margin:6px 6px; padding-bottom:6px"
          light
          dense
          class="justify-center elevation-4"
        >
          <div class="d-flex flex-no-wrap justify-space-between">
            <v-layout col wrap align-center>
              <v-flex>
                <v-layout row>
                  <v-flex>
                    <v-card-title
                      class="font-weight-bold body-1 grey--text text--darken-3"
                      size="10"
                    >상세 설명</v-card-title>
                  </v-flex>
                  <v-flex>
                    <v-card-text class="mb-n5 black--text" v-html="modaldata.overview" />
                  </v-flex>
                </v-layout>
              </v-flex>
            </v-layout>
          </div>
        </v-card>
         <p style="text-align: center; margin-top:20px;" v-if="noNext">더 이상 항목이 없습니다.</p>
   
      </div>
    </app-my-modal>
    <app-my-modal
      id="infoModal"
      title="맛집 검색 가이드"
      :visible.sync="infomodalVisible"
    >
      <div>
        <v-img
          src="../assets/img/toursearchinfo.png"
        />
      </div>
    </app-my-modal>
  </v-container>
</template>

<script>
import axios from "axios"
import Card from "@/components/Card";
import SpotListCard from "@/components/SpotListCard";
import { mapState, mapActions } from "vuex";
import Modal from '../components/Modal'
const resourceHost = process.env.VUE_APP_BACK_URL;
export default {
  components: {
    Card,
    SpotListCard,
    appMyModal:Modal,
  },
  data: () => ({
    tourspotName: "",
    loading: true,
    searchRegion:0,
    noNext: false,
    items: [],
    regions:[
      {region:'전체', areacode:'전체'},
      {region:'서울', areacode:'서울특별시'},
      {region:'인천', areacode:'인천광역시'},
      {region:'대전', areacode:'대전광역시'},
      {region:'대구', areacode:'대구광역시'},
      {region:'광주', areacode:'광주광역시'},
      {region:'부산', areacode:'부산광역시'},
      {region:'울산', areacode:'울산광역시'},
      {region:'세종', areacode:'세종특별자치시'},
      {region:'경기', areacode:'경기도'},
      {region:'강원', areacode:'강원도'},
      {region:'충북', areacode:'충청북도'},
      {region:'충남', areacode:'충청남도'},
      {region:'경북', areacode:'경상북도'},
      {region:'경남', areacode:'경상남도'},
      {region:'전북', areacode:'전라북도'},
      {region:'전남', areacode:'전라남도'},
      {region:'제주', areacode:'제주특별자치도'},
    ],
    selected:'',
    inprogress:false,
    modalVisible:false,
    modaldata:{},
    modaltitle:"",
    infomodalVisible:false,
    contentRecommendItem:[],
    colors:['amber lighten-5', 'light-blue lighten-5']
  }),
  computed: {
    ...mapState({
      tourspots: state => state.data.tourspotSearchList,
      page: state => state.data.tourspotSearchPage,
      cart: state => state.data.cartList,
    })
  },
  mounted(){
    this.init();
    this.items = this.cart
  },
  destroyed(){
    this.init();
  },
  methods: {
    ...mapActions("data", ["getTourspots","setInitTourspot", "setCart", "initCart"]),
    onSubmit: async function() {
      this.init();
      this.inprogress = true
      this.noNext = false
      var mapx = ''
      var mapy = ''
      if(this.searchRegion == 0){
        this.searchRegion = '전체'
      }
      if(this.selected.length != 0){
        mapx = this.items[this.selected].lng
        mapy = this.items[this.selected].lat
      }
      const params = {
        region: this.searchRegion,
        name: this.tourspotName,
        mapx: mapx,
        mapy: mapy,
        page: 1,
        append: false
      };
      await this.getTourspots(params);
      this.loading = false;
      this.inprogress = false
    },
    init: async function() {
      await this.setInitTourspot();
    },
    loadMore: async function() {
      this.inprogress = true
      this.loading = true;
      if(this.page == 0 ){
        this.loading = false
        this.noNext = true
        return
      }
      var mapx = ''
      var mapy = ''
      if(this.searchRegion == 0){
        this.searchRegion = '전체'
      }
      if(this.selected.length != 0){
        mapx = this.items[this.selected].lng
        mapy = this.items[this.selected].lat
      }
      const params = {
        region: this.searchRegion,
        name: this.tourspotName,
        mapx: mapx,
        mapy: mapy,
        page: this.page,
        append: true
      };
      await this.getTourspots(params);
      setTimeout(() => {
        this.loading = false;
      }, 1000);
      this.inprogress = false
    },
    isPick(id, type){
      for (var i in this.items){
        if(this.items[i].type==type && id == this.items[i].id){
          return true
        }
      }
      return false
    },
    toggle(content_id, name, type, lat, lng){
      for (var i in this.items){
        if(this.items[i].type==type && content_id == this.items[i].id){
          this.items.splice(i, 1);
          if(this.selected > i){
            this.selected = this.selected-1
          }else if(this.selected == i){
            this.selected = ''
          }
          this.setCart2()
          return
        }
      }
      this.items.push({id:content_id, title:name, type:type, lat:lat, lng:lng})
      this.setCart2()
    },
    radioCheck(){
      this.selected = ''
    },
    setCart2: async function() {
      await this.setCart(this.items);
    },
    cartDelete(){
      this.items.splice(this.selected, 1);
      this.selected = ''
      this.setCart2()
    },
    getDetail(contentid, title, image){
      axios
        .get(`${resourceHost}api/overviews`, {params: {contentid:contentid}})
        .then(
          ({ data }) => {
            if(data.count == 0){
              this.modaldata ={image:null, homepage:"정보가 없습니다.", overview:"정보가 없습니다."}
            }else{
              var overviewdata = data.results[0]
              this.modaldata ={image:image, homepage:overviewdata.homepage, overview:overviewdata.overview}
            }
          })
      this.modalVisible = !this.modalVisible
      this.modaltitle = title
    },
    getContentRecommend(id, type){
      if(type=='T'){
        axios
        .get(`${resourceHost}api/recommendAuto`, {params: {content_id:id}})
        .then(
          ({ data }) => {
            this.contentRecommendItem = data.results
              if(data.count == 0){
                this.contentRecommendItem = [{title:"추천 항목이 없습니다."}]
              }
          })
      }else{
        this.contentRecommendItem = [{title:"관광지 선택시에만 추천 항목이 있습니다."}]
      }
    },
    getColor(type){
      if(type == 'F'){
        return this.colors[0]
      }else{
        return this.colors[1]
      }
    },
    openinfo(){
      this.infomodalVisible = !this.infomodalVisible
    }
  }
};
</script>

<style>
.v-label{
  font-size:25px;
}  
.v-select {
    font-size : 20px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
   .v-select >>> .item{
    font-size : 25px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
  .v-text-field{
  font-size:25px;
}  
  div .v-btn{
  font-size:20px;
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