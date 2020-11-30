import api from "../../api";

// initial state
const state = {
  storeSearchList: [],
  storeSearchPage: "1",
  recommendSearchList: [],
  recommendSearchPage: "1",
  tourspotSearchList: [],
  tourspotSearchPage: "1",
  rankingList: [],
  rankingPage: "1",
  routeList: [],
  routePage: "1",
  
  cartList: [],
  rightcartList:[],
  // cart: {
  //   id: "",
  //   title: "",
  //   lat: 0.0,
  //   lng: 0.0,
  //   type: "",
  // },

  store: {
    id: "",
    name: "",
    branch: "",
    area: "",
    tel: "",
    address: "",
    lat: 0.0,
    lng: 0.0,
    categories: [],
    menus:[],
    bhours:[],
  },
  recommend: {
    id: "",
    addr1: "",
    addr2: "",
    areacode: "",
    cat1: "",
    cat2: "",
    cat3: "",
    content_id:0,
    content_type_id:0,
    first_image:"",
    first_image2:"",
    mapx:0.0,
    mapy:0.0,
    sigungucode:0,
    tel:"",
    title:"",
    readcount:0,
  },
  tourspot: {
    id: "",
    addr1: "",
    addr2: "",
    areacode: "",
    cat1: "",
    cat2: "",
    cat3: "",
    content_id:0,
    content_type_id:0,
    first_image:"",
    first_image2:"",
    mapx:0.0,
    mapy:0.0,
    sigungucode:0,
    tel:"",
    title:"",
    readcount:0,
  },
  ranking: {
    id: "",
    name: "",
    lat: 0.0,
    lng: 0.0,
  },
  route:{
    id: "",
    name: "",
    lat: 0.0,
    lng: 0.0,
  },
};

// actions
const actions = {
  async getStores({ commit }, params) {
    const append = params.append;
    const resp = await api.getStores(params);
    const stores = resp.data.results.map(d => ({
      id: d.id,
      name: d.store_name,
      branch: d.branch,
      area: d.area,
      tel: d.tel,
      address: d.address,
      lat: d.latitude,
      lng: d.longitude,
      categories: d.category_list,
      menus:d.menu_list,
      bhours:d.bhour_list,
    }));
    if (append) {
      commit("addStoreSearchList", stores);
    } else {
      commit("setStoreSearchList", stores);
    }
    if(resp.data.next == null){
      console.log(" There is no next page")
      commit("endStorePage");
    }else{
      commit("setStoreSearchPage", resp.data.next);
    }
  },

  async getRecommends( {commit} , params) {
    const append = params.append;
    const resp = await api.getRecommends(params);
    const recommends = resp.data.results.map(d => ({
      id:d.id,
      areacode: d.areacode,
      first_image2:d.first_image2,
      content_id:d.content_id,
      title:d.title,
    }));
    if (append) {
      commit("addRecommendSearchList", recommends);
    }else{
      commit("setRecommendSearchList", recommends);
    }

    if(resp.data.next == null){
      console.log(" There is no next page")
      commit("endRecommendPage");
    }else{
      commit("setRecommendSearchPage", resp.data.next);
    }
  },
 

  async getTourspots( {commit} , params) {
    const append = params.append;
    const resp = await api.getTourspots(params);
    const tourspots = resp.data.results.map(d => ({
      id:d.id,
      areacode: d.areacode,
      first_image:d.first_image,
      first_image2:d.first_image2,
      content_id:d.content_id,
      title:d.title,
      addr1: d.addr1,
      addr2: d.addr2,
      cat1: d.cat1,
      cat2: d.cat2,
      cat3: d.cat3,
      content_type_id:d.content_type_id,
      mapx:d.mapx,
      mapy:d.mapy,
      tel:d.tel,
      readcount:d.readcount,
    }));
    if (append) {
      commit("addTourspotSearchList", tourspots);
    }else{
      commit("setTourspotSearchList", tourspots);
    }

    if(resp.data.next == null){
      console.log(" There is no next page")
      commit("endTourspotPage");
    }else{
      commit("setTourspotSearchPage", resp.data.next);
    }
  },

  async getRankings({ commit }, params) {
    const append = params.append;
    const resp = await api.getRankings(params);

    const routes = resp.data.results.map(d => ({
      id: d.route_id,
      title: d.route_title,
      img : d.route_img,
      click : d.route_click,

    }));
    if (append) {
      commit("addRankingList", routes);
    } else {
      commit("setRankingList", routes);
    }
    if(resp.data.next == null){
      console.log(" There is no next page")
      commit("endRankingPage");
    }else{
      commit("setRankingPage", resp.data.next);
    }
  },
  async getRoutes({ commit }, params) {
    const append = params.append;
    const resp = await api.getMyRoute(params);
    const routes = resp.data.results.map(d => ({
      id: d.route_id,
      title: d.route_title,
      img : d.route_img,
      click : d.route_click,
 
    }));
    if (append) {
      commit("addRouteList",routes);
    } else {
      commit("setRouteList", routes);
    }
    if(resp.data.next == null){
      console.log(" There is no next page")
      commit("endRoutePage");
    }else{
      commit("setRoutePage", resp.data.next);
    }
  },
  async setInitRecommand({commit}){
    commit("setInitRecommand");
  },
  async setInitStore({commit}){
    commit("setInitStore");
  },
  async setInitTourspot({commit}){
    commit("setInitTourspot");
  },  
  async setInitRankings({commit}){
    commit("setInitRanking");// 비워줌
  },  
  async clearRankings({commit}){
    commit("setInitRanking"); // 비워줌
  
  },
  async setInitRoutes({commit}){
    commit("setInitRoute");// 비워줌
  },  
  async clearRoutes({commit}){
    commit("setInitRoute"); // 비워줌
  },
  async setCart({commit}, params){
    const items = params.map(d => ({
      id: d.id,
      title: d.title,
      lat: d.lat,
      lng: d.lng,
      type: d.type,
    }));
    commit("setCart", items);
  },
  async setRightCart({commit}, params){
    const items = params.map(d => ({
      id: d.id,
      title: d.title,
      lat: d.lat,
      lng: d.lng,
      type: d.type,
    }));
    commit("setRightCart", items);
  },
  
  async initCart({commit}){
    commit("initCart");
    //임시저장 목록 초기화하기
  },
};

