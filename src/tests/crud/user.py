from app.crud.user import (
    get_user_by_id,
    update_user
)

print(get_user_by_id("1"))
print(update_user(user_id="1", update_data={ "points": 600000 }))