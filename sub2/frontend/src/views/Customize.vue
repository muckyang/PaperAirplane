<template>
  <v-container class="mt-5">
    <v-flex>
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
      <v-layout row>
        <v-spacer />
        <v-sheet
          elevation="3"
          color="white"
          class="ml-9"
          height="350px"
        >
          <v-avatar
            class="elevation-4 mb-1"
            color="orange"
          >
            <v-icon dark>mdi-basket-plus</v-icon>
          </v-avatar>
          임시저장한 장소
          
          <div
            class="scroll-t"
            style="overflow-x:hidden; overflow-y:auto; width:230px; height:290px; margin:5px;"
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
                    height="50px"
                  >
                    <v-checkbox
                      v-model="selectedLeft" :label="item.title" :value="item.id"
                      color="orange"
                      light
                      dense
                      checked
                      height="42px"
                      line-height="42px"
                    />
                   
                  </v-sheet>
                </v-col>
              </v-flex>
            </v-row>
          </div>
        </v-sheet>
        <v-layout row class="align-center mx-3 justify-center">
          <div style="width:70px">
            <v-btn class="ml-4 mr-2 my-8" fab dark small color="orange darken-1" @click="goRight()">
              <v-icon dark x-large>mdi-arrow-right</v-icon>
            </v-btn>
            <v-btn class="ml-4 mr-2 my-8" fab dark small color="orange darken-1" @click="goLeft()">
              <v-icon dark x-large>mdi-arrow-left</v-icon>
            </v-btn>
          </div>
        </v-layout>
        <v-sheet
          elevation="3"
          color="white"
          class="ml-3 mr-1"
          height="350px"
        >
          <v-avatar class="elevation-4 mb-1" color="orange">
            <v-icon dark>mdi-basket-plus</v-icon>
          </v-avatar>
          경로 선택
          <div
            class="scroll-t"
            style="overflow-x:hidden; overflow-y:auto; width:230px; height:290px; margin:5px;"
          >
            <v-row justify="center">
              <v-flex>
                <v-col
                  v-for="(item, i) in selected_item"
                  :key="i"
                >
                  <v-sheet
                    elevation="3"
                    :color="getColor(item.type)"
                    class="my-n3 mx-2"
                    height="50px"
                  >
                    <v-checkbox v-model="selectedRight" color="orange" :label="item.title" :value="item.id" height="42px" light dense line-height="42px" />
                  </v-sheet>
                </v-col>
              </v-flex>
            </v-row>
          </div>
        </v-sheet>
        <v-sheet align="center" elevation="3" color="white" class="ml-1 mr-7" height="350px">
          <div class="scroll-t" style="overflow-x:hidden; overflow-y:auto; width:70px; height:290px; margin:5px;">
            <v-row justify="center">
              <v-flex>
                <v-btn class="mt-7 mb-2" fab dark color="orange darken-1" @click="NewCustom()">
                  <v-icon dark x-large>mdi-file-plus</v-icon>
                </v-btn>
                <v-btn class="mb-2" fab dark color="orange darken-1" @click="SaveCustom()">
                  <v-icon dark x-large>mdi-file-upload</v-icon>
                </v-btn>
                <v-btn class="mb-2" fab dark color="orange darken-1" @click="LoadCustom()">
                  <v-icon dark x-large>mdi-file-undo</v-icon>
                </v-btn>
                <v-btn class="mb-2" fab dark color="orange darken-1" @click="ClearCustom()">
                  <v-icon dark x-large>mdi-delete</v-icon>
                </v-btn>
              </v-flex>
            </v-row>
          </div>
        </v-sheet>
        <v-spacer />
      </v-layout>
      <v-sheet elevation="3" color="white" class="ml-3 mr-9 mt-7">
        <v-avatar
          class="elevation-4 mb-1 mr-2"
          color="blue lighten-1"
        >
          <v-icon dark>mdi-map</v-icon>
        </v-avatar>
        Map
        <v-sheet>
          <div id="map" style="height:700px;" />
        </v-sheet>
      </v-sheet>
    </v-flex>
    <app-my-modal
      id="infoModal"
      title="맛집 검색 가이드"
      style="z-index:1;"
      :visible.sync="infomodalVisible"
    >
      <div>
        <v-img
          src="../assets/img/customizeinfo.png"
        />
      </div>
    </app-my-modal>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";
