# Prompt: Create Phase II Specification

This file contains the prompt used to generate the Phase II Specification for the Evolution of Todo project.

---

/sp.specify Create the Phase II specification for the "Evolution of Todo" project.

Phase II Scope:
- Full-stack web application
- Backend: RESTful API using FastAPI
- Database: Neon Serverless PostgreSQL with SQLModel
- Frontend: Next.js (React + TypeScript)
- Authentication: Better Auth (Signup/Signin)

Required Features:
1. User Authentication (Signup, Login, Logout)
2. User Isolation (Users only see/edit their own Tasks)
3. Full CRUD for Tasks via Web UI
4. Persistent Storage (Data persists in Neon DB)

Specification must include:
- User Stories (Auth and Tasks)
- Updated Data Model (User & Task entities with relationships)
- API Endpoint Definitions (Path, Method, Auth requirement)
- Frontend Route Structure
- Acceptance Criteria
- Error Cases (Auth failure, Resource not found, Unauthorized access)

Strict Constraints:
- Use Better Auth for authentication logic
- No AI or agent features in the code
- No Phase III technologies (Kafka, Dapr, background jobs)
- Must comply with the amended Global Constitution (Phase II definitions)
