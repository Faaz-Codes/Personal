# Viral Cat Trend Radar (V1 MVP)

AI-powered radar for discovering fast-growing cat videos across TikTok, Instagram, Reddit, and YouTube Shorts.

## Stack
- Frontend: Next.js + Tailwind
- Backend: FastAPI + SQLAlchemy
- Database: PostgreSQL
- Scraping: Playwright (modular platform scrapers)
- Docker Compose for local development

## V1 Scope
1. Scrape cat-related content
2. Store metrics
3. Calculate trend score
4. Display dashboard

## Project Structure
```text
.
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── scrapers/
│   │   ├── services/
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── types/
│   └── Dockerfile
├── docker-compose.yml
└── postgres/init.sql
```

## Quick Start
```bash
docker compose up --build
```

- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Local Dev (without Docker)
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Notes
- Instagram scraper is a placeholder in V1.
- Trend score formula:
  `trend_score = (view_velocity * 0.5) + (engagement_ratio * 0.3) + (comment_velocity * 0.2)`
