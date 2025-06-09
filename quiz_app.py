import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Kuis Matematika", layout="centered")

st.title("🧠 Kuis Interaktif Matematika")

# Fungsi menyimpan ke Excel
def save_to_excel(name, score, total):
    file = "nilai_kuis.xlsx"
    new_data = {
        "Nama": [name],
        "Skor": [score],
        "Total Soal": [total],
        "Tanggal": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    df_new = pd.DataFrame(new_data)
    if os.path.exists(file):
        df_existing = pd.read_excel(file)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_excel(file, index=False)

# Timer durasi (detik)
TOTAL_TIME = 180  # 3 menit

# Ambil nama dari query params jika ada
query_name = st.query_params.get("name", [""])[0]

# Input nama siswa
if "name" not in st.session_state or not st.session_state.name:
    name = st.text_input("Masukkan nama kamu untuk mulai kuis:", query_name)
    if st.button("Mulai Kuis") and name.strip():
        st.session_state.name = name.strip()
        st.query_params["name"] = name.strip()
        st.rerun()
    else:
        st.stop()
else:
    st.write(f"Selamat datang, **{st.session_state.name}**!")

# Daftar soal
questions = [
    {"question": "Berapakah hasil dari 5 + 7?", "options": ["10", "12", "14", "15"], "answer": "12"},
    {"question": "Hasil dari 9 x 6 adalah?", "options": ["45", "54", "56", "60"], "answer": "54"},
    {"question": "Jika x = 3, maka x² = ?", "options": ["6", "9", "12", "15"], "answer": "9"},
    {"question": "Keliling persegi dengan sisi 4 cm adalah?", "options": ["12", "14", "16", "20"], "answer": "16"},
    {"question": "Berapakah 100 dibagi 25?", "options": ["2", "3", "4", "5"], "answer": "4"}
]

# Timer
if "time_start" not in st.session_state:
    st.session_state.time_start = time.time()

time_passed = int(time.time() - st.session_state.time_start)
time_left = TOTAL_TIME - time_passed

if time_left <= 0:
    st.warning("⌛ Waktu habis!")
    st.session_state.submitted = True
    time_left = 0

minutes = time_left // 60
seconds = time_left % 60
st.markdown(f"⏰ **Waktu tersisa: {minutes:02d}:{seconds:02d}**")

# Inisialisasi soal dan jawaban
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = random.sample(questions, len(questions))
    st.session_state.user_answers = [None] * len(questions)
    st.session_state.submitted = False
    st.session_state.final_score = 0

# Form kuis
if not st.session_state.submitted:
    for i, q in enumerate(st.session_state.shuffled_questions):
        st.subheader(f"Soal {i+1}")
        st.write(q["question"])
        st.session_state.user_answers[i] = st.radio(
            f"Pilih jawaban untuk Soal {i+1}",
            q["options"],
            index=q["options"].index(st.session_state.user_answers[i]) if st.session_state.user_answers[i] else 0,
            key=f"radio_{i}"
        )

    if st.button("🔒 Kunci Semua Jawaban"):
        st.session_state.submitted = True
        score = 0
        for i, q in enumerate(st.session_state.shuffled_questions):
            if st.session_state.user_answers[i] == q["answer"]:
                score += 1
        st.session_state.final_score = score
        save_to_excel(st.session_state.name, score, len(questions))
        st.rerun()
else:
    st.success(f"🎉 Skor kamu: {st.session_state.final_score} dari {len(questions)} soal")
    for i, q in enumerate(st.session_state.shuffled_questions):
        user_ans = st.session_state.user_answers[i]
        correct = user_ans == q["answer"]
        st.write(f"**Soal {i+1}**: {'✅ Benar' if correct else '❌ Salah'}")
        st.caption(f"Jawaban kamu: {user_ans} | Jawaban benar: {q['answer']}")

    if st.button("🔄 Ulangi Kuis"):
        for key in ["shuffled_questions", "user_answers", "submitted", "final_score", "time_start"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
