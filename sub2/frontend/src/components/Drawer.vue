<template>
  <v-navigation-drawer
    id="app-drawer"
    app
    dark
    floating
    permanent
    mobile-break-point="900"
    width="250"
    expand-on-hover
    style="background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.8)), url(&quot;https://demos.creative-tim.com/material-dashboard/assets/img/sidebar-1.jpg&quot;); background-position: center center;"
  >
    <v-layout column>
      <v-list rounded>
        <div v-if="this.$store.getters.isAuthenticated==null">
          <v-list-item
            :to="items[1].to"
            active-class="blue lighten-1 white--text"
            class="v-list-item ma-3"
          >
            <v-list-item-icon>
              <v-icon>{{ items[1].icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title style="font-size:18px">{{ items[1].text }}</v-list-item-title>
          </v-list-item>
        </div>
        <div v-else>
          <v-list-item
            :to="items[0].to"
            active-class="blue lighten-1 white--text"
            class="v-list-item ma-3"
          >
            <v-list-item-avatar color="orange lighten-1">
              <span class="white--text">{{ geticon() }}</span>
            </v-list-item-avatar>
            <v-list-item-title style="font-size:18px">{{ items[0].text }}</v-list-item-title>
          </v-list-item>
          <v-list-item 
          :to="items[2].to"
          active-class="blue lighten-1 white--text"
            class="v-list-item ma-3">
                 <v-list-item-avatar >
              <v-icon>{{ items[2].icon }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-title style="font-size:18px">{{ items[2].text }}</v-list-item-title>
          </v-list-item>
          <v-btn text small @click="logout()" style="font-size:18px">Logout</v-btn>
        </div>
        <v-divider />
        
        <v-list-item
          v-for="(link, i) in links"
          :key="i"
          :to="link.to"
          active-class="blue lighten-1 white--text"
          class="v-list-item ma-3"
        >
          <v-list-item-action>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-title v-text="link.text" style="font-size:18px"/>
        </v-list-item>
        <v-list-group
          no-action
          prepend-icon="mdi-map-search"
          value="true"
        >
          <template v-slot:activator>
            <v-list-item-content>
              <v-list-item-title style="font-size:18px">검색</v-list-item-title>
            </v-list-item-content>
          </template>

          <v-list-item
            v-for="(admin, i) in admins"
            :key="i"
            :to="admin[2]"
            link
            active-class="blue lighten-1 white--text"
          >
            <v-list-item-icon>
              <v-icon v-text="admin[1]" />
            </v-list-item-icon>
            <v-list-item-title style="font-size:18px" v-text="admin[0]" />
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-layout>
  </v-navigation-drawer>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import axios from "axios"

const resourceHost = process.env.VUE_APP_BACK_URL;
export default {
  props: {
    opened: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    links: [
      {
        to: "/",
        icon: "mdi-home",
        text: "Home"
      },
      {
        to: "/customize",
        icon: "mdi-map-marker-distance",
        text: "나만의 코스"
      },
      {
        to: "/rank",
        icon: "mdi-trophy",
        text: "인기 커스텀 코스"
      }, 
      {
        to: "/recommend",
        icon: "mdi-transit-connection-variant",
        text: "추천 코스"
      },
      {
        to: "/info",
        icon: "mdi-magnify",
        text: "Info"
      }
    ],
    items:[
      { to: "/userinfo",
        text:"회원정보"
      },
      { to: "/login",
        icon: "mdi-account-circle",
        text: "Login"
      },
      { to: "/myroute",
        icon: "mdi-account-details-outline",
        text: "내 여행경로"
      },
    ],
    admins: [
      ['관광지', 'mdi-eiffel-tower', '/toursearch'],
        ['맛집', 'mdi-rice', '/foodsearch'],
      ],
      isLogin: null,
      username: '',
  }),
  computed: {
    ...mapState(["userData"] , "app", ["drawer"]),
  },

  created(){
    this.geticon()
  },
  
  mounted(){
    this.isLogin = this.$store.getters.isAuthenticated
  },

  methods: {
    ...mapMutations("app", ["setDrawer"]),

    logout(){
      this.$store
          .dispatch("LOGOUT")
          .then(() => {
            axios.defaults.headers.common['Authorization']=''
            this.redirect()
          })
          .catch(({ message }) => (this.msg = message))
    },
    redirect() {
        this.$router.push("/")
      },
      geticon(){
        if(this.$store.getters.isAuthenticated != null){
          axios
            .get(`${resourceHost}rest-auth/user/`, {headers: {Authorization : 'Token ' + this.$store.getters.isAuthenticated}})
            .then(
              ({ data }) => {
                ((this.username = data.username.substring(0,2)))
          })
           return this.userData.username.substring(0,2);
        }
        // return "";
      }
  }
};
</script>

<style>
#app-drawer{
  font-family: 'Gamja Flower', 'Hi Melody', cursive;
  font-size:1.5em;
  line-height: 0.7;
}
</style>