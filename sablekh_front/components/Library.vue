<template>
  <div>
    <!-- <pre>{{data}}</pre> -->
    <div class="library-component mxw-100-mnh-100" >
      <Header />
      <!-- <img src="@/assets/logo1.png" alt="loading image" class="logo-img" /> -->
      <div v-if = "loader_on">
        <span class="loader"></span>
      </div>
      <div v-else>
        <div v-if = "not_found" class = "not_found">
          <h1>Library not found 404</h1>
        </div>
        <div v-else class="library-wrapper1">
          <img class="book-img" :src="library_thumbnail" alt="book" />
          <h1 class="library-title">{{library_name}}</h1>
          <p class="library-desc">{{library_desc}}</p>
          <div class="lib-tags" v-bind:key="tag" v-for="tag in library_tags">
            <span class="each-tag">{{tag}}</span>
          </div>
          <div id = "successBox" v-show="hasSuccess" ><p id = "successTxt"> {{success}}<img src = "@/assets/cancel.png" @click="hasSuccess =!hasSuccess" class = "cancelSuccess"></p></div>
              <div id = "errorBox" v-show="hasError" ><p id = "errorTxt"> {{error}}<img src = "@/assets/cancel.png" @click="hasError =!hasError" class = "cancelError"></p></div>
          <div class="like-div">
            <div class="like1">
              <span class="like-span">{{likes}}</span>
              <img
                @click="like_clicked"
                v-show="!is_liked"
                src="@/assets/like.png"
                alt="like"
                class="blk-like"
              />
              <img v-show="is_liked" src="@/assets/like1.png" alt="like" class="blu-like" />
            </div>
            <div class="like2">
              <span class="like-span">{{downloads}}</span>
              <img src="@/assets/download1.png" alt="download img" class="download-img">
            </div>
            <div class="like3" @click = "copy(library_name)">
                <img src="@/assets/copy.png" alt="share img" class="copy-img">
            </div> 
          </div>
          <div class="files-wrapper" v-show = "!loader_on">
            <div class="fw-each" :key="file.hid" v-for="file of files">
              <div @click="download_middle(file.hid)" class="fw1"> 
                <img src="@/assets/filenames/pdf.png" alt="png" />
                <h3>{{file.title}}</h3>
                <div class="size-div">
                  <img src="@/assets/file.png" alt="file png" class="file-img">
                  <span>{{(file.size/1024).toFixed(2)}} MB</span>
                </div>
              </div>
              <div class="fw2">
                <input type="checkbox" :id="file.hid" @input="checkbox_clicked(file.hid)" />
              </div>
            </div>
          </div>
          <div v-show="downloading" class="progress-bar">
            <div class="progress" :style="progress_bar_style"></div>
          </div>
          <div class="download-container">
            <button @click="download_clicked" class="btn download">Download</button>
            <button @click="download_all_clicked" class="btn download-all">Download all</button>
          </div> 
          <button @click="show_change_link" v-show="!changing && authenticated && is_in_user_library" class="btn" >
            Change Link
          </button> 
          <div v-show="changing && authenticated" class="change-link">
            <input type="text" v-model="new_link" :placeholder="lib_id">
            <button @click="link_changed" class="btn change-link-button">Change</button>
          </div> 
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {

  props: ["lib_id", "data"],

  data() {
    return {
      server_address: "http://104.248.39.254",
      library_name: "",
      library_username: "",
      library_desc: "",
      library_image_link: "https://pngimg.com/uploads/book/book_PNG51074.png",
      library_tags: [],
      contents: [],
      selected_file: [],
      files: [],
      refined_files: [],
      hid: "",
      library_thumbnail: "https://api.sablekh.com/thumbnails/default.jpg",
      likes: 0,
      is_liked: false,
      downloading: false,
      progress: 0,
      new_link: "",
      changing: false,
      token: "",
      authenticated: false,
      downloads: 0,
      is_in_user_library: false,
      user_libraries: [],
      loader_on: false,
      hasSuccess: false,
      success: "This is success",
      error: "This is error",
      hasError: false,
      not_found: false
    };
  },

  methods: {
    library_stuffs(){
      // this.loader_on = true

      if(window.localStorage.getItem("username") === this.library_username) {
        this.is_in_user_library = true
      }

    },
    link_changed(){
      if (this.new_link.length < 3) this.show_error("At least 3 letters required.")
      else{
        axios({
          url: this.server_address + "/change-link",
          headers: {
            ...this.implicit_data(),
            Authorization: "Token " + this.token
          },
          method: 'post',
          data: {
            hid: this.data.hid,
            link_str: this.new_link
          }
        })
        .then(res => {
          window.location.href = "/library/" + res.data.link_str
        })
        .catch(e => {
          this.show_error("Something went wrong.")
        })
      }
  },
    show_change_link(){      
      this.changing = true;
      this.show_success("Warning: This link won't exist.")
    },
    like_clicked() {
      if (!this.token){
        window.localStorage.setItem("link_str", this.$route.params.id)
        window.location.href = "/login";
      }
      axios({
        url: this.server_address + "/like",
        method: "post",
        headers: {
          ...this.implicit_data(),
          Authorization: "Token " + this.token,
        },
        data: {
          library: this.hid,
        },
      })
      .then((res) => {
        this.get_like()
        this.is_liked = true;
      }) 
      .catch((e) => {
        console.log(e.response)
      });
    },
    get_downloads() {
      axios({
        url: this.server_address + "/all-downloads",
        method: "post",
        headers: this.implicit_data(),
        data: {
          library: this.hid,
        },
      })
        .then((res) => {
          this.downloads= res.data.downloads;
        })
        .catch((e) => {
        });
    },
    get_like() {
      axios({
        url: this.server_address + "/all-likes",
        method: "post",
        headers: this.implicit_data(),
        data: {
          library: this.hid,
        },
      })
        .then((res) => {
          this.likes = res.data.likes;
        })
        .catch((e) => {
          //.log(e);
        });
    },
    check_like() {
      axios({
        url: this.server_address + "/check-like",
        method: "post",
        headers: {
          ...this.implicit_data(),
          Authorization: "Token " + this.token
        },
        data: {
          library: this.hid,
        },
      })
        .then((res) => {
          if (res.data.liked) {
            this.is_liked = true;
          }
        })
        .catch((e) => {
          //.log(e);
        });
    },
    checkbox_clicked(id) {
      if (this.selected_file.includes(id)) {
        let i = this.selected_file.indexOf(id);
        this.selected_file.splice(i, 1);
      } else {
        this.selected_file.push(id);
      }
    },

    download_all_clicked() {
      
      if (this.files.length == 0 ) {
        return null
      }

      this.downloading = true;
      this.progress = 0

      let a = this.files.map((e) => e.hid);

      this.download_middle(a.join(","));

    },

    download_clicked() {
      var file_hids = "";
      if (!this.selected_file.length > 0) {
        this.show_error("Please select files to downoad.")
        return null;
      }
      else if (this.selected_file.length === 1) {
        // let file = this.files.filter(e => e.hid === this.selected_file[0]) i guess its not necessary

        // if (file.link) {
        //   download(file.link)
        // }
        // else {
        this.downloading = true;
        this.progress = 0;
        file_hids = this.selected_file[0];
      } 
      else {
        file_hids = this.selected_file.join(",");
        this.downloading = true;        
        this.progress = 0
      }
      this.download_middle(file_hids);
    },

    download_middle(file_hids) {
      if (file_hids !== "") {
        axios({
          url: this.server_address + "/download",
          method: "post",
          data: {
            hids: file_hids,
            library: this.hid,
          },
          headers: this.implicit_data(),
        })
          .then((res) => {
            // //.log(res)
            console.log(res.data.filename)
            this.download(res.data.filename)
          })
          .catch((e) => {
            this.progress = 0
            this.downloading = false
            this.show_error("Download interrupted. Try again.")
          });
      }
    },

    download(url) {
      let file_name = url.split("/");
      axios({
        url,
        method: "GET",
        responseType: "blob",
        onDownloadProgress: (e) => {
          this.progress = Math.round(e.loaded/e.total*100)
        }
      }).then((response) => {
        var fileURL = window.URL.createObjectURL(new Blob([response.data]));
        var fileLink = document.createElement("a");
        fileLink.href = fileURL;
        fileLink.setAttribute("download", file_name[file_name.length - 1]);
        document.body.appendChild(fileLink);
        this.progress = 100;
        fileLink.click();
        this.progress = 0;
        this.downloading = false
        this.show_success("File/s downloaded.")
      }).catch(error => {
        this.show_error("Download interrupted. Try again.")
      })
      
    },

    clean_title() {
      this.files.map((each) => {
        let b = each;
        let e = each.title.split(".");
        let a = e[0];
        let lent = a.length;
        let title = `${a.substring(0, a.length > 5 ? 5 : a.length)}.${e[1]}`;
        b.title = title;
        this.contents.push(title);
        this.refined_files.push(b);
      });
    },
    implicit_data() {
      return  {
        site: document.referrer,
        link: process.server ? "" : window.location.href.toString().split(window.location.host)[1],
        timetaken: new Date().getTime() - this.time,
      };
    },
    async copy(s) {
      await navigator.clipboard.writeText(window.location.href);
      this.show_success("Link Copied. Share it now!")
    },
    show_success(successTxt){
      this.hasError = false      
      this.hasSuccess = true
      this.success = successTxt
      document.body.scrollTop = 0
      document.documentElement.scrollTop = 0
    },
    show_error(errorTxt){
      this.hasSuccess = false
      this.hasError = true 
      this.error = errorTxt 
      document.body.scrollTop = 0
      document.documentElement.scrollTop = 0
    },
  },

  computed: {
    progress_bar_style() {
      return {
        width: `${this.progress}%`
      }
    }

  },

  mounted() {
    console.log("wallah")
    window.localStorage.removeItem("link_str")
    this.time = new Date().getTime();

    if (!this.lib_id) {
      window.location.replace("/");
    }
    this.token = window.localStorage.getItem("token");
    if (this.token){
      this.authenticated = true
    }
    axios({
      url: `${this.server_address}/link`,
      method: "post",
      data: {
        link_str: this.$route.params.id,
      },
      headers: this.implicit_data(),
    })
      .then((res) => {
        console.log(res.data)
        this.hid = res.data.hid;
        this.library_name = res.data.title;
        this.library_desc = res.data.description;
         this.library_thumbnail = res.data.thumbnail
         this.library_tags = res.data.tags
         this.files = res.data.files
         this.likes = res.data.likes
         this.downloads = res.data.downloads
         this.library_username = res.data.username
        // this.get_like()
        // this.get_downloads()
        if (this.token) {
          this.check_like()
          this.library_stuffs()
        }
      })
      .catch((e) => {
        if (e.response.status == 404){
          this.loader_on = false
          this.not_found = true
        }
      });
  },
};
</script>

