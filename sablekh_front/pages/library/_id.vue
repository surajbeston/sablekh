<template>
   <div class="library">
        <Library :lib_id="this.$route.params.id" :data="data" />
        <!-- <pre>{{data}}</pre> -->
        <Footer />   
    </div> 
</template>

<script>
import axios from "axios"

export default {
  async asyncData({params}){
    console.log("this")
    var data =  axios({
      url: "http://localhost:8000" + "/link",
      method: "post",
      headers: {site: "", referrer: "", timetaken : new Date().getTime(), link: ""},
      data: {link_str: params.id}
    }).then(res =>{
      return {data:{
          hid: res.data.hid,
          library_name: res.data.title,
          library_desc: res.data.description,
          library_thumbnail: res.data.thumbnail,
          library_tags: res.data.tags,
          files: res.data.files,
          likes: res.data.likes,
          downloads: res.data.downloads
          }
      }
    }).catch(res => {
      console.log(res.response)
    })
    return data
  },
  data(){
      return {
          data: {"sdf": "sd"}
      }
  }
}

</script>

<style scoped>

</style>