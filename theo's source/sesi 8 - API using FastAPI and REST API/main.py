import requests
from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

# ambil data dari JSONPlaceholder saat server start
users_response = requests.get("https://jsonplaceholder.typicode.com/users")
posts_response = requests.get("https://jsonplaceholder.typicode.com/posts")

users_raw = users_response.json()
posts_raw = posts_response.json()

# hitung post per user
posts_per_user = {}
for post in posts_raw:
    uid = post["userId"]
    if uid not in posts_per_user:
        posts_per_user[uid] = 0
    posts_per_user[uid] += 1

# buat user_summary
user_summary = []
for user in users_raw:
    user_summary.append({
        "id": user["id"],
        "nama": user["name"],
        "email": user["email"],
        "kota": user["address"]["city"],
        "jumlah_post": posts_per_user.get(user["id"], 0)
    })

user_summary = sorted(user_summary, key=lambda u: u["jumlah_post"], reverse=True)


@app.get("/users")
def get_users(kota: Optional[str] = None):
    if kota:
        hasil = [u for u in user_summary if u["kota"].lower() == kota.lower()]
        return hasil
    return user_summary


@app.get("/users/{user_id}/posts")
def get_user_posts(user_id: int):
    user = next((u for u in user_summary if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    judul_posts = [p["title"] for p in posts_raw if p["userId"] == user_id]

    return {
        "user_id": user_id,
        "nama": user["nama"],
        "posts": judul_posts
    }
