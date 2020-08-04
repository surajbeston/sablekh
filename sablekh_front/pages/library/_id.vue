<template>
   <div class="library">
        <Library :lib_id="this.$route.params.id" />
        <Footer />   
    </div> 
</template>

<script>

export default {
//    mounted() {
//        if (!this.$route.params.id){
//            window.location.replace("/")
//        }
//    } 
}

</script>

<style scoped>

</style>