// mutations
const mutations = {
  setInitStore(state ){
    state.storeSearchList = [];
  },
  setInitRecommand(state ){
    state.recommendSearchList = [];
  },
  setInitTourspot(state ){
    state.tourspotSearchList = [];
  },
  setInitRanking(state){
    state.rankingList = [];
  },
  setInitRoute(state){
    state.routeList = [];
  },
  setStoreSearchList(state, stores) {
    state.storeSearchList = stores.map(s => s);
  },
  addStoreSearchList(state, stores) {
    state.storeSearchList = state.storeSearchList.concat(stores);
  },
  setStoreSearchPage(state, url) {
    state.storeSearchPage = new URL(url).searchParams.get("page");
  },
  endStorePage(state) {
    state.storeSearchPage = 0;
  },
  setRecommendSearchList(state, recommends) {
    state.recommendSearchList = recommends.map(s => s);
  },
  addRecommendSearchList(state, recommends) {
    state.recommendSearchList = state.recommendSearchList.concat(recommends);
  },
  setRecommendSearchPage(state, url) {
    state.recommendSearchPage = new URL(url).searchParams.get("page");
  },
  endRecommendPage(state) {
    state.recommendSearchPage = 0;
  },
  setTourspotSearchList(state, tourspots) {
    state.tourspotSearchList = tourspots.map(s => s);

  },
  addTourspotSearchList(state, tourspots) {
    state.tourspotSearchList = state.tourspotSearchList.concat(tourspots);
  },
  setTourspotSearchPage(state, url) {
    state.tourspotSearchPage = new URL(url).searchParams.get("page");
  }, 
  endTourspotPage(state) {
    state.tourspotSearchPage = 0;
  },
  setRankingList(state, rankings) {
    state.rankingList = rankings.map(s => s);
  },
  addRankingList(state, rankings) {
    state.rankingList = state.rankingList.concat(rankings);
  },
  setRankingPage(state, url) {
    state.rankingPage = new URL(url).searchParams.get("page");
  },
  endRankingPage(state) {
    state.rankingPage = 0;
  },
  setRouteList(state, routes) {
    state.routeList = routes.map(s => s);
  },
  addRouteList(state, routes) {
    state.routeList = state.routeList.concat(routes);
  },
  setRoutePage(state, url) {
    state.routePage = new URL(url).searchParams.get("page");
  },
  endRoutePage(state) {
    state.routePage = 0;
  },

  setCart(state, items)  {
    state.cartList = items.map(s => s);
  },
  setRightCart(state, items)  {
    state.rightcartList = items.map(s => s);
  },
  initCart(state)  {
    state.cartList = [];
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations
};
