<template>
    <div class="wrapper mxw-100-mnh-100">
        <Header />
        <div class="libs">
            
            <div class="fav">
                <!-- here to add star -->
                <img @click="fav_clicked" @mouseenter="fav_in" @mouseleave="fav_out" v-show="!is_fav" src="@/assets/star1.png" alt="fav" class="star1">
                <img @click="fav_clicked" @mouseenter="fav_in" @mouseleave="fav_out" v-show="is_fav" src="@/assets/star2.png" alt="fav" class="star2">
                <img @click="copy" id="copy" @mouseenter="fav_in" @mouseleave="fav_out" src="@/assets/copy1.png" alt="copy" class="copy-img">
            </div>
            <div v-show="show_fav_desc" class="fav-desc">
                <span>{{fav_desc_text}}</span>
            </div>

          <div id = "successBox" v-show="hasSuccess" ><p id = "successTxt"> {{success}}<img src = "@/assets/cancel.png" @click="hasSuccess =!hasSuccess" class = "cancelSuccess"></p></div>

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
            
            <div :key="lib.id" v-for="lib in up_libraries" @click="lib_clicked(lib)" class="each-libs">
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
            server_address: "https://api.sablekh.com",
            group: {},
            show_fav_desc: false,
            is_fav: false,
            authenticated: false,
            is_copy: false,
            hasSuccess: false,
            success: "",
            libs: [],
        }
    },
    methods: {

        async copy() {
            await navigator.clipboard.writeText(window.location.href);
            this.show_success("Link Copied. Share it now!")
        },

        show_success(successTxt){     
            this.hasSuccess = true
            this.success = successTxt
            document.body.scrollTop = 0
            document.documentElement.scrollTop = 0
        },

        check_if_fav(){
            axios({
                method: 'post',
                url: this.server_address + "/check-favourite-library-group",
                headers: {
                ...this.implicit_data(),
                Authorization: "Token " + this.token
                },
                data: {
                "hid": this.group.hid
                }
            })
            .then(res => {
                // console.log(res.data)
                this.is_fav = res.data.exists;
            })
            .catch(e => {
                // console.log(e.response)
            })
        },

        fav_in(e){
            if(e.target.id === 'copy') {
                this.is_copy = true
            }
            this.show_fav_desc = true
        },
        fav_out(){
            this.is_copy = false
            this.show_fav_desc = false

        },

        fav_clicked(){
        
        axios({
            method: this.get_method,
            url: this.server_address + "/favourite-library-group",
            headers: {
            ...this.implicit_data(),
            Authorization: "Token " + this.token
            },
            data: {
            "hid": this.group.hid
            }
        })
        .then(res => {
            // console.log(res)
            this.is_fav = !this.is_fav
        })
        

        },


        lib_clicked(lib){
            window.location.href = '/library/' + lib.link_str;
        },
        implicit_data(){
          return {"site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
        }
    },

    mounted() {

        this.token = window.localStorage.getItem("token")
        if(this.token) {S
            this.authenticated = true
        }


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
            this.libs = res.data.libraries
            this.check_if_fav()

        })
        .catch(err => {
            // console.log(err)
        })



    },
    computed: {
        up_libraries(){
            var libraries =  Object.values(this.libs)
            for (var library of libraries){
                if (library.title.length > 50) library.title = library.title.slice(0, 47) + "..."
                if (library.description.length > 70) library.description = library.description.slice(0, 67) + "..."
            }
            return libraries
        },

        get_method(){
            return (this.is_fav) ? "delete"  : "put";
        },

        fav_desc_text(){
            if(this.is_copy) return "Copy Link";
            else return (this.is_fav) ? "Remove from Favourites" : "Add to Favourites";
        }
    }



}
</script>

<style scoped>

    #successBox{
      background-color: rgba(134, 190, 87, 0.4);
      color: rgb(51, 47, 43);
      border: 1px black solid;
      border-radius: 5px;
      padding : 1%;
      font-size: 110%;
      font-family: 'Rajdhani', sans-serif;
      font-weight: 200;
      animation-name: fadein;
      animation: fadein 1s;
      width: 50%;
      animation-name: fadein;
      animation: fadein 1s;
    }
    .cancelSuccess{
      cursor: pointer;
      float: right;
  }
    @keyframes fadein {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

    .fav {
        margin-left: auto;
        width: 100px;
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .fav-desc {
        background-color: rgb(241, 241, 241);
        padding: 10px 20px;
        border-radius: 5px;
        position: absolute;
        right: 5vw;
        top: 100px;
        font-size: 80%;
        font-family: 'Comfortaa', cursive;
    }

    .copy-img {
        width: 40px;
        height: 42px;
    }
    .star1,
    .star2 {
        width: 50px;
        cursor: pointer;
    }


    .wrapper {
        background-color: rgb(255, 231, 199);
    }

    .libs {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 5vh 5vw;
        position: relative;
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
    text-align: justify;

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
    width: 20%;
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
    .tags {
        width: 90%;
    }
}

@media screen and (max-width: 700px){
#successBox{
    width: 85%;
    padding: 2%;
  }
    .fav-desc {
        /* margin-bottom: 20px; */
        padding: 5px 10px;
        font-size: 60%;
        /* top: 9vh; */
    }
}

@media screen and (max-width: 500px) {
    #successBox{
    width: 95%;
    padding: 2%;
  }
    .fav {
        width: 80px;
    }
    /* .fav-desc {
        top: 0px;
    } */
    .star1,
    .star2 {
        width: 40px;
        height: 38px;
    }
    .copy-img {
        width: 35px;
        height: 35px;
    }

    .likes-div {
        width: 50%;
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
        /* display: none; */
        height: 70px;
    }
    .title {
        font-size: 200%;
    }
    .avai-libs {
        font-size: 200%;
    }
}

</style>