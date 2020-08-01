<template>
  <div class="login-component">
    <div class="login-wrapper1">
      <div class="login1-each login11">
        <img src="@/assets/login/login.png" alt="loading image" />
      </div>
      <div class="login1-each login12">
        <h1>Login</h1>
        <div class="input-section">
          <label for="email">E-mail</label>
          <input type="email" v-model="email" id="email" autofocus />
          <label for="password">Password</label>
          <input @keyup.enter="login_button" type="password" v-model="password" id="password" />
          <span class="forget-password">
            <a href="#">Forget password ?</a>
          </span>
          <div class="remember-me-div">
            <input type="checkbox" v-model="remember" id="remember-me" />
            <span class="remember-me">Remember me</span>
          </div>
        </div>
        <button @click="login_button" class="btn login-button">Log in</button>
        <div class="dont-have-account">
          <NuxtLink to="/register">Don't have an Account ?</NuxtLink>
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
      server_address: "http://164.90.217.64",
      email: "",
      password: "",
      remember: false,
    }
  },

  methods: {
    login_button() {
      axios.post(`${this.server_address}/token`,{
        email: this.email,
        password: this.password
      })
      .then(res => {
        var token = res.data.token
        window.localStorage.setItem("token", token)

        if (this.remember) {
          this.cookie_setter(token)
        }
        window.location.replace("/login")
      })
      .catch(err => console.log(err))
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
      
  }


}

</script>

<style scoped>

.login-component {
  min-height: 100vh;
  max-width: 100vw;
  background-color: rgb(254, 227, 200);
  color: rgb(82, 71, 62);
}
.login-wrapper1 {
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
  font-size: 35px;
  text-align: center;
  margin-bottom: 5vh;
}
.login12 > .input-section {
  display: flex;
  flex-direction: column;
}
.login12 > .input-section > label {
  font-size: 18px;
  font-weight: 600;
}
.login12 > .input-section > input {
  font-size: 18px;
  margin: 20px 0;
  padding: 10px 10px;
  letter-spacing: 1px;
  border: 1px solid rgb(82, 71, 62);
  border-radius: 5px;
  outline: none;
  background: none;
}

.forget-password {
  text-align: right;
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
.dont-have-account {
  text-align: right;
}

</style>