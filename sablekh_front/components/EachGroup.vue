<template>
    <div class="wrapper mxw-100-mnh-100">
        <Header />
        <div class="libs">
            <span class="title">
                {{group.title}}
            </span>
            <span class="desc">
                {{group.description}}
            </span>
            <div class="tags">
                <span class="each-tag" :key="tag" v-for="tag in group.tags">
                    {{tag}}
                </span>
            </div>

            <span class="avai-libs">Libraries</span>
            
            <div :key="lib.id" v-for="lib in group.libraries" @click="lib_clicked(lib)" class="each-libs">
                <img class="lib-img"  src="@/assets/search/book2.png" alt="book image">
                <div class="lib-info">
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
    
    data() {
        return {
            server_address: "http://104.248.39.254",
            group: {}
        }
    },
    methods: {
        lib_clicked(lib){
            window.location.href = '/library/' + lib.link_str;
        },
        implicit_data(){
          return {"site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
        }
    },

    computed: {
    },

    mounted() {

        axios({
           url: this.server_address + '/get-library-group',
           method: 'post',
           headers: this.implicit_data(),
           data: {
               link_str: this.$route.params.id
           }

        })
        .then(res => {
            this.group = res.data
        })
        .catch(err => {
            console.log(err)
        })


    }



}
</script>

<style scoped>
    .wrapper {
        background-color: rgb(255, 231, 199);
    }

    .libs {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 5vh 0;
    }

    .title {
        font-size: 250%;
        letter-spacing: 1px;
        font-family: 'Staatliches', cursive;
        margin-bottom: 2vh;
    }
    .desc {
        font-size: 120%;
        margin-bottom: 5vh;
        font-family: 'Comfortaa', cursive;
    }

    .tags {
        margin-bottom: 2vh;
        display: flex;
        flex-wrap: wrap;
        max-width: 50%;
    }

    .avai-libs {
        font-size: 250%;
        letter-spacing: 1px;
        font-family: 'Staatliches', cursive;
        margin: 2vh;
    }

    .each-tag {
        font-family: 'Comfortaa', cursive;
        padding: 10px 20px;
        border: 1px solid rgb(250, 168, 61);
        border-radius: 5px;
        margin: 0 5px 5px 5px;
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
    width: 15%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.lib-name {
    font-size: 170%;
    font-family: 'Staatliches', cursive;
    letter-spacing: 1px;
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

@media screen and (max-width: 1200px){
    .each-libs {
        width: 70%;
    }
}

@media screen and (max-width: 900px){
    .each-libs {
        width: 90%;
    }

    .likes,
    .downloads {
        width: 40%;
    }
    .tags {
        width: 90%;
    }
}

@media screen and (max-width: 500px) {
    .lib-info {
        width: 85%;
    }
    .lib-img {
        display: none;
    }
    .title {
        font-size: 200%;
    }
    .avai-libs {
        font-size: 200%;
    }
}

</style>