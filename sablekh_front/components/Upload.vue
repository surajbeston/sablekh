<template>
    <div>
        <div class="upload-component mxw-100-mnh-100">
            <div class="upload-wrapper1" ref = "fileform" >
                <img src="@/assets/upload/upload-top.png" alt="loading image" class="upload11" >
                <div class="upload12" >
                    <div class = "content">
                        <h1 class = "head1">Upload</h1>
                        <p class = "description">Create your small library and share it with the world. You can add upto 10 files, each not exceeding 30MB in size.</p>
                        <div class="input-section" v-bind:class="{alternative: activate}">
                            <div id = "errorBox" v-show="hasError" ><p id = "errorTxt"> {{error}}<img src = "@/assets/cancel.png" @click="hasError =!hasError" class = "cancelError"></p></div>

                            <label for="title">Title {{letters_title}}/150</label>
                            <input class="input-box" type="text" v-model="title" id="title" autofocus >
                            <label for="description">Description {{letters_description}}/600</label>
                            <textarea class="input-box" v-model="description" id="description" cols="30" rows="5"></textarea>
                            <label for="file" >{{fileLabel}}</label> 
                            <input type="file" name="upload_file" id="file" @change="filesChange($event.target.files)" multiple class = "hamro">
                            <div class = "files-wrap"> 
                                <div class = "file-box" v-for="file in files" :key = "file.random_id">
                                    <img :src = "file.filename" class = "extension-image"> 
                                    <div class = "middle-collection"> 
                                        <div>
                                            <div class = "download-filename">{{file.name}}</div>
                                            <div class = "right-box">
                                                <img src = "@/assets/upload/upload.png" class = "upload-img" v-show = "!file.uploaded" ><img src = "@/assets/upload/upload-green1.png" class = "upload-img" v-show = "file.uploaded">
                                                <div class = "file-size"> {{file.uploadedsize}}MB/{{file.totalsize}}MB</div>
                                            </div> 
                                        </div>
                                        <div class = "progressbar" ><div class = "progress" v-bind:style= "{width: file.progress}"></div></div> 
                                    </div>
                                    <img src = "@/assets/cancel.png" class = "cancelDownload" @click="cancelUpload(file.random_id)" :class = "{invisible: !file.uploaded}">                                  
                                </div>
                            </div>
                            <div>
                                <div class = "tag-box">
                                    <div class = "tag-capsule" v-for = "tag in tags" :key="tag">{{tag}} <img src = "@/assets/cancel.png" class = "cancelTag" @click= "cancelTag(tag)"></div> 
                                </div> 
                                <div class = "tag-search"> 
                                    <div class = "tagsearchcapsule" v-bind:class="{  removeRadius: show_suggestions  }">
                                        <input class = "tag-search-input" v-model="tag_search" @click = "check_and_show"><img src = "@/assets/cancel.png" class = "addTag"  v-bind:class = "{ rotate: show_suggestions }" @click = "closeSuggestions"> 
                                    </div> 
                                    <div class = "tag-search-box" v-show = "show_suggestions">
                                        <div v-for = "suggestion in suggestions" :key = "suggestion">
                                            <hr><div class = "tag-search-suggestion" @click = "addTag(suggestion)" >{{suggestion}}</div>
                                        </div>
                                            
                                    </div>
                                </div> 
                            </div>
                        </div>
                    </div>
                    <div v-show="is_owner && wants_to_delete && lib_str" class="alert-box">
                        <h3>Are you sure of deleting this library ?</h3>
                        <div class="buttons">
                            <button class="btn yes-btn" @click="yes_button">Yes</button>
                            <button class="btn no-btn" @click="no_button">No</button>
                        </div>
                    </div>
                    <button style="margin-top: 10px;" class="btn" @click = "final_finish">{{finish}}</button>
                    <button v-show="is_owner && lib_str" class="btn delete-btn" @click="delete_button">Delete</button>
                </div>
                <img src="@/assets/logo1.png" alt="loading image" class="upload13">
            </div> 
        </div>
    </div>
</template>

<script>
import axios from "axios"
import Fuse from 'fuse.js' 
import Mime from 'mime-types'


