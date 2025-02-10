from app.crud.payer import (
    get_payer_by_id,
    update_payer
)

print(get_payer_by_id("1"))
print(update_payer("1", { "points": 700000 }))
