<template>
    <div class="my-library-component mxw-100-mnh-100">
        <div class="header">
            <img src="@/assets/back-arrow.png" alt="back img" class="back-img">
            <img src="@/assets/sablekh.png" alt="loading img" class="logo-img">
        </div>
        <div class="my-library-wrapper1">
            <img class="top-img" src="@/assets/library/library-top.png" alt="vector img">
            <h1 class="your-library">
                Your Library
            </h1>
            <p class="email">
                dummy@gmail.com
            </p>

            <div class="ml-libraries">
                <div class="each-library" :key="library.hid" v-for="library in libraries">
                    <button class="btn edit-btn">
                        Edit
                    </button>
                    <img src="@/assets/search/book2.png" alt="loading image" class="book-img">
                    <div class="library-info">
                        <h1>{{library.title}}</h1>
                        <p>{{library.description}}</p>
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
            libraries: [
                {
                    hid: "asdfasdfasdf",
                    title: "ANSI C",
                    description: "asdfj asdf as dfas dfas df as df as df   sdf asdfasdf asdf asd fasdf asdfasd fasdfasdf asdfasdf asdfa sdfasdfasdf."
                },
                {
                    hid: "asdfavsdfasdf",
                    title: "ANSI C",
                    description: "asdfj asdf as dfas dfas df as df as df   sdf asdfasdf asdf asd fasdf asdfasd fasdfasdf asdfasdf asdfa sdfasdfasdf."
                }
            ]
        }
    },

    methods: {
        implicit_data(){
          return {"site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
      }
    },


    mounted() {

      this.time = new Date().getTime()


        var id = window.localStorage.getItem("token")
        if (!id) {
            window.location.replace("/login")
        }
        console.log(id)

       axios({
           url: this.server_address + '/all-libraries',
           headers: {
               "Authorization": "Token " + id
           }
       })
       .then(res => {
           this.libraries = res.data
       })
       .catch(e => {
           console.log(e)
        //    alert("Internal Error please try again later")
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
    }

    .email {
        font-size: 150%;
        font-style: italic;
        letter-spacing: 1px;
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
        width: 50%;
    }

    .library-info > h1 {
        font-size: 150%;
        margin: 0;
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
    }
}

@media screen and (max-width: 700px) {
    .each-library {
        padding: 5% 1%;
        width: 95%;
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
    .each-library {
        padding-left: 10px;
        grid-template-columns: 10fr 2fr;
    }
    .book-img {
        display: none;
    }
    .library-info > h1 {
        margin-bottom: 5px;
    }
    .library-info > p {
        font-size: 12px;
    }

}

</style>