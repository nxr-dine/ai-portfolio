# AI Portfolio — Noureddine Bouderbala

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An intelligent, AI-powered portfolio website that showcases projects, skills, and experience through an interactive conversational interface. Built with Next.js 14 and FastAPI, featuring real-time AI chat powered by LangChain and Google Gemini.

## Overview

This portfolio transforms the traditional experience into an engaging conversation. Visitors can explore projects, skills, internships, freelance work, and AI/ML experience through a RAG-powered chatbot.

**Owner:** Noureddine Bouderbala  
**Role:** Software Engineer | Full-Stack Developer | AI Engineering Student  
**Location:** Bouira, Algeria

## Features

- **AI-Powered Chatbot** — RAG-based assistant with portfolio knowledge base
- **Real-time Streaming** — Server-Sent Events (SSE) for responsive chat
- **Project Showcase** — Interactive carousel with full-stack and AI projects
- **Skills Visualization** — Organized technical skills grid
- **Resume Integration** — PDF embed and email delivery
- **Contact Form** — Direct messaging via Resend
- **Command Palette** — Quick-start conversation prompts

## Tech Stack

### Frontend
Next.js 14, React 18, TypeScript, Tailwind CSS 4, Framer Motion, Radix UI

### Backend
FastAPI, LangChain, Google Gemini, PostgreSQL + pgvector, Redis, Resend

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose (for local Postgres + Redis)
- Google Gemini API Key
- Resend API Key

### Quick Start

```bash
# Install dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# Configure environment
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Edit backend/.env with your API keys

# Start database services
docker-compose up -d postgres redis

# Start backend
cd backend && uvicorn app.main:app --reload --port 8000

# Start frontend (new terminal)
cd frontend && npm run dev
```

Visit http://localhost:3000

### Deploy the Backend to Render

1. Push this repository to GitHub and create a new Blueprint on [Render](https://render.com) using `render.yaml`.
2. Set `CORS_ORIGINS` to the frontend URL, such as `https://your-frontend-domain.com`.
3. Add your Google Gemini, Resend, PostgreSQL, and Redis values to the service environment variables in Render.
4. After deployment, verify `https://your-backend-domain.onrender.com/health` returns a healthy response.
5. Set the frontend's `NEXT_PUBLIC_API_URL` to `https://your-backend-domain.onrender.com/api` and rebuild the frontend.

## Customization

### Knowledge Base
Edit files in `backend/app/data/` to update the AI chatbot's knowledge:
- `resume_summary.txt` — Experience, education, skills
- `personal_background.txt` — Interests and career direction
- `linkedin_summary.txt` — Professional summary
- `projects/*.txt` — Individual project details

### Frontend Content
- `frontend/lib/config.ts` — Site metadata and social links
- `frontend/features/projects/data/projects.tsx` — Project carousel
- `frontend/features/skills/data/skills.ts` — Skills grid
- `frontend/features/command-palette/commands.ts` — Starter questions

### Assets
Replace these files in `frontend/public/`:
- `profile.webp` — Profile photo
- `profile-alt.webp` — Alternate profile image (sidebar flip)
- `resume.pdf` — Your CV
- `og-image.png` — Social sharing image

## Environment Variables

### Backend (`backend/.env`)
| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key (required) |
| `RESEND_API_KEY` | Resend email API key (required) |
| `RESEND_FROM` | Verified sender email |
| `OWNER_EMAIL` | Where contact form messages are sent |
| `PORTFOLIO_OWNER` | Your name (used by AI persona) |
| `RESUME_LINK` | URL to your resume PDF |
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |

### Frontend (`frontend/.env`)
| Variable | Description |
|---|---|
| `NEXT_PUBLIC_API_URL` | Backend API URL |
| `NEXT_PUBLIC_APP_URL` | Production site URL (for SEO) |

## Testing

```bash
cd backend && python -m pytest
cd frontend && npm run build
```

## License

MIT License — see [LICENSE](LICENSE)

## Author

**Noureddine Bouderbala**

- GitHub: [@nxr-dine](https://github.com/nxr-dine)
- LinkedIn: [nxr-dine](https://www.linkedin.com/in/nxr-dine/)
