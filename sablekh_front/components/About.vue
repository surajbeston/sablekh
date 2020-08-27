<template>

<div class="about-main mxw-100-mnh-100">
    <Header />
    <div class="about-wrapper1">
        <div class="about-info"></div>
        <div class="about-animations"></div>
    </div>
</div>
    
</template>

<script>
export default {
    data() {
        return {
            is_extended: false,

        }
    },
    methods: {
        icon_clicked() {
            this.is_extended = !this.is_extended;
        }
    }
    
}
</script>

<style scoped>

.about-main {
    background-image: linear-gradient(to right bottom, rgb(255, 232, 206), rgb(240, 210, 176));
}

.about-wrapper1 {
    display: flex;
    flex-direction: row;
}

</style>