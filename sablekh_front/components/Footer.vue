<template>
    <div class="footer">
        <div class="footer-wrapper1">
            <a href="#">Dashboard</a>
            <a href="#">Upload</a>
            <img src="@/assets/sablekh.png" alt="loading image">
            <a href="#">Search</a>
            <a href="#">Download</a>
        </div>
    </div>
</template>

<style scoped>
    a {
        text-decoration: none;
        color: rgb(66, 62, 55);
        font-weight: 600;
        font-size: 20px;
        margin: 0 3vw;
    }
    a:hover {
        text-decoration: underline;
        color:rgb(0, 0, 0)
    }
    .footer {
        box-shadow: 0 -5px 10px rgb(223, 223, 223);
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
</style>