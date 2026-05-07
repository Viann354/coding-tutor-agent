# CodeSensei — AI Coding Tutor Agent

> AI agent untuk membantu mahasiswa belajar coding menggunakan Google Gemini API.

Built for **Google Cloud Rapid Agent Hackathon 2026**.

---

## Features

- 💬 **Chat bebas** — tanya jawab seputar programming
- 🐛 **Auto debug & fix** — paste kode + error, dapat solusi langsung
- 📝 **Generate soal + koreksi** — latihan soal sesuai topik & level
- 📚 **Rekomendasi materi** — roadmap & resource belajar
- 🗣️ **Multi bahasa** — Bahasa Indonesia & English
- 💾 **Simpan riwayat** — semua chat tersimpan di lokal

## Tech Stack

- **AI:** Google Gemini 1.5 Pro (via Gemini API)
- **Backend:** Python + Flask
- **Frontend:** HTML/CSS/JS (Vanilla)
- **Deployment:** Google Cloud Run

## Setup Lokal

```bash
# 1. Clone repo
git clone https://github.com/username/coding-tutor-agent
cd coding-tutor-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API key
cp .env.example .env
# Edit .env dan isi GEMINI_API_KEY

# 4. Jalankan
python app.py
# Buka http://localhost:5000
```

## Deploy ke Google Cloud Run

```bash
# Build dan deploy
gcloud run deploy coding-tutor-agent \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key_here
```

## Demo

[Link demo video]

## License

MIT License
