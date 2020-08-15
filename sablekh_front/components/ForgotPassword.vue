<template>
    <div class="forgot-password-component mxw-100-mnh-100">
        <div class="fpc-wrapper1">
            <div class="main">
                <div class="wrapper1">
                    <!-- <img src="@/assets/forgot_pw/left.png" alt="loading img" class="left-img">
                    <img src="@/assets/forgot_pw/right.png" alt="loading img" class="right-img"> -->
                    <div class="main12">
                        <img src="@/assets/forgot_pw/logo.png" alt="logo" class="main121">
                        <img src="@/assets/forgot_pw/top.png" alt="loading image" class="main122">
                        <div class="main123">
                            <h1>PASSWORD RESET</h1>
                            <h2>E-mail</h2>
                            <p v-show="email_sent" style="margin-top: 20px;color:red;">
                              <b>Check Your Email</b>
                            </p>
                            <input type="email" v-model="email" class="email-field" placeholder="Your e-mail">
                            <button id="verify-btn" @click="send_clicked">Send</button>
                        </div>
                    </div>
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
            email: "",
            email_sent: false
        }
    },

    methods: {

        send_clicked() {
          if (!this.validate_email) {
            alert('Enter valid E-mail address')
          }
          else {
            axios({
              url: this.server_address + "/send-password-key",
              method: 'post',
              data: {
                email: this.email
              },
              headers: this.implicit_data()
            })
            .then(res => {
              this.email_sent = true
            })
            .catch(e => {
            })
          }
        },
        validate_email(){
          const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return re.test(String(this.email).toLowerCase());
        },
        implicit_data(){
          return {"site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
      }

    }
}
</script>

<style scoped>
    .forgot-password-component {
        background-color: rgb(255, 235, 209);
        overflow: hidden;
    }
    .main {
      width: 100%;
      height: 100%;
    }

    .wrapper1 {
      width: 100%;
      display: flex;
      justify-content: center;
      position: relative;
    }

    /* .wrapper1 > img {
      position: absolute;
      height: 100vh;
      width: 40vw;
    }

    .left-img {
      left: 0;
    }

    .right-img {
      right: 0;
    } */

    .main12 {
      text-align: center;
      width: 70vw;
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-top: 5vh;
    }

    .main121 {
      width: 10%;
      margin-bottom: 5vh;
    }

    .main122 {
      width: 12%;
      margin-bottom: 5vh;
    }

    .main123>h1 {
      letter-spacing: 1px;
      font-size: 250%;
      font-family: 'Staatliches', cursive;
      letter-spacing: 5px;
    }

    .main123>h2 {
        margin-top: 5vh;
      font-size: 200%;
      text-decoration: underline;
    }

    .main123>input {
        width: 100%;
      font-size: 150%;
      margin: 5vh 0;
      background: none;
      padding: 10px 20px;
      border: 2px solid rgb(163, 135, 98);
      border-radius: 10px;
      outline: none;
    }


    .main123 > button {
      cursor: pointer;
      font-size: 100%;
      padding: 2vw 7vw;
      letter-spacing: 1px;
      font-weight: bold;
      outline: none;
      border: none;
      background-color: rgb(228, 182, 122);
      border-radius: 5px;
    }

    .main123>button:hover {
      background: none;
      background-color: rgba(209, 170, 118, 0.137);
      border: 2px solid rgb(228, 182, 122);
    }

    @media screen and (max-width: 1200px) {
      .main121 {
        width: 20%;
      }

      .main122 {
        width: 20%;
      }
    }

    @media screen and (max-width: 700px) {
      /* .wrapper1 > img {
        display: none;
      } */
      .main12 {
        width: 90vw;
      }

      .main121 {
        width: 100px;
      }

      .main122 {
        width: 80px;
      }

      .main123>h1 {
        font-size: 25px;
      }

      .main123>h2 {
        font-size: 20px;
      }

      .main123>p {
        font-size: 20px;
      }
        .main123 > input {
            font-size: 18px;
            padding: 5px 10px;
        }
      .main123 > button {
        padding: 25px 50px;
      }
    }
</style>