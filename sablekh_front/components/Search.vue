<template>
    <div class="search-component">
        <div class="search-wrapper1 mxw-100-mnh-100">
            <div class="header">
                <img src="@/assets/logo1.png" alt="log0" class="logo-img">
            </div>
            <div class="search11">
                <img src="@/assets/search/top.png" alt="loading image">
            </div>
            <div class="search12">
                <h1>Search Anything</h1>
            </div>
            <div class="search13">
                <input @keyup.enter="search_button" type="text" v-model="search" id="search">
                <a href="#results-div"><img @click="search_button" src="@/assets/search/search.png" alt="loading image"></a>
            </div>
            <div class="search14">
                <div class="all-tags">
                    <div class="each-tag" v-bind:key="tag" v-for="tag in tags">
                        <img src="@/assets/tag.png" alt="tag" class="tag_png">
                        <span>{{tag}}</span>
                        <img src="@/assets/cancel.png" alt="loading image" :id="tag" @click="cancel_button" class = "cancel">
                    </div>
                    <input  type="text" v-model="current_tag" id="current-tag" @input="current_tag_changed" placeholder="Add tags here" autocomplete="off">
                </div>
            </div>
            <div v-show="show_suggessions" class="input-options">
                <span :key="option.item" v-for="option in avialable_tags" @click="options_clicked">
                    {{option.item}}
                </span>
            </div>
            <!-- <div class="search15">
                <h2 @click="to_link" id="to">{{this.get_name}}</h2>
            </div> -->
            <span class="loader" v-show = "loader_on"></span>
            <h2  v-show="no_search && !loader_on" class = "no_search">No libraries found for the query.</h2>
            <div id="results-div" class="search15" v-show = "!loader_on && !no_search">
                <NuxtLink :to="`library/${book.link_str}`" v-bind:key="book.hid" v-for="(book, index) in computed_libraries" >
                    <div class="search151">
                        <div class="search151-each">
                            <img :src="book.thumbnail" alt="loading image">
                            <div class="search1512">
                                <p> 
                                   <span class = "tag">Notes</span><span v-for="tag in book.tags" class = "tag">{{tag}}</span> 
                                </p>
                                <h1>{{book.title}}</h1>
                                <p>{{book.description}}</p>
                            </div>
                            <div class = "action-box">
                                <div class="action">
                                    <span>{{book.downloads}}</span>
                                    <img src="@/assets/download1.png" alt="like">
                                </div>
                                <div class="action">
                                    <span>{{book.likes}}</span>
                                    <img src="@/assets/like.png" alt="like">
                                </div>
                            </div>
                        </div>
                    </div>
                </NuxtLink>
            </div>
        </div>
    </div>
</template>

<script>

import Fuse from "fuse.js";
import axios from "axios";

import {setCookie} from "@/extras/cookie";

