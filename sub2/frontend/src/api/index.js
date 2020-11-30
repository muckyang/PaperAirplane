import axios from "axios";

// const apiUrl = "http://127.0.0.1:8000/api";

const resourceHost = process.env.VUE_APP_BACK_URL;
export default {
  getStores(params) {
    return axios.get(`${resourceHost}api/recommendStores`, {
      params
    });
  },
  getRecommends(params) {
    return axios.get(`${resourceHost}api/courses`, {
      params
    });
  },
  getTourspots(params) {
    return axios.get(`${resourceHost}api/recommendTourSpot`, {
      params
    });
  },
  getRankings(params) {
    return axios.get(`${resourceHost}api/routeRankRead`, {
      params
    });
  },
  getMyRoute(params) {
    return axios.get(`${resourceHost}api/routeRead`, {
      params
    });
  }
};
