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
                            <h2>Enter your email address</h2>
                           <div id = "successBox" v-show="hasSuccess" ><p id = "successTxt"> {{success}}<img src = "@/assets/cancel.png" @click="hasSuccess =!hasSuccess" class = "cancelSuccess"></p></div>
                            <div id = "errorBox" v-show="hasError" ><p id = "errorTxt"> {{error}}<img src = "@/assets/cancel.png" @click="hasError =!hasError" class = "cancelError"></p></div>
                            <input type="email" v-model="email" class="email-field" placeholder="dummy@sablekh.com">
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
            email_sent: false,
            hasSuccess: false,
            success: "This is success",
            error: "This is error",
            hasError: false
        }
    },

    methods: {
        send_clicked() {
          if (!this.validate_email() || this.email.replace(/\s/g, '') == "dummy@sablekh.com") {
            this.show_error('Enter valid E-mail address')
          }
          else if (this.email_sent){
            this.show_success("Email already sent. Please wait & check your mailbox.")
          }
          else {
            axios({
              url: this.server_address + "/send-password-key",
              method: 'post',
              data: {email: this.email},
              headers: this.implicit_data()
            })
            .then(res => {
              this.email_sent = true
              this.show_success("Reset instructions sent to following email.")
            })
            .catch(e => {
              if (e.response.status == 404) this.show_error("Following email not found. ")
              else if (e.response.status == 500) this.show_error("Something went wrong.")
            })
          }
        },
    validate_email(){
      const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(String(this.email).toLowerCase());
    },
        implicit_data(){
          return {"site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
      },
      show_success(successTxt){
        this.hasError = false
        this.hasSuccess = true
        this.success = successTxt
      },
      show_error(errorTxt){
        this.hasSuccess = false
        this.hasError = true 
        this.error = errorTxt 
      },

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
      font-family: 'Ubuntu', sans-serif;
    }

    .main123>button:hover {
      background: none;
      background-color: rgba(209, 170, 118, 0.137);
      border: 2px solid rgb(228, 182, 122);
    }


    #successBox{
      background-color: rgba(134, 190, 87, 0.4);
      color: rgb(51, 47, 43);
      border: 1px black solid;
      border-radius: 5px;
      padding : 1%;
      font-size: 110%;
      font-family: 'Rajdhani', sans-serif;
      font-weight: 200;
      animation-name: fadein;
      animation: fadein 1s;
      width: 100%;
      animation-name: fadein;
      animation: fadein 1s;
    }

    @keyframes fadein {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

  .cancelSuccess{
      cursor: pointer;
      float: right;
  }

  #errorBox{
    background-color: rgba(255, 0, 0, 0.4);
    color: rgb(51, 47, 43);
    border: 1px black solid;
    border-radius: 5px;
    padding : 1%;
    font-size: 110%;
    font-family: 'Rajdhani', sans-serif;
    animation-name: fadein;
    animation: fadein 1s;
    margin: 2% 0 2% 0;
    font-weight: bold;
    width: 100%;
    animation-name: fadein;
    animation: fadein 1s;

}

.cancelError{
    cursor: pointer;
    right: 0;
    float: right;
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
        font-size: 30px;
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

      .main{
        margin-left: 0;
      }
    }
</style>