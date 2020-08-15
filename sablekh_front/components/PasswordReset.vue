<template>
    <div class="password-reset-component mxw-100-mnh-100">
        <img src="@/assets/logo1.png" alt="logo" class="logo-img">
        <div class="password-reset-wrapper1">
            <div class="password-reset11">
                <!-- <img v-show="first_phase" src="@/assets/password_reset/1.png" alt="loading img"> -->
                <img src="@/assets/password_reset/2.png" alt="loading img">
            </div>
            <div class="password-reset12">

                <!-- <div v-show="first_phase" class="grid-set pr121 w-100-h-100">
                    <h1>Forget Password ?</h1>
                    <p>Then reset your password by clicking the button below.</p>
                    <button class="btn" @click="reset_button">
                        Reset
                    </button>
                </div> -->
                <div class="grid-set pr122 w-100-h-100">
                    <div class="pr1221">
                        <h1>Change Password</h1>
                        <p>{{email}}</p>
                    </div> 
                    <div class="input-section">
                        <input type="password" v-model="password1" id="password1" placeholder="New Password">
                        <input type="password" v-model="password2" id="password2" placeholder="Old Password">
                    </div>
                    <p v-show="diff_pass">Different Password</p>
                    <p v-show="short_pass">Short Password</p>
                    <button class="btn" @click="done_button">
                        Done
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import axios from "axios";

export default {
    data() {
        return {
            server_address: "https://api.sablekh.com",
            // first_phase: true,
            // second_phase: false,
            password1: "",
            password2: "",
            email: "dfadfa@gmail.com",
            diff_pass: false,
            short_pass: false
        }
    },
    methods: {

        done_button() {
            this.short_pass = false;
            this.diff_pass = false;

            if(!this.similarity_check) {
                this.diff_pass = true;
            }
            else if(!this.length_check) {
                this.short_pass = true
            }
            else {
              axios({
                  url: this.server_address + "/reset-password", 
                  method: 'post',
                  data: {
                    token: this.$route.params.id,
                    type: "action-change",
                    password: this.password1
                  },
                  headers: this.implicit_data()
              })
              .then(res => {
                  window.location.replace("/login")
              })
            }

        },

        reset_button() 
            axios.post(this.server_address + "/reset-password", {
                token: this.$route.params.id,
                type: "test"
            })
            .then(res => {
                if (res.data.message === "token valid") {
                    this.first_phase = false
                    this.second_phase = true
                }
            })
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
      }
    },
    mounted() {

        if(!this.$route.params.id) {
            window.location.replace("/login")
        }

        axios.post(this.server_address + "/reset-password", {
                token: this.$route.params.id,
                type: "test"
            })
            .then(res => {
                if (!res.data.message === "token valid") {
                    alert("Invalid link")
                }
            })
            .catch(e => {
                alert("Internal error")
                console.log(e)
            })
    }
}
</script>

<style scoped>
    .password-reset-component {
        background-color: rgb(255, 233, 203);
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .logo-img {
        width: 8%;
        margin: 5vh 0;
    }
    .password-reset-wrapper1{
        width: 80%;
        display: flex;
    }
    .password-reset11 {
        width: 60%;
        height: 60vh;
        box-shadow: -5px 0 10px rgb(211, 188, 158);
    }
    .password-reset11 > img {
        width: 70%;
        margin: 10vh 0 0 20%;
    }
    .password-reset12 {
        background-color: white;
        box-shadow: 5px 0 10px rgb(196, 174, 146);
        width: 40%;
        height: 60vh;
    }
    .grid-set {
       display: grid;
       grid-template-rows: auto auto auto;
       justify-content: space-around;
       align-content: space-around;
       padding: 20% 10%;
    }
    .pr121 > h1{
        text-align: center;
      letter-spacing: 5px;
      font-family: 'Staatliches', cursive;

    }
    .pr121 > p {
        font-size: 130%;
        font-family: 'Ubuntu', sans-serif;
        text-align: center;
    }
    .pr122 {
        padding: 10% 1%;
    }
    .pr122 > p {
        color: red;
    }
    .pr1221 > p {
        font-style: italic;
        font-size: 120%;
        margin: 2% 0 0 5%;
    }
    .input-section > input {
        margin-bottom: 5%;
        display: block;
        width: 100%;
        font-size: 130%;
        outline: none;
        border: none;
        background-color: rgb(253, 197, 123);
        padding: 2% 5%;
        border-radius: 5px;
        box-shadow: 0 5px 5px rgb(214, 214, 214);
        color: rgb(165, 140, 106);
        font-family: 'Staatliches', cursive;
    }

/* extras  */

    .btn {
        outline: none;
        cursor: pointer;
        padding: 5% 0;
        font-size: 18px;
        letter-spacing: 1px;
        font-weight: bold;
        border-radius: 10px;
        background-color: rgb(247, 206, 152);
        
    }
    .btn:hover {
        background-color: rgba(229, 186, 130, 0);
        border: 2px solid burlywood;
    }

    .w-100-h-100 {
        width: 100%;
        height: 100%;
    }

    @media screen and (max-width: 1000px) {
        .logo-img {
            width: 100px;
        }
        .password-reset-wrapper1 {
            width: 90%;
        }
        .password-reset11 {
            display: none;
        }
        .password-reset12 {
            width: 100%;
            padding: 10px;
        }
    }
</style>