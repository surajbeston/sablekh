<template>
    <div class="search-component">
        <div class="search-wrapper1 mxw-100-mnh-100">
            <button @click="logout_button" v-if="get_link" class="btn btn-logout">logout</button>
            <div class="search11">
                <img src="@/assets/search/top.png" alt="loading image">
            </div>
            <div class="search12">
                <h1>Search any PDFs here</h1>
            </div>
            <div class="search13">
                <input @keyup.enter="search_button" type="text" v-model="search" id="search">
                <a href="#results-div"><img @click="search_button" src="@/assets/search/search.png" alt="loading image"></a>
            </div>
            <div class="search14">
                <h2 @click="to_link" id="to">{{this.get_name}}</h2>
            </div>
        </div>
        <div v-if="is_searched" id="results-div" class="search-wrapper2 mxw-100-mnh-100">
            <div v-bind:key="book.id" v-for="book in search_books" class="search-wrapper2-layer1">
                <div class="search2-each">
                    <h1>{{book.title}}</h1>
                    <p>{{book.desc}}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import {setCookie} from "@/extras/cookie";

export default {

    data() {
        return {
            search: "",
            is_searched: false,
            search_books: [
                {
                    id: 1,
                    title: "physics",
                    desc: "fjadfa asdfjasdf asd fadsf asdf asdfasdf asdfasdfasf"
                },
                {
                    id: 2,
                    title: "physics",
                    desc: "fjadfa asdfjasdf asd fadsf asdf asdfasdf asdfasdfasf"
                },
            ]
        }
    },

    methods: {
        search_button() {
            this.is_searched = true;
        },
        to_link() {
            this.get_link ? window.location.replace("/upload") : window.location.replace("/login");
        },
        logout_button() {
            setCookie("ikmrfs", "", -1)
            window.localStorage.removeItem("token");
            window.location.reload()
        }
    }, 

    computed: {
        get_link() {
            if (process.browser) {
                return window.localStorage.getItem("token") ? true : false; 
            }
        },
        get_name() {
            return this.get_link ? "upload" : "login to upload";
        }
    },

    mounted() {

        setTimeout(() => {
            console.clear()
            }, 2000);
        
        // if (window.localStorage.getItem("token")) {
        //   document.getElementById("to-upload").setAttribute("class", "")
        // }
        // else {
        //     document.getElementById("to-login").setAttribute("class", "")
        // }
    }

}

</script>

<style scoped>
    .search-component {
        background-color: rgb(255, 151, 255);
    }
    .search-wrapper1 {
        position: relative;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .btn-logout {
        position: absolute;
        right: 2vw;
        top: 2vh;
        background: none;
        border: 2px solid black;
        border-radius: 5px;
        font-size: 16px;
    }
    .btn-logout:hover {
        background-color: rgba(182, 57, 117, 0.13);
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
    .search13 > a > img {
        cursor: pointer;
        position: absolute;
        top: 7px;
        right: 20px;
        width: 40px;
    }
    .search14 > h2 {
        color: rgb(94, 29, 59);
        text-decoration: underline;
        cursor: pointer;
    }
    .search14 > h2:hover {
        color: rgb(49, 16, 31)
    }

    /* wrapper2  */

    .search-wrapper2 {
        padding-top: 5vh;
        background-color: rgb(254, 227, 200);
    }
    .search-wrapper1-layer1 {
        width: 100%;
    }
    .search2-each {
        margin: 0 auto;
        margin-top: 2vh;
        width: 70vw;
        border: 2px solid black;
    }
</style>