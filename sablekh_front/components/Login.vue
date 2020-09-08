<template>
  <div class="login-component">
    <img src="@/assets/login/vector1.png" alt="loading image" class="mobile-view-img">
    <div class="login-wrapper1">
      <div class="login1-each login11">
        <img src="@/assets/login/login.png" alt="loading image" />
      </div>
      <div class="login1-each login12"> 
        <h1 class = "head1">Login</h1> 
        <div class="input-section"> 
          <div id = "errorBox" v-show="hasError" ><p id = "errorTxt"> {{error}}<img src = "@/assets/cancel.png" @click="hasError =!hasError" class = "cancelError"></p></div>
          <label for="email">E-mail</label> 
          <input type="email" v-model="email" id="email" autofocus /> 
          <label for="password">Password</label>
          <input @keyup.enter="login_button" type="password" v-model="password" id="password" />
          <span class="forget-password">
            <NuxtLink to="forgot-password">Forgot password</NuxtLink>
          </span>
          <div class="remember-me-div">
            <input type="checkbox" v-model="remember" id="remember-me" />
            <span class="remember-me">Remember me</span>
          </div>
        </div>
        <button @click="login_button" class="btn login-button">{{btn_txt}}</button>
        <div class="dont-have-account">
          <NuxtLink to="/register">Don't have an Account</NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import CryptoJS from "crypto-js";
import { v4 as uuidv4 } from "uuid";

import { setCookie, getCookie } from "@/extras/cookie";

