# Phase II Atomic Tasks: Full-Stack Web Todo App

These tasks define the atomic steps required to implement Phase II, following the Global Constitution.

## Backend Implementation

### [T1] Initialize Backend Project
- **Description**: Setup FastAPI project structure using `uv`.
- **Preconditions**: Python 3.13+ installed.
- **Outcome**: A working skeleton with a "Hello World" endpoint.
- **Artifacts**: `backend/pyproject.toml`, `backend/main.py`.
- **Reference**: Plan Section 1.

### [T2] Configure Neon PostgreSQL Connection
- **Description**: Setup SQLModel engine and session management for Neon DB.
- **Preconditions**: Neon DB connection string available.
- **Outcome**: Connection test successful.
- **Artifacts**: `backend/app/database.py`.
- **Reference**: Plan Section 3.

### [T3] Define User & Todo Models
- **Description**: Create SQLModel classes for User and Todo with relationships.
- **Preconditions**: [T2].
- **Outcome**: Database schema matches spec.
- **Artifacts**: `backend/app/models.py`.
- **Reference**: Spec Section 3.

### [T4] Implement Better Auth Signup API
- **Description**: Create endpoint to handle new user registration via Better Auth.
- **Preconditions**: [T3].
- **Outcome**: New user record created in DB.
- **Artifacts**: `backend/app/routers/auth.py`.
- **Reference**: Spec Section 4.

### [T5] Implement Better Auth Signin API
- **Description**: Create endpoint to handle user login and session return.
- **Preconditions**: [T4].
- **Outcome**: Valid session/token received on success.
- **Artifacts**: `backend/app/routers/auth.py`.
- **Reference**: Spec Section 4.

### [T6] Implement Auth Middleware
- **Description**: Create FastAPI dependency to verify the session token for protected routes.
- **Preconditions**: [T5].
- **Outcome**: Routes reject requests without valid tokens (401).
- **Artifacts**: `backend/app/dependencies.py`.
- **Reference**: Plan Section 1.

### [T7] Create Todo CRUD Endpoints
- **Description**: Implement Create, Read (List/Detail), Update, and Delete endpoints.
- **Preconditions**: [T6].
- **Outcome**: Tasks can be managed via API.
- **Artifacts**: `backend/app/routers/todos.py`.
- **Reference**: Spec Section 4.

### [T8] Enforce User-Level Data Isolation
- **Description**: Apply filters to all Todo queries to strictly use `current_user.id`.
- **Preconditions**: [T7].
- **Outcome**: User A cannot access User B's todos even with valid ID.
- **Artifacts**: `backend/app/routers/todos.py`.
- **Reference**: Plan Section 1.

### [T9] Backend Error Handling
- **Description**: Implement global exception handlers for 403, 404, and validation errors.
- **Preconditions**: [T8].
- **Outcome**: API returns standardized JSON error responses.
- **Artifacts**: `backend/app/main.py`.
- **Reference**: Spec Section 8.

## Frontend Implementation

### [T10] Initialize Next.js Project
- **Description**: Setup Next.js with TypeScript and Tailwind CSS.
- **Preconditions**: Node.js installed.
- **Outcome**: Default Next.js landing page running.
- **Artifacts**: `frontend/package.json`, `frontend/app/`.
- **Reference**: Plan Section 2.

### [T11] Build Signup Page
- **Description**: Create registration form using Better Auth client SDK.
- **Preconditions**: [T10].
- **Outcome**: Form submits to backend and handles success.
- **Artifacts**: `frontend/app/auth/signup/page.tsx`.
- **Reference**: Spec Section 5.

### [T12] Build Signin Page
- **Description**: Create login form with session persistence.
- **Preconditions**: [T11].
- **Outcome**: User can login and see auth state.
- **Artifacts**: `frontend/app/auth/signin/page.tsx`.
- **Reference**: Spec Section 5.

### [T13] Implement Auth State Management
- **Description**: setup `AuthContext` to provide user data across components.
- **Preconditions**: [T12].
- **Outcome**: Protected routes redirect unauthenticated users.
- **Artifacts**: `frontend/context/AuthContext.tsx`.
- **Reference**: Plan Section 2.

### [T14] Build Todo List Page
- **Description**: Create the main dashboard to list tasks for the current user.
- **Preconditions**: [T13].
- **Outcome**: Displays tasks fetched from backend.
- **Artifacts**: `frontend/app/todos/page.tsx`.
- **Reference**: Spec Section 6.

### [T15] Build Add/Edit Todo UI
- **Description**: Create forms for creating and updating tasks.
- **Preconditions**: [T14].
- **Outcome**: Forms submit and update the backend state.
- **Artifacts**: `frontend/app/todos/add/page.tsx`, `frontend/app/todos/edit/[id]/page.tsx`.
- **Reference**: Spec Section 6.

### [T16] Toggle & Delete Functionality
- **Description**: Add buttons to the list items to toggle completion or delete.
- **Preconditions**: [T15].
- **Outcome**: List updates immediately after action.
- **Artifacts**: `frontend/components/TaskItem.tsx`.
- **Reference**: Spec Section 6.

### [T17] Responsive Layout & Error Handling
- **Description**: Finalize CSS and add Error Boundaries/Empty states.
- **Preconditions**: [T16].
- **Outcome**: App looks good on mobile and handles API failures.
- **Artifacts**: `frontend/app/globals.css`.
- **Reference**: Spec Section 7.

## Final Integration

### [T18] Local Development Sync
- **Description**: Configure `.env` files and ensure communication between Frontend (3000) and Backend (8000).
- **Preconditions**: All T-tasks.
- **Outcome**: Full end-to-end flow working in local environment.
- **Artifacts**: `README.md` update.
- **Reference**: Plan Section 4.
