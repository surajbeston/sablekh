<template>
    <div class="library-component mxw-100-mnh-100">
        <img src="@/assets/logo1.png" alt="loading image" class="logo-img">
        <div class="library-wrapper1">
            <div class="library11">
                <img src="data:image/jpeg;base64,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" alt="loading image">
                <a href="#">Read here</a>
                <div class="library111">
                    <h1>Content</h1>
                    <div class="library-contents">
                        
                    </div>
                </div>
            </div>
            <div class="library12">
                <h1>ANSI C</h1>
                <p>Lorem Lorem ipsum Lorem ipsum dolor, sit amet consectetur adipisicing elit. Asperiores, facere optio nihil autem neque ipsum eius sit quisquam itaque amet nesciunt explicabo error veniam aliquid enim nam excepturi rem non! dolor, sit amet consectetur adipisicing elit. Vel maiores tenetur, delectus deserunt veniam libero? Quos dolores pariatur distinctio perferendis! ipsum dolor sit amet consectetur, adipisicing elit. Pariatur commodi quo, enim blanditiis doloribus ex. Porro eaque doloremque, facere assumenda repellat amet suscipit accusamus quam officiis praesentium quas exercitationem culpa.</p>
                <h2>Download PDFs</h2>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: [
        "lib_id"
    ],
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
        box-shadow: 0 0 10px rgb(151, 137, 118);
        margin-right: 2vw;
        margin-bottom: 5vh;
    }
    .library11 > a {
        font-size: 18px;
    }
    .library111 {
        margin-top: 5vh;
        padding: 5px;
        box-shadow: 0 0 10px rgb(165, 143, 115);
    }
    .library12 {
        padding: 10px 2vw;
    }
    .library12 > p{
        margin-top: 10px;
        font-size: 20px;
    }
    .library12 > h2 {
        margin-top: 10vh;
    }
</style>