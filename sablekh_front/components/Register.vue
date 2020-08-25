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
                    <div id = "errorBox" v-show="hasError" ><p id = "errorTxt"> {{error}}<img src = "@/assets/cancel.png" @click="hasError =!hasError" class = "cancelError"></p></div>
                    <label for="email">E-mail</label>
                    <input type="email" v-model="email" id="email" autofocus>
                    <label for="password">Password</label>
                    <input type="password" v-model="password1" id="password1">
                    <label for="confirm password">Confirm Password</label>
                    <input @keyup.enter="create_button" type="password" v-model="password2" id="password2">
                </div>

                <p class="privacy-stuff">*By signing up you accept all our <a href = "/terms-and-conditions">Terms & Conditions</a> and <a href = "/privacy-policy">Privacy Policy.</a></p>

                <button @click="create_button" class="btn create-button">{{btn_txt}}</button>
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
        server_address: "http://localhost:8000",
        email: "",
        password1: "",
        password2: "",
        hasError: false,
        error: "this is error.",
        btn_txt: "Create",
        sending: false,
        time: 0
    } 
  },
  methods: {
      create_button() {
        this.same_password = false
        this.small_password = false
        this.wrong_email = false

        if (this.sending){
            this.show_error("Please wait, sending request.")
        }
        else if (!navigator.onLine){
            this.show_error("Please check your internet connection and try again.")
        }
        else if (!this.validate_email){
            this.show_error("Please enter correct email address.")
        }
        else if (!this.similarity_check) {
            this.show_error("Passwords below don't match.")
        }
        else if (!this.length_check) {
            this.show_error("Please make your password at least 8 character long.")
        }
        else {
            this.sending = true
            this.btn_txt = "Sending"
            axios({
                url: this.server_address + "/users",
                method: "post",
                data: {"email": this.email, "password": this.password1},
                headers: this.implicit_data()
            })
            .then(res => {
                this.sending = true
                this.btn_txt = "Create"
                console.log("reached here")
                axios({
                    url: this.server_address + "/token",
                    method: "post",
                    headers: this.implicit_data(),
                    data: {"email": this.email, "password": this.password1}
                })
                .then(res => {
                    this.sending = true
                    this.btn_txt = "Create"
                    var token = res.data.token
                    if (token != undefined){
                        window.localStorage.setItem("token", token)
                        window.localStorage.setItem("email", this.email)
                    }
                    if (this.remember) {
                    this.cookie_setter(token)
                    }
                    window.location.replace("/")
                })
                .catch(err => {
                    var data = err.response
                    this.btn_txt = "Create"
                    this.sending = false
                    this.window.href = "/login"
                })
                    })
                    .catch(err => {
                        var data = err.response
                        console.log(data)
                        this.sending = false
                        this.btn_txt = "Create"
                        if (data.status == 303) this.show_error("User with this email already exists.")
                        else this.show_error("Something went wrong. please try again.")
                        this.password1 = ""
                        this.password2 = ""
                    })
          }
      },
      show_error(errorTxt){
          this.hasError = true
          this.error = errorTxt
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
    implicit_data(){
            return {"site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
        }
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

      this.time = new Date().getTime()
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
        font-size: 110%;
        letter-spacing: .8px;
        background-color: rgb(40, 43, 42);
        color: rgb(255, 239, 223);
        border-radius: 5px;
        margin-top: 5vh;
        font-family: 'Rajdhani', sans-serif;
        cursor: pointer;
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

    .privacy-stuff{
        font-family: 'Comfortaa', cursive;
        font-size: 80%;
    }


    .community{
        display: none;
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