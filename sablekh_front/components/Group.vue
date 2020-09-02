<template>
    <div class="group-main mxw-100-mnh-100">
        <Header />
        <div v-show="!is_deleting" class="group1">
           <img class="top-img" src="@/assets/library/library-top.png" alt="image"> 
           <span class="username">{{username}}</span>
           <span class="create-group">{{create_or_update}} your Group</span>
           <div id = "errorBox" v-show="hasError" ><p id = "errorTxt"> {{error}}<img src = "@/assets/cancel.png" @click="hasError =!hasError" class = "cancelError"></p></div>
           <div class="input-div">
               <label for="name">Name</label>
               <input type="text" v-model="name" id="name" autofocus>
               <label for="description">Description</label>
               <textarea v-model="description" id="description" rows="7 "></textarea>
           </div>
           <div class="search-section">
               <input type="text" v-model="search" id="search" placeholder="Search for Library" @keyup.enter="search_clicked">
               <img src="@/assets/search/search.png" alt="icon" class="search-icon" @click="search_clicked">
           </div>

            <span v-show="check_len" class="av-lib">Available Libraries</span>

            <div v-show="check_len" class="results-section">
               <div :key="lib.hid" v-for="lib in selected_libs" class="each-lib">
                   <div class="each1">
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
                   <div class="each2">
                       <div @click="checkbox_clicked(lib.hid)" class="check-box">
                           <img v-show="show_tick(lib.hid)" src="@/assets/tick.png" alt="tick" class="tick">
                       </div>
                   </div>
               </div>
           </div>
           <button class="btn create-btn" @click="create_clicked">{{create_or_update}}</button>
           <button v-show="show_delete" class="btn delete-btn" @click="delete_clicked">Delete</button>
        </div>
        <div v-show="is_deleting" class="alert-box">
            <h3>Are you sure, you wanna delete this?</h3>
            <div class="buttons">
                <button class="btn yes-btn" @click="yes_button">Yes</button>
                <button class="btn no-btn" @click="no_button">No</button>
            </div>
        </div>
    </div>
</template>

<script>

import axios from "axios";
import Fuse from "fuse.js";

