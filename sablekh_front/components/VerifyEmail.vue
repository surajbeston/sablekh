<template>
  <div class="main">
    <div class="wrapper1">
      <img src="@/assets/forgot_pw/left.png" alt="loading img" class="left-img">
      <img src="@/assets/forgot_pw/right.png" alt="loading img" class="right-img">
      <div class="main12">
        <img src="@/assets/logo1.png" alt="logo" class="main121">
        <img src="@/assets/forgot_pw/top.png" alt="loading image" class="main122">
        <div class="main123">
          <h1>E-mail</h1>
          <h2>{{message}}</h2>
          <!-- <p>Click on the button to verify the e-mail address for <b>Sublekh.</b></p>
            <button @click="verify_clicked">Verify</button> -->
        </div>
      </div>
    </div>
  </div>
</template>


<script>

import axios from 'axios';


export default {

    data() {
        return {
            server_address: "http://18.141.160.193",
            message: "Verifying..."
        }
    },

    methods: {
        verify_clicked() {
            axios({
                url: this.server_address + "/verify-email",
                method: 'post',
                headers: {
                ...this.implicit_data()
                },
                data: {
                token: this.$route.params.token
                }
            })
            .then(res => {
                this.message = "Verified! Redirecting..."
                window.location.replace("/")
            })
            .catch(e => {
                this.message = "Error occured! Try again..."
            })
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
            return {"site": document.referrer+"---"+session_key, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
        }
    },

    mounted() {
      this.verify_clicked();

    }
}
</script>


<style scoped>

.main {
  background-color: rgb(240, 218, 191);
    max-width: 100vw;
    min-height: 100vh;
}
.wrapper1 {
      width: 100%;
      display: flex;
      justify-content: center;
      position: relative;
    }

    .wrapper1 > img {
      position: absolute;
      height: 100vh;
      width: 40vw;
    }

    .left-img {
      left: 0;
    }

    .right-img {
      right: 0;
    }

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
      margin-bottom: 10vh;
      text-decoration: underline;
    }

    .main123>h2 {
      font-size: 200%;
    }

    .main123>p {
      font-size: 150%;
      margin: 5vh 0;
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
      .wrapper1 > img {
        display: none;
      }
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
        font-size: 25px;
      }

      .main123>p {
        font-size: 20px;
      }

      .main123 > button {
        padding: 25px 50px;
      }
    }

</style>