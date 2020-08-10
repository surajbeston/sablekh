<template>
    <div class="error">
        <div class="error-wrapper1">
            <div class="error1" :key="err.name" v-for="err in errors">
                <h4>{{err.desc}}</h4>
                <img src="@/assets/cancel.png" alt="cancel img" @click="cancel_clicked(err.name)">
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
          errors: [
              {
                name: "int-err",
                desc: "some internal error please try again later"
              },
              {
                name: "idk-err",
                desc: "i dont know whats the error"
              }
          ]  
        }
    },
    props: [
        // "errors"
    ],
    methods: {
        cancel_clicked(name) {
            this.errors.filter(err => err.name == name)
            // console
        }
    }
}
</script>

<style scoped>
    .error-wrapper1 {
        width: 100%;
    }
    .error1 {
        width: 100%;
        position: relative;
        display: flex;
        align-items: center;
        background-color: rgba(255, 0, 0, 0.164);
        padding: 10px 20px;
        border-radius: 20px;
        border: 2px solid brown;
        margin-top: 6px;
        margin-bottom:6px;
    }
    .error1 > img {
        cursor: pointer;
        position: absolute;
        right: 20px;
    }
</style>