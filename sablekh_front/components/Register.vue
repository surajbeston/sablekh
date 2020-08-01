<template>
    <div class="register-component mxw-100-mnh-100">
        <div class="register-wrapper1">
            <div class="register1-each register11">
                <img src="@/assets/register/create_account.png" alt="loading image">
            </div>
            <div class="register1-each register12">
                <h1>Create an Account</h1>
                <div class="input-section">
                    <label for="email">E-mail</label>
                    <input type="email" v-model="email" id="email" autofocus>
                    <label for="password">Password</label>
                    <input type="password" v-model="password1" id="password1">
                    <label for="confirm password">Confirm Password</label>
                    <input @keyup.enter="create_button" type="password" v-model="password2" id="password2">
                    <span class="none" id="different-password" style="color:red;">Passwords aren't same</span>
                    <span class="none" id="length-error" style="color:red;">Password should be at least 4 character long</span>
                </div>
                <button @click="create_button" class="btn create-button">Create</button>
                <div class="already-have-account">
                    <NuxtLink to="/login">Already have an Account ?</NuxtLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import axios from "axios";

import {getCookie} from "@/extras/cookie"

export default {

  data() {
    return {
        server_address: "http://164.90.217.64",
        email: "",
        password1: "",
        password2: "",
    }
  },

  methods: {
      create_button() {
          document.getElementById("different-password").setAttribute("class", "none")
          document.getElementById("length-error").setAttribute("class", "none")

          if (!this.similarity_check) {
              document.getElementById("different-password").setAttribute("class", "")
          }
          else if (!this.length_check) {
              document.getElementById("length-error").setAttribute("class", "")
          }

          else {
              axios.post(`${this.server_address}/users`, {
                  email: this.email,
                  password: this.password1
              })
              .then(res => {
                  console.log(res)
                  window.location.replace("/login")
              })
              .catch(err => {
                  console.log(err)
                  alert("some error please try again later!")
              })
          }
      },
      
  },

  computed: {
      similarity_check() {
          return this.password1 === this.password2 ? true : false ;
      },
      length_check() {
          return this.password1.length > 4 ? true : false ;
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
  },



}

</script>

<style scoped>
    .register-component {
        background-color: rgb(254.0, 227, 200);
        color: rgb(82, 71, 62);
        padding-bottom: 2vh;
    }
    .register-wrapper1 {
        width:100%;
        display: grid;
        grid-template-columns: 58% 42%;
    }
    .register11 > img {
        width: 100%;
    }
    .register12 {
        margin: 10% 10% 0 10%;
    }
    .register12 > h1 {
        font-weight: 200;
        font-size: 35px;
        text-align: center;
        margin-bottom: 5vh;
    }
    .register12 > .input-section {
        display: flex;
        flex-direction: column;
    }
    .register12 > .input-section > label {
        font-size: 18px;
        font-weight: 600;
    }
    .register12 > .input-section > input {
        font-size: 18px;
        margin: 20px 0;
        padding: 10px 10px;
        letter-spacing: 1px;
        border: 1px solid rgb(82, 71, 62);
        border-radius: 5px;
        outline: none;
        background: none;
    }
    .create-button {
        font-size: 18px;
        letter-spacing: .8px;
        background-color: rgb(40, 43, 42);
        color: rgb(255, 239, 223);
        border-radius: 5px;
        margin-top: 5vh;
    }
    .already-have-account {
        text-align: right;
    }

    @media screen and (max-width: 1500px){
        .register11 {
            margin-top: 10%;
        }
    }

    @media screen and (max-width: 1300px){
        .register-wrapper1 {
            grid-template-columns: auto;
        }
    }
    

</style>