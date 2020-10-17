from typing import Dict, Any

USERS = [
    {
        "id": 1,
        "name": "Clark",
        "surname": "Kent",
        "age": 37,
        "mail": "superman@justiceleague.com",
        "active": True
    },
    {
        "id": 2,
        "name": "Bruno",
        "surname": "Diaz",
        "age": 34,
        "mail": "batman@justiceleague.com",
        "active": True
    },
    {
        "id": 3,
        "name": "Ricardo",
        "surname": "Tapia",
        "age": 23,
        "mail": "robin@justiceleague.com",
        "active": False
    },
    {
        "id": 4,
        "name": "Diana",
        "surname": "Prince",
        "age": 28,
        "mail": "wonderwoman@justiceleague.com",
        "active": True
    },

]

def get_user_by_id(user_id: int) -> Dict[str, Any]:
    res_user = None
    for user in USERS:
        if user["id"] == user_id:
            res_user = user
            break
    return res_user
