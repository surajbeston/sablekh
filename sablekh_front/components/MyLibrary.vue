<template>
    <div class="my-library-component mxw-100-mnh-100">
        <div class="header">
            
            <img src="@/assets/sablekh.png" alt="loading img" class="logo-img">
        </div>
        <div class="my-library-wrapper1">
            <img class="top-img" src="@/assets/library/library-top.png" alt="vector img">
            <h1 class="your-library">
                Your Library
            </h1>
            <p class="email">
                {{email}}
            </p>

            <span class="loader" v-show="loader_on"></span>
            <div v-show="!loader_on">
                <h2  v-show="no_library" class = "no_library">No libraries found, please upload to find it here.</h2>
                <div class="ml-libraries"  v-show="!no_library"> 
                    <div class="each-library" :key="library.hid" v-for="library in up_libraries">
                        <button @click="edit_clicked(library)" class="btn edit-btn">
                            Edit
                        </button>
                        <img @click="heading_clicked(library.link_str)" :src="library.thumbnail" alt="loading image" class="book-img">
                        <div @click="heading_clicked(library.link_str)" class="library-info">
                            <h1 >{{library.title}}</h1>
                            <p>{{library.description}}</p>
                        </div>
                        <div class="likes-div">
                            <span>{{library.likes}}</span>
                            <img src="@/assets/like.png" alt="like img" class="like-img">
                            <span id="span">{{library.downloads}}</span>
                            <img src="@/assets/download1.png" alt="download img" class="download-img">
                        </div>
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
            libraries: [],
            email: "dummy@sablekh.com",
            no_library: false,
            loader_on: false
        }
    },

    methods: {
        edit_clicked(lib) {
            window.location.href = "upload/" + lib.link_str
        },

        heading_clicked(link_str){
            window.location.href = "library/" + link_str
        },
        implicit_data(){
          return {"Authorization": "Token " + this.id, "site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
        }
    },

    computed: {
        id(){
            var id = window.localStorage.getItem("token")
            if (!id) {
                window.location.replace("/login")
            }
            return id
        },
        up_libraries(){
            var libraries =  Object.values(this.libraries)
            for (var library of libraries){
                if (library.title.length > 50) library.title = library.title.slice(0, 47) + "..."
                if (library.description.length > 70) library.description = library.description.slice(0, 67) + "..."
            }
            return libraries
        }
    },


    mounted() {

      this.time = new Date().getTime()
        this.loader_on = true
        if (window.localStorage.getItem("email")) this.email = window.localStorage.getItem("email")
       axios({
           url: this.server_address + '/all-libraries',
           method: 'post',
           headers: this.implicit_data()
       })
       .then(res => {
           this.loader_on = false
           if (res.data.length == 0){
               this.no_library = true
           }
           this.libraries = []
            res.data.map(lib => {
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
                    })
                    .catch(e => {
                        lib.likes = 0
                    })

                axios({
                    url: this.server_address + "/all-downloads",
                    method: 'post',
                    headers: this.implicit_data(),
                    data: {
                        library: lib.hid
                    }
                })    
                    .then(res => {
                        lib.downloads = res.data.downloads
                        this.libraries.push(lib)
                    })
                    .catch(e => {
                        lib.downloads = 0
                    })
            })
       })
       .catch(e => {
           //.log(e)
       })
    }
}
</script>

<style scoped>
    .my-library-component {
        background-color: rgb(255, 228, 197);
        display: flex;
        flex-direction: column;
    }
    
    .header {
        display: flex;
        width: 100%;
        padding: 10px;
        flex-direction: row;
        align-items: center;
        border-bottom: 1px solid rgb(218, 195, 165);
    }
    .logo-img {
        margin-left: auto;
        width: 10%;
    }
    .back-img {
        width: 50px;
        height: 50px;
        display: none;
    }

    .my-library-wrapper1 {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    .top-img {
        width: 20%;
    }

    .your-library {
        margin: 2% 0;
        padding: 20px 50px;
        border-top: 1px solid rgb(83, 75, 64);
        border-bottom: 1px solid rgb(83, 75, 64);
        font-size: 210%;
        font-family: 'Staatliches', cursive;
        letter-spacing: 5px;
    }

    .email {
        font-size: 150%;
        letter-spacing: 1px;
        font-family: 'Ubuntu', sans-serif;
    }

    .ml-libraries {
        display: flex;
        flex-direction: column;
        width: 100%;
        margin-top: 5%;
    }
   
    .each-library {
        background-color: white;
        width: 50%;
        min-height: 150px;
        margin: 0 auto 1% auto;
        padding: 1%;
        border-radius: 10px;
        display: grid;
        grid-template-columns: 2fr 10fr 2fr;
        align-items: center;
        position: relative;
    }

    .edit-btn {
        position: absolute;
        cursor: pointer;
        top: 0;
        right: 0;
        border-radius: 0 10px 0 0;
        background-color: rgb(255, 170, 58);
    }
    .edit-btn:hover {
        color: white;
        background-color: rgb(153, 110, 55);
    }

    .book-img {
        cursor: pointer;
        width: 80%;
    }
    .library-info {
        cursor: pointer;
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .library-info > h1 {
        font-size: 150%;
        margin: 0;
        font-family: 'Rajdhani', sans-serif;

    }

    .library-info > p {
        margin-top: 5%;
        font-family: 'Ubuntu', sans-serif;
        font-size: 120%;
    }

    .likes-div {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        justify-content: flex-end;

    }

    .likes-div > span {
        margin-right: 10%;
    }
    .download-img {
        width: 18%;
        margin-right: 10%;
    }
    .like-img {
        width: 15%;
        margin-bottom: 5px;
         margin-right: 10%;
    }

    .no_library{
        font-family: 'Rajdhani', sans-serif;
        margin: 5%;
        text-align: center;
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



@media screen and (max-width: 1200px) {
    .logo-img {
        width: 150px;
    }
    .back-img {
        display: block;
    }
    .top-img {
        width: 200px;
    }
    .each-library {
        width: 80%;
        min-height: 120px;
    }
    .edit-btn {
        padding: 5px 20px;
    }

        .loader {
            width: 30px;
            height: 30px;
        }

        .loader::after {
            width: 36px;
            height: 36px;
        }

            .book-img {
        cursor: pointer;
        width: 90%;
        height: 80%;
    }
}

@media screen and (max-width: 700px) {
    .each-library {
        padding: 5% 1%;
        width: 95%;
        min-height: 100px;
        margin-bottom: 3%;
    }
    .library-info > h1 {
        font-size: 18px;
    }
    .library-info > p {
        font-size: 14px;
    }
    .edit-btn {
        font-size: 14px;
        padding: 5px 10px;
    }

    .book-img {
        cursor: pointer;
        width: 90%;
        height: 120%;
    }
}

@media screen and (max-width: 500px){
    .logo-img {
        width: 100px;
    }
    .your-library {
        font-size: 25px;
    }
    .email {
        font-size: 18px;
    }
    /* .each-library {
        padding: 10px 15px;
        grid-template-columns: 10fr 2fr;
    } */
    /* .book-img {
        display: none;
    } */
    .library-info > h1 {
        margin-bottom: 5px;
    }
    .library-info > p {
        font-size: 12px;
    }
    span {
        font-size: 10px;
    }
    .likes-div > span{
        margin-right: 80%;
    }

    .like-img {
        width: 30%;
        margin-right: 80%;
    }
    .download-img {
        width: 30%;
        margin-bottom: 0;
        margin-right: 80%;
    }

    .book-img {
        cursor: pointer;
        width: 90%;
        height: 120%;
    }

}

</style>