export default {
    data() {
        return {
            server_address: "http://localhost:8000",
            image_address: "https://pngimg.com/uploads/book/book_PNG51083.png",
            show_suggessions: true,
            off_width: 0,
            current_tag: "",
            tags: [],
            avialable_tags: [],
            all_tags: [],
            search: "",
            search_books: [],
            likes: [],
            downloads: [],
            libraries: [],
            loaded: false,
            loader_on: false,
            holder: [],
            previous_libraries: [],
            hids: [],
            no_search: false
        }
    },

    methods: {
        add_to_localstorage(name, data) {
            let s = false
            try{
                window.localStorage.setItem(name, "")
                window.localStorage.setItem(name, JSON.stringify(data))
                s = true
            }
            catch{}

            return s
        },
        retrive_from_localstorage(name) {
            let data = window.localStorage.getItem(name);
            return data ? JSON.parse(data) : [];
        },
        current_tag_changed() {
            this.show_suggessions = true
            this.avialable_tags = this.fuse.search(this.current_tag)
            this.avialable_tags = this.avialable_tags.filter(e => !this.tags.includes(e.item))
        },
        options_clicked(e) {
            let i = e.target.innerText
            this.current_tag = i
            if (! this.tags.includes(this.current_tag) ) {
                this.tags.push(i)
            }
            this.show_suggessions = false;
            this.current_tag = "";
        },
        cancel_button(e) {
            let i = this.tags.indexOf(e.target.id)
            this.tags.splice(i, 1)
        },
        search_button() {
            this.libraries = [] 
            if (this.search != "") {
                this.loader_on = true
                axios({
                    url: `${this.server_address}/search`,
                    method: 'POST',
                    data: {
                        query: this.search,
                        tags: this.tags.length > 0 ? this.tags : [""]
                    },
                    headers: this.implicit_data()
                })
                .then(res => {
                    this.add_to_localstorage("search", res.data)
                    this.no_search = res.data.length > 0 ? false: true
                    //.log(this.no_search)
                    this.search_books = res.data
                    this.libraries = []
                    this.hids = []
                    this.fill_extra()

                    this.loaded = false
                    this.loader_on = false 
                }) 
            }
        },
        to_link() {
            this.get_link ? window.location.replace("/upload") : window.location.replace("/login");
        },
        async fill_extra(){
            return await this.get_likes_downloads()
        },
        get_likes_downloads(){
            if (this.search_books.length > 0){
                this.search_books.map(lib => {
                    axios({
                        url: this.server_address + "/all-likes",
                        method: 'post',
                        headers: this.implicit_data(),
                        data: {
                            library: lib.hid
                        }
                        })    
                        .then(res => {
                            lib.likes = res.data.likes
                            axios({
                                url: this.server_address + "/all-downloads",
                                method: 'post',
                                headers: this.implicit_data(),
                                data: {library: lib.hid}
                            })
                            .then(res => {
                                lib.downloads = res.data.downloads
                                if (!this.hids.includes(lib.hid)){
                                    this.hids.push(lib.hid)
                                    this.libraries.push(lib)
                                }
                            })
                            .catch(e => {
                                lib.downloads = 0
                            })
                        })
                        .catch(e => {
                            lib.likes = 0
                        })

                    })
                }
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
        ,
    }, 

    computed: {
        get_link() {
            if (process.browser) {
                return window.localStorage.getItem("token") ? true : false; 
            }
        },
        get_name() {
            return this.get_link ? "upload" : "login to upload";
        },
        computed_libraries(){
            for (var book of this.libraries){
                if (book.title.length > 50) book.title = book.title.slice(0, 67) + "..."
                if (book.description.length > 70) book.description = book.description.slice(0, 67) + '...'
                if (book.tags.length > 2) book.tags = book.tags.splice(0, 3)
            }
            return this.libraries
        }
    },

    mounted(){
        this.time = new Date().getTime()
        this.previous_libraries = this.retrive_from_localstorage("search")
        this.search_books = []

        var libs = this.previous_libraries;
        for (var previous_library of this.previous_libraries){
            axios({
                url: `${this.server_address}/get-library`,
                method: "post",
                headers: this.implicit_data(),
                data: {"hid": previous_library.hid}
            }).then(res => {
                this.loaded = false
                this.search_books.push(res.data)
                this.fill_extra()
                this.loader_on = false
            })
            .catch(err => {
            })
        }
        axios({
            url: `${this.server_address}/tags`,
            method: "get",
            headers: this.implicit_data()
        }).then(res => {
            this.all_tags = res.data.tags
            this.fuse = new Fuse(this.all_tags, {}) 
        })
    }
}

</script>

<style scoped>
    a {
        text-decoration: none;
    }
    .search-component {
        padding-bottom: 5vh;
        background-color: rgb(254, 227, 200);
        overflow: hidden;
    }
    .search-wrapper1 {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .header {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-end;
        width: 100%;
        height: 17vh;
        box-shadow: 0 5px 5px rgb(184, 166, 143);
    }
    .logo-img {
        width: 7%;
        margin-right: 2vw;
    }
    .search11 > img {
        width: 25vw;
    }
    .search12 > h1 {
        padding: 0 10px;
        font-family: 'Staatliches', cursive;
        letter-spacing: 5px;
        font-size: 300%;
        font-weight: 100;
    }
    .search13 {
        position: relative;
        margin: 2vh 0 5vh 0;
    }
    .search13 > input {
        width: 40vw;
        font-size: 20px;
        padding: 15px 20px;
        padding-right: 70px;
        border-radius: 50px;
        box-shadow: 0 5px 10px rgb(175, 157, 139);
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
    .search14 {
        width: 30vw;
        display: flex;
        /* justify-content: center; */
        border-radius: 10px;
        background-color: white;
        padding: 5px 0;
        font-family: 'Comfortaa', cursive;
        overflow: hidden;
    } 
    .all-tags {
        min-width: 10px;
        background-color: white;
        display: flex;
        flex-wrap: wrap;
        margin: 0 1vw;
    }
    .all-tags > input {
        font-size: 20px;
        padding: 10px 20px;
        border: none;
        outline: none;
        font-family: 'Comfortaa', cursive;
        margin-left: 0;
        text-align: left;
        width: 200px;
        display: inline-block;
    }
    .each-tag {
        border-radius: 5px;
        position: relative;
        background-color: rgb(238, 177, 97);
        margin: 5px;
        padding: 5px 30px;
        border-radius: 5px;
        font-size: 18px;
        display: inline-block;
    }

    .no_search{
        margin-top: 5%;
        text-align: center;
        font-family: 'Rajdhani', sans-serif;

    }
    .each-tag > img {
        position: absolute;
        right: 5px;
        top: 7px;
        width: 16px;
    }
    .tag_png {
        left: 7px;
    }
    .input-options {
        width: 30%;
        display: flex;
        flex-direction: column;
        background-color: rgb(238, 177, 97);
        border-radius: 10px;

    }
    .input-options > span {
        text-align: center;
        letter-spacing: 1px;
        font-size: 20px;
        padding-top: 1vh;
        padding-bottom: 1vh;
        width: 100%;
        cursor: pointer;
    }
    .input-options > span:hover {
        background-color: rgb(187, 140, 80);
    }
    .search15 > h2 {
        color: rgb(133, 117, 102);
        text-decoration: underline;
        cursor: pointer;
    }
    .search15 > h2:hover {
        color: rgb(71, 63, 55);
    }
    .search15 {
        padding-top: 5vh;
        background-color: rgb(254, 227, 200);
    }
    .search151 {
        width: 100%;
        margin-bottom: 5%;
    }

    .search1512{
        /* border-left: solid rgb(56, 53, 53) 2px; */
        padding-left: 5%;
        
    }
    .search1512 > h1{
        margin-top: 0;
        font-family: 'Rajdhani', sans-serif;
        font-size: bolder;
        margin-top: 2%;
    }

    .search1512 > p{
        font-family: 'Ubuntu', sans-serif;
        font-size: bolder;
        text-align: left;

    }   
    .search151-each {
        margin: 0 auto;
        margin-top: 2vh;
        width: 60vw;
        background-color: white;
        padding: 10px 10px 10px 10px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgb(201, 178, 157);
        display: flex;
        flex-direction: row;
        align-items: center;
        position: relative;
    }
    .search151-each > img {
        height: 120px;
        width: 100px;
        margin: 0 5% 0 0;
    }
    .search1512 > p {
        text-align: justify;
        font-size: 20px;
        margin-top: 10px;
    }
    .action {
        width: 50px;
        margin: 10px;
    }
    .action > img {
        width: 50%;
    }

    .action-box{
        margin-left: 10%;
        position: absolute;
        right: 0;
        background-color: white;
    }

    .tag{
        border: solid 3px rgb(238, 177, 97);
        border-radius: 5px;
        padding: 2px 5px 2px 5px;
        margin: 0 5px 10px 5px;
        font-size: 80%;
        font-family: 'Comfortaa', cursive;
        font-weight: bolder;
        display: inline-block;
    }


    .loader {
        width: 48px;
        height: 48px;
        border: 3px solid #FFF;
        border-radius: 50%;
        display: inline-block;
        position: relative;
        box-sizing: border-box;
        animation: rotation 1s linear infinite;
        margin-top: 5%;
    }
    .loader::after {
    content: '';  
    box-sizing: border-box;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 56px;
    height: 56px;
    border-radius: 50%;
    border: 3px solid;
    border-color: #FF3D00 transparent;
    }

    @keyframes rotation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
    } 

    @media screen and (max-width: 1500px) {
        .search1512{
            margin-right: 10%;
        }
    }

    
    @media screen and (max-width: 1200px) {
        .logo-img {
            width: 100px;
        }
        .search11 > img {
            width: 30vw;
        }
        .search12 > h1 {
            font-size: 40px;
        }
        .search13 > input {
            width: 90vw;
        }
        .search151-each {
            width: 90vw;
        }
        .all-tags {
            margin: 0 5vw;
        }

        .search1512 > h1{
            font-size: 170%;
        }

        .search1512 > p{
            font-size: 100%;
            text-align: left;
        }

        .search14 {
        width: 60vw;
        }

        .loader {
            width: 30px;
            height: 30px;
        }

        .loader::after {
            width: 36px;
            height: 36px;
        }
    }
    @media screen and (max-width: 900px) {
          .input-options {
              width: 300px;
          }

        .search151-each > img {
            height: 100px;
            width: 80px;
        }

        .tag{
            margin-bottom: 5px;
            border-width: 2px;
        }

        .action {
            width: 40px;
        }

        .all-tags > input{
            font-size: 100%;
            width: 170px;
        }

        .input-options > span{
            font-size: 100%;
        }

        .each-tag {
            font-size: 100%;
        }

        .no_search{
            font-size: 100%;
        }


    }
    @media screen and (max-width: 600px) {
        .logo-img {
            width: 50px;
        }
        .search11 > img {
            width: 200px;
        }
        .input-options {
            width: 90vw;
        }
        .search14 {
            padding: 1px;
            width: 70vw;
        }
        .all-tags {
            margin: 0 5vw;
        }
        .all-tags > input {
            max-width: 80%;
        }
        .search12 > h1 {
            font-size: 24px;
        }
        .search13 > input {
            width: 90vw;
            padding: 10px 10px;
            font-size: 16px;
        }
        .search13 > a > img {
            width: 22px;
        }
        .search151-each > img {
            width: 20%;
        }
        .search1512 > h1 {
            font-size: 15px;
        }
        .search1512 > p {
            font-size: 10px;
            text-align: left;
        }
        .search151-each {
            padding: 5px 40px 5px 5px;
        }
        .likes {
            width: 30px;
        }
        .likes > span {
            font-size: 10px;
        }

    }


    @media screen and (max-width: 500px) {
        .header{
            height: 12vh;
        }

        .action {
            width: 30px;
        }  

        .search151-each > img {
            height: 80px;
            width: 60px;
        }

        .all-tags > input{
            font-size: 80%;
            width: 200px;
        }

        .input-options > span{
            font-size: 80%;
        }

        .each-tag {
            font-size: 80%;
        }

        .each-tag > img{
            width: 12px;
        }

        .search14{
            width: 85vw;
        }

         .tag{
            margin-bottom: 3px;
            border-width: 1px;
            border-radius: 3px;
        }

        .search1512 > h1{
            margin-top: 0;
        } 

        .search12 > h1 {
            letter-spacing: 2px;
        }

        .search1512 > h1{
            font-size: 110%;
        }

        .search1512 > p{
            font-size: 80%;
            text-align: left;
        }
    }
</style>