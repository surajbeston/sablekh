# File 
 One needs to be authenticated to send file and also a library should be created to push files. Keep in mind to store the `library-hid` in localstorage.

### Create File
* Because we're sending files, you need to add `{"content-type": "multipart/form-data"}` to headers.
* A user can create a file under a library by sending `POST` request to `ip/file` in following format:
`{
    "_file": [file],
    "library": "fafbb99e6283af52dd2b2c20814fb4f9e8acadae52a73160b01ca069" 
}
`
* You should get response something like this:
`{
    "hid": "6c7b8f7c6e684eb9b9e18b1e107f968dc506cbd9af56b3838cbfc8ef",
    "title": [file],
    "size": 379,
    "library": "fafbb99e6283af52dd2b2c20814fb4f9e8acadae52a73160b01ca069"
}`

* Don't forget to add `authentication-token` and make sure that the `library-hid` in request belongs to the same user who has been authenticated.

* Only upto 10 files are allowed per library and every file should have size smaller than 30MB.

### Delete File

* To delete a file, you can send `DELETE` request to `ip/file` in following data format:
 `{"hid" : "159456c630b8cf5036b04f72f1f1042d6e8bddace4d82e8298a15a17"}`
 * This should send you following response:
 `{
  "hid": "6c7b8f7c6e684eb9b9e18b1e107f968dc506cbd9af56b3838cbfc8ef",
  "title": [filename],
  "size": 379,
  "library": "fafbb99e6283af52dd2b2c20814fb4f9e8acadae52a73160b01ca069",
  "deleted": true
}`