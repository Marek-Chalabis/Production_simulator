
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
| [/api/v1/](#URIs_list)                             | Returns a list of links to the other available URIs | N/A                                   | N/A                               | N/A                                         |
| [/api/get-token](#Token)                                 | N/A                            | Returns token for user                 | N/A                               | N/A                                         |
| [/api/v1/informations/](#Informations)                                 | Returns a list of informations                           | Creates a new information                   | N/A                               | N/A                                         |
| [/api/v1/informations/{id}](#Informations)                                 | Returns a information                           | N/A                   | Updates a information                               | Deletes a information                                        |N/A 
| [/api/v1/informations/{id}/detail/](#Informations)                                 | Returns a more detailed  information                           |                    | N/A                               | N/A                                         |




### URIs_list

| URI | Method   |**GET** |
| --- |  ------- |  ------- |
| `/api/v1/`  | Permission |All      |

> GET

Returns list of avalible URIs.

### Token

| URI | Method   |**POST** |
| --- |  ------- |  ------- |
| `/api/get-token`  | Permission |Users      |

> POST

Returns token for user.

| Element / Attribute	 | Type         |Permission|
| -------------------- |  ------------- |----------|
|  username  |  String    |Required|
|  password |   String   |Required|


Example:

`{
    "username": "admin",
    "password": "admin"
}`

### Users_list

| URI                  | Method         |**GET**     |
| -------------------- |  ------------- |  --------- |
| `/api/v1/users/`  | Permission     | Users      | 

> GET

Returns list of users with branch, position and image.

| Filter                | lookups           | Description |
| --------------------- | ---------------- | ----------- |
| **search**                | SearchFilter           | Search given value in: username, last_name, email, position, branch  |
| **fields**      | Selective fields          | Returns only selected fields |
| **omit**      | Selective fields          | Returns all fields except omitted ones |
| **page**      | Pagination          | Returns page |
| **page_size**      | Pagination          | Returns number of records on page (default=50, max_page_size=500 |

Example: 

`/api/v1/users/?search=da`

### User

| URI | Method   |**GET** |
| --- |  ------- |  ------- |
| `/api/v1/users/{id}`  | Permission |Users      |

> GET

Returns informations about user.





### Informations

#### Single example: 

```{
    "id": 1009,
    "author": 2,
    "title": "fdsfsf3ds2",
    "info": "fdsfsfs",
    "date_posted": "2020-05-16"
}```

> Permissible Fields

| Element / Attribute     | PUT       | POST      |
| ----------------------- | --------- | --------- |
| **id**                    | Forbidden  | Forbidden |
| **author**              | Forbidden   | Required  |
| **title**          | Required   | Required  |
| **info**             | Required   | Forbidden  |
| **date_posted**              | Forbidden   | Forbidden  |

> Sortable Fields

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

#### GET

Returns list of Informations



> POST

Adds new Patient (date_of_register and registered_by are done automatically)


| Element / Attribute	 | Type         |Permission|
| -------------------- |  ------------- |----------|
|  first_name  |  String    |Required|
|  last_name |   String   |Required|
|   pesel|   Integer(BigIntegerField)   |Required|
|   blood_group|   String(chocies: 0 Rh+, A Rh+, B Rh+, AB Rh+, 0 Rh-, A Rh-, B Rh-, AB Rh-)   |Required|
|   gender|  String(chocies: male, female)    |Required|
|   email|   String(EmailField)   |Allowed|
|  phone_number |  Integer(PhoneNumberField)  *should start with Country calling code like: "+48"*    |Allowed|

Example:

`{
    "first_name": "Testowy",
    "last_name": "Testowicz",
    "pesel": 12345678910,
    "blood_group": "0 Rh+",
    "gender": "male",
    "email": "test@vp.pl",
    "phone_number": "+48123456789",
}`

### Patient

| URI                  | Method         |**GET**     |**PUT** |**DELETE** |
| -------------------- |  ------------- |  --------- |-------- | ----------|
| `/api/v1/patients/{id}`  | Permission     | Users      | Users   | Admin/staff|

> GET

Returns detaiil information about Patient with all of his/her donations and medical employee responsible for register, also there is added dynamic field which returns information if the Patient can donate.

> PUT

Updates Patient.

| Element / Attribute	 | Type         |Permission|
| -------------------- |  ------------- |----------|
|  first_name  |  String    |Required|
|  last_name |   String   |Required|
|   pesel|   Integer(BigIntegerField)   |Required|
|   blood_group|   String(chocies: 0 Rh+, A Rh+, B Rh+, AB Rh+, 0 Rh-, A Rh-, B Rh-, B Rh-)   |Required|
|   gender|  String(chocies: male, female)    |Required|
|   email|   String(EmailField)   |Allowed|
|  phone_number |  Integer(PhoneNumberField)  *should start with Country calling code like: "+48"*    |Allowed|

Example:

`{
    "first_name": "ZMIANATestowy",
    "last_name": "Testowicz",
    "pesel": 12345678910,
    "blood_group": "0 Rh+",
    "gender": "male"
}`

> DELETE

Deletes Patient.

### Donations_list

| URI                  | Method         |**GET**     |**POST** |
| -------------------- |  ------------- |  --------- |-------- |
| `/api/v1/donations/`  | Permission     | Users      | Users   |

> GET

Returns list of Donations.

| Filter                | lookups           | Description |
| --------------------- | ---------------- | ----------- |
| **id**                | in           | Django’s built-in lookup |
| **medical_staff**         | in            | Django’s built-in lookup |
| **patient**          | in          | Django’s built-in lookup |
| **date_of_donation**            | exact, icontains, gt, gte, lt, lte, year, month, day          | Django’s built-in lookup |
| **accept_donate**      | exact          | Django’s built-in lookup |
| **refuse_information**      | icontains          | Django’s built-in lookup |
| **fields**      | Selective fields          | Returns only selected fields |
| **omit**      | Selective fields          | Returns all fields except omitted ones |
| **page**      | Pagination          | Returns page |
| **page_size**      | Pagination          | Returns number of records on page (default=250, max_page_size=2000 |

Example: 

`/api/v1/donations/?medical_staff=32,54,534,56,33,77,23,43&accept_donate=true`

> POST

Adds new Donation (date_of_donation and medical_staff are done automatically)


| Element / Attribute	 | Type         |Permission|
| -------------------- |  ------------- |----------|
|   patient|   Integer(BigIntegerField)   |Required|
|   accept_donate|  String(chocies: male, female)    |Required|
|   refuse_information|   String(EmailField)   |Allowed|

Example:

`{
    "accept_donate": "True",
    "patient": 123
}`

### Donation

| URI                  | Method         |**GET**     |**PUT** |**DELETE** |
| -------------------- |  ------------- |  --------- |-------- | ----------|
| `/api/v1/donations/{id}`  | Permission     | Users      | Admin/staff   | Admin/staff|

> GET

Returns detaiil information about Donation, patient and medical employee.

> PUT

Updates Donation.

| Element / Attribute	 | Type         |Permission|
| -------------------- |  ------------- |----------|
|   patient|   Integer(BigIntegerField)   |Required|
|   accept_donate|  String(chocies: male, female)    |Required|
|   refuse_information|   String(EmailField)   |Allowed|

Example:

`{
    "accept_donate": "False",
    "patient": 123,
    "refuse_information": "Because I say so"
}`

> DELETE

Deletes Donation.

