
my-startup-app/
├─ docker-compose.yml
├─ .env.example
├─ README.md
├─ apps/
│  ├─ backend/
│  │  ├─ Dockerfile
│  │  ├─ requirements.txt
│  │  └─ app/
│  │     ├─ main.py
│  │     ├─ core/
│  │     │  ├─ config.py
│  │     │  └─ sentry.py
│  │     ├─ db/
│  │     │  ├─ session.py
│  │     │  └─ models.py
│  │     ├─ api/
│  │     │  └─ v1/
│  │     │     ├─ health.py
│  │     │     └─ jobs.py
│  │     ├─ celery_app.py
│  │     ├─ tasks.py
│  │     └─ utils/
│  │        └─ csv_validate.py
│  └─ frontend/
│     ├─ Dockerfile
│     ├─ package.json
│     ├─ vite.config.ts
│     ├─ .env.example
│     └─ src/
│        ├─ main.tsx
│        ├─ api/client.ts
│        └─ pages/
│           ├─ Dashboard.tsx
│           └─ JobDetails.tsx
└─ infra/
   └─ mysql/
      └─ init.sql
