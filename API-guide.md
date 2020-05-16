
# REST API documentation        !!!!!!!!!!!!! IN PRODUCTION THERE IS NO CODE YET OR ONLINE VERSION !!!!!!!!!!!!
>  All endpoints explained

## Login

Use API as admin:

login: admin

password: admin

Token: d5c46c545a579513e88456bd8a85aee36e7a646f

## Endpoints

| URI                                              | GET                                                 | POST                                  | PUT                               | DELETE                                      |
| ----------------------------------------------------- | --------------------------------------------------- | ------------------------------------- | --------------------------------- | ------------------------------------------- |
| [/api/v1/](#URIs list)                             | Returns a list of links to the other available URIs | N/A                                   | N/A                               | N/A                                         |
| [/api/get-token](#Token)                                 | N/A                            | Returns token for user                 | N/A                               | N/A                                         |
| [/api/v1/users/](#Users)                                 | Returns a list of users                           | N/A                   | N/A                               | N/A                                         |
| [/api/v1/users/{id}](#Users)                                 | Returns a user                           | N/A                   | N/A                               | N/A                                         |
| [/api/v1/informations/](#Informations)                                 | Returns a list of informations                           | Creates a new information                   | N/A                               | N/A                                         |
| [/api/v1/informations/{id}](#Informations)                                 | Returns a information                           |   N/A                 | Updates a information                               | Deletes a information                                        |N/A 
| [/api/v1/informations/{id}/detail/](#Informations)                                 | Returns a more detailed  information                           |     N/A                | N/A                               | N/A                                         |




### URIs list
#### Single example: 

```
{
    TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
}
```

| URI | Method   |**GET** |
| --- |  ------- |  ------- |
| `/api/v1/`  | Permission |All      |

> GET

Returns list of avalible URIs.

### Token

#### Single example: 

```
{
    "token": "dee9a966e4fe39abf1e59b9e950d28632e4454f6"
}
```

#### Permissible Fields

| Element / Attribute     | POST       |  
| ----------------------- | --------- | 
| **username**                    | Required  | 
| **password**              | Required   |

| URI | Method   |**POST** |
| --- |  ------- |  ------- |
| `/api/get-token`  | Permission |All      |

> POST

Returns token for user.









### Users

#### Single example: 

```
{
    "id": 2,
    "username": "mwjxfqdgw",
    "first_name": "Maxwell",
    "last_name": "Mazurek",
    "email": "gkhopldi@mail2uptown.com",
    "branch": "Lublin",
    "image": "http://127.0.0.1:8000/media/profile_image/1.jpg"
}
```

#### Sortable Fields

| Filter                | Type | lookups           | Description |
| --------------------- | --|---------------- | ----------- |
| **search**                | | SearchFilter           | Search given value in: username, last_name, email, position, branch  |
| **fields**      | |Selective fields          | Returns only selected fields |
| **omit**      | |Selective fields          | Returns all fields except omitted ones |
| **page**      | |Pagination          | Returns page |
| **page_size**      | |Pagination          | Returns number of records on page (default=50, max_page_size=500 |

| URI                  | Method         |**GET**     |
| -------------------- |  ------------- |  --------- |
| `/api/v1/users/`  | Permission     | Users      | 

> GET

Returns list of users with branch, position and image.

| URI | Method   |**GET** |
| --- |  ------- |  ------- |
| `/api/v1/users/{id}`  | Permission |Users      |

> GET

Returns informations about user.



### Informations

#### Single example: 

```
{
    "id": 1009,
    "author": 2,
    "title": "fdsfsf3ds2",
    "info": "fdsfsfs",
    "date_posted": "2020-05-16"
}
```

#### Permissible Fields

| Element / Attribute     | PUT       | POST      |
| ----------------------- | --------- | --------- |
| **id**                    | Forbidden  | Forbidden |
| **author**              | Forbidden   | Required  |
| **title**          | Required   | Required  |
| **info**             | Required   | Forbidden  |
| **date_posted**              | Forbidden   | Forbidden  |

#### Sortable Fields

| Filter                | Type | lookups           | Description |
| --------------------- | --|---------------- | ----------- |
| **id**                |Integer    |exact, in         | Django’s built-in lookup |
| **author**                | Integer   |exact, in           | Django’s built-in lookup |
| **title**                |  String  |exact, icontains           | Django’s built-in lookup |
| **info**                |   String |exact, icontains            | Django’s built-in lookup |
| **date_posted**                |Date    |exact, icontains, gt, gte, lt, lte, year, month, day           | Django’s built-in lookup |
| **my**                |Boolean    |         | If my=True, returns all informations created by current user |
| **fields**      | |Selective fields          | Returns only selected fields |
| **omit**      | |Selective fields          | Returns all fields except omitted ones |
| **page**      | |Pagination          | Returns page |
| **page_size**      | |Pagination          | Returns number of records on page (default=100, max_page_size=1000 |

| URI                  | Method         |**GET**     |**POST** |
| -------------------- |  ------------- |  --------- |-------- |
| `/api/v1/informations/`  | Permission     | All      | Users   |

> GET

Returns list of Informations

> POST

Adds new Information 

| URI                  | Method         |**GET** |**PUT**     |**DELETE** |
| -------------------- |  ------------- |--------- |  --------- |-------- |
| `/api/v1/informations/{id}`  | Permission     |All      | Users      | Users(creator)   |

> GET

Return single Information

> PUT

Updates Information

> DELETE

Deletes Information

| URI                  | Method         |**GET**     |
| -------------------- |  ------------- |  --------- |
| `/api/v1/informations/{id}/detail/`  | Permission     | Users      |

> GET

Returns single Information with extra data about author

