# Library
 A library is a collection of files. And in database level it a `Library` object has one to many relationship with `File` objects.This makes a library hold multiple files. `Remember to place authentication-token in you headers to create, patch and delete libraries. Getting all libraries from a user also requires authentication-token, but getting one library does not require this for obvious reasons.`

### Create Library

*  Library can be created with a `POST` request to `ip/library` with data in following format:
`{
	"title": "History Notes",
	"description": "Contains brief notes about WWI and WWII",
  "tags": ["Tribhuvan University", "Anthropology", "Third Semester", "Social History"]
}`

*  This should result in following :
`{
  "hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca",
  "title": "History Notes",
  "description": "Contains brief notes about WWI and WWII",
  "link_str": "History-Notes-wAsDr",
    "tags": ["Tribhuvan University", "Anthropology", "Third Semester", "Social History"],
  "datetime": "2020-07-26T19:49:22.663912Z"
}`

* This will not actually create a library. you shoud also send a `PATCH` request to the same endpoint with additional boolean variable `finished`. See `Change Library`.

* You won't have it searchable until you alter it once more.

### Retrieve Library

*  This does require the authentication, any user, even without authentication can request this.

*  Library can be retrieved by sending `POST` request to `ip/get-library` with data in following format:
`{
	"hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca"
}`

*  This will return following response:
`{
  "hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca",
  "title": "History Notes",
  "description": "Contains brief notes about WWI and WWII",
  "link_str": "History-Notes-wAsDr",
    "tags": ["Tribhuvan University", "Anthropology", "Third Semester", "Social History"],
  "datetime": "2020-07-26T19:49:22.663912Z",
  "likes": 2,
  "downloads": 5,
  "files": [{
    "hid": "6c7b8f7c6e684eb9b9e18b1e107f968dc506cbd9af56b3838cbfc8ef",
    "title": [file],
    "size": 379,
    "library": "fafbb99e6283af52dd2b2c20814fb4f9e8acadae52a73160b01ca069"
  }]
}`

### Change Library 

*  Library can be changed with `PATCH` request to `ip/ibrary' with data in following format:
`{
  "hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca",    
	"title": "History Notes",
	"description": "Contains brief notes about WWI and WWII and also about their economic impacts.",
  "tags": ["Tribhuvan University", "Anthropology", "Third Semester", "Social History"],
}
`
*  This should yield following json:
`{
  "hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca",
  "title": "History Notes",
  "link_str": "History-Notes-wAsDr",
  "description": "Contains brief notes about WWI and WWII and also about their economic impacts.",
  "tags": ["Tribhuvan University", "Anthropology", "Third Semester", "Social History"],
  "datetime": "2020-07-26T19:55:33.606052Z",
  "deleted": false
}`

*  Remember to add all three fields, `title`, `description` and `tags` , changed value will be checked and updated. 
* 

### Delete Library

*  To delete a library, send `DELETE` request to `ip/library` in follwing format:
`{
	"hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca"
}`

*  This will give following response:
`{
  "hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca",
  "title": "History Notes",
  "link_str": "History-Notes-wAsDr",
  "description": "Contains brief notes about WWI and WWII and also about their economic impacts.",
  "tags": ["Tribhuvan University", "Anthropology", "Third Semester", "Social History"],
  "datetime": "2020-07-26T19:55:33.606052Z",
  "deleted": true
}`

### All libraries from a user

*  For this, you'll have to send a `blank` `POST` request to `ip/all-libraries`.

*  This will result an array of libraries from the authorized user:
` {
  "data": [
    {
      "hid": "ebd960e43d5fef91fa682b6e826a77a06826135226d8077ae6945ee1",
      "title": "sdfasdf",
      "description": "sfdasdfsdf",
      "thumbnail": "https://api.sablekh.com/thumbnails/default.jpg",
      "link_str": "sdfasdf-Mxprw",
      "tags": [
        "sdf",
        "sdfas"
      ],
      "finished": true,
      "datetime": "2020-08-26T12:24:54.065705Z",
      "no_files": 0,
      "likes": 0,
      "downloads": 0
    },
    ....
  ]
      "page": 1,
  "total_pages": 3,
  "number": 10
}`

* Now, with this you may also specify `page` which will return specific `page` content. For that, you will have to send a `POST` request to `ip/all-libraries` in following format:

`{
  "page": 4
  }
`
* This will yeild data similar to previous bullet.

* If you don't specify `page` field in request, by default you will receive `page 1` as shown above.


### Change library link

* You can change library link string to something that user wants to keep, just send a `POST` request to `ip/change-link` whith data in following format:

`{
  "hid": "e815c9146fe738bb57484c8bdab3cd3be1ade2f9848528b1e41c5182",
	"link_str": "wogH0o bhoo * lo"
}`

* This `hid` means `hid of library`.
* You should get similar response:
`{
  "hid": "e815c9146fe738bb57484c8bdab3cd3be1ade2f9848528b1e41c5182",
  "title": "this is title",
  "description": "this is description",
  "tags": ["Tribhuvan University", "Anthropology", "Third Semester", "Social History"],
  "link_str": "wogH0o-bhoo-lo",
  "datetime": "2020-07-30T08:52:18.034731Z",
  "no_files": 0
}`
* This requires the user to be authenticated and the library should belog to the user.

### Getting library from link

* When user pushes a link you'd want to know fetch and display library according to that link, just have to send a `POST` request to `ip/link` in following format:

`{
  "link_str": "wogH0o-bhoo-lo"
}`

* This will return correponding library like this:

`{
  "hid": "e815c9146fe738bb57484c8bdab3cd3be1ade2f9848528b1e41c5182",
  "title": "this is title",
  "description": "this is description",
  "link_str": "wogH0o-bhoo-lo",
  "thumbnail": "default.png",
  "tags": ["Tribhuvan University", "Anthropology", "Third Semester", "Social History"],
  "datetime": "2020-07-30T08:52:18.034731Z",
  "no_files": 0,
  "likes": 2,
  "downloads": 5,
  "files": [{
  "hid": "6c7b8f7c6e684eb9b9e18b1e107f968dc506cbd9af56b3838cbfc8ef",
  "title": [file],
  "size": 379,
  "library": "fafbb99e6283af52dd2b2c20814fb4f9e8acadae52a73160b01ca069"
}]
}`

* Anyone can do this, even without authentication.