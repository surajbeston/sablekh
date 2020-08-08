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
            <!-- <div class="search14">
                <input  type="text" :style="dynamic_padding" v-model="current_tag" id="current-tag" @input="current_tag_changed" placeholder="Add tags here">
                <div v-show="show_suggessions" class="input-options">
                    <span :key="option.item" v-for="option in avialable_tags" @click="options_clicked">
                        {{option.item}}
                    </span>
                </div>
                <div class="all-tags" id="all-tags">
                    <div class="each-tag" v-bind:key="tag" v-for="tag in tags">
                        <span>{{tag}}</span>
                        <img src="@/assets/cancel.png" alt="loading image" :id="tag" @click="cancel_button">
                    </div>
                </div>
            </div> -->
            <div class="search14">
                <div class="all-tags">
                    <div class="each-tag" v-bind:key="tag" v-for="tag in tags">
                        <span>{{tag}}</span>
                        <img src="@/assets/cancel.png" alt="loading image" :id="tag" @click="cancel_button">
                    </div>
                    <input  type="text" v-model="current_tag" id="current-tag" @input="current_tag_changed" placeholder="Add tags here">
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
            <div v-show="is_searched" id="results-div" class="search15">
                <NuxtLink to="library/fasdfasdfasdf" v-bind:key="book.id" v-for="book in search_books" >
                    <div class="search151">
                        <div class="search151-each">
                            <img :src="book.img" alt="loading image">
                            <div class="search1512">
                                <h1>{{book.title}}</h1>
                                <p>{{book.desc}}</p>
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
            show_suggessions: false,
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
            is_searched: false,
            search_books: [
                {
                    id: 1,
                    title: "physics",
                    desc: "fjadfa asdfjasdf asd fadsf asdf asdfasdf asdfasdfasf",
                    img: "data:image/jpeg;base64,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"
                },
                {
                    id: 2,
                    title: "physics",
                    desc: "fjadfa asdfjasdf asd fadsf asdf asdfasdf asdfasdfasf",
                    img: "data:image/jpeg;base64,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"
                },
            ]
        }
    },

    methods: {
        current_tag_changed() {
            this.show_suggessions = true
            this.avialable_tags = this.fuse.search(this.current_tag)
        },
        options_clicked(e) {
            let i = e.target.innerText

            this.current_tag = i

            if (! this.tags.includes(this.current_tag) ) {
                this.tags.push(i)
            }

            this.show_suggessions = false;
            this.current_tag = "";
            this.change_padding()
        },
        cancel_button(e) {
            let i = this.tags.indexOf(e.target.id)
            this.tags.splice(i, 1)
            this.change_padding()
        },
        change_padding() {
            setTimeout(() => {
                this.off_width = document.getElementById("all-tags").offsetWidth
            }, 200);
        },
        search_button() {
            this.is_searched = true;
            // axios.get(`${this.server_address}/search`, {
            //     "query": this.search,
            //     "tags": this.tags
            // })
            // .then()
            // .catch()
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
        // dynamic_padding() {
        //     return {
        //         paddingLeft: `${this.off_width + 10}px`
        //     }
        // },
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
        this.fuse = new Fuse(this.all_tags, {})    
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
        padding-top: 10vh;
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
        background-color: rgba(126, 113, 96, 0.13);
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
    } 
    .all-tags {
        min-width: 10px;
        background-color: white;
        /* border-radius: 10px; */
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
        position: relative;
        background-color: rgb(238, 177, 97);
        margin: 5px;
        padding: 5px 30px 5px 10px;
        border-radius: 5px;
        font-size: 18px;
    }

    .each-tag > img {
        position: absolute;
        right: 5px;
        top: 7px;
        width: 16px;
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

    /* wrapper2  */

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
        width: 50vw;
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgb(201, 178, 157);
        display: flex;
    }
    .search151-each > img {
        width: 100px;
        margin: 0 5vw 0 0;
    }
    .search1512 > p {
        /* text-decoration: none; */
        font-size: 20px;
        margin-top: 10px;
    }

    

    @media screen and (max-width: 1200px) {
        .search11 > img {
            width: 70vw;
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
            /* grid-template-columns: auto auto auto; */
        }
    }
    @media screen and (max-width: 900px) {
        /* .all-tags {
            grid-template-columns: auto auto;
        } */
          .input-options {
              width: 300px;
          }
    }
    @media screen and (max-width: 600px) {
        .search-wrapper1 {
            padding-top: 70px;
        }
        .input-options {
            width: 90vw;
        }
        .search14 {
            width: 98%;
        }
        .all-tags {
            margin: 0 5vw;
            /* grid-template-columns: auto; */
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
            width: 70px;
        }
        .search1512 > h1 {
            font-size: 20px;
        }
        .search1512 > p {
            font-size: 15px;
        }
    }
</style>