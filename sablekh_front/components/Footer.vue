<template>
    <div class="footer">
        <div class="footer-wrapper1">
            <NuxtLink class = "foot-link" to="/my-library">My Libraries</NuxtLink>
            <NuxtLink class = "foot-link" to="/upload">Upload</NuxtLink>
            <img src="@/assets/sablekh.png" alt="loading image" id = "main-img">
            <NuxtLink class = "foot-link" to="/">Search</NuxtLink>
            <NuxtLink class = "foot-link" to="/about">About Us</NuxtLink>
        </div>
    </div>
</template>

<style scoped>
    .foot-link{
        text-decoration: none;
        color: rgb(66, 62, 55);
        font-weight: 600;
        font-size: 140%;
        margin: 0 3vw;
        font-family: 'Staatliches', cursive;
        letter-spacing: 2px;
    }

    .foot-link:hover {
        text-decoration: underline;
        color:rgb(0, 0, 0)
    }
    .footer {
        height: 200px;
        max-width:100vw;
        background-color: white;
    }
    .footer-wrapper1 {
        width: 100%;
        height: 100%;
        display:flex;
        justify-content: center;
        align-items: center;
    }

    @media screen and (max-width: 1500px){
       .footer{
            height: 170px;
       }
       #main-img{
           height: 50%;
       }
        .foot-link{
            font-size: 130%;
        }
    }

    @media screen and (max-width: 1200px){
       .footer{
            height: 150px;
       }
       #main-img{
           height: 45%;
       }
        .foot-link{
            font-size: 120%;
        }
    }

    @media screen and (max-width: 700px){
       .footer{
            height: 135px;
       }
       #main-img{
           height: 35%;
       }
        .foot-link{
            font-size: 100%;
            font-weight: bold;
        }
    }

    @media screen and (max-width: 500px){
       .footer{
            height: 400px;
       }
       .foot-link {
           margin-top: 5vh;
           margin-bottom: 2vh;
           font-size: 20px;
        font-weight: bold;
       }
       .footer-wrapper1 {
           flex-direction: column;
       }
       #main-img{
           height: 25%;
       }
    }

</style>