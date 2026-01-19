# Me-API Playground

A production-ready full-stack application that stores and exposes personal profile data via a clean REST API, with a simple frontend for browsing and searching.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Local Development

1. **Clone and setup:**
   ```bash
   cd me-api-playground
   cd backend
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```

2. **Run the backend:**
   ```bash
   # From backend directory
   uvicorn app.main:app --reload
   ```

3. **Open the frontend:**
   ```bash
   # Open frontend/index.html in your browser
   # Or serve it with a local server
   cd frontend
   python -m http.server 3000
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🏗️ Architecture

### Backend (FastAPI + SQLAlchemy)
- **Framework:** FastAPI for high-performance async API
- **Database:** SQLite with SQLAlchemy ORM
- **Migrations:** Alembic for database schema management
- **Authentication:** API key-based for write operations
- **CORS:** Configured for frontend integration

### Frontend (Vanilla JS)
- **HTML/CSS/JS:** No frameworks, lightweight and fast
- **Responsive:** Mobile-friendly design
- **Real-time:** API integration with error handling

### Database Schema

```sql
-- Core tables
profiles (id, name, email, education, github_link, linkedin_link, portfolio_link)
skills (id, name)
projects (id, title, description, github_link, demo_link)
work (id, company, role, duration, website_link)

-- Many-to-many relationships
profile_skills (profile_id, skill_id)
profile_projects (profile_id, project_id)
profile_work (profile_id, work_id)
```

## 📡 API Endpoints

### Profile Management
- `GET /profile` - Get profile data
- `POST /profile` - Create profile (auth required)
- `PUT /profile` - Update profile (auth required)

### Query APIs
- `GET /projects?skill={skill}` - Filter projects by skill
- `GET /skills/top` - Get top skills by usage count
- `GET /search?q={query}` - Search across all content

### Health Check
- `GET /health` - Service health status

### Authentication
All write operations require API key in header:
```
X-API-Key: your-api-key-here
```

## 🧪 Testing

```bash
# Run pytest tests
cd backend
pytest tests/

# Run specific test
pytest tests/test_health.py -v
```

## 🚀 Production Deployment

### Render Deployment

1. **Connect to Render:**
   - Import this repository to Render
   - Use the `render.yaml` configuration

2. **Environment Variables:**
   ```env
   DATABASE_URL=sqlite:///./me_api.db
   API_KEY=your-production-api-key-here
   ```

3. **Deploy:**
   - Render will automatically build and deploy both services
   - Backend: `me-api-backend`
   - Frontend: `me-api-frontend`

### Manual Deployment

#### Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Seed database
python -c "from app.seed import seed_database; seed_database()"

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend
Serve the `frontend/` directory with any static file server (nginx, Apache, etc.)

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: Database connection string (default: SQLite)
- `API_KEY`: API key for write operations (default: dev key)

### CORS Configuration
Update `main.py` CORS settings for production domains:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Production domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📖 Example API Usage

### Get Profile
```bash
curl http://localhost:8000/profile
```

### Search Projects by Skill
```bash
curl "http://localhost:8000/projects?skill=python"
```

### Full-text Search
```bash
curl "http://localhost:8000/search?q=arduino"
```

### Create/Update Profile (with auth)
```bash
curl -X POST http://localhost:8000/profile \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "name": "Mir Asrar",
    "email": "mir.asrar@example.com",
    "education": "NIT Delhi – Electronics & Communication Engineering",
    "skills": ["Python", "FastAPI"],
    "projects": [{
      "title": "Sample Project",
      "description": "A sample project",
      "github_link": "https://github.com/example"
    }]
  }'
```

## 🛠️ Development

### Database Management

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Adding New Endpoints

1. Create router in `app/routers/`
2. Add to `main.py` imports and includes
3. Update schemas if needed
4. Add CRUD operations to `crud.py`

### Frontend Development

- Edit `frontend/app.js` for new features
- Update `frontend/style.css` for styling
- Modify `frontend/index.html` for structure

## 🔒 Security Considerations

- API keys for write operations
- CORS properly configured
- Input validation via Pydantic
- SQLite suitable for small-scale applications

## 🐛 Known Limitations

- Single profile support (by design)
- SQLite concurrency limitations
- No rate limiting implemented
- Basic authentication (API key only)

## 📄 License

This project is for demonstration purposes.

## 👨‍💻 Resume

[View My Resume](https://example.com/resume.pdf) (placeholder - replace with actual resume link)

---

Built with ❤️ using FastAPI, SQLAlchemy, and vanilla JavaScript.