<style scoped>

.lib-tags{
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

.each-tag {
  margin-top: 10px;
  padding: 5px 10px;
  font-size: 110%;
  border: 2px solid rgb(255, 160, 35);
  border-radius: 5px;
  font-family: 'Comfortaa', cursive;
}

.size-div {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  padding-right: 10px;
}

.file-img {
  width: 20%;
}

.change-link {
  width: 100%;
  /* display: grid; */
  grid-template-columns: 10fr 1fr;
  grid-column-gap: 5px;
}

.change-link-button {
  padding: 5px 10px;
}
.change-link >input {
  outline: none;
  font-size: 20px;
  padding: 3px 10px;
  width: 50%;
  margin-left: 20%;
  border: none;
  border-radius: 5px;
}

.progress-bar {
  width: 100%;
  height: 15px;
  border-radius: 10px;
  background-color: white;
}
.progress {
  background-color: black;
  height: 100%;
  border-radius: 10px;
}

.like-div {
  margin-top: 5%;
  padding: 1% 2%;
  width: 50%;
  height: 25%;
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  text-align: center;
  background-color: rgb(245, 245, 245);
  box-shadow: 0 5px 10px rgb(177, 145, 105);
  border-radius: 5px;
}

.blk-like,
.blu-like,
.copy-img {
  cursor: pointer;
}

.blk-like,
.blu-like,
.download-img
 {
  width: 25%;
}
.copy-img {
  width: 25%;
}

.download-container {
  margin-top: 5%;
  margin-bottom: 5%;
}

.btn {
  cursor: pointer;
  background-color: rgb(255, 165, 47);
  border-radius: 5px;
  font-size: 120%;
  border: 2px solid rgb(255, 165, 47);
}

.btn:hover {
  background-color: rgba(255, 165, 47, 0.274);
}

.files-wrapper {
  margin-top: 5%;
  display: flex;
  flex-direction: column;
  width: 50%;
}

.fw-each {
  display: grid;
  grid-template-columns: 5fr 1fr;
  grid-gap: 1em;
}



.fw1 {
  margin-bottom: 1em;
  background-color: rgba(255, 255, 255, 0.603);
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  border-radius: 5px;
  cursor: pointer;
  font-family: 'Ubuntu', sans-serif;
}

.fw1 > img {
  width: 20%;
}

.fw2 {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-bottom: 1em;
}

.fw2 > input {
  width: 50%;
  height: 50%;
}

.library-component {
  background-color: rgb(254, 227, 200);
  padding: 0px 0 10px 0;
  position: relative;
}
.back-arrow {
  cursor: pointer;
  position: absolute;
  width: 35px;
  height: 35px;
  top: 40px;
  left: 5px;
  display: none;
}
.logo-img {
  position: absolute;
  top: 1vh;
  right: 1vw;
  width: 130px;
}
.library-wrapper1 {
  width: 50%;
  margin: 100px auto 50px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 0 10px rgb(207, 187, 161);
  padding: 2%;
  border-radius: 10px;
}
.book-img {
  width: 20%;
  box-shadow: 0 0 10px rgb(189, 169, 143);
}
.library-title {
  margin-top: 5%;
  font-size: 210%;
  font-family: 'Rajdhani', sans-serif;
}
.library-desc {
  margin-top: 3%;
  font-size: 150%;
  text-align: center;
  font-family: 'Ubuntu', sans-serif;
}

.not_found{
  text-align: center;
  font-family: 'Rajdhani', sans-serif;
}

  #successBox{
      background-color: rgba(134, 190, 87, 0.4);
      color: rgb(51, 47, 43);
      border: 1px black solid;
      border-radius: 5px;
      padding : 1%;
      font-size: 110%;
      font-family: 'Rajdhani', sans-serif;
      font-weight: 200;
      animation-name: fadein;
      animation: fadein 1s;
      width: 50%;
      animation-name: fadein;
      animation: fadein 1s;
    }

    @keyframes fadein {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
  .cancelSuccess{
      cursor: pointer;
      float: right;
  }

  #errorBox{
    background-color: rgba(255, 0, 0, 0.4);
    color: rgb(51, 47, 43);
    border: 1px black solid;
    border-radius: 5px;
    padding : 1%;
    font-size: 110%;
    font-family: 'Rajdhani', sans-serif;
    animation-name: fadein;
    animation: fadein 1s;
    margin: 2% 0 2% 0;
    font-weight: bold;
    width: 50%;
    animation-name: fadein;
    animation: fadein 1s;
    }

