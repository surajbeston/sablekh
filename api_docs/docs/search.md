# Search 
Sablekh has got quite good search engine built with `whoosh`. It can search `title` and `description` fields based on provided query to return a set of `libraries`. And authentication is not required to place a search query, anyone can search.

### Searching Procedure
* It is quite straight forward to place a query. Just send a `POST` request to  `[api-backend]/search`:
`{
    "query": "bullshit"
    "tags": ["tag1", "tag2"]
}`
* This should return response in following format:
`[
    {
        "description": "this is bullshit",
        "hid": "dea0cf6e359c65648472770d6d1c937b3cdebb15cadee276cebffe22",
        "tags": ["tag2"],
        "thumbnail": "default.png",
        "title": "renderless renderer"
    }
]`