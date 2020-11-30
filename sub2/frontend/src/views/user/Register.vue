<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="5">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Register form</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text> 
            <v-form v-model="valid">
            <v-layout >
               <v-text-field
                v-model="username"
                :rules="nameRules"
                :state="nameState"
                label="username (영문과 숫자로 이루어진 이름을 입력해주세요)"
                prepend-icon="mdi-account"
                type="text"
                required
              />
              <v-btn color="primary" @click="checkname(username)">중복확인</v-btn>
              </v-layout>
              <v-text-field
                v-model="user.email"
                :rules="emailRules"
                label="Email"
                prepend-icon="mdi-email"
                type="email"
                required
              />
              <v-text-field
                v-model="user.password"
                :rules="passwordRules"
                label="Password"
                prepend-icon="mdi-lock"
                type="password"
                required
              />
              <v-text-field
                v-model="password2"
                :rules="passwordCheckRules"
                label="PasswordCheck"
                prepend-icon="mdi-lock-check"
                type="password"
                required
              />
              <!-- <v-text-field
                v-model="user.nickname"
                label="nickname"
                prepend-icon="mdi-lock-check"
                type="text"
              /> -->
              <v-text-field
                v-model="user.bornyear"
                :rules="bornyearRules"
                label="bornyear"
                prepend-icon="mdi-cake"
                type="number"
                 required
              /> 
              <v-radio-group v-model="user.gender" row prepend-icon="mdi-gender-male-female"  required>
                <v-radio label="남" value="남"></v-radio>
                <v-radio label="여" value="여"></v-radio>
              </v-radio-group>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn color="primary" @click="onSubmit(user)">회원가입</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState, mapActions} from "vuex";
export default {
  data() {
    return {
      username: "",
      user:{
        username: "",
        email: "",
        password: "",
        nickname: "",
        gender: "",
        bornyear: ""
      },
      password2: "",
      msg: "",
      message:"",
      lenCheck: false,
      isCheck: false,
      ducheck: false,
      valid: false,
      nameRules: [
        v => !!v || '영문과 숫자로 이루어진 이름을 입력해주세요',
        v => v.length >= 6 || '이름은 6글자 이상 작성해 주세요!',
      
      ],
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+/.test(v) || 'E-mail 형식이 유효하지 않습니다!'
      ],
      passwordRules: [
        v => !!v || '비밀번호를 입력해주세요',
        v => !(v.length <= 8) || '비밀번호는 9자리 이상 입력해주세요!',
        v => !/^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^*+=-])$/.test(v) || '비밀번호가 유효하지 않습니다!',
      ],
      passwordCheckRules: [
        v => !!v || '비밀번호 확인을 입력해주세요',
        v => this.user.password != "" || "비밀번호를 확인해주세요" , 
        v => v == this.user.password || '비밀번호가 일치하지 않습니다!'
      ],
      bornyearRules: [
        v => !!v  ||  '4자리 숫자로 입력해주세요',
        v => (v.length == 4) ||  '4자리 숫자로 입력해주세요',
      ]
    };
  },
  computed:{
    nameState() {
      var nickType = /^[a-z|A-Z|0-9|*]+$/;
      var message =''
      if (this.lenCheck) {
        if (this.isChecked) {
          message =
            "username은 0~9까지의 숫자, 영문, 한글만으로 조합하여야 합니다.";
        } else {
           message = "이미 사용중인 username입니다.";
        }
      } else {
         message = "username은 2글자 이상 입력하셔야 합니다.";
      }
      return nickType.test(this.user.username) && this.lenCheck && this.isChecked 
        ? true
        : false;
    },
  },
  mounted(){
    this.$store.nameChecked = false
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
  methods: {
    ...mapActions(["DuCheck"]),
    onSubmit(user) {
      if(this.user.username == ''){
        msg = "사용자명을 입력해주세요!"
        this.Alert(msg)
      }else if(this.user.email == ''){
        msg = "이메일을 입력해주세요!"
        this.Alert(msg)
      }else if(this.user.password == ''){
        msg = "비밀번호를 입력해주세요!"
        this.Alert(msg)
      }else if(this.password2 == ''){
        var msg = "비밀번호확인을 입력해주세요!"
        this.Alert(msg)
      }else if(this.user.bornyear == ''){
         msg = "출생년도를 입력해주세요!"
        this.Alert(msg)
      }else if(this.user.gender == ''){
        msg = "성별을 선택해주세요!"
        this.Alert(msg)
      }
      if(this.user.password === this.password2){
        console.log("비번 일치!")
         this.$store
        .dispatch("REGISTER", user)
        .then(() => {
          console.log("회원가입 성공!!!")
          this.$router.push("/")
          })
        .catch(({ message }) => (this.msg = message));
      }else {
        console.log("비번 불일치!")
      }
        // REGISTER 액션 실행
     
    },
    Alert(msg){
        swal.fire({
            width: 400,
            icon: "warning",
            title:
              '<a style="font-size:20px; font-family: Recipekorea; color:black">'+ msg +'</a>',
            confirmButtonText:
              '<a style="font-size:20px; font-family: Recipekorea; color:black">확인</a>',
          })

    },
    checkname(username){
      if(this.lenCheck && this.isCheck){
          console.log("if")
          this.DuCheck(username)
      }else{
         swal.fire({
            width: 300,
            icon: "warning",
            title:
              '<a style="font-size:20px; font-family: Recipekorea; color:black">'+ this.message +'</a>',
            confirmButtonText:
              '<a style="font-size:20px; font-family: Recipekorea; color:black">확인</a>',
          })
      }
        
    },
    redirect() {
      const { search } = window.location;
      const tokens = search.replace(/^\?/, "").split("&");
      const { returnPath } = tokens.reduce((qs, tkn) => {
        const pair = tkn.split("=");
        qs[pair[0]] = decodeURIComponent(pair[1]);
        return qs;
      }, {});

      // 리다이렉트 처리
      this.$router.push(returnPath);
    },
  },
};
</script>
