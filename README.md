# MyMoviesApp

Problem - 
Create a backend service for searching and wishlisting movies. A user can login into the application, can search for movies and then add the movies to following lists:

Watched

To watch

Favourites

User can also create more lists like this and 1 movie can exist in their more than 1 list. 

Following APIs need to be created:

GET api/v1/search/ → search a movie by name and other filters(take reference from CLI project) like year, genre etc

GET api/v1/search/autocomplete → search autocomplete API

GET api/v1/search/history → get user’s search history, the items users clicked on search suggestions

GET api/v1/mylists/all → Get a list of all my lists

POST api/v1/mylists → create a new list

GET api/v1/mylists/<list-id> → get details of a specific list (name, created date, etc)

PUT api/v1/mylists/<list-id> → update list details

GET api/v1/movies/?list_name=<list_name>  → get a list of all the movies in a list

 

Create more APIs with contract for:

Adding a movie to a list

Removing a movie from a list

authentication (any technique like jwt)

The basic contract of all APIs can look like this(although you are free to follow your own convention, but it should be consistent across all APIs):


```
// success
{
  "data": [{},{},{}],
  "success": true,
  "meta_data": {
    
  }
}
```
``` 
// error:
{
  "error": {
    "status_code": 404,
    "message": "ID not found",
    "details": ""
  },
  "success": false,
  "meta_data"
}
```

