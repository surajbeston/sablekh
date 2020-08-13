<template>
  <div class="library-component mxw-100-mnh-100">
    <img src="@/assets/back-arrow.png" alt="loading img" class="back-arrow" />
    <img src="@/assets/logo1.png" alt="loading image" class="logo-img" />
    <div class="library-wrapper1">
      <div class="library11">
        <img src="@/assets/search/book2.png" alt="loading image" />
        <a href="#">Read here</a>
        <div class="library111">
          <h1>Contents</h1>
          <div class="library-contents">
            <ul>
              <li :key="content" v-for="content in contents">{{content}}</li>
            </ul>
          </div>
        </div>
      </div>
      <div class="library12">
        <h1>{{library_name}}</h1>
        <p>{{library_desc}}</p>
        <h2>Download PDFs</h2>
        <div class="library121">
          <div :key="file.hid" v-for="file in refined_files" class="each-files">
            <img src="@/assets/filenames/pdf.png" alt="loading-img" class="pdf-image" />
            <span>{{file.title}}</span>
            <img src="@/assets/download.png" alt="loading image" class="download-img" @click="download_clicked(file)"/>
          </div>
        </div>
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
      server_address: "http://localhost",
      library_name: "",
      library_desc: "",
      library_image_link: "https://pngimg.com/uploads/book/book_PNG51074.png",
      contents: [],
      files: [],
      refined_files: [],
      hid: "",
    };
  },

  methods: {
    download_clicked(file) {

        if (!file.link) {
            axios.post(this.server_address + "/download", {
                hids : file.hid,
                library: file.library
            })
            .then(res => {
                this.download(this.server_address + '/download/' + res.data.filename)
            })
            .catch(e => console.log(e))
        }

        else {
            this.download(file.link)
        }

        
    },

    download(url) {
          axios({
            url,
            method: "GET",
            responseType: "blob",
          })
          .then((response) => {
            var fileURL = window.URL.createObjectURL(new Blob([response.data]));
            var fileLink = document.createElement("a");
            fileLink.href = fileURL;
            fileLink.setAttribute("download", "download.zip");
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

      console.log(this.refined_files);
    },
  },

  mounted() {
    if (!this.lib_id) window.location.replace("/");

    axios
      .post(`${this.server_address}/link`, {
        link_str: this.$route.params.id,
      })
      .then((res) => {
        this.hid = res.data.hid;
        this.library_name = res.data.title;
        this.library_desc = res.data.description;

        axios
          .post(`${this.server_address}/all-files`, {
            hid: this.hid,
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
.library-component {
  background-color: rgb(254, 227, 200);
  padding: 150px 0 10px 0;
  position: relative;
}
.back-arrow {
  cursor: pointer;
  position: absolute;
  width: 35px;
  height: 20px;
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
  border-radius: 10px;
  box-shadow: 0 0 10px rgb(187, 167, 142);
  width: 90vw;
  margin: 0 auto;
  padding: 1.5vw;
  display: flex;
}
.library11 > img {
  width: 20vw;
  box-shadow: 0 0 10px rgb(151, 137, 118);
  margin-right: 2vw;
  margin-bottom: 5vh;
}
.library11 > a {
  font-size: 18px;
}
.library111 {
  margin-top: 5vh;
  padding: 10px;
  width: 20vw;
  box-shadow: 0 0 10px rgb(165, 143, 115);
  border-radius: 10px;
}
.library-contents > ul {
  margin: 10px 0 0 20px;
}
.library-contents > ul > li {
  padding: 5px 10px;
  font-size: 20px;
}
.library12 {
  width: 100%;
  padding: 10px 2vw;
}
.library12 > h1 {
  font-size: 500%;
}
.library12 > p {
  margin-top: 10px;
  font-size: 120%;
  text-align: justify;
}
.library12 > h2 {
  font-size: 30px;
  margin-top: 10vh;
  margin-bottom: 2vh;
}
.library121 {
  max-height: 70vh;
  min-height: 20vh;
  overflow-y: auto;
}
.each-files {
  display: flex;
  align-items: center;
  margin: 0 auto;
  position: relative;
  margin-top: 20px;
  width: 70%;
  height: 70px;
  border-radius: 20px;
  padding: 5px 20px;
  background-color: rgb(238, 198, 147);
}
.each-files > span {
  margin: 0 0 0 2vw;
  font-size: 20px;
  letter-spacing: 1px;
  font-weight: bold;
}
.each-files > a {
  width: 100%;
  height: 100%;
}
.download-img {
  cursor: pointer;
  position: absolute;
  right: 20px;
  width: 60px;
}

@media screen and (max-width: 1300px) {
  .library-component {
    padding: 120px 0 10px 0;
  }
  .logo-img {
    width: 100px;
  }
  .library-wrapper1 {
    width: 95vw;
  }
  .library12 > h1 {
    font-size: 250%;
  }
  .library12 > p {
    font-size: 16px;
  }
  .library12 > h2 {
    font-size: 25px;
  }
  .library111 > h1 {
    font-size: 20px;
  }
  .library-contents > ul {
    margin: 5px 5px;
  }
  .library-contents > ul > li {
    padding: 5px 5px;
    font-size: 16px;
  }
  .library12 {
    padding: 10px 10px;
  }
  .library121 {
    max-height: 50vh;
  }
  .each-files {
    height: 50px;
  }
  .pdf-image {
    width: 70px;
  }
  .each-files > span {
    font-size: 14px;
  }
  .download-img {
    width: 40px;
  }
}

@media screen and (max-width: 700px) {
  .library11 > a {
    font-size: 14px;
  }
  .back-arrow {
    display: block;
  }
  .library12 > h1 {
    font-size: 200%;
  }
  .library12 > p {
    font-size: 14px;
  }
  .library12 > h2 {
    font-size: 18px;
  }
  .library111 > h1 {
    font-size: 14px;
  }
  .library-contents > ul {
    margin: 2px 0px;
    padding: 0 0 0 20px;
  }
  .library-contents > ul > li {
    padding: 2px 0px;
    font-size: 12px;
  }
  .library121 {
    max-height: 40vh;
  }
  .each-files {
    width: 100%;
    height: 30px;
  }
  .pdf-image {
    width: 50px;
  }
  .each-files > span {
    font-size: 10px;
  }
  .download-img {
    width: 20px;
  }
}

@media screen and (max-width: 500px) {
  .logo-img {
    width: 70px;
  }
  .library-component {
    padding: 90px 0 10px 0;
  }
  .library11 {
    display: none;
  }
  .library12 > h1 {
    font-size: 150%;
  }
}
</style>