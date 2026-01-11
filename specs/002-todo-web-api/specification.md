# Phase II Specification: Full-Stack Web Todo App

## 1. Overview
Phase II transitions the "Evolution of Todo" project from a CLI tool to a production-ready, multi-user web application. This phase introduces data persistence via Neon PostgreSQL, user authentication via Better Auth, and a modern web interface built with Next.js.

## 2. User Stories

### Authentication
- **Signup**: As a new user, I want to create an account so I can start managing my own private tasks.
- **Login**: As a returning user, I want to log in securely so I can access my saved tasks.
- **Session**: As a user, I want to remain logged in so I don't have to re-authenticate for every action.

### Task Management (User Isolated)
- **Create**: As an authenticated user, I want to create a task with a title and optional description.
- **View**: As an authenticated user, I want to see only my tasks in a clear list.
- **Update**: As an authenticated user, I want to edit my task details.
- **Complete**: As an authenticated user, I want to mark my tasks as complete or incomplete.
- **Delete**: As an authenticated user, I want to remove my tasks permanently.

## 3. Data Model

### User Entity
- `id`: UUID (Primary Key)
- `email`: String (Unique, Indexed)
- `auth_provider_id`: String (Reference to Better Auth record)
- `created_at`: Timestamp

### Todo Entity
- `id`: UUID (Primary Key)
- `title`: String (Required, max 255 chars)
- `description`: String (Optional)
- `completed`: Boolean (Default: False)
- `user_id`: UUID (Foreign Key to User.id)
- `created_at`: Timestamp
- `updated_at`: Timestamp

## 4. API Endpoints (REST)

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| POST | `/api/todos` | Create a new todo | Yes |
| GET | `/api/todos` | List user's todos | Yes |
| GET | `/api/todos/{id}` | Get specific todo | Yes |
| PUT | `/api/todos/{id}` | Update todo details | Yes |
| PATCH | `/api/todos/{id}/toggle` | Toggle completion status | Yes |
| DELETE | `/api/todos/{id}` | Delete a todo | Yes |

## 5. Frontend Routes (Next.js)
- `/`: Landing / Redirect (to list if auth, else signin)
- `/auth/signup`: User registration
- `/auth/signin`: User login
- `/todos`: The main dashboard (Todo List)
- `/todos/add`: Form to create a task
- `/todos/edit/{id}`: Form to edit an existing task

## 6. Frontend Interaction Flow
1. **Auth Flow**: User lands on Signin → Switches to Signup → Registers → Redirected to `/todos`.
2. **Dashboard**: Fetches todos on load → Displays list → Provides buttons for Add, Edit, Toggle, Delete.
3. **Form Flow**: User clicks "Add" → Navigates to `/todos/add` → Submits → Redirected back to `/todos`.

## 7. Acceptance Criteria
- **Security**: A user MUST NOT be able to view, edit, or delete another user's todos via the API or UI (403 Forbidden).
- **Persistence**: Data must survive application restarts and page refreshes (Neon DB).
- **Validation**: API must reject empty titles (400 Bad Request).
- **UX**: UI must remain responsive and show loading/empty states.
- **Auth**: Only authenticated users can access `/todos` routes (Redirect to login).

## 8. Error Handling
- **401 Unauthorized**: Redirect to login page.
- **403 Forbidden**: Display "Access Denied" message if attempting to access another's resource.
- **404 Not Found**: Show clear "Resource not found" state.
- **400 Bad Request**: Show validation error messages in the frontend forms.

## 9. Constraints (Constitution Compliance)
- **No AI**: No LLM-driven features in the app logic.
- **No Phase III Leak**: No Kafka, Docker (unless for local dev), or background workers.
- **Better Auth Only**: No custom JWT or roll-your-own auth logic.

---
*This specification complies with the Global Constitution.*
