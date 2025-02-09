# Why Do We Need __init__.py in Each Directory?
✅ __init__.py makes directories importable Python packages.
✅ Prevents ModuleNotFoundError.
✅ Used to expose only specific imports.
✅ Can initialize settings or logic at package level.

# Project Structure
Below is one way to structure your application. In this example we build a simple FastAPI backend that performs CRUD on a **User** entity. Instead of a traditional database, we “persist” the data in a CSV file (using [pandas](https://pandas.pydata.org/)) that lives in the `data` folder. We split the code into several layers:

- **Models:** Define your data objects (here a simple dataclass for a User).
- **Schemas:** Define the Pydantic models for request/response validation.
- **CRUD:** Provide low‑level operations (reading/writing from CSV).
- **Services:** Wrap CRUD operations in business logic (or simply pass them through).
- **Dependencies:** (Optional) Provide dependencies for injection (here the UserService).
- **Routers:** Define your API endpoints.
- **Main:** Create the FastAPI app and include routers.
- **Tests:** Use FastAPI’s TestClient to exercise the endpoints.

Below is an example of what each file might look like. You can adjust names and details to suit your needs.

---

## Folder Structure

```
src/
├── app/
│   ├── __init__.py
│   ├── crud/
│   │   └── __init__.py
│   │   └── user.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models/
│   │   └── __init__.py
│   │   └── user.py
│   ├── routers/
│   │   └── __init__.py
│   │   └── users.py
│   ├── schemas/
│   │   └── __init__.py
│   │   └── user.py
│   ├── services/
│   │   └── __init__.py
│   │   └── user.py
│   └── utils/
│       └── __init__.py
├── data/
│   └── users.csv
└── tests/
    └── __init__.py
    └── test_users.py
```

> **Note:** Although your original structure shows a file named `transaction.py` in several places, in this example we’re focusing on the **User** entity. Feel free to remove or rename unused files.

---

## 1. **Model** – Define the data structure

Create `src/app/models/user.py`:

```python
# src/app/models/user.py
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
```

---

## 2. **Schemas** – Define request and response models

Create `src/app/schemas/user.py`:

```python
# src/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
```

---

## 3. **CRUD** – Low-level CSV operations with pandas

Create `src/app/crud/user.py`:

```python
# src/app/crud/user.py
import os
from typing import List, Optional
import pandas as pd
from app.models.user import User

# Construct the absolute path to the CSV file.
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.csv")

def read_users_from_csv() -> pd.DataFrame:
    try:
        df = pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        # If file doesn’t exist, create an empty DataFrame with the proper columns.
        df = pd.DataFrame(columns=["id", "name", "email"])
        df.to_csv(DATA_FILE, index=False)
    return df

def write_users_to_csv(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False)

def get_all_users() -> List[User]:
    df = read_users_from_csv()
    return [User(id=row["id"], name=row["name"], email=row["email"]) 
            for _, row in df.iterrows()]

def get_user_by_id(user_id: int) -> Optional[User]:
    df = read_users_from_csv()
    user_row = df[df["id"] == user_id]
    if not user_row.empty:
        row = user_row.iloc[0]
        return User(id=row["id"], name=row["name"], email=row["email"])
    return None

def create_user(user_data: dict) -> User:
    df = read_users_from_csv()
    new_id = 1 if df.empty else int(df["id"].max()) + 1
    user_data["id"] = new_id
    # Create a DataFrame for the new user and concatenate it with the current df.
    new_row = pd.DataFrame([user_data])
    df = pd.concat([df, new_row], ignore_index=True)
    write_users_to_csv(df)
    return User(**user_data)

def update_user(user_id: int, update_data: dict) -> Optional[User]:
    df = read_users_from_csv()
    indices = df.index[df["id"] == user_id]
    if not indices.empty:
        idx = indices[0]
        for key, value in update_data.items():
            if value is not None:
                df.at[idx, key] = value
        write_users_to_csv(df)
        row = df.iloc[idx]
        return User(id=row["id"], name=row["name"], email=row["email"])
    return None

def delete_user(user_id: int) -> bool:
    df = read_users_from_csv()
    initial_count = len(df)
    df = df[df["id"] != user_id]
    if len(df) < initial_count:
        write_users_to_csv(df)
        return True
    return False
```

---

## 4. **Services** – Business logic (here just a thin wrapper)

Create `src/app/services/user.py`:

```python
# src/app/services/user.py
from typing import List, Optional
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.crud import user as user_crud

class UserService:
    def get_all_users(self) -> List[UserOut]:
        users = user_crud.get_all_users()
        return [UserOut(id=user.id, name=user.name, email=user.email) for user in users]

    def get_user(self, user_id: int) -> Optional[UserOut]:
        user = user_crud.get_user_by_id(user_id)
        if user:
            return UserOut(id=user.id, name=user.name, email=user.email)
        return None

    def create_user(self, user_create: UserCreate) -> UserOut:
        user_data = user_create.dict()
        user = user_crud.create_user(user_data)
        return UserOut(id=user.id, name=user.name, email=user.email)

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserOut]:
        update_data = user_update.dict(exclude_unset=True)
        user = user_crud.update_user(user_id, update_data)
        if user:
            return UserOut(id=user.id, name=user.name, email=user.email)
        return None

    def delete_user(self, user_id: int) -> bool:
        return user_crud.delete_user(user_id)
```

---

## 5. **Dependencies** – Provide injected dependencies

Create `src/app/dependencies.py`:

```python
# src/app/dependencies.py
from app.services.user import UserService

def get_user_service():
    return UserService()
```

---

## 6. **Routers** – Define API endpoints

Create `src/app/routers/users.py`:

```python
# src/app/routers/users.py
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.dependencies import get_user_service
from app.services.user import UserService

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def get_users(service: UserService = Depends(get_user_service)):
    return service.get_all_users()

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(user)

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate, service: UserService = Depends(get_user_service)):
    updated_user = service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}
```

Also, update (or create) `src/app/routers/__init__.py` so that your router is accessible if you prefer:

```python
# src/app/routers/__init__.py
from .users import router as users_router

__all__ = ["users_router"]
```

---

## 7. **Main** – Bring everything together in your FastAPI app

Create `src/app/main.py`:

```python
# src/app/main.py
from fastapi import FastAPI
from app.routers import users_router

app = FastAPI(title="CSV-Backed User Service")

app.include_router(users_router, prefix="/users", tags=["users"])

# Optional: add a simple root endpoint.
@app.get("/")
def read_root():
    return {"message": "Welcome to the CSV-Backed User Service"}
```

---

## 8. **Tests** – Write tests using FastAPI’s TestClient

Create `src/tests/test_users.py`:

```python
# src/tests/test_users.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"

def test_get_users():
    # Create a user so that we have at least one
    client.post("/users/", json={"name": "Jane Doe", "email": "jane@example.com"})
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Expect at least one user in the list
    assert len(data) >= 1

def test_get_user_not_found():
    response = client.get("/users/9999")
    assert response.status_code == 404

def test_update_user():
    # Create a user first
    create_response = client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
    user_id = create_response.json()["id"]
    
    # Update the user’s name
    update_response = client.put(f"/users/{user_id}", json={"name": "Alice Updated"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["name"] == "Alice Updated"

def test_delete_user():
    # Create a user to delete
    create_response = client.post("/users/", json={"name": "Bob", "email": "bob@example.com"})
    user_id = create_response.json()["id"]

    # Delete the user
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    # Verify deletion
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
```

---

## Running the App

1. **Install dependencies:**  
   Make sure to install FastAPI, Uvicorn, and pandas (and optionally, pytest for testing):

   ```bash
   pip install fastapi uvicorn pandas
   ```

2. **Run the Server:**  
   From the `src` folder, run:

   ```bash
   uvicorn app.main:app --reload
   ```

3. **Run the Tests (Optional):**  
   If you have [pytest](https://docs.pytest.org/en/stable/) installed, you can run:

   ```bash
   pytest
   ```

---

This structure cleanly separates concerns into different layers, and by using pandas you can easily read from and write to your CSV file. Adjust error handling and concurrency (e.g. file locks) as needed for your production use case. Enjoy coding your backend!


# Models vs Schemas (DTO)
Model &rarr; Database Table Structure
Schemas (DTO) &rarr; Request/Response Structure