import axios from "axios";
import Modal from '../components/Modal'
const resourceHost = process.env.VUE_APP_BACK_URL;
const APP_KEY = process.env.VUE_APP_KAKAO_APP_KEY;
export default {
  components: {
    appMyModal:Modal,
  },
  data: () => ({
    loading: true,
    selectedLeft:[],
    selectedRight:[],
    items: [],
    dbtemplist: [],
    selected_item:[],
    kakaomap :'',
    markers:[],
    infomodalVisible:false,
    colors:['amber lighten-5', 'light-blue lighten-5'],
    tourSpotIcon:['https://blog.kakaocdn.net/dn/SPQa4/btqKhkuCVb1/04h5vSI3DpW0uu07u7B941/img.png',
    'https://blog.kakaocdn.net/dn/pe3Gt/btqKibc7VPl/JMG0zmTTAZuBAegMSA2c9k/img.png',
    'https://blog.kakaocdn.net/dn/cohULe/btqKjdhw6FU/6b0kW79Yif93wNFlG70Am0/img.png',
    'https://blog.kakaocdn.net/dn/UGYLa/btqKibEadVP/UpOEGxKFkNDkZwjwKWxPQ1/img.png',
    'https://blog.kakaocdn.net/dn/bvf92J/btqKqyqRQ04/Fy5PFkKUKKdiHh51Is4NGK/img.png',
    'https://blog.kakaocdn.net/dn/bdmShR/btqKhkuCVbs/ojP7mziDENGz9Y6D5nD7ZK/img.png',
    'https://blog.kakaocdn.net/dn/bHpHqL/btqKhlf0cPd/9S1Is1yv0OdWbqZT0PwmEk/img.png',
    'https://blog.kakaocdn.net/dn/Hp8PE/btqKgE7VicQ/P6F4MkEdrvhsrmb6eKwlok/img.png',
    'https://blog.kakaocdn.net/dn/bUJbmS/btqKmoJiK44/ZvWMnrkwxUas06or7b7jkk/img.png',
    ],

    foodSpotIcon:['https://blog.kakaocdn.net/dn/s7zKy/btqKibqFGbn/KApKCa9pF76nuHWBU8ryQk/img.png',
    'https://blog.kakaocdn.net/dn/bkdFGn/btqKgFMxUtI/xPDP0p2kJT82l9sjULFMlk/img.png',
    'https://blog.kakaocdn.net/dn/HgH33/btqKhjJdgg2/A344bGg8RKWioQpX9QK7L1/img.png',
    'https://blog.kakaocdn.net/dn/BJMKZ/btqKkNQoqEk/E2kJ42ayb0D6f0Ryg1hNRk/img.png',
    'https://blog.kakaocdn.net/dn/bKLXIr/btqKgFyZfVE/kRSKk5hF2ToZBTHP2pFP61/img.png',
    'https://blog.kakaocdn.net/dn/bOv5TL/btqKlT3Qoj7/lPR9Vx061fTmy4vTAKY7OK/img.png',
    'https://blog.kakaocdn.net/dn/eHw9vf/btqKhj3AdbD/wjouln3abRXTomBgG2w2b1/img.png',
    'https://blog.kakaocdn.net/dn/bjYlVH/btqKlUhpx3U/zVBvKO21koI0vuKxDwjNI1/img.png',
    'https://blog.kakaocdn.net/dn/b1OFLG/btqKlUIti88/3pnbUkhaSyNawkxJdUEAKK/img.png',
    ],
  }),
  computed: {
    ...mapState({
      userData : state => state.userData,
      cart : state => state.data.cartList,
      rightcart : state =>state.data.rightcartList
    })
  },
  mounted(){
    if(this.userData == null || this.userData.username== ""){
        Swal.fire({
          title:'로그인이 필요합니다!!',
          width:'300px',
          icon:'error',
          showConfirmButton: false,
          timer: 800,
        })
       return this.$router.push("/login")
    }
    // console.log(this.userData)
    this.selected_item = this.rightcart
    this.items = this.cart
    this.dbtemplist = this.getTempDB(this.userData.username)
    for(var i=0 ; i<this.dbtemplist.length;i++){
      // var temp = this.dbtemplist[i]
      // var tempitem = []
      // tempitem.id = temp.temp_id
      this.items.push(this.dbtemplist[i])
    }
    
    if (window.kakao && window.kakao.maps&& map!= undefined) {
      this.initMap();
    } else {
      const script = document.createElement("script");
      script.onload = () => kakao.maps.load(this.initMap);
      script.src = `http://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${APP_KEY}&libraries=services`;
      document.head.appendChild(script);
    }
  },
  methods:{
    ...mapActions("data", ["getRightCart","setRightCart"]),
    async setCart(){
      await this.setRightCart(this.selected_item)
    },
    async getTempDB(username){
      axios.get(`${resourceHost}route/tempRead`, {params: {username:username}})
      .then((data)=>{
        return data  
      }).catch(()=>{
        return null
      })
    },
    async setTempDB(username,word){
      axios.delete(`${resourceHost}route/tempDelete`, {params: {username:username}})
      .then(()=>{
        axios.post(`${resourceHost}route/tempCreate`, {params:{username:username, word:word }} )
        .then(()=>{
          // console.log("DB modify")
        }).catch(()=>{
          // console.log("tempDB 1")
        })
      }).catch(()=>{
        // console.log("tempDB 2")
      })
    },
    NewCustom(){
      if(this.selected_item.length > 0){
        Swal.fire({
          title: '저장되지않은 내용이있습니다!',
          text: "기존내용을 삭제하시겠습니까??",
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: '네 삭제합니다.',
          cancelButtonText: '취소'
        }).then((result) => {
          if (result.isConfirmed) {
            this.selectedRight =[]
            this.selected_item=[]
            this.setCart()
            this.initMap()
            if(this.cart != undefined){
              this.setTempDB(this.userData.username,this.cart)
            }
            Swal.fire({
              title:'삭제완료!',
              width:'300px',
              icon:'success',
              showConfirmButton: false,
              timer: 1000,
            })
          }else{
            this.New_SaveCustom();
          }
        })
      }
    },
    openinfo(){
      this.infomodalVisible = !this.infomodalVisible
    },
    SaveCustom(){
      if(this.selected_item.length > 0){
        Swal.fire({
          title: '여행경로 이름을 입력해주세요!',
          icon: 'info',
          showCancelButton: true,
          showLoaderOnConfirm: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: '저장하기',
          cancelButtonText: '취소',
          input: 'text',
          inputAttributes: {
            autocapitalize: 'off'
          },
          preConfirm: (title) => {
            var titledupl = "" 
            return axios.post(`${resourceHost}api/titlecheck`, {title:title,username : this.userData.username})
            .then((data) =>{
                titledupl = data.data.message
                if(title == ''){
               Swal.showValidationMessage(
                "여행경로명을 입력해주세요"
              )}else if(titledupl === "존재하는 title 입니다."){
                 Swal.showValidationMessage(
                "이미 존재하는 경로명입니다."
                )}else{
                axios.post(`${resourceHost}api/routeCreate`, {params :{username : this.userData.username,title:title, list: this.selected_item}} )
                .then(() => {
                    Swal.fire({
                    title:'저장완료!',
                    width:'300px',
                    icon:'success',
                    showConfirmButton: false,
                    timer: 1000,
                  })
                })
              }

            })
            .catch(()=>{
            
            })
          },
          allowOutsideClick: () => !Swal.isLoading()
          }).then((result) => {
          if (result.isConfirmed) {
            // axios.post(`${resourceHost}route/Route`, {title, list} )
            //   .then((response) => {
            //     commit("DuCheck", true);
            //     Swal.fire({
            //     title:'저장완료!',
            //     width:'300px',
            //     icon:'success',
            //     showConfirmButton: false,
            //     timer: 1000,
            //   })
            // })
          }
        })
      }
    }, 
    New_SaveCustom(){
      if(this.selected_item.length > 0){
        Swal.fire({
          title: '여행경로 이름을 입력해주세요!',
          icon: 'info',
          showCancelButton: true,
          showLoaderOnConfirm: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: '저장하기',
          cancelButtonText: '취소',
          input: 'text',
          inputAttributes: {
            autocapitalize: 'off'
          },
          preConfirm: (title) => {
            var titledupl = "" 
            return axios.post(`${resourceHost}api/titlecheck`, {title:title,username : this.userData.username})
            .then(() =>{
                titledupl = data.data.message
                if(title == ''){
               Swal.showValidationMessage(
                "여행경로명을 입력해주세요"
              )}else if(titledupl === "존재하는 title 입니다."){
                 Swal.showValidationMessage(
                "이미 존재하는 경로명입니다."
                )}else{
                axios.post(`${resourceHost}api/routeCreate`, {params :{username : this.userData.username,title:title, list: this.selected_item}} )
                .then(() => {
                    Swal.fire({
                    title:'저장완료!',
                    width:'300px',
                    icon:'success',
                    showConfirmButton: false,
                    timer: 1000,
                  })
                  this.selected_item=[]
                  this.setCart()
                  this.initMap()
                })
              }
            })
            .catch(()=>{
            
            })
          },
          allowOutsideClick: () => !Swal.isLoading()
          }).then(() => {
          
        })
      }
    },
    async LoadCustom(){
      var list = [];
      var Options = {};
      axios.get(`${resourceHost}api/routeRead`, {params : {username : this.userData.username}})
      .then((data)=> {
          var res = data.data.results
          for(var n in res ){
            var obj = { id :res[n].route_id , data : res[n].route_title};
            list.push(obj)
          }
          for(var k = 0 ; k< list.length; k++){
            Options[list[k].id] = list[k].data
            // Options[k] = "["+list[k].id+"] "+list[k].data
          }

          const { value: course } = Swal.fire({
          title: '불러올 경로를 선택해주세요!',
          input: 'select',
          inputOptions: Options,
          inputPlaceholder: '선택',
          showCancelButton: true,
          inputValidator: (value) => {
            return new Promise((resolve) => {
              if (value === '') {
                resolve('땀땀')
              } else {
                axios.get(`${resourceHost}api/routeDetailRead`, {params : {username : this.userData.username,routeid:value}})
                .then((data) => {
                  var items = []
                  for(var k=0; k < data.data.results.length; k++){
                    var item = []
                    item.id = data.data.results[k].rdtypeid
                    item.title = data.data.results[k].rdtitle
                    item.type = data.data.results[k].rdtype
                    item.lat = data.data.results[k].rdlat
                    item.lng = data.data.results[k].rdlon
                    items.push(item)
                  }
                  this.selected_item = items
                  this.setCart()
                  this.initMap()

                }).catch(()=>{

                })
                resolve()
              }
            })
          }
        })
        if (course) {
          Swal.fire(`You selected: ${course}`)
        }
      }) 
    },
    ClearCustom(){
      Swal.fire({
        title: '저장되지 않은 내용이있습니다!',
        text: "기존내용을 삭제하시겠습니까??",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: '네 삭제합니다.',
        cancelButtonText: '취소'
      }).then((result) => {
        if (result.isConfirmed) {
          this.SaveCustom()
          this.selected_item= []
          this.setCart()
          this.setTempDB(this.userData.username,this.cart)
          Swal.fire(
            '삭제완료!',
            '삭제되었습니다.',
            'success'
          )
        }
      })
    },
    initMap() { 
      var container = document.getElementById('map'); 
      var selected_item2 = this.rightcart;
      var sumlat = 0;
      var sumlng = 0;
      var minlat = 0;
      var minlng = 0;
      var maxlat = 0;
      var maxlng = 0;
      var level = 0;
      var latlng = 0;
      
      //선택지 없을때 디폴트 값 
      if(selected_item2.length == 0){
        sumlat =36.450701;
        sumlng =127.570667;
        level = 17
        latlng = new kakao.maps.LatLng(sumlat,sumlng);
      
      }else{
        minlat = selected_item2[0].lat
        maxlat = selected_item2[0].lat
        minlng = selected_item2[0].lng
        maxlng = selected_item2[0].lng   
        for (var i in selected_item2){
          sumlat += selected_item2[i].lat
          sumlng += selected_item2[i].lng
          minlat = Math.min(minlat,selected_item2[i].lat)
          maxlat = Math.max(maxlat,selected_item2[i].lat)
          minlng = Math.min(minlng,selected_item2[i].lng)
          maxlng = Math.max(maxlng,selected_item2[i].lng)
        }
        var maxdiff = Math.round(Math.max((maxlat - minlat)*3,(maxlng - minlng)*1.5 ))
        level = 8 + maxdiff
        latlng = new kakao.maps.LatLng(sumlat/(selected_item2.length), sumlng/(selected_item2.length));
      }
      var options = { 
        // center: new kakao.maps.LatLng(36.450701, 127.570667), level: 16 
        center: latlng, level: level 
      }; 
      //마커추가하려면 객체를 아래와 같이 하나 만든다. 
      if(this.kakaomap ==''){
        this.kakaomap = new kakao.maps.Map(container, options);
      } else{
        this.kakaomap.setCenter(latlng)
        this.kakaomap.setLevel(level)
        for(var j =0; j< this.markers.length;j++){
            this.markers[j].setMap(null);
        }
        this.markers = []
      }
      for (var k in selected_item2){
      var imageSize = new kakao.maps.Size(55, 55);  
      var imageSrc = '';
      if(selected_item2[k].type=='T'){
        imageSrc = this.tourSpotIcon[k]
      }else{
        imageSrc = this.foodSpotIcon[k]
      }
      var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);
        var marker = new kakao.maps.Marker({
            map:  this.kakaomap, // 마커를 표시할 지도
            position: new kakao.maps.LatLng(selected_item2[k].lat, selected_item2[k].lng), // 마커를 표시할 위치
            text : selected_item2[k].title, 
            image : markerImage // 마커 이미지 
        });
        // marker.setImage(MarkerImage)
        // marker.setMap(this.kakaomap);
        this.markers.push(marker);
        var infowindow = new kakao.maps.InfoWindow({
          content: `<div fill align="center">`+selected_item2[k].title+`</div>`// 인포윈도우에 표시할 내용
        });

        // for문에서 클로저를 만들어 주지 않으면 마지막 마커에만 이벤트가 등록됩니다
        kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(this.kakaomap, marker, infowindow));
        kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow));
      }
      function makeOverListener(map, marker, infowindow) {
      return function() {
        infowindow.open(map, marker);
      };
    }

    // 인포윈도우를 닫는 클로저를 만드는 함수입니다 
    function makeOutListener(infowindow) {
      return function() {
          infowindow.close();
      };
    }
    },
    
    getColor(type){
      if(type == 'F'){
        return this.colors[0]
      }else{
        return this.colors[1]
      }
    },
    async goLeft(){
      for (var i in this.selectedRight){
        for (var item in this.selected_item){
          if(this.selectedRight[i] == this.selected_item[item].id){
            this.items.push(this.selected_item[item])
            const idx = this.selected_item.indexOf(this.selected_item[item])
            this.selected_item.splice(idx, 1);
          }
        }
      }
      await this.setRightCart(this.selected_item)
      this.initMap()
      // this.rightcart = this.selected_item
      this.selectedRight=[]
    },
    async goRight(){
      for (var i in this.selectedLeft){
        for (var item in this.items){
          if(this.selectedLeft[i] == this.items[item].id){
            this.selected_item.push(this.items[item])
            const idx = this.items.indexOf(this.items[item])
            this.items.splice(idx, 1);
          }
        }
      }
      this.selectedLeft=[]
      await this.setRightCart(this.selected_item)
      this.initMap() 
    }
  },

  // updated(){
  //   this.items = this.cart
  //   this.initMap();
  // },
};
</script>

<style>
.v-label{
  font-size:25px;
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