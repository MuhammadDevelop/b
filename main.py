from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 1. Ob'ekt nomini aynan "api" deb belgilaymiz:
api = FastAPI()

# 2. CORS sozlamalari
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

insonlar = [
    {"id": 1, "ismi": "Muhammad", "yoshi": 23},
    {"id": 2, "ismi": "Isfandiyor", "yoshi": 15},
    {"id": 3, "ismi": "Shamsiddin", "yoshi": 13}
]

class InsonModel(BaseModel):
    ismi: str
    yoshi: int

# 3. Dekorator nomi ham aynan "@api.get" bo'lishi shart:
@api.get("/all")
def get_all():
    return {
        "success": True,
        "users": insonlar
    }

# Qolgan @api.post, @api.put, @api.delete qismlari ham "@api" bilan boshlanishi kerak...


### 2. READ (Bitta insonni ID bo'yicha qidirish)
@api.get("/user/{user_id}")
def get_user(user_id: int):
    for inson in insonlar:
        if inson["id"] == user_id:
            return {"success": True, "user": inson}
    
    raise HTTPException(status_code=404, detail="Inson topilmadi")


### 3. CREATE (Yangi inson qo'shish)
@api.post("/create")
def create_user(user: InsonModel):
    # Ro'yxat bo'sh bo'lmasa oxirgi ID ga 1 ni qo'shadi, aks holda ID dynamic 1 bo'ladi
    yangi_id = insonlar[-1]["id"] + 1 if insonlar else 1
    
    yangi_inson = {
        "id": yangi_id,
        "ismi": user.ismi,
        "yoshi": user.yoshi
    }
    insonlar.append(yangi_inson)
    return {
        "success": True,
        "message": "Yangi inson muvaffaqiyatli qo'shildi",
        "user": yangi_inson
    }


### 4. UPDATE (Ma'lumotni tahrirlash)
@api.put("/update/{user_id}")
def update_user(user_id: int, updated_user: InsonModel):
    for inson in insonlar:
        if inson["id"] == user_id:
            inson["ismi"] = updated_user.ismi
            inson["yoshi"] = updated_user.yoshi
            return {
                "success": True,
                "message": "Ma'lumotlar muvaffaqiyatli yangilandi",
                "user": inson
            }
            
    raise HTTPException(status_code=404, detail="Yangilash uchun inson topilmadi")


### 5. DELETE (O'chirish)
@api.delete("/delete/{user_id}")
def delete_user(user_id: int):
    for inson in insonlar:
        if inson["id"] == user_id:
            insonlar.remove(inson)
            return {
                "success": True,
                "message": f"ID: {user_id} bo'lgan inson o'chirib tashlandi"
            }
            
    raise HTTPException(status_code=404, detail="O'chirish uchun inson topilmadi")