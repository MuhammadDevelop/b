// Tepada importlar turibdi...
import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css"; 

// FAQAT SHU QATORNI QOLDIRING (Boshqa hech qanday shart kerak emas):
const API_URL = "http://127.0.0.1:8000";

function App() {
  // ... qolgan kodlar o'zgarishsiz qoladi
  const [users, setUsers] = useState([]);
  const [ismi, setIsmi] = useState("");
  const [yoshi, setYoshi] = useState("");
  const [editingId, setEditingId] = useState(null);

  // 1. READ - Barcha foydalanuvchilarni olish
  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_URL}/all`);
      if (response.data.success) {
        setUsers(response.data.users);
      }
    } catch (error) {
      console.error("Ma'lumotlarni yuklashda xatolik:", error);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  // 2. CREATE yoki UPDATE - Saqlash
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!ismi || !yoshi) return alert("Hamma maydonlarni to'ldiring!");

    try {
      if (editingId) {
        // Tahrirlash (PUT)
        const response = await axios.put(`${API_URL}/update/${editingId}`, {
          ismi,
          yoshi: parseInt(yoshi),
        });
        if (response.data.success) {
          alert("Ma'lumot yangilandi!");
          setEditingId(null);
        }
      } else {
        // Yangi qo'shish (POST)
        const response = await axios.post(`${API_URL}/create`, {
          ismi,
          yoshi: parseInt(yoshi),
        });
        if (response.data.success) {
          alert("Yangi inson qo'shildi!");
        }
      }

      setIsmi("");
      setYoshi("");
      fetchUsers();
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.message || "Noma'lum xatolik";
      alert("Xatolik yuz berdi: " + errorMsg);
    }
  };

  const startEdit = (user) => {
    setEditingId(user.id);
    setIsmi(user.ismi);
    setYoshi(user.yoshi);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setIsmi("");
    setYoshi("");
  };

  // 3. DELETE - O'chirish
  const deleteUser = async (id) => {
    if (window.confirm("Rostdan ham o'chirmoqchimisiz?")) {
      try {
        const response = await axios.delete(`${API_URL}/delete/${id}`);
        if (response.data.success) {
          alert("Muvaffaqiyatli o'chirildi!");
          fetchUsers();
        }
      } catch (error) {
        console.error("O'chirishda xatolik:", error);
      }
    }
  };

  return (
    <div className="min-h-screen">
      {/* Forma Bloki */}
      <div className="w-full">
        <h2 className="text-center">
          {editingId ? "Ma'lumotni Tahrirlash 📝" : "Yangi Inson Qo'shish ➕"}
        </h2>
        
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Ismi"
            value={ismi}
            onChange={(e) => setIsmi(e.target.value)}
          />
          <input
            type="number"
            placeholder="Yoshi"
            value={yoshi}
            onChange={(e) => setYoshi(e.target.value)}
          />
          <div className="flex-gap">
            <button
              type="submit"
              className={editingId ? "bg-yellow-button" : ""}
            >
              {editingId ? "Yangilash" : "Qo'shish"}
            </button>
            {editingId && (
              <button type="button" onClick={cancelEdit}>
                Bekor qilish
              </button>
            )}
          </div>
        </form>
      </div>

      {/* Ro'yxat Bloki */}
      <div className="w-full">
        <h2 className="border-b">Insonlar Ro'yxati</h2>
        {users.length === 0 ? (
          <p className="text-gray-500 text-center">Ro'yxat bo'sh yoki yuklanmoqda...</p>
        ) : (
          <div className="divide-y">
            {users.map((user) => (
              <div key={user.id}>
                <div>
                  <span className="font-medium">{user.ismi}</span>
                  <span className="text-sm">({user.yoshi} yoshda)</span>
                  <span className="text-xs">ID: {user.id}</span>
                </div>
                <div>
                  <button onClick={() => startEdit(user)} className="btn-edit">
                    Tahrirlash
                  </button>
                  <button onClick={() => deleteUser(user.id)} className="btn-delete">
                    O'chirish
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;