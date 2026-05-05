# FastAPI Backend

This project is a FastAPI backend service that integrates authentication, chat functionality, and external APIs (Supabase, Tavily Search, and Anthropic).

---

## 🚀 Prerequisites
Before starting, ensure you have the following installed:
- [Python 3.11+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/)
- [Git](https://git-scm.com/)

You must also create accounts and retrieve API keys from:
- [Supabase](https://supabase.com/)
- [Tavily Search](https://app.tavily.com/)
- [Anthropic](https://console.anthropic.com/)

---

## 🔑 Environment Variables
You **must** create a `.env` file in the root directory of the project.

Example `.env`:
```env
SUPABASE_URL=https://<your-supabase-project>.supabase.co
SUPABASE_KEY=<your-supabase-service-role-key>
TAVILY_API_KEY=<your-tavily-api-key>
ANTHROPIC_API_KEY=<your-anthropic-api-key>
```

---

## 🛠 Local Development Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI server
```bash
uvicorn main:app --reload
```

The application will be available at:  
👉 [http://localhost:8000](http://localhost:8000)

---

## 🐳 Running with Docker

### 1. Build the Docker image
```bash
docker build -t fastapi-backend .
```

### 2. Run the container with `.env`
```bash
docker run -d -p 8000:8000 --env-file .env fastapi-backend
```

The API will be available at:  
 [http://localhost:8000](http://localhost:8000)

---

##  API Documentation
FastAPI automatically provides documentation:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Supabase Setup

1. **Sign up at Supabase**  
   [https://supabase.com/](https://supabase.com/)

2. **Create a new project**  
   - Give it a name and choose a database password.
   - Wait until the project is initialized.

3. **Get your API credentials**  
   - Go to `Project Settings > API`.
   - Copy:
     - **Project URL** → `SUPABASE_URL`
     - **Service Role Key** → `SUPABASE_KEY`

4. **Import the database dump file**  
   - Go to the `SQL Editor` in Supabase.
   - Click `Upload` and choose the provided dump file.
   - Execute it to create all required tables automatically.

---

##  Next Steps
- Configure your Supabase database using the provided dump file.
- Add Tavily and Anthropic API keys to `.env`.
- Test the `/auth` and `/api` routes.
- Deploy using Docker or Docker Compose if needed.