export default {
    data() {
        return{
            is_owner: false,
            wants_to_delete: false,
            title: "",
            description: "",
            // files: [{"name": "something.pdf", "filename": "/filenames/pdf.png", "uploadedsize": "12", "totalsize": "25"}, {"name": "something.txt", "filename": "/filenames/text.png", "uploadedsize": "12", "totalsize": "25"}],
            files: [],
            url: "https://api.sablekh.com/",
            library: "",
            auth_token: "",
            last_title: "",
            last_description: "",
            headers: "",
            hasError: false,
            error: "This is error.",
            onDrag: true,
            fileLabel: "Drag & drop/click to add file",
            activate: false,
            file_hids: [],
            tags: [],
            suggest_tags: [],
            tag_search: "Add tags for your library",
            show_suggestions: false,
            finish: "Finish",
            time: 0,
            to_search: ["Tribhuvan University", "Purwanchal University", "First Semester", "Second Semester", "Third Semester", "Fourth Semester", "First Year", "Second Year", "Third Year", "Fourth Year", "Pokhara University", "Kathmandu University", "Economics", "Mechanical Engineering", "Social Engineering", "Sociology"]
        }
    },

    props: [
        'lib_str'
    ],

    methods: {

        delete_button() {
            this.wants_to_delete = true;
        },

        yes_button() {

            axios({
                url: this.url + "library",
                method: 'delete',
                headers: {
                    ...this.implicit_data(),
                    Authorization: 'Token ' + this.auth_token
                },
                data: {hid: this.library}
            })
            .then(res => {
                window.location.href = "/library"
            })
            .catch(err => alert("Delete not avialable for this library!"))

        },

        no_button() {
            
            this.wants_to_delete = false;

        },

        library_stuffs() {

            axios({
                url: this.url + "all-libraries",
                method: 'post',
                headers: {
                    ...this.implicit_data(),
                    Authorization: 'Token ' + this.auth_token
                },
            })
            .then(res => {
                if (res.data.filter(e => e.hid === this.library)) {
                    this.is_owner = true;
                }
            })
            .catch(e => alert("Internal error"))

        },

        filesChange(files){
            if (this.library === ""){
                if (this.title == "" || this.description == ""){
                    var title = String(Math.random()*10**17)
                    var description = String(Math.random()*10**17)
                }
                else{
                    var title = this.title
                    var description= this.description
                } 
                console.log(this.auth_token)
                axios({
                    url: this.url+"library",
                    method: "post",
                    headers: {"Content-Type": "application/json", "Authorization": "Token "+this.auth_token, ...this.implicit_data()},
                    data: {"title": title, "description": description, "tags": this.tags}
                }).then(res => {
                    this.library = res.data.hid
                    console.log(this.library)
                    this.last_title = res.data.title
                    this.last_description = res.data.description
                    this.last_tags = res.data.tags
                    this.send_files(files)
                })
                .catch(err => {
                    console.log(err)
                    this.displayError("Problem uploading file, please try again.")
                })
            }
            else{
                console.log(files)
                this.send_files(files)
                }
            },
            send_files(files){
                if (this.files.length >= 10){
                    this.displayError("To make library compact, we only allow 10 files per library." )
                }
                for (var file of files){
                        if (file === undefined){
                            this.displayError("Problem uploading file. Please try again.")
                            continue
                        }
                        var already_uploaded = false
                        console.log("reached here")
                        for (var already_file of this.files){
                            console.log("reached here")
                            console.log(already_file.size_bytes)
                            console.log(file.size)
                            if (already_file.size_bytes == file.size){
                                console.log("already reaced here")
                                this.displayError(file.name + " already uploaded/in queue.")
                                already_uploaded = true
                                break
                            } 
                        }
                        if (already_uploaded){continue}
                        if (file.size/1024/1024 <=30){
                        console.log(file.size)
                        var dom_file_name = file.name;
                        if (dom_file_name.length > 20){
                            dom_file_name = dom_file_name.slice(0, 17)+ "..."
                        }
                        var totalsize = (file.size/1024/1024).toFixed(2)
                        if (totalsize == 0){totalsize = 0.01} 
                        this.files.push({"name": dom_file_name, "totalsize": totalsize, "uploadedsize": 0, "filename": "/filenames/" + this.get_filename(file.type), "progress": "0", "size_bytes": file.size, "random_id": String(Math.random()*10**17), "uploaded": false, "hid": ""})
                        var file_index = this.files.length - 1
                        var formData = new FormData()
                        formData.append("_file", file) 
                        formData.append("library", this.library) 
                        axios({
                            url: this.url+"file",
                            method: "post",
                            headers: {"Content-Type": "application/json", "Authorization": "Token "+this.auth_token, ...this.implicit_data()},
                            data: formData,
                            onUploadProgress: (e) => {
                                for (var file of this.files){

                                    if (Math.abs(file.size_bytes/1024 - e.total/1024) <= 5 ){
                                        console.log("reached here")
                                        file.uploadedsize = (e.loaded/1024/1024).toFixed(2);
                                        file.progress = Math.round(e.loaded/e.total*100) + "%";
                                    } 
                                } 
                            }
                            }).then(res => {
                                if (this.library != ""){ 
                                    this.file_hids.push(res.data.hid) 
                                }
                                for (var file of this.files){

                                        if (Math.abs(file.size_bytes/1024 - res.data.size) <= 5){
                                            file.uploadedsize = file.totalsize
                                            file.progress = 100+ "%"
                                            file.uploaded = true
                                            file.hid = res.data.hid
                                            console.log("finished id", file.random_id)
                                        }
                                    }
                                console.log(res.data)
                            })
                            .catch(err => {
                                console.log(err)
                            });
                    }
                    else {
                        this.displayError(file.name + " exceeds file size limit of 30MB.")
                    }
                }
            },
            get_filename(fileType){
                    console.log(fileType)
                    var filename;
                    if (file.size/1024/1024 <= 30)
                        var category = fileType.split("/")[0] 
                        var extension = fileType.split("/")[1]
                         if ( category == "application"){
                             if (extension == "pdf"){
                                 filename = "pdf.png"
                             }
                             else if (extension == "msword"){
                                 filename = "word.png"
                             }
                             else if (extension == "vnd.ms-excel"){
                                 fiename = "excel.png"
                             }
                             else if (extension == "vnd.ms-powerpoint"){
                                 filename = "powerpoint.png"
                             }
                             else if (extension == "zip"){
                                 filename = "zip.png"
                             }
                             else if (extension == "x-tar"){
                                 filename = "zip.png"
                             }
                             else if (extension == "octet-stream"){
                                 filename = "binary.png"
                             }
                             else if (extension == "vnd.openxmlformats-officedocument.spreadsheetml.sheet"){
                                 filename = "excel.png"
                             }
                             else{
                                 console.log("reached here")
                                 filename == "text.png"
                             }
                         }
                         else if (category == "audio"){
                             filename = "audio.png"
                         }
                         else if (category == "image"){
                             filename = "image.png"
                         }
                         else if (category == "text"){
                             filename = "text.png"
                         }
                         else if (category == "video"){
                             filename = "video.png"
                         }
                         else{
                             filename = "text.png"
                            }
                        if (filename === undefined){
                            filename = "text.png"
                        } 
                        return filename
            },
            final_finish(){
                if (this.finish == "Finish"){
                    if (this.files.length > 0){
                        if (this.description == "" || this.title == ""){
                            this.displayError("Title and Description fields are required to create a library.")
                        }
                        else{
                            var continue_on = true
                            console.log("there is title iand description")
                            for (var file of this.files){
                                if (!file.uploaded){
                                    this.displayError("Please wait until file upload is completed.")
                                    continue_on = false
                                    break
                                }
                            }
                            if (continue_on){
                                console.log("no remaining upload, started axios")
                                axios({
                                    url: this.url + "library",
                                    method: "patch",
                                    headers: {"Content-Type": "application/json", "Authorization": "Token "+this.auth_token, ...this.implicit_data()},
                                    data: {"hid": this.library, "title": this.title, "description": this.description, "tags": this.tags, "finished": true}
                                }).then(res => {
                                    this.finish = "Just a second"
                                    window.location.replace("/library/" + res.data.link_str)
                                })
                                .catch(err => {
                                    console.log(err)
                                });
                                
                            }
                        }
                    }
                    else {
                        this.displayError("Please upload something to finish creating library.")
                    }
                }
            },
            displayError(errorText){
                this.hasError = true
                this.error = errorText
            },
        cancelUpload(random_id){
            console.log(random_id)
            for (var i in this.files){
                if (this.files[i].random_id == random_id){
                    var hid = this.files[i].hid
                    console.log(hid)
                    this.files.splice(i, 1)
                    axios({
                        url: this.url + "file",
                        method: "delete",
                        headers: {"Content-Type": "application/json", "Authorization": "Token "+this.auth_token , ...this.implicit_data()},
                        data: {"hid": hid}
                    }).then( res => {
                        console.log(res.data)
                    })
                }
            }
        },
        cancelTag(tag){
            var index = this.tags.indexOf(tag)
            this.tags.splice(index, 1)
        },
        addTag(tag){
            this.tags.push(tag)
            this.show_suggestions = false
        },
        check_and_show(){
            if (this.tag_search == "Add tags for your library"){
                this.tag_search = ""
            }
            if (this.suggestions != undefined){
                if (this.suggestions.length > 0){
                    this.show_suggestions = true
                }
            }
        },
        closeSuggestions(){
            if (this.show_suggestions){
                this.show_suggestions = false
            }
        },
        implicit_data(){
            return {"site": document.referrer, "link": window.location.href.toString().split(window.location.host)[1], "timetaken": new Date().getTime() -this.time }
        }
    },
    computed: {
        suggestions(){
            if (this.tag_search == "" || this.tag_search == "Add tags for your library"){
                this.show_suggestions = false
                
            }
            else{
                var options = {}

                var fuse = new Fuse(this.to_search, options)
                var results = fuse.search(this.tag_search)

                var suggestion_list = []

                for (var result of results){
                    if (!this.tags.includes(result.item)){suggestion_list.push(result.item)}
                }
                console.log(suggestion_list)
                if (suggestion_list.length > 0){
                    this.show_suggestions = true
                    return suggestion_list.slice(0, 5)
                }
                this.show_suggestions = false
            }
        },
        letters_description(){
            var length = this.description.length
            if (length >= 600) this.description = this.description.slice(0, 599)
            return length
        },
        letters_title(){
            var length = this.title.length
            if (length >= 150) this.title = this.title.slice(0, 14)
            return length
        }
    },
    mounted() {

        this.auth_token = window.localStorage.getItem('token')
        if (!this.auth_token) {
            window.location.replace("/login")
            }

        ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'drop'].forEach( function( evt ) {
            this.$refs.fileform.addEventListener(evt, function(e){
                e.preventDefault();
                e.stopPropagation();
                this.activate = true
                this.fileLabel = "Drop it!"
                }.bind(this), false);
        }.bind(this));

        ['dragleave'].forEach( function( evt ) {
            this.$refs.fileform.addEventListener(evt, function(e){
                e.preventDefault();
                e.stopPropagation();
                this.activate = false
                this.fileLabel = "Drag & drop/click to add file"
                }.bind(this), false);
        }.bind(this));

        this.$refs.fileform.addEventListener('drop', function(e){

            this.activate = false
            this.fileLabel = "Drag & drop/click to add file"
            document.getElementById("file").style.backgroundColor = "sky-blue";
            this.filesChange(e.dataTransfer.files)
            
        }.bind(this));

        this.time = new Date().getTime()

        if (this.lib_str) {

            var i = 0;

            this.library_stuffs()

            axios({
                url: this.url + "link",
                method: 'post',
                data: {
                    link_str: this.lib_str
                },
                headers: this.implicit_data()
            })
            .then(res => {
                this.title = res.data.title,
                this.description = res.data.description
                this.library = res.data.hid

                axios({
                    url: this.url + "all-files",
                    method: 'post',
                    data: {
                        hid: this.library
                    },
                    headers: this.implicit_data()
                })
                .then(res => {
                    this.files = res.data
                    this.files = this.files.map(e => {
                        let a = {   
                                    ...e,
                                    name: e.title,
                                    filename: this.get_filename(e.title),
                                    progress: '100%',
                                    totalsize: (e.size / 1024).toFixed(2),
                                    uploadedsize: (e.size / 1024).toFixed(2),
                                    filename: "/filenames/" + this.get_filename(Mime.lookup(e.title)),
                                    random_id: i++,
                                    uploaded: true
                                }
                        return a
                    })
                })

            })
            .catch(e => {
                console.log(e)
                alert('error')
            })

        }



    }
}
</script>

