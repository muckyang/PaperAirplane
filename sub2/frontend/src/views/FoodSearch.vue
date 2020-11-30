<template>
  <v-container fluid grid-list-xl>
    <v-layout col >
      <v-col cols="3" >
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
            class="float-left">
            <v-avatar
              class="elevation-4"
              color="orange"
            >
              <v-icon dark>mdi-earth</v-icon>
            </v-avatar>
            지역 선택
          <v-row justify="center" style="width:85%">
              <v-select
              :items="regions"
              item-text="region"
              item-value="areacode"
              label="전체"
              solo
              style="left:25px; margin-top:10px; margin-bottom:-10px"
              v-model="searchRegion"
            >
            </v-select>
          </v-row>
          </v-sheet>
          <v-sheet
            elevation="3"
            style="width:20%; position: fixed; top: 200px; left: 90px; "
            left
            absolute
            class="float-left pb-3">
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
                    :label="item.title"
                    :value="i"
                    color="orange"
                    height="55px"
                    line-height="55px"
                    class="mb-n6 ml-1"
                    @change="getContentRecommend(item.id, item.type)"
                  ></v-radio>
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
          class="float-left pb-3">
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
                  color="orange lighten-5"
                  class="my-n2 mx-2 ml-1 grey--text text--darken-2"
                  style="padding:1px"
                  >{{item.store_name}}</v-sheet>
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
          <card title="맛집 검색">
            <!-- enter 입력시 새로고침 방지-->
            <v-form onsubmit="return false;">
              <v-container py-0>
                <v-layout wrap>
                  <v-flex xs12 md12>
                    <!-- 반응형 검색 -->
                    <!-- <v-text-field v-model="storeName" v-on:keyup="onSubmit" label="음식점 이름" /> -->
                     <v-text-field v-model="storeName" label="음식점 이름" />
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
          <v-flex v-for="store in stores" :key="store.id" pa-4>
            <v-sheet
              elevation="4"
              class="my-1 mr-n3 pa-1"
              height="350"
            >
              <div fill>
                  <v-btn icon color="blue lighten-2" x-small class="ma-2">
                    <v-icon large v-if="isPick(store.id, 'F')" @click="toggle(store.id, store.name, 'F', store.lat, store.lng)" title="임시저장">mdi-star</v-icon>
                    <v-icon large v-else @click="toggle(store.id, store.name, 'F', store.lat, store.lng)" title="임시저장">mdi-star-outline</v-icon>
                  </v-btn>
                  <v-btn style="float:right" icon color="blue lighten-2" x-small class="ma-2" title="상세정보" @click="getDetail(store.id, store.name, store.menus, store.bhours)">
                    <v-icon large class="float-right">mdi-information-outline</v-icon>
                  </v-btn>
              </div>
            <store-list-card
              :id="store.id"
              :name="store.name"
              :categories="store.categories"
              :address="store.address"
              :tel="store.tel"
              :lat="store.lat"
              :lng="store.lng"
            >
            </store-list-card>
            </v-sheet>
          </v-flex>
          </v-row>
          <div class="text-center mx-2" v-if="this.inprogress">
            <v-progress-circular
              :size="50"
              :width="6"
              color="purple"
              indeterminate
              class="mx-2"
            ></v-progress-circular>

            <v-progress-circular
              :width="3"
              color="red"
              indeterminate
              class="mx-2"
            ></v-progress-circular>

            <v-progress-circular
              :size="70"
              :width="10"
              color="blue lighten-1"
              indeterminate
              class="mx-2"
            ></v-progress-circular>

            <v-progress-circular
              :width="3"
              color="green"
              indeterminate
              class="mx-2"
            ></v-progress-circular>

            <v-progress-circular
              :size="50"
              :width="6"
              color="orange"
              indeterminate
              class="mx-2"
            ></v-progress-circular>
          </div>
        </v-flex>
      </v-layout>
    </div>
    </v-col>
    </v-layout>
  
  
      <app-my-modal
        :title="modaltitle"
        :visible.sync="modalVisible">
        <div>
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
              >메뉴</v-card-title>
              </v-flex>
              <v-flex>
                <v-card-text
                  v-for="(m, i) in modaldata.menu"
                  :key="i"
                  class="mb-n5 black--text"
                  v-text="m">
                </v-card-text>
              </v-flex>
              </v-layout>
              </v-flex>
              </v-layout>
            </div>
          </v-card>
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
              <v-layout row>
              <v-flex>
              <v-card-title
                class="font-weight-bold body-1 grey--text text--darken-3"
                size="10"
              >운영시간</v-card-title>
              </v-flex>
              <v-flex>
              <v-card-text
                v-for="(b, i) in modaldata.bhour"
                :key="i"
                class="mb-n5 black--text"
                v-text="b">
              </v-card-text>
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
        :visible.sync="infomodalVisible">
        <div>
          <v-img
            src="../assets/img/foodSearchInfo.png"
          ></v-img>
        </div>
      </app-my-modal>
  </v-container>
