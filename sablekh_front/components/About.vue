<template>

<div class="about-main mxw-100-mnh-100">
    <Header />
    <div class="about-wrapper1">
        <div class="about-info">
            <h2>About Us</h2>
            <p>
               Content collection and sharing is the first step to digital education. It can be achieved soon if the medium to collect and share content is kept open and free. We aim to make educational materials easily accessible and free for everyone. 
            </p>
            <p>
                The main problem of students and the learners is difficulty to find their files when wanted. It is because of the unmanaged storing of data in their device. Anyone can upload their documents and files here and access whenever wanted. 
            </p>
            <p>
                We strongly believe this platform will play the lifesaver role for those who are going through different struggles like:
            </p>
            <ul>
                <li>Difficult finding educational notes</li>
                <li>Unmanaged files</li>
                <li>Lack of storage</li>
                <li>Sharing files</li>
                <li>Getting recognition</li>
                <li>And mainly the contribution to the digital and free education</li>
            </ul>
        </div>
        <div class="about-animations" ref="anim" @mouseenter="mouse_anim" @mouseleave="mouse_anim">
            <transition name="fade">
                <img v-show="!which_book" src="@/assets/about/book.png" alt="image" class="first-img">
            </transition>
            <transition name="fade1">
                <img v-show="which_book" src="@/assets/about/book1.png" alt="image" class="sec-img" >
            </transition>
        </div>
    </div>
</div>
    
</template>

<script>
export default {
    data() {
        return {
            is_extended: false,
            which_book: false,

        }
    },

    head(){
        return {
            title: "Sablekh: About",
            meta: [
                {
                    hid: "description",
                    name: "description",
                    content: "Sablekh is a platform to share small files with the world."
                }
            ]
        }
    },
    methods: {
        mouse_anim(){
            this.which_book = !this.which_book
        },
        icon_clicked() {
            this.is_extended = !this.is_extended;
        }
    },
    mounted() {
    }
    
}
</script>

<style scoped>

/* anim */

    .fade-enter-active, .fade-leave-active {
        transition: transform 1s, opacity 1s;
    }
    .fade-enter, .fade-leave-to {
        opacity: 0;
        transform: scale(.4);
        transform-origin: 50% 120%;
    }
    .fade1-enter-active {
        transition: opacity 1s;
    }
    .fade1-leave-active {
        transition: opacity .5s;
    }
    .fade1-enter, .fade1-leave-to {
        opacity: 0;
    }

/* anim  */

.first-img,
.sec-img {
    position: absolute;
    top: 15%;
    left: 10%;
    width: 80%;
}

.about-animations {
    width: 45%;
    text-align: center;
    position: relative;
}

.about-info > ul {
    margin-left: 10%;
}

.about-info > p, .about-info > ul {
    padding: 2vh 2vw;
    font-size: 150%;
    font-family: 'Comfortaa', cursive;
    line-height: 40px;
    text-align: justify;
}


.about-info > h2 {
    padding: 20px;
    border-bottom: 2px solid rgb(66, 61, 54);
    /* font-family: 'Staatliches', cursive; */
    /* letter-spacing: 1px; */
    font-size: 250%;
}


.about-info {
    width: 55%;
    padding: 20px 0 0 20px;
}

.about-wrapper1 {
    display: flex;
    flex-direction: row;
}

.about-main {
    background-image: linear-gradient(to right bottom, rgb(255, 232, 206), rgb(240, 210, 176));
}

@media screen and (max-width: 1500px){
    
    .about-info > p, .about-info > ul {
        font-size: 120%;
        line-height: 35px;
    }

}

@media screen and (max-width: 1200px){

    .about-info > p, .about-info > ul{
        font-size: 100%;
        line-height: 30px;
    }

}

@media screen and (max-width:900px){
    .about-wrapper1 {
        flex-direction: column;
        align-items: center;
    }
    .about-info {
        width: 100%;
    }
    .about-animations {
        /* min-height: 80vh; */
        height: 650px;
        width: 650px;
        
    }
}

@media screen  and (max-width: 700px){
    .about-animations {
        height: 450px;
        width: 450px;
        
    }
}


@media screen and (max-width:500px) {
    .about-info {
        padding: 5px 0 0 5px;
    }
    .about-info > h2 {
        font-size: 100%;
    }
    .about-info > p, .about-info > ul {
        font-size: 80%;
        line-height: 25px;
    }
    .about-animations {
        height: 300px;
        width: 300px;
        
    }
}

@media screen and (max-width: 350px){
    .about-animations {
        height: 250px;
        width: 250px;
        
    }
}

</style>