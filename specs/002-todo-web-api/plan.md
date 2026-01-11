# Phase II Implementation Plan: Full-Stack Web Todo App

This document outlines **HOW** Phase II of the Evolution of Todo project will be built, adhering to the Global Constitution and Phase II Specification.

## 1. Backend Implementation (Python/FastAPI)
- **Framework**: FastAPI will be used for high-performance RESTful routing and Pydantic-based validation.
- **Routing**: Controllers will be grouped by domain (`/auth` and `/todos`).
- **Better Auth Integration**:
    - The backend will act as a client to the Better Auth service.
    - Protected routes will use a dependency injection middleware to verify the session/token from the request header.
- **Database Context**: A session generator will provide SQLModel sessions for each request, ensuring transactional integrity.
- **User Isolation Logic**: Every query to the `todos` table will include a mandatory `.where(Todo.user_id == current_user.id)` clause to prevent data leakage.

## 2. Frontend Implementation (Next.js/TypeScript)
- **Framework**: Next.js App Router for server-side rendering and client-side interactivity.
- **Auth Management**: Use the Better Auth client-side SDK to manage signin/signup flows and persist the user session in cookies/localStorage.
- **State Management**: React `useState` and `useEffect` for managing the list of todos and form inputs.
- **API Client**: A shared `apiClient` utility using `fetch` will be created to handle base URLs, headers (authorization tokens), and standardized error parsing.
- **UI System**: Tailwind CSS for a modern, responsive mobile-first design.

## 3. Database Strategy (Neon/PostgreSQL)
- **ORM**: SQLModel (pydantic-sqlmodel) to unify Python classes and database schemas.
- **Schema**:
    - `User`: `id` (PK, UUID), `email` (Unique), `auth_id` (Index), `created_at`.
    - `Todo`: `id` (PK, UUID), `title` (VarChar), `description` (Text), `completed` (Bool), `user_id` (FK -> User.id), `created_at`, `updated_at`.
- **Migrations**: Use Alembic for versioned schema evolution.

## 4. Integration & Development
- **Local Dev**:
    - Backend: `uv` for dependency management, running locally on port 8000.
    - Frontend: `npm/yarn` running on port 3000.
    - Environment: `.env` files for database URLs and Better Auth credentials.
- **Auth Flow**:
    1. Frontend calls Better Auth.
    2. Better Auth returns session/token.
    3. Frontend includes token in `Authorization` header for all requests to the FastAPI backend.

## 5. Constraint Compliance
- **No Background Services**: All operations are synchronous request-response.
- **No AI/Agents**: All code logic is deterministic and traditionally programmed.
- **Strict Isolation**: No shared todo state; every database operation is scoped by the authenticated user's ID.

---
*This plan strictly adheres to the Phase II Specification and the Global Constitution.*
