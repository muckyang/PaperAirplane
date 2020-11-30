<template>
  <v-container fill-height fluid grid-list-xl>
    <v-row
      align="center"
      justify="center"
    >
      <v-col
        cols="12"
        sm="8"
        md="4"
      >
        <v-layout justify-center wrap mt-5>
          <v-flex xs12>
            <card title="회원 정보" max-width="500px">
              <v-form>
                <v-container py-0>
                  <v-flex>
                    <v-layout>
                      <v-text-field
                        v-model="username"
                        label="User Name"
                        color="orange light-1"
                        outlined
                        shaped
                        class="mx-3"
                        prepend-icon="mdi-account"
                      />
                      <v-btn small class="ml-1 mr-3 my-2" width="100px" height="40px" color="primary" @click="checkname(username)"> 중복확인</v-btn>
                    </v-layout>
                  </v-flex>
                  <v-flex>
                    <v-text-field
                      v-model="email"
                      label="Email"
                      color="orange light-1"
                      outlined
                      readonly
                      shaped
                      class="my-n7"
                      prepend-icon="mdi-email"
                    />
                  </v-flex>
                  <v-flex>
                    <v-text-field
                      v-model="bornyear"
                      label="출생 년도"
                      color="orange light-1"
                      outlined
                      readonly
                      shaped
                      prepend-icon="mdi-cake"
                    />
                  </v-flex>
                  <v-flex>
                    <v-radio-group
                      v-model="gender"
                      :mandatory="false"
                      readonly
                      row
                      class="my-n7"
                      prepend-icon="mdi-gender-male-female"
                    >
                      <v-radio label="남" value="남" color="orange lighten-1" />
                      <v-radio label="여" value="여" color="orange lighten-1" />
                    </v-radio-group>
                  </v-flex>
                  <v-flex xs12 text-center>
                    <v-btn
                      class="indigo white--text ma-5"
                      rounded
                      color="blue lighten-1"
                      @click="modify"
                    >수정</v-btn>
                    <v-btn
                      class="indigo white--text ma-5"
                      rounded
                      color="blue lighten-1"
                      @click="withdraw"
                    >회원탈퇴</v-btn>
                  </v-flex>
                </v-container>
              </v-form>
            </card>
            <v-divider class="mx-4" />
          </v-flex>
        </v-layout>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios"
import Card from "@/components/Card";
import {mapActions} from "vuex";
const resourceHost = process.env.VUE_APP_BACK_URL;
  export default {
    components: {
      Card,
    },
    data() {
      return {
        user: null,
        accessLog: [],
        uid:"",
        msg:'',
        username: "",
        email: "",
        gender: "",
        bornyear: "",
        lenCheck: false,
        isCheck: false,
      }
    },
    
   
    computed:{
      nameState() {
        var nickType = /^[a-z|A-Z|0-9|*]+$/;
        if (this.lenCheck) {
          if (this.isChecked) {
            this.msg =
              "username은 0~9까지의 숫자, 영문, 한글만으로 조합하여야 합니다.";
          } else {
            this.msg = "이미 사용중인 username입니다.";
          }
        } else {
         this.msg = "username은 6글자 이상 입력하셔야 합니다.";
        }
        return nickType.test(this.user.username) && this.lenCheck && this.isChecked 
          ? true
          : false;
      },
    },
    watch: {
      username() { 
        var nickType = /^[a-z|A-Z|0-9|*]+$/;
        if (this.username.length >= 2) {
          this.user.username = this.username
          this.lenCheck = true
        }else{
          this.lenCheck = false
        }
        if(nickType.test(this.username)){
          this.isCheck = true
        }else {
          this.isCheck = false
        }
      },
    },
    created() {
        axios
        .get(`${resourceHost}users/user/`, {headers: {Authorization : 'Token ' + this.$store.getters.isAuthenticated}})
        .then(
          ({ data }) => {
            this.user = data
            this.uid = this.user.uid
            this.username = this.user.username
            this.email = this.user.email
            this.gender = this.user.gender
            this.bornyear = this.user.bornyear
          })
    },
     mounted(){
      this.$store.nameChecked = false
    },
    methods: {
      ...mapActions(["DuCheck"]),
      modify() {
        axios
        .put(`${resourceHost}users/update/`, {username:this.username})
        .then(()=>{
          swal.fire({
              width: 350,
              icon: "success",
              title:
                '<a style="font-size:20px; color:black">수정이 완료되었습니다.!</a>',
              confirmButtonText:
                '<a style="font-size:20px; color:black">확인</a>',
            })
        })
        this.$router.push("/home")
        .catch(()=>{
         })
      },
      withdraw() {
        url=`${resourceHost}users/delete/`+this.user.uid
        axios
        .delete(url)
        .then(
        )
        .catch(
        )
      },
      checkname(username){
        if(this.lenCheck && this.isCheck){
            this.DuCheck(username)
        }else{
          swal.fire({
              width: 300,
              icon: "warning",
              title:
                '<a style="font-size:20px; color:black">'+ this.msg +'</a>',
              confirmButtonText:
                '<a style="font-size:20px; color:black">확인</a>',
            })
        }
          
      },
    }
  }
</script>
<style scoped>
  .v-text-field , .v-card title{
    font-size : 20px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
   .v-text-field >>> label {
    font-size : 24px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
  .v-btn, .v-radio >>> label {
    font-size : 25px;
    font-family: 'Gamja Flower', 'Hi Melody', cursive;
  }
</style>