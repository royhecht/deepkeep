RESTful chat endpoint

User mention moderation

Block and auto-unblock logic

Async OpenAI API requests via httpx

PostgreSQL + FastAPI stack

Kubernetes- and Docker-compatible setup

📐 Architecture
Tech Stack:

API: FastAPI (Python)

Async HTTP: httpx (with async/await)

Database: PostgreSQL (SQLAlchemy ORM)

Containerization: Docker + docker-compose

Configuration: .env + constants.py

for implement queuing system (NOT IMPLEMENTED:

Moderation Store: Redis (for Celery if used, otherwise optional)

Queue: Removed Celery in favor of direct async calls

Feature	Description
/chat	Accepts chat prompt, enforces moderation, and returns response
Moderation	Users cannot mention other users
Blocking	After 3 mention violations, users are blocked
Unblock	Auto-unblock after a timeout or via admin interface 

API Endpoints
POST /chat

Request:

{
  "username": "roye",
  "prompt": "hello @john"
}
Response (if OK):

{
  "status": "This is a response from OpenAI",
  "request_id": 17
}

Response (if blocked):


{
  "detail": "User is blocked"
}
🛠️ Design Decisions
No Celery: Async OpenAI requests are handled using httpx.AsyncClient for simplicity and reduced infra overhead.

Session Consistency: All DB operations pass around a shared Session object to avoid detached ORM issues.

Blocking Logic: Defined in crud.py, based on mention count per user, auto-resets after BLOCK_DURATION_MINUTES.

Stateless API: All operations are stateless and safe to run across K8s pods.

Constants: Centralized in app/constants.py and loaded via .env.

🧪 Running the Project
1. Setup .env
env
Copy
Edit
DATABASE_URL=postgresql+psycopg2://postgres:password@db:5432/postgres
REDIS_BROKER_URL=redis://redis:6379/0
OPENAI_API_KEY=sk-...
BLOCK_LIMIT=3
BLOCK_DURATION_MINUTES=60
2. Start with Docker Compose
bash
Copy
Edit
docker-compose up --build
Access the API at http://localhost:8000