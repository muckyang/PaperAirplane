<template>
  <v-container
    class="fill-height"
    fluid
  >
    <v-row
      align="center"
      justify="center"
    >
      <v-col
        cols="12"
        sm="8"
        md="4"
      >
        <v-card class="elevation-12">
          <v-toolbar
            color="primary"
            dark
            flat
          >
            <v-toolbar-title>Login form</v-toolbar-title>
            <v-spacer />
          </v-toolbar>
          <v-card-text>
            <v-form>
              <v-text-field
                v-model="userData.username"
                label="Username"
                :rules="nameRules"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                required
              />
              <v-text-field
                v-model="userData.email"
                label="Email"
                :rules="emailRules"
                name="email"
                prepend-icon="mdi-email"
                type="text"
                required
              />
              <v-text-field
                v-model="userData.password"
                :rules="passwordRules"
                label="Password"
                name="password"
                prepend-icon="mdi-lock"
                type="password"
                required
              />
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" @click="goRegister()">회원가입</v-btn>
            <v-btn color="primary" @click="onSubmit(userData)">로그인</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios"
  export default {
    data() {
      return {
        userData:{
          username: "",
          email: "",
          password: "",
        },
        msg: "",
        valid: false,
      nameRules: [
        v => !!v || '이름을 입력해주세요!',
      ],
      emailRules: [
        v => !!v || 'E-mail을 입력해주새요',
        v => /.+@.+/.test(v) || 'E-mail 형식이 유효하지 않습니다!'
      ],
      passwordRules: [
        v => !!v || '비밀번호를 입력해주세요',
      ],
      }
    },
    methods: {
      goRegister(){
        this.$router.push("/register")
      },
      onSubmit(userData) {
        if(userData.username== ''){
           swal.fire({
                width: 300,
                icon: "warning",
                title:
                  '<a style="font-size:20px; font-family: Recipekorea; color:black">아이디 입력해주세요.</a>',
                confirmButtonText:
                  '<a style="font-size:20px; font-family: Recipekorea; color:black">확인</a>',
          })
          return
        }else if(userData.password== ''){
           swal.fire({
                width: 300,
                icon: "warning",
                title:
                  '<a style="font-size:20px; font-family: Recipekorea; color:black">비밀번호를 입력해주세요.</a>',
                confirmButtonText:
                  '<a style="font-size:20px; font-family: Recipekorea; color:black">확인</a>',
          })
          return
        }else if(userData.email== ''){
           swal.fire({
                width: 300,
                icon: "warning",
                title:
                  '<a style="font-size:20px; font-family: Recipekorea; color:black">이메일를 입력해주세요.</a>',
                confirmButtonText:
                  '<a style="font-size:20px; font-family: Recipekorea; color:black">확인</a>',
          })
          return
        }
        // LOGIN 액션 실행
        this.$store
          .dispatch("LOGIN", userData)
          .then(() => {
            if(axios.defaults.headers.common['Authorization'] == undefined || axios.defaults.headers.common['Authorization'] == '' ){
              swal.fire({
                width: 300,
                icon: "warning",
                title:
                  '<a style="font-size:20px; font-family: Recipekorea; color:black">아이디와 비밀번호를 확인해주세요.</a>',
                confirmButtonText:
                  '<a style="font-size:20px; font-family: Recipekorea; color:black">확인</a>',
              })
            }else{
              this.$router.push("/")
            }
            
          })
   
      },
      redirect() {
        const { search } = window.location
        // console.log(search)
        const tokens = search.replace(/^\?/, "").split("&")

        const { returnPath } = tokens.reduce((qs, tkn) => {
          const pair = tkn.split("=")
          qs[pair[0]] = decodeURIComponent(pair[1])
          return qs
        }, {})


        //둘다 필요없음!! 
        // this.$router.go()
        // this.$router.push("/")
         
      },
    },
  }
</script>