<template>
    <div class="each-group">
        <EachGroup :data="data"/>
        <Footer />
    </div>
</template>

<script>
import axios from "axios";

export default {
    async asyncData({params}){
        
        var data = axios({
            url: "https://api.sablekh.com/get-library-group",
            method: "post",
            data: {
                link_str: params.id
            },
            headers: {site: "", referrer: "", timetaken : new Date().getTime(), link: ""},
        }).then(res => {

            return {
                data:{
                    title: res.data.title,
                    description: res.data.description,
                    loaded: true
                }
            }
        }).catch(err => {

        })
        return data
        
    },
    data(){
        return {
            data: {loaded: false}
        }
    }
}
</script>