export default {

  data() {
    return {
      server_address: "http://104.248.39.254",
      email: "",
      password: "",
      remember: false,
      hasError: false,
      error: "",
      sending: false,
      btn_txt: "Log in",
      time: 0,
      link: "",
    }
  },

  methods: {
    login_button() {

      if (this.sending){
            this.show_error("Please wait, sending request.")
        }
      else if (!this.validate_email){
            this.show_error("Please enter correct email address.")
        }
      else if (!navigator.onLine){
            this.show_error("Please check your internet connection and try again.")
      }
        else if (!this.length_check) {
            this.show_error("Please make your password at least 8 character long.")
        }
        else {
          this.sending = true
          this.btn_txt = "Sending"
          axios({
            url: this.server_address + "/token",
            method: "post",
            headers: this.implicit_data(),
            data: {"email": this.email, "password": this.password}
          })
          .then(res => {
            // console.log(res.data)
            this.sending = true
            this.btn_txt = "Sending"
            var token = res.data.token
            if (token != undefined){
                window.localStorage.setItem("token", token)
                window.localStorage.setItem("email", this.email)
            }
            if (this.remember) {
              this.cookie_setter(token)
            }

            axios({
              url: this.server_address + "/users",
              method: 'get',
              headers: {
                ...this.implicit_data(),
                Authorization: "Token " + token
              }
            })
            .then(res => {
              window.localStorage.setItem("username", res.data.username)
              if (this.link) {
                window.location.replace("/library/" + this.link)
              }
              else {
                window.location.replace("/login")
              }
            })
          })
          .catch(err => {
            var data = err.response
            this.btn_txt = "Log In"
            this.sending = false
            if (data.status == 404) this.show_error("User with this email not found.")
            else if (data.status == 401) this.show_error("Email or password incorrect.")
            else this.show_error("Something went wrong, pease try again.")
          })
        }
      },

    cookie_setter(token) {
      var id = uuidv4();
      id = id.replace(/-/g, "")
      var enc = CryptoJS.AES.encrypt(token, id).toString();
      this.assembler(enc, id);
    },

    assembler(enc, id) {
      var assembled = `${enc}+${id}`
      setCookie("ikmrfs", assembled, 30)

    },

    disassembler(enc) {
      let some_list = enc.split("+")
      let cip = ""
      let key = some_list[some_list.length - 1]

      some_list.pop();

      cip = some_list.join("+")

      let bytes = CryptoJS.AES.decrypt(cip, key)

      return bytes.toString(CryptoJS.enc.Utf8);

    },
    show_error(errorTxt){
      this.hasError = true 
      this.error = errorTxt 
    },
    implicit_data(){
      var session_key = window.localStorage.getItem('session_key')
        if (!session_key){
            var letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
                session_key = ""
                for (var i = 0; i<50; i++) {
                    session_key += letters.charAt(Math.round(Math.random()*letters.length))
            }
            window.localStorage.setItem("session_key", session_key)
        }
          return { "site": document.referrer+"---"+session_key, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
      }
  },

  mounted() {

      var enc = getCookie("ikmrfs")

      if (window.localStorage.getItem('token')) {
        window.location.replace("/")
      }
      else if (enc != "") {
        let token = this.disassembler(enc)
        window.localStorage.setItem("token", token)

        window.location.replace("/")
      }

      this.link = window.localStorage.getItem("link_str")

      this.time = new Date().getTime()
  },

  computed: {
    length_check() {
        return this.password.length > 7 ? true : false ;
    },
    validate_email(){
      const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(String(this.email).toLowerCase());
    }
},
}

</script>

<style scoped>

.login-component {
  min-height: 100vh;
  max-width: 100vw;
  background-color: rgb(254, 227, 200);
  color: rgb(82, 71, 62);
  position: relative;
  overflow: hidden;
}
.mobile-view-img {
  display: none;
  position: absolute;
  top: 10vh;
  right: -50px;
  opacity: 50%;
  z-index: 5;
}
.login-wrapper1 {
  position: relative;
  z-index: 10;
  display: grid;
  grid-template-columns: 60% 40%;
}
.login11 > img {
  width: 75%;
}
.login12 {
  margin: 10% 10% 0 10%;
}
.login12 > h1 {
  font-weight: 200;
  text-align: center;
  margin-bottom: 20%;
}
.login12 > .input-section {
  display: flex;
  flex-direction: column;
  font-family: 'Rajdhani', sans-serif;
}
.login12 > .input-section > label {
  font-size: 130%;
  font-weight: 600;
}

.login12 > .input-section > input {
  font-size: 110%;
  margin: 20px 0;
  padding: 10px 10px;
  letter-spacing: 1px;
  border: 1px solid rgb(82, 71, 62);
  border-radius: 5px;
  outline: none;
  background: none;
}

.login-button{
  cursor: pointer;
  font-size: 150%;
  letter-spacing: .8px;
  background-color: rgb(40, 43, 42);
  color: rgb(255, 239, 223);
  border-radius: 5px;
  margin-top: 5vh;
  font-family: 'Rajdhani', sans-serif;
}

.forget-password {
  text-align: right;
}

  .dont-have-account {
    margin-top: 1vh;
      text-align: right;
      font-family: 'Comfortaa', cursive;
  }

  .dont-have-account:hover{
      font-weight: bolder;
  }

.head1{
  font-family: 'Staatliches', cursive;
  letter-spacing: 5px;
  font-size: 250%;
  }

#remember-me {
  position: relative;
  top: 4px;
  width: 20px;
  height: 20px;
}

.login-button {
  font-size: 18px;
  letter-spacing: 0.8px;
  background-color: rgb(40, 43, 42);
  color: rgb(255, 239, 223);
  border-radius: 5px;
  margin-top: 5vh;
}

#errorBox{
    background-color: rgba(255, 0, 0, 0.4);
    color: rgb(51, 47, 43);
    border: 1px black solid;
    border-radius: 5px;
    padding : 2%;
    font-size: 110%;
    font-family: 'Rajdhani', sans-serif;
    animation-name: fadein;
    animation: fadein 1s;
    margin: 2% 0 2% 0;
    font-weight: bold;
}

.cancelError{
    cursor: pointer;
    right: 0;
    float: right;
}

  @media screen and (max-width: 1200px){
      .login-wrapper1 {
          grid-template-columns: auto;
      }
      .login11{
        display: none;
      }
      .mobile-view-img {
        display: block;
      }

  }

  @media screen {
    
  }

</style>