.cancelError{
    cursor: pointer;
    right: 0;
    float: right;
}

  .loader {
      width: 48px;
      height: 48px;
      border: 3px solid #FFF;
      border-radius: 50%;
      display: inline-block;
      position: relative;
      box-sizing: border-box;
      animation: rotation 1s linear infinite;
      margin-top: 5%;
      text-align: center;
      position: absolute;
      margin-left: 48%;
  }
  .loader::after {
    content: '';  
    box-sizing: border-box;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 56px;
    height: 56px;
    border-radius: 50%;
    border: 3px solid;
    border-color: #FF3D00 transparent;
    }

    @keyframes rotation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
    } 

    @media screen and (max-width: 1500px) {
        .search1512{
            margin-right: 10%;
        }
    }
    


@media screen and (max-width: 1300px) {
  .library-wrapper1 {
    width: 80%;
  }
  .logo-img {
    width: 100px;
  }

  .like-div{
    height: 25%;
    padding: 10px;
  }

  .blk-like,
.blu-like,
.download-img
 {
  width: 20%;
}
.copy-img {
  width: 20%;
}

  .loader {
      width: 30px;
      height: 30px;
  }

  .loader::after {
      width: 36px;
      height: 36px;
  }

  .each-tag {
    font-size: 90%;
  }
}

