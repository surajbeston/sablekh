<template>
    <div class="password-reset-component mxw-100-mnh-100">
        <img src="@/assets/logo1.png" alt="logo" class="logo-img">
        <div class="password-reset-wrapper1">
            <div class="password-reset11">
                <img v-show="first_phase" src="@/assets/password_reset/1.png" alt="loading img">
                <img v-show="second_phase" src="@/assets/password_reset/2.png" alt="loading img">
            </div>
            <div class="password-reset12">
                <div v-show="first_phase" class="grid-set pr121 w-100-h-100">
                    <h1>Forget Password ?</h1>
                    <p>Then reset your password by clicking the button below.</p>
                    <button class="btn" @click="reset_button">
                        Reset
                    </button>
                </div>
                <div v-show="second_phase" class="grid-set pr122 w-100-h-100">
                    <div class="pr1221">
                        <h1>fadfaf adfadf</h1>
                        <p> adfadfa adfadf asdfad fadfa</p>
                    </div>
                    <div class="input-section">
                        <input type="password" v-model="password1" id="password1" placeholder="New Password">
                        <input type="password" v-model="password2" id="password2" placeholder="Old Password">
                    </div>
                    <button class="btn">
                        Done
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            first_phase: true,
            second_phase: false,
            password1: "",
            password2: ""
        }
    },
    methods: {
        reset_button() {
            this.first_phase = false
            this.second_phase = true
        }
    }
}
</script>

<style scoped>
    .password-reset-component {
        background-color: rgb(255, 233, 203);
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .logo-img {
        width: 8%;
        margin: 5vh 0;
    }
    .password-reset-wrapper1{
        width: 80%;
        display: flex;
    }
    .password-reset11 {
        width: 60%;
        height: 60vh;
        box-shadow: -5px 0 10px rgb(211, 188, 158);
    }
    .password-reset11 > img {
        width: 70%;
        margin: 10vh 0 0 20%;
    }
    .password-reset12 {
        background-color: white;
        box-shadow: 5px 0 10px rgb(196, 174, 146);
        width: 40%;
        height: 60vh;
    }
    .grid-set {
       display: grid;
       grid-template-rows: auto auto auto;
       justify-content: space-around;
       align-content: space-around;
       padding: 20% 10%;
    }
    /* .pr121 {

    } */
    .pr121 > p {
        font-size: 130%;
    }
    .pr122 {
        padding: 10% 1%;
    }
    .pr1221 > p {
        font-style: italic;
        font-size: 120%;
        margin: 2% 0 0 5%;
    }
    .input-section > input {
        margin-bottom: 5%;
        display: block;
        width: 100%;
        font-size: 130%;
        outline: none;
        border: none;
        background-color: rgb(253, 197, 123);
        padding: 2% 5%;
        border-radius: 5px;
        box-shadow: 0 5px 5px rgb(214, 214, 214);
        color: rgb(165, 140, 106);
    }

/* extras  */

    .btn {
        outline: none;
        cursor: pointer;
        padding: 5% 0;
        font-size: 18px;
        letter-spacing: 1px;
        font-weight: bold;
        border-radius: 10px;
        background-color: rgb(247, 206, 152);
    }
    .btn:hover {
        background-color: rgba(229, 186, 130, 0);
        border: 2px solid burlywood;
    }

    .w-100-h-100 {
        width: 100%;
        height: 100%;
    }
</style>