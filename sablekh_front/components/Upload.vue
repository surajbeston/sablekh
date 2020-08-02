<template>
    <div class="upload-component mxw-100-mnh-100">
        <div class="upload-wrapper1">
            <img src="@/assets/upload/upload-top.png" alt="loading image" class="upload11">
            <div class="upload12">
                <h1 class = "head1">Upload</h1>
                <p class = "description">Create your small library and share it with the world. You can add upto 10 files, each not exceeding 30MB in size.</p>
                <div class="input-section">
                    <label for="title">Title</label>
                    <input class="input-box" type="text" v-model="title" id="title" autofocus >
                    <label for="description">Description</label>
                    <textarea class="input-box" v-model="description" id="description" cols="30" rows="5"></textarea>
                    <label for="file">Add your File Here</label>
                    <input type="file" name="upload_file" id="file">
                </div>
                <button class="btn" >Upload</button>
            </div>
            <img src="@/assets/logo1.png" alt="loading image" class="upload13">
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return{
            title: "",
            description: ""
        }
    },
    
    mounted() {
        if (!window.localStorage.getItem("token")) {
            window.location.replace("/login")
        }
    }
}
</script>

<style scoped>
    .upload-component {
        background-color: rgb(254, 227, 200);
        color:rgb(51, 47, 43);
        padding-bottom: 2vh;
    }
    .upload-wrapper1 {
        display: flex;
        position: relative;
        width: 100%;
    }
    .upload11 {
        width: 25%;
        height: 25%;
    }
    .upload12 {
        width: 60%;
        margin: 10vh 5vw 0 5vw;
    }
    .upload12 > h1 {
        margin-bottom: 2vh;
    }
    .upload12 > p {
        color: rgb(90, 81, 72);
        font-weight: 400;
        margin: 1vh 0;
    }
    .input-section {
        margin: 5vh 5vw;
        display: flex;
        flex-direction: column;
    }
    .input-section > input {
        letter-spacing: 1px;
    }
    .input-section > label {
        font-family: 'Rajdhani', sans-serif;
        margin-top: 1vh;
        font-size: 170%;
    }
    .input-section > [type="file"] {
        width: .1px;
        height: .1px;
        opacity: 0;
        overflow: hidden;
        z-index: -1;
    }
    .input-section > [for="file"] {
        text-align: center;
        width: 100%;
        height: 20vh;
        padding-top: 9vh;
        border: 2px dashed rgb(90, 81, 72);
        border-radius: 10px;
        margin-top: 2vh;
        cursor: pointer;
    }
    .upload13 {
        width: 10%;
        position: absolute;
        right: 2vw;
        top: 2vh;
    }

    .head1{
        font-family: 'Staatliches', cursive;
        letter-spacing: 5px;
        font-size: 250%;
    }

    .description{
        font-family: 'Comfortaa', cursive;
        padding-right: 20%;
        font-size: 120%;
    }

    /* extras  */

    .btn {
        background-color: rgb(255, 176, 98);
        font-weight: bold;
        font-size: 16px;
        letter-spacing: 1px;
        border-radius: 5px;
    }

    .input-box {
        padding: 15px 10px;
        font-size: 20px;
        margin-top: 1vh;
        background: none;
        outline: none;
        border: 2px solid rgb(87, 77, 66);
        border-radius: 10px;
    }
</style>