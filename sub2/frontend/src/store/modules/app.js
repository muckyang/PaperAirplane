import { set, toggle } from "@/utils/vuex";

const state = {
  drawer: null
};

// mutations
const mutations = {
  setDrawer: set("drawer"),
};

export default {
  namespaced: true,
  state,
  mutations
};
