from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 1. CORS modulini chaqiramiz
from pydantic import BaseModel

api = FastAPI()

# 2. Ruxsat berilgan domenlar (Origin) ro'yxati
origins = [
    "http://localhost:3000",      # Masalan, React yoki Next.js loyihalar uchun
    "http://127.0.0.1:3000",
    "http://localhost:5173",      # Vite (Vue/React) loyihalar uchun
    # "*",                        # Agar xohlagan mehmonga ruxsat bermoqchi bo'lsangiz, shunchaki "*" qo'ying
]

# 3. CORS ni ilovaga (middleware sifatida) qo'shamiz
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Qaysi domenlardan so'rov qabul qilishni belgilaydi
    allow_credentials=True,           # Cookie va xavfsizlik tokenlariga ruxsat beradi
    allow_methods=["*"],              # Barcha metodlarga (GET, POST, PUT, DELETE va h.k.) ruxsat beradi
    allow_headers=["*"],              # Barcha sarlavhalarga (Headers) ruxsat beradi
)

# Ma'lumotlar bazasi vazifasini bajaruvchi ro'yxat
insonlar = [
    {"id": 1, "ismi": "Muhammad", "yoshi": 23},
    {"id": 2, "ismi": "Isfandiyor", "yoshi": 15},
    {"id": 3, "ismi": "Shamsiddin", "yoshi": 13},
    {"id": 4, "ismi": "MuhammadAli", "yoshi": 15},
    {"id": 5, "ismi": "Ahror", "yoshi": 15},
    {"id": 6, "ismi": "Nigina", "yoshi": 13},
    {"id": 7, "ismi": "Robiya", "yoshi": 13},
]

class InsonModel(BaseModel):
    ismi: str
    yoshi: int


### 1. READ (Barchasini olish)
@api.get("/all")
def get_all():
    return {
        "success": True,
        "users": insonlar
    }

@api.get("/user/{user_id}")
def get_user(user_id: int):
    for inson in insonlar:
        if inson["id"] == user_id:
            return {"success": True, "user": inson}
    
    raise HTTPException(status_code=404, detail="Inson topilmadi")

@api.post("/create")
def create_user(user: InsonModel):
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

@api.put("/update/{user_id}")
def update_user(user_id: int, updated_user: InsonModel):
    for inson in insonlar:
        if inson["id"] == user_id:
            inson["ismi"] = updated_user.ismi
            inson["yoshi"] = updated_user.yoshi
            return {
                "success": True,
                "message": "Ma'lumotlar yangilandi",
                "user": inson
            }
            
    raise HTTPException(status_code=404, detail="Yangilash uchun inson topilmadi")

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