<style scoped>
    .upload-component {
        background-color: rgb(254, 227, 200);
        color:rgb(51, 47, 43);
        padding-bottom: 2vh;
    }
    .upload-wrapper1 {
        display: flex;
        position: relative;
        width: 100%;
    }
    .back-arrow {
        display: none;
        position: absolute;
        top: 50px;
        left: 5px;
        width: 40px;
        height: 35px;
    }
    .upload11 {
        width: 25%;
        height: 25%;
    }
    .upload12 {
        position: relative;
        width: 60%;
        margin: 10vh 0 0 5vw;
    }
    .upload12 > h1 {
        margin-bottom: 2vh;
    }
    .upload12 > p {
        color: rgb(90, 81, 72);
        font-weight: 400;
        margin: 1vh 0;
    }
    .input-section {
        margin: 5vh 5vw;
        display: flex;
        flex-direction: column;
    }
    .input-section > input {
        letter-spacing: 1px;
    }
    .input-section > label {
        font-family: 'Rajdhani', sans-serif;
        margin-top: 1vh;
        font-size: 170%;
    }
    .input-section > [type="file"] {
        width: .1px;
        height: .1px;
        opacity: 0;
        overflow: hidden;
        z-index: -1;
    }
    .input-section > [for="file"] {
        text-align: center;
        width: 100%;
        height: 20vh;
        padding-top: 9vh;
        border: 2px dashed rgb(90, 81, 72);
        border-radius: 10px;
        margin-top: 2vh;
        cursor: pointer;

    }
    .alternative > [for="file"]{
        background-color: rgb(248, 165, 82);
    }
    .upload13 {
        width: 10%;
        position: absolute;
        right: 2vw;
        top: 2vh;
    }

    .head1{
        font-family: 'Staatliches', cursive;
        letter-spacing: 5px;
        font-size: 250%;
    }

    .description{
        font-family: 'Comfortaa', cursive;
        padding-right: 20%;
        font-size: 120%;
    }


    .btn {
        background-color: rgb(255, 176, 98);
        font-weight: bold;
        font-size: 16px;
        letter-spacing: 1px;
        border-radius: 5px;
        cursor: pointer;
    }

    .delete-btn {
        position: absolute;
        background-color: rgb(255, 99, 99);
        right: 0;
        bottom: 0;
    }

    .alert-box {
        margin-top: 5px;
        padding: 2%;
        text-align: center;
        display: flex;
        flex-direction: column;
        border: 2px solid rgb(145, 121, 90);
        border-radius: 10px;
        background-color: rgba(255, 0, 0, 0.226);
    }

    .buttons {
        display: inline;
    }

    .yes-btn {
        background-color: rgb(255, 99, 99);
    }

    .no-btn {
        margin-left: 2%;
        margin-top: 2%;
        background-color: rgb(109, 216, 109)
    }

    .input-box {
        padding: 15px 10px;
        font-size: 20px;
        margin-top: 1vh;
        background: none;
        outline: none;
        border: 2px solid rgb(87, 77, 66);
        border-radius: 10px;
        font-family: 'Ubuntu', sans-serif;
    }

    #errorBox{
        background-color: rgba(255, 0, 0, 0.4);
        color: rgb(51, 47, 43);
        border: 1px black solid;
        border-radius: 5px;
        padding : 2%;
        font-size: 110%;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 200;

        animation-name: fadein;
        animation: fadein 1s;
    }

    @keyframes fadein {
        from { opacity: 0; }
        to   { opacity: 1; }
    }

    .darken{
        background-color: black;
        opacity: 0.4;
        position: absolute;
        top: 0;
        height: 100%;
        width: 100%;
    }

    .cancelError{
        cursor: pointer;
        right: 0;
        float: right;
    }

    .file-box{
        width: 100%;
        border-radius: 5px;
        background-color: #fee3c8;
        border: 2px solid rgba(87, 77, 66, 0);
        box-shadow: 0px 0px 6px rgba(87, 77, 66, 0.5);
        margin-bottom: 5%;
    }


    .files-wrap{
        padding-top: 5%;
        padding-bottom: 5%;
    }

    .extension-image{
        height: 60px;
        display: inline-block;
    }

    .middle-collection{
        display: inline-block;
        position: relative;
        top: -30px;
        font-family: 'Ubuntu', sans-serif;
    }

    .progressbar{
        width: 42vw;
        height: 10px;
        background-color: rgba(188, 182, 216, 0.8);
        position: relative;
        border-radius: 5px;
    }

    .progress{
        background-color: rgb(17, 15, 14);
        border-radius: inherit;
        width: 99%;
        height: 100%;
        position: relative;
        left: 0;
    }

    .download-filename{
        display: inline-block;
        width: 29%;
    }

    .upload-img{
        display: inline-block;
        position: relative;
        bottom: -5px;
    }
    
    .file-size{
        display: inline-block;
    }

    .right-box{
        display: inline-block;
        width: 70%;
        text-align: right;
        margin-bottom: 10px;

    }
    .cancelDownload{
        position: relative;
        top: -5px;
        left: 10px;
    }
    .invisible{
        display: none;
    }

    .cancelDownload:hover{
        cursor: pointer;
    }

    .tag-box{
        display: inline-block;
        font-family: 'Comfortaa', cursive;
        font-size: 100%;
    }

    .tag-capsule{
        display: inline-block;
        border: 3px solid rgb(255, 176, 98);
        border-radius: 5px;
        padding: 5px 5px 0 5px;
        margin: 5px;
        font-weight: bolder;
    }

    .tag-search{
        display: inline-block;
        font-family: 'Comfortaa', cursive;
        font-size: 100%;
        font-weight: bolder;
        vertical-align: top;
        
    }
    .tag-search-box{
        font-family: 'Comfortaa', cursive;
        font-size: 100%;
        font-weight: bolder;
        padding: 5px;
        text-align: center;
        background-color: rgb(255, 176, 98);
        border-bottom-right-radius: 20px;
        border-bottom-left-radius: 20px;
    }

    .tag-search-input{
        background-color: rgb(255, 176, 98);
        border: none;
        margin-left: 15px;
        padding: 10px;
        min-width: 10vw;
        font-family: 'Comfortaa', cursive;
        font-size: 100%;
        font-weight: bolder;
        text-align: center;
        outline: none;
    }

    .tagsearchcapsule{
        background-color: rgb(255, 176, 98);
        border-radius: 20px;
    }

    .tag-search-suggestion{
        margin: 5px;
        padding: 5px;
        border-radius: 10px;
    }

    .tag-search-suggestion:hover{
        background-color: rgb(230, 114, 0);
        cursor:pointer;
    }

    .removeRadius{
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
    }

    .addTag{
        position: relative;
        top: 5px;
        margin-left:5px;
        margin-right: 5px;
        transform: rotate(45deg);
    }

    .rotate{
        transform: rotate(0deg);
    }

    .cancelTag{
        width: 20px;
        height: 20px;
        margin-left: 10px;
        margin-bottom: 0;
    }
    .cancelTag:hover{
        cursor: pointer;
    }


    @media screen and (max-width: 1500px){
        .progressbar{
            width: 40vw;
        }
        .right-box{
            width: 70%;
        }
    }

    @media screen and (max-width: 1200px){
        .progressbar{
            width: 47vw;
        }
        /* .upload13{
            display: none;
        } */
        
        .upload12{
            width: 80%;
        }

        .right-box{
            width: 60%;
        }

        
    }

    @media screen and (max-width: 900px){
        .progressbar{
            width: 43vw;
        }
        
    }

    @media screen and (max-width: 700px){
        .upload-wrapper1 {
            width: 98%;
        }
        .back-arrow {
            display: block;
        }
        .upload11 {
            position: absolute;
            top: 100px;
            height: 150px;
            width: 150px;
            /* display: none; */
        }
        .head1 {
            margin-top: 20px;
            margin-left: 10px;
        }
        .upload13 {
            width: 100px;
        }
        .upload12 {
            width: 100%;
            margin: 5px;
            margin-top: 250px;
        }
        .description{
            padding-right: 0;
            font-size: 90%;
            margin-right: 10px;
            margin-left: 20px;
            margin-bottom: 20px;
        }
        .input-section {
            margin: 0;
        }
        .input-section > label {
            font-size: 120%;
        }
        .input-box {
            font-size: 16px;
            padding: 5px 10px;
        }
        .progressbar{
            width: 70vw;
        }

    }

    @media screen and (max-width: 500px){
    .progressbar{
            width: 67vw;
        }
    .download-filename {
        font-size: 90%;
    }
    .right-box{
        font-size: 90%;
    }

    }

    @media screen and (max-width: 500px){
    .progressbar{
            width: 69vw;
        }

    .download-filename {
        font-size: 80%;
    }
    .right-box{
        font-size: 80%;
    }
    .upload-img{
        width: 15%;
    }

    .cancelDownload{
        width: 20px;
    }


    }

@media screen and (max-width: 400px){

    .extension-image{
        width: 13%;
    }
}


    /* @media screen and (max-width: 450px){
    .progressbar{
            width: 60vw;
        }
    } */






</style>