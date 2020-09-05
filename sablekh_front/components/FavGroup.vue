<template>
    <div class="favgroup-main mxw-100-mnh-100">
        <Header />

        <div class="favgroup-wrapper">

            <h1>Favourite Groups</h1>

            <div class="each-library" :key="group.hid" v-for="group in groups" @click="group_clicked(group)">
                <img :src="group.thumbnail" alt="loading image" class="book-img">
                <div class="library-info">
                    <h1 >{{group.title}}</h1>
                    <p>{{group.description}}</p>
                </div>
                <div class="group-libs">
                    <img src="@/assets/book.png" alt="book">
                    <span ><b>{{group.no_libraries}}</b></span>
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
            server_address: "http://104.248.39.254",
            groups: [],
            page: 0,
            total_page: 0,
            is_axios: false,

        }
    },
    methods: {

        group_clicked({link_str}) {
            window.location.href = "/group/" + link_str
        },

        return_groups(groups){
            return groups.map(e => e.library_group)
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
            return raw_data.map(e => e.library)
        },

        implicit_data(){
          return { Authorization: "Token " + this.token , "site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
        }
    },
    mounted(){
        this.check_token();

        axios({
           url: this.server_address + '/favourite-library-group',
           method: 'post',
           headers: this.implicit_data(),

        })
        .then(res => {
            console.log(res.data)
            this.page = res.data.page
            this.total_page = res.data.total_page
            this.groups = this.return_groups(res.data.data)
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
                        this.groups = this.groups.concat(this.return_groups(res.data.data))
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

    .group-libs {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .group-libs > img {
        width: 80%;
        margin-bottom: 5px;
    }

    .group-libs > span {
        font-size: 150%;
    }

    .book-img {
        cursor: pointer;
        width: 100%;
    }
    .library-info {
        cursor: pointer;
        display: flex;
        flex-direction: column;
        height: 100%;
        padding-left: 2vw;
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

    .each-library {
        background-color: white;
        width: 50%;
        min-height: 150px;
        margin: 0 auto 1% auto;
        padding: 1%;
        border-radius: 10px;
        display: grid;
        grid-template-columns: 2fr 10fr 1fr;
        align-items: center;
        box-shadow: 0 5px 10px rgb(228, 213, 193);
    }

    h1 {
        font-size: 250%;
        font-family: 'Staatliches', cursive;
        letter-spacing: 2px;
        margin-bottom: 5vh;
    }

    .favgroup-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 5vh 0;
    }

    .favgroup-main {
        background-color: rgb(255, 236, 211);
    }


    @media screen and (max-width: 1200px) {

    .each-library {
        width: 80%;
        min-height: 120px;
    }

    .book-img {
        cursor: pointer;
        width: 90%;
        height: 80%;
    }
}

@media screen and (max-width: 700px) {
    .group-libs > span {
        font-size: 100%;
    }
    .each-library {
        padding: 5% 3%;
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

    .book-img {
        cursor: pointer;
        width: 90%;
        height: 120%;
    }

}

@media screen and (max-width: 500px){
    .library-info > h1 {
        margin-bottom: 5px;
    }
    .library-info > p {
        font-size: 12px;
    }

    .book-img {
        cursor: pointer;
        width: 90%;
        height: 120%;
    }
    h1  {
        font-size: 150%;
    }

}

</style>