<template>
    <div class="library-component mxw-100-mnh-100">
        <img src="@/assets/logo1.png" alt="loading image" class="logo-img">
        <div class="library-wrapper1">
            <div class="library11">
                <img src="@/assets/search/book2.png" alt="loading image">
                <a href="#">Read here</a>
                <div class="library111">
                    <h1>Contents</h1>
                    <div class="library-contents">
                        <ul>
                            <li :key="content" v-for="content in contents">{{content}}</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="library12">
                <h1>{{library_name}}</h1>
                <p>{{library_desc}}</p>
                <h2>Download PDFs</h2>
                <div class="library121">
                    <div :key="file" v-for="file in files" class="each-files">
                        <img src="@/assets/filenames/pdf.png" alt="loading-img" class="pdf-image">
                        <span>{{file}}</span>
                        <img src="@/assets/download.png" alt="loading image" class="download-img">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: [
        "lib_id"
    ],
    data() {
        return {
            library_name: 'ANSI C',
            library_desc: 'deserunt veniam libero? Quos dolores pariatur distinctio perferendis! ipsum dolor sit amet consectetur, adipisicing elit. Pariatur commodi quo, enim blanditiis doloribus ex. Porro eaque doloremque, facere assumenda repellat amet suscipit accusamus quam officiis praesentium quas exercitationem culpa.',
            library_image_link: 'https://pngimg.com/uploads/book/book_PNG51074.png',
            contents: ["Intro", "Chorus", "Verse", "Chorus", "End"],
            files: ["Intro", "Chorus", "Verse", "Chorus", "End"],
        }
    },
    mounted() {
        if (!this.lib_id) window.location.replace("/")
    }
}
</script>

<style scoped>

    .library-component {
        background-color: rgb(254.0, 227, 200);
        padding: 20vh 0;
        position: relative;
    }
    .logo-img {
        position: absolute;
        top: 1vh;
        right: 1vw;
        width: 7vw;
    }
    .library-wrapper1 {
        border-radius: 10px;
        box-shadow: 0 0 10px rgb(187, 167, 142);
        width: 90vw;
        margin: 0 auto;
        padding: 1.5vw;
        display: flex;
    }
    .library11 > img {
        width: 20vw;   
        box-shadow: 0 0 10px rgb(151, 137, 118);
        margin-right: 2vw;
        margin-bottom: 5vh;
    }
    .library11 > a {
        font-size: 18px;
    }
    .library111 {
        margin-top: 5vh;
        padding: 10px;
        width: 20vw;
        box-shadow: 0 0 10px rgb(165, 143, 115);
    }
    .library-contents > ul {
        margin: 10px 0 0 20px;
    }
    .library-contents > ul >  li {
        padding: 5px 10px;
        font-size: 20px;
    }
    .library12 {
        padding: 10px 2vw;
    }
    .library12 > p{
        margin-top: 10px;
        font-size: 120%;
    }
    .library12 > h2 {
        margin-top: 10vh;
    }
    .library121 {
        /* height: 40vh; */
        overflow-y: auto;
    }
    .each-files {
        display: flex;
        align-items: center;
        margin: 0 auto;
        position: relative;
        margin-top: 20px;
        width: 70%;
        height: 70px;
        border-radius: 20px;
        padding: 5px 20px;
        background-color: rgb(238, 198, 147);
    }
    .each-files > span {
        margin: 0 0 0 2vw;
        font-size: 20px;
        letter-spacing: 1px;
        font-weight: bold;
    }
    .download-img {
        position: absolute;
        right: 20px;
        width: 60px;
    }

    @media screen and (max-width: 1300px) {
        .logo-img {
            width: 100px;
        }
        .library-wrapper1 {
            width: 95vw;
        }
        .library12 > h1 {
            font-size: 25px;
        }
        .library12 > p {
            font-size: 16px;
        }
        .library12 > h2 {
            font-size: 20px;
        }
        .library111 > h1 {
            font-size: 20px;
        }
        .library-contents > ul {
            margin: 5px 5px;
        }
        .library-contents > ul >  li {
            padding: 5px 5px;
            font-size: 16px;
        }
        .library12 {
            padding: 10px 10px;
        }
        .library121 {
            /* height: 30vh; */
        }
        .each-files {
            height: 50px;
        }
        .pdf-image {
            width: 70px;
        }
        .each-files > span {
            font-size: 14px;
        }
        .download-img {
            width: 40px;
        }     
    }

    @media screen and (max-width: 700px){
        .library12 > h1 {
            font-size: 16px;
        }
        .library12 > p {
            font-size: 12px;
        }
        .library12 > h2 {
            font-size: 14px;
        }
        .library111 > h1 {
            font-size: 14px;
        }
        .library-contents > ul {
            margin: 2px 0px;
            padding: 0 0 0 20px;
        }
        .library-contents > ul >  li {
            padding: 2px 0px;
            font-size: 12px;
        }
        .library121 {
            /* height: 20vh; */
        }
        .each-files {
            height: 30px;
        }
        .pdf-image {
            width: 50px;
        }
        .each-files > span {
            font-size: 10px;
        }
        .download-img {
            width: 20px;
        }  
    }

</style>