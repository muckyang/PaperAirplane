import Vue from "vue";
import Vuex from "vuex";
import data from "./modules/data";
import app from "./modules/app";
import axios from "axios"

import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

// const resourceHost = "http://127.0.0.1:8000/"

const resourceHost = process.env.VUE_APP_BACK_URL;
const enhanceAccessToeken = () => {
  const {accessToken} = localStorage
  if (!accessToken) return
  axios.defaults.headers.common['Authorization'] = `Token ${accessToken}`;
}
enhanceAccessToeken()

export default new Vuex.Store({
  plugins: [
    createPersistedState({
      path:["index"],
    })
  ],
  state: {
    userData:{
      username : "",
      email : "",
      // nickname: "", 
      gender: "",
      bornyear: "" ,
    },
  
    nameChecked : "",
    accessToken: null,
  },
  getters: {
    isAuthenticated (state) {
      state.accessToken = state.accessToken || localStorage.accessToken
      return state.accessToken
    }
  },
  mutations: {
  
    LOGIN(state,accessToken ) {
      state.accessToken = accessToken
      // 토큰을 로컬 스토리지에 저장
      localStorage.accessToken = accessToken
    },
    LOGOUT(state) {
      state.accessToken = null
      state.userData = null
      delete localStorage.accessToken
    },
    REGISTER(state,data) {
      state.userData = data.user
    },
    DuCheck(state, bool){
      state.nameChecked = bool
    },
  },
  actions: {
    DuCheck( {commit}, username){
      axios
      .post(`${resourceHost}users/check/`, {username} )
      .then((response) => {
        if (response.data.message === "존재하는 username 입니다.") {
          commit("DuCheck", true);
          swal.fire({
            width: 300,
            icon: "warning",
            title:
              '<a style="font-size:20px; font-family: Recipekorea; color:black">존재하는 username 입니다.</a>',
            confirmButtonText:
              '<a style="font-size:20px; font-family: Recipekorea; color:black">확인</a>',
          })
        } else {
          commit("DuCheck", false);
          swal.fire({
            width: 300,
            icon: "success",
            title:
              '<a style="font-size:20px; font-family: Recipekorea; color:black">사용가능한 username 입니다.</a>',
            confirmButtonText:
              '<a style="font-size:20px; font-family: Recipekorea; color:black">확인</a>',
          })
        }
      })

    },
    LOGIN({ state, commit }, userData) {
      return axios
        .post(`${resourceHost}rest-auth/login/`, userData)
        .then(({data}) => {
          state.userData = userData
          state.userData.password = null
          commit('LOGIN', data.key)
          swal.fire({
            width: 300,
            icon: 'success',
            title: '로그인이 완료되었습니다.',
            showConfirmButton: false,
            timer: 1500
          })
          if(state.data.cartList.length != 0)
          axios.get(`${resourceHost}route/tempRead`, {params:{ username:state.userData.username }} )
          .then((data) =>{
            w:for(var i in data.data.results){
              for(var j in state.data.cartList){
                if(state.data.cartList[j].id == data.data.results[i].temp_typeid){
                  continue w
                }
              }
              var temp = data.data.results[i]
              var tempitem = []
              tempitem.id = temp.temp_typeid
              tempitem.lat = temp.temp_lat
              tempitem.lng = temp.temp_lon
              tempitem.title = temp.temp_title
              tempitem.type = temp.temp_type
              state.data.cartList.push(tempitem)
            }
            // 로그인시 vuex와 DB 동일하게 만듬  
            axios.delete(`${resourceHost}route/tempDelete`, {params: {username:state.userData.username }})
            .then(()=>{
              axios.post(`${resourceHost}route/tempCreate`,  {params:{username:state.userData.username , word:state.data.cartList }} )
              .then(()=>{
                console.log("DB modify")
              }).catch((err)=>{
                console.log("tempDB ERROR1")
              })
            }).catch((err)=>{
              console.log("tempDB ERROR2")
            })
          })
          .catch(()=>{
            console.log("err1")
          })
          // 모든 HTTP 요청 헤더에 Authorization 을 추가한다.
          axios.defaults.headers.common['Authorization'] = `Token ${data.key}`;
        }).catch((err)=>{
          console.log(err)
        })
    },
    LOGOUT({state, commit }) {
      swal.fire({
        width: 400,
        icon: "success",
        title:
          '<a style="font-size:20px; font-family: Recipekorea; color:black">로그아웃 완료되었습니다.</a>',
        confirmButtonText:
          '<a style="font-size:20px; font-family: Recipekorea; color:black">확인</a>',
      })

      state.data.rightcartList = []

      commit("LOGOUT")
    },
    REGISTER({ commit }, regiData) {
      return axios
        .post(`${resourceHost}users/register/`, regiData)
        .then(({data}) => {
          commit('REGISTER', data)
          swal.fire({
            width: 400,
            icon: "success",
            title:
              '<a style="font-size:20px; font-family: Recipekorea; color:black">회원가입이 완료되었습니다.</a>',
            confirmButtonText:
              '<a style="font-size:20px; font-family: Recipekorea; color:black">확인</a>',
          })
        })
       
    },
  },
  modules: {
    data,
    app
  }
});
