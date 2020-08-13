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
                <h1>Search any PDFs here</h1>
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
                        <img src="@/assets/cancel.png" alt="loading image" :id="tag" @click="cancel_button">
                    </div>
                    <input  type="text" v-model="current_tag" id="current-tag" @input="current_tag_changed" placeholder="Add tags here" autocomplete="off">
                </div>
            </div>
            <div v-show="show_suggessions" class="input-options">
                <span :key="option.item" v-for="option in avialable_tags" @click="options_clicked">
                    {{option.item}}
                </span>
            </div>
            <div class="search15">
                <h2 @click="to_link" id="to">{{this.get_name}}</h2>
            </div>
            <div id="results-div" class="search15">
                <NuxtLink :to="`library/${book.link_str}`" v-bind:key="book.hid" v-for="book in search_books" >
                    <div class="search151">
                        <div class="search151-each">
                            <img :src="image_address" alt="loading image">
                            <div class="search1512">
                                <h1>{{book.title}}</h1>
                                <p>{{book.description}}</p>
                            </div>
                            <div class="likes">
                                <span>{{likes}}</span>
                                <img src="@/assets/like.png" alt="like">
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
            server_address: "https://api.sablekh.com",
            image_address: "https://pngimg.com/uploads/book/book_PNG51083.png",
            show_suggessions: true,
            off_width: 0,
            current_tag: "",
            tags: [],
            avialable_tags: [],
            all_tags: [
                'Science',
                'Math',
                'Social',
                'English',
                'Dont think of this'
            ],
            search: "",
            search_books: [],
            likes: 100,
        }
    },

    methods: {

        add_to_localstorage(name, data) {
            let s = false
            try {
                window.localStorage.setItem(name, JSON.stringify(data))
                s = true
            }
            catch {}
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
            
            if (this.search != "") {
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
                    this.search_books = res.data
                    this.add_to_localstorage("search", res.data)
                })
                .catch(err => {
                    console.log(err)
                })
            }
        },
        to_link() {
            this.get_link ? window.location.replace("/upload") : window.location.replace("/login");
        },
        implicit_data(){
          return {"site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
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

        this.time = new Date().getTime();

        this.fuse = new Fuse(this.all_tags, {}) 

        this.search_books = this.retrive_from_localstorage("search")
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
        font-size: 2.5vw;
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
        min-width: 30vw;
        display: flex;
        justify-content: center;
        border-radius: 10px;
        background-color: white;
        padding: 5px 0;
    } 
    .all-tags {
        min-width: 10px;
        background-color: white;
        display: flex;
        flex-wrap: wrap;
        margin: 0 1vw;
    }
    .all-tags > input {
        min-width: 30vw;
        font-size: 20px;
        padding: 10px 20px;
        border: none;
        outline: none;
    }
    .each-tag {
        border-radius: 5px;
        position: relative;
        background-color: rgb(238, 177, 97);
        margin: 5px;
        padding: 5px 30px;
        border-radius: 5px;
        font-size: 18px;
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
    }
    .search151-each {
        margin: 0 auto;
        margin-top: 2vh;
        width: 60vw;
        background-color: white;
        padding: 10px 70px 10px 10px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgb(201, 178, 157);
        display: flex;
        flex-direction: row;
        align-items: center;
        position: relative;
    }
    .search151-each > img {
        height: 10vw;
        margin: 0 5vw 0 0;
    }
    .search1512 > p {
        text-align: justify;
        font-size: 20px;
        margin-top: 10px;
    }
    .likes {
        width: 50px;
        display: flex;
        flex-direction: column;
        position: absolute;
        right: 0;
    }
    .likes > img {
        width: 50%;
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
    }
    @media screen and (max-width: 900px) {
          .input-options {
              width: 300px;
          }
    }
    @media screen and (max-width: 600px) {
        .logo-img {
            width: 70px;
        }
        .search11 > img {
            width: 200px;
        }
        .input-options {
            width: 90vw;
        }
        .search14 {
            padding: 1px;
            width: 98%;
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
</style>