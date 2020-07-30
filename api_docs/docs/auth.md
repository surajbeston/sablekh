# Authentication & Authorization

 It is not important for users to be authenticated to search and download libraries but to be able to create libraries user will have to authenticated.

## Authentication

*  First send `POST` request to `ip/users`. And it should be in this format: 
`{
	"email" : "hari@ktm.com.np",
	"password": "password"
}`
*  This will create a new user.
*  This should authenticate user with response similar to this format:
`{
	"username": "hari",
	"email" : "hari@ktm.com.np",
	"password": "password",
    "hid": "a9ebc0fe82377cacb2084263636a336c4fa93ffe8d68370d1f06b04d"
}`
*  You may want to store `hid` in localstorage or cookies for future reference.

## Authorization 

*  This API uses token authentication as mentioned in introduction.
*  So, you should send `POST` request to `ip/token` with data in this format: 
`{
	"username": "hari",
	"password": "password"
}`
*  This should return response similar to this:
`{
  "token": "9bb12bc19309ce2f0ee434972b8e846f3d010887"
}`
*  Now, you should use this `token` for all the jobs through the API to remain authorized. Also save this in localstorage or cookies.

*  For that you should add header in your request in this format:
`{"Authorization": "Token 9bb12bc19309ce2f0ee434972b8e846f3d010887"}`


