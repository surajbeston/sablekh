<template>
    <div class="favlib-main mxw-100-mnh-100">
        <Header />
        <div class="favlib-wrapper">

            <img src="@/assets/ill2.png" alt="vector" class="top-img">

            <h1>Favourite Libraries</h1>

            <div :key="lib.id" v-for="lib in libraries" class="each-libs">
                <button @click="remove_clicked(lib)" class="remove">Remove</button>
                <img class="lib-img" @click="lib_clicked(lib)"  :src="lib.thumbnail" alt="book image">
                <div class="lib-info" @click="lib_clicked(lib)" >
                    <span class="lib-name">{{lib.title}}</span>
                    <span class="lib-desc">{{lib.description}}</span>
                </div>
                <div class="likes-div">
                    <div class="likes">
                        <span>{{lib.likes}}</span>
                        <img src="@/assets/like.png" alt="like-img">
                    </div>
                    <div class="downloads">
                        <span>{{lib.downloads}}</span>
                        <img src="@/assets/download1.png" alt="download img">
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>

import axios from "axios";

export default {

    data(){
        return{
            server_address: "https://api.sablekh.com",
            libraries: [],
            page: 0,
            total_page: 0,
            is_axios: false,
        }
    },
    methods: {
        remove_clicked(lib){
            axios({
                method: 'delete',
                url: this.server_address + "/favourite-library",
                headers: {
                ...this.implicit_data()
                },
                data: {
                "hid": lib.hid
                }
            })
            .then(res => {
                // //.log(res)
                // this.is_fav = !this.is_fav
                window.location.reload()
            })
        },

        lib_clicked({link_str}){
            window.location.href = '/library/' + link_str
        },

        check_token(){
            this.token = window.localStorage.getItem('token');
            if (!this.token) {
                window.location.href = "/login";
            }
        },

        return_libs(raw_data){
            return raw_data.map(e => {
                return {
                    ...e.library,
                    likes: e.likes,
                    downloads: e.downloads
                }
            })
        },

        implicit_data(){
          return { Authorization: "Token " + this.token , "site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
        }

    },
    mounted(){

        this.check_token();

        axios({
           url: this.server_address + '/favourite-library',
           method: 'post',
           headers: this.implicit_data(),

        })
        .then(res => {
            // //.log(res.data)
            this.page = res.data.page
            this.total_page = res.data.total_page
            this.libraries = this.return_libs(res.data.data)

        })


        window.addEventListener("scroll" ,(e) => {
            if (window.innerHeight - window.scrollY < 200 ) {
                if (this.page < this.total_page && !this.is_axios) {
                    this.is_axios = true
                    axios({
                        url: this.url+ 'all-libraries',
                        method: 'post',
                        headers: {
                                Authorization: "Token " + this.token, 
                                ...this.implicit_data()
                            },
                        data: {
                            page: this.page + 1
                        }
                    })
                    .then(res => {
                        this.libraries = this.libraries.concat(this.return_libs(res.data.data))
                        this.total_page = res.data.total_pages
                        this.page = res.data.page
                        this.is_axios = false
                    })
                    .catch(e => {
                        // if (e.response.status == 404){
                        //     this.no_library = true
                        //     this.loader_on = false
                        // }
                        
                    })
                }
            }
        })

    }
    
}
</script>

<style scoped>

.remove {
    border: none;
    outline: none;
    position: absolute;
    padding: 5px 10px;
    cursor: pointer;
    right: 0;
    top: 0;
    background-color: rgb(255, 158, 32);
    border-top-right-radius: 10px;
}

.top-img {
    margin: 5vh 0;
}

.likes > img,
.downloads > img {
    height: 50%;
    margin-left: auto;
}

.likes,
.downloads {
    width: 30%;
    display: flex;
    flex-direction: row;
    height: 30px;
}

.likes-div {
    width: 20%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

    .lib-name {
        font-size:  180%;
        font-family: 'Rajdhani', sans-serif;
        letter-spacing: 1px;
        font-weight: 500;
    }

    .lib-desc {
        font-size: 100%;
        font-family: 'Comfortaa', cursive;
    } 


    .lib-info {
        width: 75%;
        padding: 0 2%;
        display: grid;
        flex-direction: column;
    }

    .lib-img {
        max-width: 15%;
        height: 115px;
        align-self: center;
    }

    .each-libs {
        background-color: white;
        margin-top: 1vh;
        margin-bottom: 1vh;
        border-radius: 10px;
        padding: 10px;
        display: flex;
        flex-direction: row;
        width: 50%;
        cursor: pointer;
        position: relative;
    }

    h1 {
        font-size: 250%;
        font-family: 'Staatliches', cursive;
        letter-spacing: 2px;
        margin-bottom: 5vh;
    }

    .favlib-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 5vh 5vw;
    }

    .favlib-main {
        background-color: rgb(255, 236, 211);
    }

    @media screen and (max-width: 1200px){
    .each-libs {
        width: 80%;
    }
}

@media screen and (max-width: 900px){
    .each-libs {
        width: 100%;
    }
    .likes,
    .downloads {
        width: 40%;
    }
}

@media screen and (max-width: 500px) {
    .top-img {
        width: 70%;
    }
    .likes-div {
        padding-top: 20px;
        width: 50%;
    }
    h1  {
        font-size: 150%;
    }
    .lib-name {
        font-size: 100%;
    }
    .lib-desc {
        font-size: 80%;
    }
    .lib-info {
        width: 85%;
    }
    .lib-img {
        height: 70px;
    }
}


</style>