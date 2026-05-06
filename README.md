# Project Management API

A Django REST Framework (DRF) based project management system with user authentication: JWT tokens, and asynchronous task processing using Celery.

## 📝 Custom User Model

The project uses a custom User model with:
- Email as the unique identifier (instead of username)
- No username field
- Email-based authentication

## 🚀 Features

- **User Authentication**: Email-based registration and login system
- **JWT Token Management**: Secure authentication with access and refresh tokens
- **Password Management**: Forgot password and reset functionality with email notifications
- **User Profile Management**: Update user information
- **Asynchronous Tasks**: Celery integration for background job processing
- **Docker Support**: Complete containerized deployment with Docker Compose
- **Database**: PostgreSQL with Redis for Celery broker
- **Monitoring**: Flower for Celery task monitoring

## 🛠️ Technology Stack

- **Backend**: Django 5.2.13, Django REST Framework 3.17.1
- **Authentication**: Django REST Framework SimpleJWT
- **Database**: PostgreSQL with psycopg2-binary
- **Task Queue**: Celery 5.6.3 with Redis broker
- **Monitoring**: Flower 2.0.1
- **Containerization**: Docker & Docker Compose

## 📁 Project Structure

```
ProjectManagement/
├── projectmanagement/          # Main Django project directory
│   ├── __init__.py
│   ├── settings.py           # Django settings with environment variables
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   ├── asgi.py               # ASGI configuration
│   └── celery.py             # Celery configuration
├── users/                    # User management app
│   ├── models.py             # Custom User model
│   ├── views.py              # API views
│   ├── serializers.py        # DRF serializers
│   ├── urls.py               # User app URLs
│   ├── services.py           # Business logic services
│   └── admin.py              # Django admin configuration
├── utils/                    # Utility modules
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── .env                    # Environment variables
└── manage.py               # Django management script
```

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ProjectManagement
   ```

2. **Set up environment variables**
   ```bash
   # create .env file & edit it with your configuration
   
   # Django Settings
   SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database Configuration
   DATABASE_URL=postgresql://postgres:postgres@database:5432/project_management_db
   
   # Email Configuration (for password reset)
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   
   # JWT Configuration
   ACCESS_TOKEN_LIFETIME=5
   REFRESH_TOKEN_LIFETIME=20
   
   # Celery Configuration
   CELERY_BROKER_URL=redis://redis:6379/0
   
   # Frontend URL (for password reset)
   FRONTEND_RESET_PASSWORD_URL=http://localhost:3000/reset-password/
   ```
3. **Start all services**
   ```bash
   docker compose up --build -d
   ```

4. **Run database migrations**
   ```bash
      docker compose exec web python manage.py migrate

   ```

5. **Create a superuser**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

6. **Access the application**
   - API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin/
   - Flower (Celery Monitor): http://localhost:5555
     - Username: admin
     - Password: password123

## Useful Commands
```bash
   # View logs
   docker compose logs -f web
   
   # Access container
   docker compose exec web bash
   
   # Restart services
   docker compose restart
   
   # Stop everything
   docker compose down
```
## 📡 API Endpoints

### Authentication Endpoints

- `POST /user/auth/register/` - User registration
- `POST /user/auth/login/` - User login (returns JWT tokens)
- `POST /user/auth/logout/` - User logout (blacklist refresh token)
- `POST /user/auth/token/refresh/` - Refresh access token
- `POST /user/auth/forgot-password/` - Request password reset email
- `POST /user/auth/reset-password/` - Reset password with reset-token

### User Management Endpoints

- `PATCH /user/update-user/` - Update user profile (requires authentication)

### Admin Endpoints

- `/admin/` - Django admin panel

## 🔐 Authentication Flow

### 🟢 Login

- User sends email and password  
- Server returns:

```json
{
  "access": "token",
  "refresh": "token"
}
```

---

### 🟡 Authenticated Requests

Include access token in headers:

```http
Authorization: Bearer <access_token>
```

---

### 🔁 Token Refresh

When the access token expires:

```http
POST /user/auth/token/refresh/
```

- Returns a new access token  
- Returns a new refresh token (because, rotation is enabled)
- so, Old refresh token will be blacklisted.
---

### 🔴 Logout

- Client sends refresh token to server  
- Server blacklists the refresh token  

**Notes:**
- Access token remains valid until expiry (JWT is stateless)  
- Refresh token becomes unusable after logout  

---

### 🔐 Password Reset Flow

1. User requests password reset  
2. Reset email is sent via Celery  
3. User clicks the reset link  
4. User sets a new password  
5. All refresh tokens are invalidated  