export default {
    data() {
        return{
            url: "http://104.248.39.254/",
            username: "",
            name: "",
            description: "",
            search: "",
            available_libs: [
                // {
                //     id: 1,
                //     image: "",
                //     title: "ANSI C",
                //     description: "lorem sadf asdf adsfjadfasdjf fkjgnsdfg jsirsf sfg asjfksdfg dfgnsdf gsldfgs fdgsdfg",
                //     selected: false,
                //     likes: 1,
                //     downloads: 1,
                // },
                // {
                //     id: 2,
                //     image: "",
                //     title: "ANSI C",
                //     description: "lorem sadf asdf adsfjadfasdjf fkjgnsdfg jsirsf sfg asjfksdfg dfgnsdf gsldfgs fdgsdfg",
                //     selected: true,
                //     likes: 3,
                //     downloads: 3,
                // },
            ],
            selected_libs: [],
            checked_libs: [],
            is_deleting: false,
            hid: "",
            tags: [],
            is_axios: false,
            hasError: false,
            error: "Aejhg kj kug"
        }
    },

    methods: {

        no_button(){
            this.is_deleting = false;
        },

        yes_button(){
            axios({
                url: this.url + "library-group",
                method: 'delete',
                headers: {
                    Authorization: "Token " + this.token, 
                    ...this.implicit_data()
                },
                data: {
                    hid: this.hid,
                }
            })
            .then(res => {
                window.location.href = "/"
            })
            .catch(e => console.log(e))
        },

        delete_clicked() {
            window.scrollTo(0, 0)
            this.is_deleting = true;
        },
        create_clicked(){
            if (this.check_len) this.displayError("Please add some library to create a group.")
            else if (!this.check_name_des) this.displayError("Please add name and description to create a group.")
            else{
                axios({
                    url: this.url + "library-group",
                    method: this.give_method,
                    headers: {
                        Authorization: "Token " + this.token, 
                        ...this.implicit_data()
                    },
                    data: {
                        hid: this.hid,
                        title: this.name,
                        description: this.description,
                        tags: this.tags,
                        libraries: this.checked_libs.join(",")

                    }
                })
                .then(res => {
                    window.location.href = "/create-group/" + res.data.link_str;
                })
                .catch(e => console.log(e))
           }
        },
        checkbox_clicked(id) {
            var filter_list = this.checked_libs.filter(e => e === id)
            if (filter_list.length === 0) {
                this.checked_libs.push(id)
            }
            else {
                this.checked_libs = this.checked_libs.filter(e => e !== id)
            }
        },
        search_clicked(){
            this.selected_libs = this.fuse.search(this.search)
            this.selected_libs = this.selected_libs.map(e => e.item)
            this.checked_libs.forEach(id => {
                if (this.selected_libs.filter(e => e.hid === id).length == 0) {
                    this.selected_libs.push(this.available_libs.filter(e => e.hid === id)[0])
                }
            })
        },
        show_tick(id){
            return this.checked_libs.includes(id) 
        },
        implicit_data(){
          return {"site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
        },
        check_lib(){
            if (this.$route.params.id) {
                axios({
                    url: this.url + "get-library-group",
                    method: 'post',
                    headers: {
                        Authorization: "Token " + this.token, 
                        ...this.implicit_data()
                    },
                    data: {
                        link_str: this.$route.params.id
                    }
                })
                .then(res => {
                    // console.log(res)
                    this.name = res.data.title
                    this.description = res.data.description
                    this.checked_libs = res.data.libraries.map(lib => lib.hid)
                    this.hid = res.data.hid
                    this.tags = res.data.tags

                    var user_libs = this.available_libs.map(e => e.hid)
                    if (!user_libs.includes(this.checked_libs[0])) {
                        window.location.replace("/group")
                    }
                })
                .catch(e => {
                    alert("library not available")
                })
            }
        },
        displayError(errorText){
                this.hasError = true
                this.error = errorText
                document.body.scrollTop = 0
                document.documentElement.scrollTop = 0
        },
    },

    computed: {
        create_or_update(){
            return (this.show_delete) ? "Update" : "Create";
        },
        show_delete(){
            return (this.$route.params.id) ? true : false;
        },
        give_method() {
            if (this.$route.params.id) {
                return "patch"
            }
            return "post"
        },
        check_len() {
            return this.available_libs.length > 0
        },
        check_name_des(){
            return this.name.length > 0 && this.description.length > 0
        }
    },

    mounted() {
        this.token = window.localStorage.getItem("token")
        if (!this.token) { 
            window.location.href = "/login"
        }
        this.username = window.localStorage.getItem("username")

        axios({
            url: this.url + "all-libraries",
            method: 'post',
            headers: {
                Authorization: "Token " + this.token, 
                ...this.implicit_data()
            }
        })
        .then(res => {
            this.page = res.data.page
            this.total_page = res.data.total_pages
            this.available_libs = res.data.data
            this.selected_libs = res.data.data
            this.fuse = new Fuse(this.available_libs, {
            keys: ['title', 'description']
            })

            this.check_lib()

        })
        .catch(err => console.log(err))


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
                        this.available_libs = this.available_libs.concat(res.data.data)
                        this.selected_libs = this.selected_libs.concat(res.data.data)
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

.alert-box {
        width: 50%;
        padding: 2%;
        text-align: center;
        display: flex;
        flex-direction: column;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 5px 10px rgb(197, 165, 124);
        margin: 30vh auto;
    }

    .buttons {
        display: inline;
    }

    .yes-btn {
        background-color: white;
        border: black solid 2px;
        cursor: pointer;
    }

    .no-btn {
        margin-left: 2%;
        margin-top: 2%;
        background-color: rgb(255, 176, 98);
        border: rgb(255, 176, 98) solid 2px;
        cursor: pointer;
    }


.delete-btn {
    font-size: 20px;
    border-radius: 5px;
    padding: 10px 30px;
    margin-top: 2vh;
    background-color: rgb(255, 127, 22);
    cursor: pointer;
}

.create-btn {
    font-size: 20px;
    border-radius: 5px;
    padding: 10px 30px;
    margin-top: 2vh;
    background-color: rgb(255, 178, 78);
    cursor: pointer;
}

.tick {
    width: 70%;
    
}

.check-box {
    width: 50px;
    height: 50px;
    background-color: rgb(255, 174, 68);
    border-radius: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

.each2 {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
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

    #name #description{
        font-family: 'Ubuntu', sans-serif;
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


    #errorBox{
        background-color: rgba(255, 0, 0, 0.4);
        color: rgb(51, 47, 43);
        border: 1px black solid;
        border-radius: 5px;
        padding : 1%;
        font-size: 110%;
        font-family: 'Rajdhani', sans-serif;
        font-weight: bolder;
        animation-name: fadein;
        animation: fadein 1s;
    }

    @keyframes fadein {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

    .cancelError{
        cursor: pointer;
        right: 0;
        float: right;
        margin-left: 10px;
    }

.each1 {
    background-color: white;
    margin-top: 1vh;
    margin-bottom: 1vh;
    border-radius: 10px;
    padding: 10px;
    display: flex;
    flex-direction: row;
}

.each-lib {
    display: grid;
    grid-template-columns: 10fr 1fr;
    width: 60%;
    height: 150px;
    grid-column-gap: 1vw;
}

.results-section {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.av-lib {
    font-size: 200%;
    font-weight: bold;
    letter-spacing: 1px;
    margin: 5vh 0;
}

.search-icon {
    position: absolute;
    width: 5%;
    right:3%;
    top:13%;
    cursor: pointer;
}

#search {
    text-align: center;
    width: 100%;
    font-size: 150%;
    padding: 10px ;
    border-radius: 50px;
    border: none;
    outline: none;
    box-shadow: 0 5px 10px rgb(204, 187, 165);
    letter-spacing: 1px;
    padding-right: 70px;
}

.search-section {
    width: 40%;
    position: relative;  
}

#name,
#description {
    background: transparent;
    font-size: 130%;
    padding: 10px ;
    border-radius: 10px;
    outline: none;
    border: 1px solid rgb(161, 134, 97);
    letter-spacing: 1px;
}

label {
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 2px;
    font-size: 160%;
    margin-top: 3vh;
    margin-bottom: 1vh;
}

.input-div {
    display: flex;
    flex-direction: column;
    width: 50%;
    margin-bottom: 5vh;
}

.create-group {
    font-family: 'Staatliches', cursive;
    letter-spacing: 3px;
    font-size: 250%;
    margin-top: 2vh;
}

.username {
    font-family: 'Comfortaa', cursive;
    font-weight: bold;
    letter-spacing: 1px;
    font-size: 140%;
    margin-top: 1vh;
}

.top-img {
    width: 20%;
}

.group1 {
    width: 100%;
    display: flex;
    flex-direction: column; 
    align-items: center;
}

.group-main {
    background-color: rgb(254, 227, 200);
    padding-bottom: 5vh;
}

@media screen and (max-width: 1500px){

    .search-section {
        width: 55%;
    }

}


@media screen and (max-width: 1200px){
    .each-lib {
        width: 90%;
    }
    .input-div {
        width: 90%;
    }
    .search-section {
        width: 65%;
    }
}

@media screen and (max-width: 900px){

    .likes,
    .downloads {
        width: 40%;
    }

    .top-img {
        width: 40%;
    }

    .search-section {
        width: 90%;
    }
    .check-box {
        width: 40px;
        height: 40px;
    }


}


@media screen and (max-width: 700px){

    .lib-name {
        font-size: 150%;
    }

    .lib-desc {
        font-size: 80%;
    }

    .likes,
    .downloads {
        width: 50%;
    }

    .check-box {
        width: 30px;
        height: 30px;
    }

    .search-icon {
        width: 30px;
    }

}

@media screen and (max-width: 500px){

    .each-lib {
        height: 100px;
    }
    .lib-name {
        font-size: 15px;
    }



    .likes,
    .downloads {
        width: 100%;
    }

    .top-img {
        width: 80%;
    }

    .username {
        font-size: 100%;
    }

    .create-group {
        font-size: 150%;
    }
    .lib-img {
        height: 60px;
    }
    .lib-info {
        width: 85%;
    }

    #search {
        font-size: 100%;
    }
    .search-icon {
        width: 25px;
    }

    #errorBox{
        margin-left: 5%;
        margin-right: 5%;
    }

}


</style>