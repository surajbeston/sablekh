<template>
  <div class="library-component mxw-100-mnh-100">
    <img src="@/assets/back-arrow.png" alt="loading img" class="back-arrow" />
    <img src="@/assets/logo1.png" alt="loading image" class="logo-img" />

    <div class="library-wrapper1">
      <img class="book-img" src="@/assets/search/book2.png" alt="book" />
      <h1 class="library-title">{{library_name}}</h1>
      <p class="library-desc">{{library_desc}}</p>

      <div class="like-div">
        <span>{{likes}}</span>
        <img
          @click="like_clicked"
          v-show="!is_liked"
          src="@/assets/like.png"
          alt="like"
          class="blk-like"
        />
        <img v-show="is_liked" src="@/assets/like1.png" alt="like" class="blu-like" />
        <span>{{downloads}}</span>
        <img src="@/assets/download1.png" alt="download img" class="download-img">
      </div>

      <div class="files-wrapper">
        <div class="fw-each" :key="file.hid" v-for="file in refined_files">
          <div class="fw1">
            <img src="@/assets/filenames/pdf.png" alt="png" />
            <h3>{{file.title}}</h3>
          </div>
          <div class="fw2">
            <input type="checkbox" :id="file.hid" @input="checkbox_clicked(file.hid)" />
          </div>
        </div>
      </div>
      <div v-show="downloading" class="progress-bar">
        <div class="progress" :style="progress_bar_style">
        </div>
      </div>
      <div class="download-container">
        <button @click="download_clicked" class="btn download">Download</button>
        <button @click="download_all_clicked" class="btn download-all">Download all</button>
      </div>
      <button @click="show_change_link" v-show="!changing && authenticated" class="btn" >
        Change Link
      </button>
      <div v-show="changing && authenticated" class="change-link">
        <input type="text" v-model="new_link" :placeholder="lib_id">
        <button @click="link_changed" class="btn change-link-button">Change</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {

  props: ["lib_id"],

  data() {
    return {
      server_address: "https://api.sablekh.com",
      library_name: "",
      library_desc: "",
      library_image_link: "https://pngimg.com/uploads/book/book_PNG51074.png",
      contents: [],
      selected_file: [],
      files: [],
      refined_files: [],
      hid: "",
      likes: 0,
      is_liked: false,
      downloading: false,
      progress: 0,
      new_link: "",
      changing: false,
      token: "",
      authenticated: false,
      downloads: 0
    };
  },

  methods: {
    
    link_changed() {

      axios({
        url: this.server_address + "/change-link",
        headers: {
          ...this.implicit_data(),
          Authorization: "Token " + this.token
        },
        method: 'post',
        data: {
          hid: this.hid,
          link_str: this.new_link
        }
      })
      .then(res => {
        window.location.href = "/library/" + res.data.link_str
      })
      .catch(e => {
        console.log(e)
      })

    },

    show_change_link(){      
      this.changing = true;
    },

    like_clicked() {
      if (!this.token) {
        window.location.href = "login";
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
          console.log(e);
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
          console.log(e);
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
          console.log(e);
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
          console.log(e);
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

      this.progress = 20;

    },

    download_clicked() {
      var file_hids = "";

      if (!this.selected_file.length > 0) {
        alert("None selected");
        return null;
      }

      this.downloading = true;
      this.progress = 0;

      if (this.selected_file.length === 1) {
        // let file = this.files.filter(e => e.hid === this.selected_file[0]) i guess its not necessary

        // if (file.link) {
        //   download(file.link)
        // }
        // else {
        file_hids = this.selected_file[0];
        // }
      } else {
        file_hids = this.selected_file.join(",");
      }
      this.progress = 20
      this.download_middle(file_hids);
    },

    download_middle(file_hids) {
      if (file_hids !== "") {
        this.progress = 60;
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
            // console.log(res)
            this.download(res.data.filename);
            this.progress = 80;
          })
          .catch((e) => {
            alert("try again");
          });
      }
    },

    download(url) {
      let file_name = url.split("/");

      axios({
        url,
        method: "GET",
        responseType: "blob",
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
      });
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
      return {
        site: document.referrer,
        link: window.location.href.toString().split(window.location.host)[1],
        timetaken: new Date().getTime() - this.time,
      };
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
    this.time = new Date().getTime();

    if (!this.lib_id) window.location.replace("/");

    this.token = window.localStorage.getItem("token");
    if (this.token) {
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
        this.hid = res.data.hid;
        this.library_name = res.data.title;
        this.library_desc = res.data.description;
        this.get_like()
        this.get_downloads()
        if (this.token) {
          this.check_like()
        }
        
        axios({
          url: `${this.server_address}/all-files`,
          method: "post",
          data: {
            hid: this.hid,
          },
          headers: this.implicit_data(),
        })
          .then((res) => {
            this.files = res.data;
            this.clean_title();
            // console.log(res);
          })
          .catch((err) => console.log(err));
      })
      .catch((e) => {
        console.log(e);
      });
  },
};
</script>

<style scoped>

.change-link {
  width: 100%;
  display: grid;
  grid-template-columns: 10fr 1fr;
  grid-column-gap: 5px;
}

.change-link-button {
  padding: 5px 10px;
}
.change-link >input {
  outline: none;
  font-size: 20px;
  padding: 0 10px;
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
.download-img,
.blk-like,
.blu-like {
  width: 10%;
  cursor: pointer;
}

.download-img {
  cursor: auto;
}

.like-div {
  margin-top: 5vh;
  padding: 1% 0;
  width: 50%;
  height: 20%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  background-color: rgb(255, 182, 85);
  box-shadow: 0 5px 10px rgb(177, 145, 105);
  border-radius: 10px;
}

.like-div > span {
  margin: 0 5%;
  font-size: 200%;
}

.blu-like,
.blk-like {
  margin-right: 5%;
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
  background-color: white;
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  border-radius: 10px;
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
  padding: 150px 0 10px 0;
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
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.book-img {
  width: 20%;
  box-shadow: 0 0 10px rgb(189, 169, 143);
}
.library-title {
  margin-top: 5%;
  font-size: 210%;
}
.library-desc {
  margin-top: 3%;
  font-size: 150%;
  text-align: center;
}

@media screen and (max-width: 1300px) {
  .library-wrapper1 {
    width: 80%;
  }

  .library-component {
    padding: 120px 0 10px 0;
  }
  .logo-img {
    width: 100px;
  }
}

@media screen and (max-width: 700px) {
  .progress-bar {
    height: 10px;
  }

.download-img,
.blk-like,
.blu-like {
  width: 15%;
  cursor: pointer;
}
  .like-div > span {
    font-size: 30px;
  }
  .like-div {
    padding: 2% 0 ;
    margin-top: 15px;
  }
  .library-wrapper1 {
    width: 90%;
  }

  .files-wrapper {
    width: 90%;
  }

  .back-arrow {
    display: block;
  }
}

@media screen and (max-width: 500px) {
  .progress-bar {
    height: 5px;
  }
  
.like-div {
  margin-top: 10px;
  width: 70%;
}

.like-div > span {
  font-size: 25px;
}
  .logo-img {
    width: 70px;
  }

  .book-img {
    width: 70%;
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
}
</style>