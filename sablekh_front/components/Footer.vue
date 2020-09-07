<template>
    <div class="footer">
        <div class="footer1">
            <div class="each-footer1 footer11">
                <hr class="hr-top">
                <div class="footer11-links">
                    <NuxtLink class = "top-link" to="/">Search</NuxtLink>
                    <NuxtLink class = "top-link" to="/library">My Libraries</NuxtLink>
                    <NuxtLink class = "top-link" to="/about">About Us</NuxtLink>
                </div>
                
            </div>
            <div class="each-footer1 footer12">
                <img src="@/assets/sablekh.png" alt="logo" class="bottom-logo">
                <div class="icons">
                    <a href = "https://www.facebook.com/groups/598216594197165"><img src="@/assets/footer/FACEBOOK.png" alt="icon" class="sm-icon"></a>
                    <a href = "https://www.instagram.com/amoebatech/"> <img src="@/assets/footer/INSTA.png" alt="icon" class="sm-icon"></a>
                    <a href = "https://www.linkedin.com/in/anil-kumar-panta/" ><img src="@/assets/footer/LINKEDIN.png" alt="icon" class="sm-icon"></a>
                </div>
                <div class="weamoeba-stuffs">
                    <p>
                        POWERED BY
                    </p>
                    <a href = "https://weamoeba.com" target="_blank"> <img src="@/assets/footer/bottom-logo.png" alt="logo" class="weamoeba-logo"></a>
                </div>

            </div>
            <div class="each-footer1 footer13">
                <hr class="hr-top">
                <NuxtLink class = "top-link" to="/upload">Upload</NuxtLink>
                <NuxtLink class = "top-link" to="/group">My Groups</NuxtLink>
                <NuxtLink class = "top-link" to="/login" v-show="!authenticated">Log in</NuxtLink>
                <a class = "top-link" @click = "logout" v-show="authenticated">Log out</a>
            </div>
        </div>
        <div class="footer2">
            <NuxtLink class = "bottom-link" to = "/privacy-policy">Privacy Policy</NuxtLink>
            <NuxtLink class = "bottom-link" to = "/terms-and-conditions">Terms and Conditions</NuxtLink>
        </div>
    </div>
</template>

<script>

import {setCookie} from "@/extras/cookie"

export default {
    data() {
        return {
            authenticated: false,
        }
    },
    methods: {
        logout(){
            if (process.browser){
                setCookie("ikmrfs", "", -1)
                window.localStorage.removeItem("token");
                window.location.reload()
            }
        },
    },
    mounted() {

        if (window.localStorage.getItem("token")){
            this.authenticated = true
        }
        else{
            this.authenticated = false
        }
    
    }
    
}
</script>

<style scoped>

    .weamoeba-stuffs {
        display: flex;
        flex-direction: column;
        align-items: center;
        /* margin-top: 20px; */
    }

    .weamoeba-logo {
        width: 70px;
    }

    .weamoeba-stuffs > p {
        padding-bottom: 10px;
    }

    .icons {
        display: inline;
        margin: 30px 0;
        cursor: pointer;
    }

    .bottom-logo {
        width: 25%;
    }

    .footer11-links {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }

    .hr-top {
        border: 1.5px solid rgb(255, 209, 149);
    }

    .footer11 {
        width: 100%;
    }

    .footer12 {
        align-items: center;
        width: 100%;
    }
    
    .footer13 {
        width: 100%;
        
    }

    .each-footer1 {
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .footer1 {
        width: 100%;
        display: grid;
        grid-template-columns: auto auto auto;
        padding: 0 2vw;
    }

    .footer {
        max-width: 100vw;
        box-shadow: 0 -5px 10px rgb(214, 198, 180);
    }
    .footer2 {
        text-align: center;
        padding: 10px 0;
        box-shadow: 0 -5px 10px rgb(223, 223, 223);
    }
    .top-link {
        font-family: 'Staatliches', cursive;
        text-decoration: none;
        margin-top: 10px;
        font-size: 140%;
        cursor: pointer;
    }
    .bottom-link {
        font-family: 'Staatliches', cursive;
        text-decoration: none;
        padding: 0 5vw;

    }
    .bottom-link:first-child {
        border-right: 2px solid black;
    }

    @media screen and (max-width: 800px){
        .bottom-logo {
            width: 40%;
        }
    }


    @media screen and (max-width: 500px){
        .bottom-logo {
            width: 50%;
        }
        .icons {
            text-align: center;
        }
        .sm-icon {
            width: 20%;
        }
        .top-link {
            font-size: 100%;
        }
        .weamoeba-stuffs > p {
            font-size: 80%;
        }
    }


</style>