Base Url 
https://town-market-backend.vercel.app/

Authentication:

(only unauthenticated user can login)

POST /account/login/

Body:{
    username,
    password
}

Response : [
    message="Login successfull",
    user={
        id,
        email,
        user_type
    },
    access,
    refresh
]


(only unauthenticated user can register)

POST  /account/register/
Body:{username,first_name,last_name,email,phone,profile_photo,password,
confirm_password
}


GET /account/register/

Response : 
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 4,
            "profile_photo": null,
            "username": "salah12",
            "email": "xeyacil260@cristout.com",
            "password": "pbkdf2_sha256$1000000$X7kVSMf4HmsajEiScWqJVk$h9Z6JqotlYkFtrP5bqb+OggRFLRE8y6yvOI8NUo5ReA=",
            "phone": "0180632323",
            "user_type": "customer",  # read only field
            "first_name": "Salah",
            "last_name": "Uddin",
            "is_active": true     # read only field
        }
    ]
}

PATCH  /account/register/4/

you can update :
 profile_photo
 first_name,
 last_name,
 email,
 username,
 phone,


POST /account/logout/

with access and refresh token


Market api:

(anyone can get market )

GET /market/list/

Response :

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Sohid Market",
            "location": "Feni",
            "description": "Feni's Shohid Market is an informal name for a shopping area centered around the Shahid Hossain Uddin Market in the city. It is known as a busy commercial hub where you can find a wide variety of goods, including clothing, groceries, and other household items.",
            "active": true, #default true
            "created_at": "2025-09-10T11:21:08.284970Z", #read only field
            "updated_at": "2025-09-10T11:21:08.284987Z", #read only field
            "district": "Feni", #default Feni
            "upazila": "Feni sadar"
        }
    ]
}


(only admin can create market)

POST /market/list/

BODY:{
    name,
    location,
    description,
    active,  #default =True
    district  #default =Feni
    upazila 
    ('Feni sadar','Feni sadar'),
    ('Daganbhuiyan','Daganbhuiyan'),
    ('Parshuram','Parshuram'),
    ('Chhagalnaiya','Chhagalnaiya'),
    ('Sonagazi','Sonagazi'),
    ('Fulgazi','Fulgazi'),
}

PATCH  or PUT or DELETE  /market/list/1/

body data same previous one 

















