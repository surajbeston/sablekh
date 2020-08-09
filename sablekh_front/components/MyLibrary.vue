<template>
    <div class="my-library-component mxw-100-mnh-100">
        <div class="my-library-wrapper1">
            <img src="@/assets/logo1.png" alt="loading img" class="logo-img">
            <div class="my-library11">
                <h1>Your Library</h1>
                <div class="my-library111">
                    <NuxtLink :to="`/library/${library.link_str}`" :key="library.hid" v-for="library in libraries">
                        <div class="each-library" >
                            <img src="@/assets/filenames/pdf.png" alt="loading img">
                            <h1>{{library.title}}</h1>
                        </div>
                    </NuxtLink>
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
            libraries: []
        }
    },
    mounted() {
        var id = window.localStorage.getItem("token")
        if (!id) {
            window.location.replace("/login")
        }
        console.log(id)

       axios({
           url: this.server_address + '/all-libraries',
           headers: {
               "Authorization": "Token " + id
           }
       })
       .then(res => {
           this.libraries = res.data
       })
       .catch(e => {
           console.log(e)
           alert("Internal Error please try again later")
       })
    }
}
</script>

<style scoped>
    .my-library-component {
        background-color: rgb(248, 219, 181);
    }
    .my-library-wrapper1 {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        position: relative;
    }
    .logo-img {
        width: 7%;
        position: absolute;
        right: 2vw;
        top: 2vh;
    }
    .my-library11 {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 5vh 0;
    }
    .my-library111 {
        margin: 5vh 0 0 0;
        width: 70vw;
    }
    .each-library {
        align-items: center;
        width: 100%;
        display: flex;
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 3vh;
        background-color: white;
        box-shadow: 0 5px 10px rgb(196, 176, 150);
    }
    .each-library > h1 {
        margin-left: 5%;
    }

    a {
        text-decoration: none;
    }
</style>