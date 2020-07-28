# User
 This page discusses about the ways to manipulate `user`'s data. 

### Create User

*  This is mentioned in `Authentication` page.

### Retrieve User

*  To retrieve user data, you need to send `blank` `GET` request to `ip\users`.

### Change User

*  This is not enabled for because of the complications with `email-verification` while password reset.

### Delete User

*  To delete a user you should send a `DELETE` request to `ip/users` whith data in this format:
`{
    "hid" : "a9ebc0fe82377cacb2084263636a336c4fa93ffe8d68370d1f06b04d"
}`

*  This should yeild a response like this:
`{
  "hid": "a9ebc0fe82377cacb2084263636a336c4fa93ffe8d68370d1f06b04d",
  "username": "hari",
  "email": "hari@ktm.com.np"
}`
