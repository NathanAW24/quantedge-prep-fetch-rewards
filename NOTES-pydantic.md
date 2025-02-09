# **📌 Pydantic Notes for FastAPI and General Python Usage**

## **1️⃣ What is Pydantic?**
Pydantic is a **data validation and serialization library** for Python, built on top of **type hints**. It ensures **data integrity** by validating incoming data against pre-defined models.

✅ **Key Features**:
- Type validation using **Python type hints**.
- Automatic **data parsing** (e.g., string `"123"` → integer `123`).
- Built-in **error handling**.
- Works seamlessly with **FastAPI**.

---

## **2️⃣ Installing Pydantic**
Pydantic is automatically installed with FastAPI, but you can install it separately:
```bash
pip install pydantic
```

To check your Pydantic version:
```bash
pip show pydantic
```

---

## **3️⃣ Defining a Basic Pydantic Model**
A **Pydantic model** is a class that inherits from `BaseModel`.

### **✅ Example: Basic User Model**
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    age: int
```
💡 **How it Works:**
- Defines **type constraints** (`id` must be an `int`, `name` must be a `str`).
- Automatically **validates** data when creating an instance.

---

## **4️⃣ Data Validation and Parsing**
Pydantic **automatically parses data** into the correct type.

### **✅ Example: Data Validation**
```python
user = User(id="123", name="Alice", age="25")
print(user)
```
💡 **Even though** `id` and `age` were **passed as strings**, Pydantic **converts them to integers**.

**Output:**
```bash
id=123 name='Alice' age=25
```

---

## **5️⃣ Handling Validation Errors**
If the input **does not match** the schema, Pydantic raises **ValidationError**.

### **✅ Example: Invalid Data**
```python
from pydantic import ValidationError

try:
    user = User(id="abc", name="Alice", age="twenty")
except ValidationError as e:
    print(e)
```

**Output:**
```
1 validation error for User
id
  Input should be a valid integer (type=int_validation)
age
  Input should be a valid integer (type=int_validation)
```

---

## **6️⃣ Using Pydantic in FastAPI**
FastAPI automatically **validates request body** using Pydantic models.

### **✅ Example: FastAPI with Pydantic**
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.post("/users/")
def create_user(user: User):
    return {"message": f"User {user.name} created!", "age": user.age}
```

### **💡 What Happens?**
- FastAPI **automatically validates** `name` (must be a string) and `age` (must be an integer).
- If data is **invalid**, FastAPI returns **HTTP 422 Unprocessable Entity** with an error message.

---

## **7️⃣ Adding Default Values**
You can **set default values** in your Pydantic models.

### **✅ Example: Defaults & Optional Fields**
```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int = 18  # Default age is 18
```

- If no `age` is provided, it defaults to `18`.

---

## **8️⃣ Making Fields Optional**
Use `None` or `Optional[]` for **optional fields**.

### **✅ Example: Optional Fields**
```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    age: Optional[int] = None  # Age is optional
```

- If `age` is missing, it defaults to `None`.

---

## **9️⃣ Field Validation & Constraints**
Use `pydantic.Field` to enforce **constraints**.

### **✅ Example: Constraining Values**
```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    age: int = Field(..., ge=18, le=100)  # Must be 18–100
```

💡 **Field Constraints:**
- `min_length=3` → Name must be at least **3 characters**.
- `max_length=50` → Name cannot exceed **50 characters**.
- `ge=18` → Age must be **greater than or equal to 18**.
- `le=100` → Age cannot exceed **100**.

---

## **🔟 Custom Validators**
Use `@field_validator` (Pydantic v2) or `@validator` (Pydantic v1) for **custom validation**.

### **✅ Example: Custom Validation**
```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int

    @field_validator("name")
    def validate_name(cls, value):
        if not value.isalpha():
            raise ValueError("Name must contain only letters")
        return value
```

💡 **How It Works:**
- The function `validate_name` ensures `name` **contains only letters**.
- If invalid, Pydantic **raises an error**.

---

## **1️⃣1️⃣ Nested Models**
Pydantic supports **nested models**.

### **✅ Example: Address Inside User Model**
```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    address: Address
```

💡 **Now, `address` must be a valid `Address` model.**

---

## **1️⃣2️⃣ ORM Integration (SQLAlchemy)**
To use Pydantic with **SQLAlchemy ORM models**, add:
```python
class Config:
    from_attributes = True  # (Pydantic v2)
```

### **✅ Example: SQLAlchemy + Pydantic**
```python
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLAlchemy Model
class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

# Pydantic Schema
class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True  # Required for ORM support in Pydantic v2
```

---

## **1️⃣3️⃣ Converting Pydantic Models to Dictionaries**
Use `.model_dump()` (Pydantic v2) or `.dict()` (Pydantic v1) to **convert models to dictionaries**.

### **✅ Example: Converting to Dict**
```python
user = User(name="Alice", age=25)
print(user.model_dump())  # Pydantic v2
```

**Output:**
```json
{"name": "Alice", "age": 25}
```

---

## **🚀 Summary of Key Features**
| Feature                  | Example Usage |
|--------------------------|--------------|
| **Basic Model** | `class User(BaseModel): name: str` |
| **Validation** | `@field_validator("name")` |
| **Field Constraints** | `age: int = Field(ge=18, le=100)` |
| **Optional Fields** | `Optional[str] = None` |
| **Nested Models** | `class Address(BaseModel):` |
| **ORM Mode** | `from_attributes = True` |
| **Model to Dict** | `model_dump()` |

---

## **🔥 Conclusion**
✅ **Pydantic automatically validates data** in FastAPI and Python.  
✅ **Handles nested models, constraints, and ORM integration.**  
✅ **Supports default values, optional fields, and custom validators.**  

Let me know if you need **code examples** for a specific use case! 🚀