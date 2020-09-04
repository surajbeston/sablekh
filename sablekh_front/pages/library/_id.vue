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
      url: "http://104.248.39.254" + "/link",
      method: "post",
      headers: {site: "", referrer: "", timetaken : new Date().getTime(), link: ""},
      data: {link_str: params.id}
    }).then(res =>{
      
      var files = res.data.files

      files = files.map(e => {
        let each = e.title.split(".");
        let a = each[0];
        let lent = a.length;
        e.title = `${a.substring(0, a.length > 5 ? 5 : a.length)}.${each[1]}`;
        return e
      });


      return {data:{
          hid: res.data.hid,
          library_name: res.data.title,
          library_desc: res.data.description,
          library_thumbnail: res.data.thumbnail,
          library_tags: res.data.tags,
          files,
          likes: res.data.likes,
          downloads: res.data.downloads,
          username: res.data.username
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
  },

}

</script>

<style scoped>

</style>