<template>
    <div class="home-component mxw-100-mnh-100">
        <div class="home-wrapper1">
            <img class="home11" src="@/assets/logo1.png" alt="loading image">
            <div class="home12">
                <img src="@/assets/homepage/download.png" alt="loading image" class="imgpab0 home121">
                <img src="@/assets/homepage/user.png" alt="loading image" class="imgpab0 home122">
                <img src="@/assets/homepage/search.png" alt="loading image" class="imgpab0 home123">
                <img src="@/assets/homepage/upload.png" alt="loading image" class="imgpab0 home124">
            </div>
            <div class="home13">
                <img src="@/assets/homepage/book.png" alt="loading image">
            </div>
        </div>
    </div>
</template>

<style scoped>
    .home-component {
        background-image: url("../assets/homepage/background1.png");
        background-size: cover;
        background-repeat: no-repeat;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .home-wrapper1 {
        text-align: center;
        height: 90vh;
        width: 50vw;
        position: relative;
    }
    .home11 {
        width: 200px;
    }
    .home121{
        bottom: 25vh;
        left: 10vw;
    }
    .home122 {
        bottom: 35vh;
        left: 18vw;
    }
    .home123 {
        bottom: 35vh;
        right: 17vw;
    }
    .home124 {
        right: 10vw;
        bottom: 25vh;
    }
    .home13 {
        position: absolute;
        bottom: 0;
        width: 100%;
        text-align: center;
    }
    .home13 > img {
        width: 50vw;
    }

    /* extras */
    .imgpab0 {
        position: absolute;
        width: 80px;
    }
</style> 