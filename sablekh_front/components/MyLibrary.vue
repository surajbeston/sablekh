<template>
    <div class="my-library-component mxw-100-mnh-100">
        <div class="my-library-wrapper1">
            <img src="@/assets/logo1.png" alt="loading img" class="logo-img">
            <div class="my-library11">
                <h1>Your Library</h1>
                <div class="my-library111">
                    <div class="each-library" :key="library" v-for="library in libraries">
                        <img src="@/assets/filenames/pdf.png" alt="loading img">
                        <h1>library</h1>
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
            libraries: ["afad", "asdfafd", "adfadf"]
        }
    },
    mounted() {
       axios.post(this.server_address + '/search', {
           query: "aa",
           tags: [""]
       })
       .then(res => {
           console.log(res)
       })
       .catch(e => {
           console.log(e)
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
    }
    .each-library > h1 {
        margin-left: 5%;
    }
</style>