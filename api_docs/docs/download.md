# Library/File Download
One can download single file or multiple file from a directory or the entire directory. Response will be in zipped form. When you send the `hids` of the file, at first the backend searches for zipped file for the requested hid combination, if its already there then it will be send it as response but if zipped version is not already there then the file should be individually retrieved and then zipped to be sent as response, which then is stored for future requests.

### Download Procedure

* To download a file or a group of files from a directory, user should just send a request in following format:

`{
	"hids" : "77176dbd65ea83e6c56871eacaf181875c92c1a33627e8394aaa353b,44538aca61fdf07e32bc689d9377c214168279c9d627527a076cd575",
	"library": "f3cca10e9b0a0c06d05b3fa431fcff8c40ef1784171e6b7d6ea2c5f3"
}`

* This will give you a response like this:

`{
  "filename": "ip/downloadable/science_notes962082165.zip",
  "by": "created"
}`

* The link on `filename` key can then be used to download file from the static server.