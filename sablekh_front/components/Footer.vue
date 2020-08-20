<template>
    <div class="footer">
        <div class="footer-wrapper1">
            <NuxtLink class = "foot-link" to="/">Search</NuxtLink>
            <NuxtLink class = "foot-link" to="/library">My Libraries</NuxtLink>
            <img src="@/assets/sablekh.png" alt="loading image" id = "main-img">
            <NuxtLink class = "foot-link" to="/upload">Upload</NuxtLink>
            <NuxtLink class = "foot-link" to="/login" v-show="!authenticated">Log in</NuxtLink>
            <a class = "foot-link" @click = "logout" v-show="authenticated">Log out</a>
        </div>
        <div class="bottom-links">
            <NuxtLink class = "bottom-link" to = "/privacy-policy">Privacy Policy</NuxtLink>
            <NuxtLink class = "bottom-link" to = "/terms-and-conditions">Terms and Conditions</NuxtLink>
        </div>
    </div>
</template> 
<script>

import {setCookie} from "@/extras/cookie";
import axios from "axios"

export default {
    data() {
        return{
            authenticated: false
        }
    },
    methods: {
        logout(){
            if (process.browser){
                setCookie("ikmrfs", "", -1)
                window.localStorage.removeItem("token");
                window.location.reload()
            }
        }
    },
    mounted() {
        if (window.localStorage.getItem("token")){
            this.authenticated = true
        }
        else{
            this.authenticated = false
        }
        // console.log("referring")
        // console.log(document.referrer)
        // axios({
        //     url: "http://localhost/tags",
        //     method: "get",
        //     headers: {"referer": document.referer}
        // }).then(res => {
        //     console.log(res)
        // })
    }
}
</script>


<style scoped>
    .foot-link{
        text-decoration: none;
        color: rgb(66, 62, 55);
        font-weight: 600;
        font-size: 140%;
        margin: 0 3vw;
        font-family: 'Staatliches', cursive;
        letter-spacing: 2px;
    }

    .foot-link:hover {
        text-decoration: underline;
        cursor: pointer;
        color:rgb(0, 0, 0)
    }
    .footer {
        height: 200px;
        max-width:100vw;
        background-color: white;
    }

    .footer-wrapper1 {
        width: 100%;
        height: 100%;
        display:flex;
        justify-content: center;
        align-items: center;
    }

    .bottom-links{
        /* background-color: rgb(254, 227, 200); */
        background-color: rgb(254, 227, 200);
        padding: 5px 0 5px 0;
        text-align: center;
    }

    .bottom-link{
        color: black;
        margin: 0 5% 0 5%;
        text-decoration: none;
        font-family: 'Ubuntu', sans-serif;
        font-size: 90%;
    }


    @media screen and (max-width: 1500px){
       .footer{
            height: 170px;
       }
       #main-img{
           height: 50%;
       }
        .foot-link{
            font-size: 130%;
        }
    }

    @media screen and (max-width: 1200px){
       .footer{
           height: 150px;
       }
       #main-img{
           height: 45%;
       }
        .foot-link{
            font-size: 120%;
        }

        .bottom-link{
            font-size: 90%;
        }
    }

    @media screen and (max-width: 700px){
       .footer{
            height: 135px;
       }
       #main-img{
           height: 35%;
       }
        .foot-link{
            font-size: 100%;
            font-weight: bold;
        }
        .bottom-link{
            font-size: 80%;
        }
    }

    @media screen and (max-width: 500px){
       .foot-link{
           font-size: 20px;
            font-weight: bold;
       }
       .footer-wrapper1 {
           padding:0;
       }
       #main-img{
           height: 25%;
       }
       .foot-link{
            font-size: 90%;
       }
       .bottom-link{
           font-size: 70%;
       }
    }

    @media screen and (max-width: 370px){
        .footer {
            height: 300px;
        }
        .footer-wrapper1 {
            flex-direction: column;
        }
        .foot-link {
            margin-top: 20px;
            margin-bottom: 10px;
        }
    }

</style>