</template>

<script>
import Card from "@/components/Card";
import StoreListCard from "@/components/StoreListCard";
import { mapState, mapActions } from "vuex";
import Modal from '../components/Modal';
import axios from "axios";
const resourceHost = process.env.VUE_APP_BACK_URL;
export default {
  components: {
    Card,
    StoreListCard,
    appMyModal:Modal,
  },
  data: () => ({
    storeName: "",
    loading: true,
    searchRegion:0,
    items: [],
    noNext:false,
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
      stores: state => state.data.storeSearchList,
      page: state => state.data.storeSearchPage,
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
    ...mapActions("data", ["getStores","setInitStore", "setCart", "initCart"]),
    onSubmit: async function() {
      this.init();
      this.inprogress = true
      var lat = ''
      var lng = ''
      if(this.searchRegion == 0){
        this.searchRegion = '전체'
      }
      if(this.selected.length != 0){
        lat = this.items[this.selected].lat
        lng = this.items[this.selected].lng
      }
      const params = {
        region: this.searchRegion,
        name: this.storeName,
        lat: lat,
        lon: lng,
        page: 1,
        append: false
      };
      await this.getStores(params);
      this.loading = false;
      this.inprogress = false
    },
       init: async function() {
      await this.setInitStore();
    },
    loadMore: async function() {
      this.inprogress = true
      this.loading = true;
      if(this.page == 0 ){
        this.loading = false
        this.noNext= true
        return
      }
      var lat = ''
      var lng = ''
      if(this.searchRegion == 0){
        this.searchRegion = '전체'
      }
      if(this.selected.length != 0){
        lat = this.items[this.selected].lat
        lng = this.items[this.selected].lng
      }
      const params = {
        region: this.searchRegion,
        name: this.storeName,
        lat: lat,
        lon: lng,
        page: this.page,
        append: true
      };
      await this.getStores(params);
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
    toggle(id, name, type, lat, lng){
      for (var i in this.items){
        if(this.items[i].type==type && id == this.items[i].id){
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
      this.items.push({id:id, title:name, type:type, lat:lat, lng:lng})
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
    getDetail(contentid, title, menus, bhours){
      if(menus.length == 0){
        menus = ["정보가 없습니다!"]
      }
      if(bhours.length == 0){
        bhours = ["정보가 없습니다!"]
      }else{
        for(var i in bhours){
          var temp = String(bhours[i]).substring(1, bhours[i].length-1)
          var parse = temp.split(',')
          bhours[i] = parse
          var open = ""
          if(bhours[i][0] == "1"){
            open = open + "정상 운영 :"
          }else if(bhours[i][0] == "2"){
            open = open + "쉬는 시간 :"
          }else{
            open = open + "휴무일 :"
          }

          if(bhours[i][1] == "1"){
            open = open + "매주 "
          }else if(bhours[i][1] == "2"){
            open = open + "첫째주 "
          }else if(bhours[i][1] == "3"){
            open = open + "둘째주 "
          }else if(bhours[i][1] == "4"){
            open = open + "셋째주 "
          }else if(bhours[i][1] == "5"){
            open = open + "넷째주 "
          }else {
            open = open + "공휴일 "
          }

          if(bhours[i][2] == "1"){
            open = open + "월 "
          }
          if(bhours[i][3] == "1"){
            open = open + "화 "
          }
          if(bhours[i][4] == "1"){
            open = open + "수 "
          }
          if(bhours[i][5] == "1"){
            open = open + "목 "
          }
          if(bhours[i][6] == "1"){
            open = open + "금 "
          }
          if(bhours[i][7] == "1"){
            open = open + "토 "
          }
          if(bhours[i][8] == "1"){
            open = open + "일 "
          }

          if(bhours[i][0] == "1" || bhours[i][0] == "2"){
            open = open + " [" + bhours[i][9] + " ~ " + bhours[i][10] + "]"
          }

          open = open + bhours[i][11]
          bhours[i] = open
        }
      }
      this.modaldata = {menu:menus, bhour:bhours}
      this.modalVisible = !this.modalVisible
      this.modaltitle = title
    },
    getContentRecommend(contentid, type){
      if(type == 'F'){
        axios
          .get(`${resourceHost}api/topFiveStores`, {params: {storeid:contentid}})
          .then(
            ({ data }) => {
              this.contentRecommendItem = data.results
              if(data.count == 0){
                this.contentRecommendItem = [{store_name:"추천 항목이 없습니다."}]
              }
            })
      }else{
        this.contentRecommendItem = [{store_name:"음식점 선택시에만 추천 항목이 있습니다."}]
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
.v-text-field{
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