@media screen and (max-width: 700px) {
  .progress-bar {
    height: 10px;
  }
  .library-wrapper1 {
    width: 72%;
    margin: 50px auto 0 auto;
  }

  .files-wrapper {
    width: 72%;
  }

  .back-arrow {
    display: block;
  }

      .blk-like,
  .blu-like,
  .download-img
  {
    width: 25%;
  }
  .copy-img {
    width: 25%;
}

  .like-div{
    width: 67%;
  }

  .each-tag {
    font-size: 80%;
  }

  #errorBox{
    width: 85%;
    padding: 2%;
  }

  #successBox{
    width: 85%;
    padding: 2%;
  }

  .cancelError{
    width: 20px;
  }

  .not_found{
    font-size: 80%;
  }

}

@media screen and (max-width: 500px) {
  .like-div {
    margin-top: 1vh;
    margin-bottom: 2vh;
    width: 80%;
  }
  .size-div > span {
    font-size: 12px;
  }

  .progress-bar {
    height: 5px;
  }
  .logo-img {
    width: 70px;
  }

  .book-img {
    width: 50%;
  }

  .library-title {
    font-size: 30px;
  }
  .library-desc {
    font-size: 18px;
    margin-bottom: 20px;
  }
  .btn {
    font-size: 16px;
  }

  .fw1 {
    width: 115%;
  }

  .fw1 > h3{
    font-size: 90%;
  }

  .library-wrapper1{
    width: 90%;
  }

  .library-title{
    font-size: 150%;

  }

  .each-tag {
    font-size: 70%;
  }

  .file-img{
    display: none;
  }

  .size-div{
    width: 40%;
  }

  .change-link >input {
    margin-left: 10%;
    width: 60%;
  }
}

@media screen and (max-width: 400px) {
  .change-link >input {
    margin-left: 5%;
    width: 60%;
  }

}


</style>