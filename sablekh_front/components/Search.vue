<template>
    <div class="search-component mxw-100-mnh-100">
        <div class="search-wrapper1">
            <div class="search11">
                <img src="@/assets/search/top.png" alt="loading image">
            </div>
            <div class="search12">
                <h1>Search any PDFs here</h1>
            </div>
            <div class="search13">
                <input @keyup.enter="search_button" type="text" v-model="search" id="search">
                <img @click="search_button" src="@/assets/search/search.png" alt="loading image">
            </div>
            <div class="search14">
                <h2 class="none" id="to-login"><NuxtLink to="/login">login to upload</NuxtLink></h2>
                <h2 class="none" id="to-upload"><NuxtLink to="/upload">upload</NuxtLink></h2>
            </div>
        </div>
    </div>
</template>

<script>

export default {

    data() {
        return {
            search: "",
        }
    },

    methods: {
        search_button() {
            console.log("some")
        }
    }, 

    mounted() {

        if (window.localStorage.getItem("token")) {
          document.getElementById("to-upload").setAttribute("class", "")
        }
        else {
            document.getElementById("to-login").setAttribute("class", "")
        }
    }

}

</script>

<style scoped>
    .search-component {
        background-color: rgb(254, 80, 164);
    }
    .search-wrapper1 {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .search11 > img {
        width: 25vw;
    }
    .search12 > h1 {
        font-size: 2.5vw;
    }
    .search13 {
        position: relative;
        margin: 2vh 0;
    }
    .search13 > input {
        width: 40vw;
        font-size: 20px;
        padding: 15px 20px;
        padding-right: 70px;
        border-radius: 50px;
        box-shadow: 0 5px 10px rgb(128, 40, 82);
        letter-spacing: 1px;
        outline: none;
        border: none;
    }
    .search13 > img {
        cursor: pointer;
        position: absolute;
        top: 7px;
        right: 20px;
        width: 40px;
    }
    .search14 > h2 > a {
        color: rgb(94, 29, 59)
    }
</style>