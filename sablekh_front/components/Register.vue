<template>
    <div class="register-component mxw-100-mnh-100">
        <div class="register-wrapper1">
            <div class="register1-each register11">
                <img src="@/assets/register/create_account.png" alt="loading image">
            </div>
            <div class = "community">
                <img src = "@/assets/logo1.png" id = "small-logo">
                <img src = "@/assets/register/community_half.png" id = "community" alt = "loading image">
            </div>
            <div class="register1-each register12">
                <h1 class = "head1">Create an Account</h1>
                <div class="input-section">
                    <label for="email">E-mail</label>
                    <input type="email" v-model="email" id="email" autofocus>
                    <label for="password">Password</label>
                    <input type="password" v-model="password1" id="password1">
                    <label for="confirm password">Confirm Password</label>
                    <input @keyup.enter="create_button" type="password" v-model="password2" id="password2">
                    <span class="warning" v-show= "same_password">Passwords don't match.</span>
                    <span class="warning" v-show= "small_password">Password should be at least 8 character long.</span>
                    <span class = "warning" v-show = "wrong_email">Enter correct email address.</span>
                </div>
                <button @click="create_button" class="btn create-button">Create</button>
                <div class="already-have-account">
                    <NuxtLink to="/login">Already have an account?</NuxtLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import axios  from "axios";

import {getCookie} from "@/extras/cookie"

export default {

  data() {
    return {
        server_address: "http://164.90.217.64",
        email: "",
        password1: "",
        password2: "",
        same_password: false,
        small_password: false,
        wrong_email: false
    }
  },

  methods: {
      create_button() {
        this.same_password = false
        this.small_password = false
        this.wrong_email = false

        console.log("shit")

        if (!this.validate_email){
            this.wrong_email = true
        }
        else if (!this.similarity_check) {
            this.same_password = true
        }
        else if (!this.length_check) {
            this.small_password = true
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
          return this.password1.length > 7 ? true : false ;
      },
      validate_email(){
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(this.email).toLowerCase());
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
        text-align: center;
        margin-bottom: 20%;
    }
    .input-section{
        font-family: 'Rajdhani', sans-serif;

    }
    .register12 > .input-section {
        display: flex;
        flex-direction: column;
    }
    .register12 > .input-section > label {
        font-size: 130%;
        font-weight: 600;
    }
    .register12 > .input-section > input {
        font-size: 110%;
        margin: 20px 0;
        padding: 10px 10px;
        letter-spacing: 1px;
        border: 1px solid rgb(82, 71, 62);
        border-radius: 5px;
        outline: none;
        background: none;
    }
    .create-button {
        font-size: 150%;
        letter-spacing: .8px;
        background-color: rgb(40, 43, 42);
        color: rgb(255, 239, 223);
        border-radius: 5px;
        margin-top: 5vh;
        font-family: 'Rajdhani', sans-serif;
    }

    .already-have-account {
        margin-top: 1vh;
        text-align: right;
        font-family: 'Comfortaa', cursive;
    }

    .already-have-account:hover{
        font-weight: bolder;
    }

    .head1{
        font-family: 'Staatliches', cursive;
        letter-spacing: 5px;
        font-size: 250%;
    }

    .warning{
        color: red;
        font-size: 130%;
        font-weight: bolder;
        
    }
    .community{
        display: none;
    }

    @media screen and (max-width: 1500px){
        .register11 {
            margin-top: 10%;
        }
    }

    @media screen and (max-width: 1200px){
        .register-wrapper1 {
            grid-template-columns: auto;
        }

        .community{
        display: block;
        }

        #small-logo{
            margin-left: 45%;
            margin-bottom: 5%;
            width: 10%;
        }

        #community{
            width: 100%;

        }
        .register11{
            display: none;
        }

        .head1{
            font-size: 200%;
        }
    } 

    @media screen and (max-width: 700px){
        /* .head1{
            font-size: 150%;
        } */

        #small-logo{
            margin-left: 40%;
            margin-bottom: 5%;
            width: 20%;
        }
    }
    

</style>