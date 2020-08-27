<template>
    <div class="header-main">
        <img v-show="!is_extended" @click="icon_clicked" class="menu-icon" src="@/assets/about/menu-icon.png" alt="icon">
        <img v-show="is_extended" @click="icon_clicked" class="cancel-icon" src="@/assets/about/cancel.png" alt="icon">
        <transition name="slide">
            <div v-show="is_extended" class="header-contents">
                <NuxtLink class = "header-link" to="/">Search</NuxtLink>
                <NuxtLink class = "header-link" to="/library">My Libraries</NuxtLink>
                <NuxtLink class = "header-link" to="/upload">Upload</NuxtLink>
                <NuxtLink class = "header-link" to="/about">About Us</NuxtLink>
                <NuxtLink class = "header-link" to="/login" v-show="!authenticated">Log in</NuxtLink>
                <a class = "header-link" @click = "logout" v-show="authenticated">Log out</a>
            </div>
        </transition>  
        <img v-show="!is_extended" src="@/assets/logo1.png" alt="logo" class="logo">
    </div>
</template>

<script>

import {setCookie} from "@/extras/cookie"

export default {
    data() {
        return {
            is_extended: false,
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
        icon_clicked() {
            this.is_extended = !this.is_extended;
        }
    },
    computed: {
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

/* animation stuffs */

.slide-enter-active {
    transition: all .5s ease;
}
.slide-leave-active {
    transition: all .5s cubic-bezier(1.0, 0.5, 0.8, 1.0); 
}
.slide-enter, .slide-leave-to
{
    transform: translateX(5%);
    opacity: 0;
}

/* end animation stuffs */

.header-link {
    font-family: 'Staatliches', cursive;
    text-decoration: none;
    font-size: 140%;
    margin-left: 5%;
    cursor: pointer;
}

.header-contents {
    display: flex;
    flex-direction: row;
    width: 100%;
}

.logo {
    width: 5%;
    position: absolute;
    right: 3%;
}

.menu-icon,
.cancel-icon {
    width: 2%;
    cursor: pointer;
}

.header-main {
    width: 100%;
    min-height: 120px;
    box-shadow: 0 5px 10px rgb(214, 190, 160);
    display: flex;
    flex-direction: row;
    padding: 0 3%;
    align-items: center;
    background-image: linear-gradient(to right bottom, rgb(255, 232, 206), rgb(240, 214, 185));
    position: relative;
}

@media screen and (max-width: 1300px) {
    .logo {
        width: 8%;
    }
}

@media screen and (max-width: 1000px) {
    .menu-icon,
    .cancel-icon {
        width: 25px;
    }
    .logo {
        width: 60px;
    }
}

@media screen and (max-width: 700px) {
    .header-link {
        font-size: 100%;
    }
}

@media screen and (max-width: 500px) {
    .header-main {
        min-height: 0px;
        height: 100px;
    }
    .menu-icon,
    .cancel-icon {
        width: 15px;
    }  
    .logo {
        width: 50px;
    }
    .header-link {
        font-size: 80%;
    }
}

@media screen and (max-width:400px) {
    .header-link {
        font-size: 70%;
    }
    .slide-enter, .slide-leave-to
    {
        transform: translateX(2%);
    }
}


</style>