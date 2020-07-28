# Library
 A library is a collection of files. And in database level it a `Library` object has one to many relationship with `File` objects.This makes a library hold multiple files. `Remember to place authentication-token in you headers to create, patch and delete libraries. Getting all libraries from a user also requires authentication-token, but getting one library does not require this for obvious reasons.`

### Create Library

*  Library can be created with a `POST` request to `ip/library` with data in following format:
`{
	"title": "History Notes",
	"description": "Contains brief notes about WWI and WWII"
}
`
*  This should result in following :
`{
  "hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca",
  "title": "History Notes",
  "description": "Contains brief notes about WWI and WWII",
  "datetime": "2020-07-26T19:49:22.663912Z"
}`

### Retrieve Library

*  This does require the authentication, any user, even without authentication can request this.

*  Library can be retrieved by sending `GET` request to `ip/get-library` with data in following format:
`{
	"hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca"
}`

*  This will return following response:
`{
  "hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca",
  "title": "History Notes",
  "description": "Contains brief notes about WWI and WWII",
  "datetime": "2020-07-26T19:49:22.663912Z"
}`

### Change Library 

*  Library can be changed with `PATCH` request to `ip/ibrary' with data in following format:
`{
    "hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca",    
	"title": "History Notes",
	"description": "Contains brief notes about WWI and WWII and also about their economic impacts."
}
`
*  This should yield following json:
`{
  "hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca",
  "title": "History Notes",
  "description": "Contains brief notes about WWI and WWII and also about their economic impacts.",
  "datetime": "2020-07-26T19:55:33.606052Z",
  "deleted": false
}`

*  Remember to add both fields, changed value will be checked and updated. 

### Delete Library

*  To delete a library, send `DELETE` request to `ip/library` in follwing format:
`{
	"hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca"
}`

*  This will give following response:
`{
  "hid": "491ae542fb36e33d46824bce48468e62fc6bf84dce0775eb3bdc95ca",
  "title": "History Notes",
  "description": "Contains brief notes about WWI and WWII and also about their economic impacts.",
  "datetime": "2020-07-26T19:55:33.606052Z",
  "deleted": true
}`

### All libraries from a user

*  For this, you'll have to send a `blank` `GET` request to `ip/all-libraries`.

*  This will result an array of libraries:
`[
  {
    "hid": "4d42c43296e22f397ac4d5e57eabcc9a99c8e49372f23ac71f01c23c",
    "title": "History Notes",
    "description": "Contains brief notes about WWI and WWII",
    "datetime": "2020-07-26T19:47:53.353703Z"
  }
]`
