<template>
  <div class="library-component mxw-100-mnh-100">
    <img src="@/assets/back-arrow.png" alt="loading img" class="back-arrow" />
    <img src="@/assets/logo1.png" alt="loading image" class="logo-img" />

    <div class="library-wrapper1">

      <img class="book-img" :src="library_thumbnail" alt="book" >
      <h1 class="library-title">{{library_name}}</h1>
      <p class="library-desc">
        {{library_desc}} 
      </p>

      <div class="files-wrapper">
        <div class="fw-each" :key="file.hid" v-for="file in refined_files">
          <div class="fw1">
            <img src="@/assets/filenames/pdf.png" alt="png">
            <h3>{{file.title}}</h3>
          </div>
          <div class="fw2">
            <input type="checkbox" :id="file.hid" @input="checkbox_clicked(file.hid)">
          </div>
        </div>
      </div>

      <div class="download-container">
        <button @click="download_clicked" class="btn download">Download</button>
        <button @click="download_all_clicked" class="btn download-all">Download all</button>
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
      library_thumbnail: ""
    };
  },

  methods: {

    checkbox_clicked(id) {
      if (this.selected_file.includes(id)) {
        let i = this.selected_file.indexOf(id)
        this.selected_file.splice(i, 1)
      }
      else {
        this.selected_file.push(id)
      }
    },

    download_all_clicked() {

      let a = this.files.map(e => e.hid)

      this.download_middle(a.join(","))

    },


    download_clicked() {

      var file_hids = ""

      if (!this.selected_file.length > 0 ) {
        alert("None selected")
        return null
      }
        
      if (this.selected_file.length === 1) {
        // let file = this.files.filter(e => e.hid === this.selected_file[0]) i guess its not necessary

        // if (file.link) {
        //   download(file.link)
        // }
        // else {
        file_hids = this.selected_file[0]
        // }
      }
      else {
        file_hids = this.selected_file.join(',')
      }

      this.download_middle(file_hids)
   
    },

    download_middle(file_hids){
      if (file_hids !== "") {
        axios({
            url: this.server_address + "/download",
            method: "post",
            data: {
              hids: file_hids,
              library: this.hid
            },
            headers: this.implicit_data()
          })
          .then(res => {
            // console.log(res)
            this.download(res.data.filename)

            console.log(res.data)
          })
          .catch(e => {
            alert("try again")
          })
      }
    },

    download(url) {

      let file_name = url.split("/")

          axios({
            url,
            method: "GET",
            responseType: "blob",
          })
          .then((response) => {
            var fileURL = window.URL.createObjectURL(new Blob([response.data]));
            var fileLink = document.createElement("a");
            fileLink.href = fileURL;
            fileLink.setAttribute("download", file_name[file_name.length-1])
            document.body.appendChild(fileLink);
            fileLink.click();
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

      // console.log(this.refined_files);
    },

    implicit_data(){
              return {"site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
          }


  },

  mounted() {

    this.time = new Date().getTime()
    


    if (!this.lib_id) window.location.replace("/");

    axios({
      url: `${this.server_address}/link`,
      method: 'post',
      data: {
        link_str: this.$route.params.id,
      },
      headers: this.implicit_data()
    })
      .then((res) => {
        this.hid = res.data.hid;
        this.library_name = res.data.title;
        this.library_desc = res.data.description;
         this.library_thumbnail = res.data.thumbnail
        axios({
          url: `${this.server_address}/all-files`,
          method: 'post',
          data: {
            hid: this.hid,
          },
          headers: this.implicit_data()
        })
          .then((res) => {
            this.files = res.data;
            this.clean_title();
            console.log(res);
           
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

.download-container {
  margin-top: 5%;
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
  font-family: 'Rajdhani', sans-serif;
}
.library-desc {
  margin-top: 3%;
  font-size: 150%;
  text-align: center;
  font-family: 'Ubuntu', sans-serif;
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