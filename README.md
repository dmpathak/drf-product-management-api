# Product Management API

A Django REST Framework (DRF) based product management system with user authentication, JWT tokens, product/category management, and asynchronous task processing using Celery.

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
- **Product Management**: Full CRUD operations for products and categories
- **Category Management**: Attach products into categories & CRUD of category.
- **Bulk Upload**: Asynchronous bulk import of products and categories via JSON
- **Soft Delete**: Products and categories are soft-deleted (marked as deleted)
- **Role-based Access**: Public read access, admin-only write operations
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
│   ├── celery.py             # Celery configuration
│   ├── views.py              # Bulk upload view
│   └── serializers.py        # Upload serializer
├── users/                    # User management app
│   ├── models.py             # Custom User model
│   ├── views.py              # API views
│   ├── serializers.py        # DRF serializers
│   ├── urls.py               # User app URLs
│   ├── services.py           # Business logic services
│   └── admin.py              # Django admin configuration
├── product/                  # Product management app
│   ├── models.py             # Product and Category models
│   ├── views.py              # Product/Category ViewSets
│   ├── serializers.py        # Product/Category serializers
│   ├── urls.py               # Product app URLs
│   └── admin.py              # Django admin configuration
├── utils/                    # Utility modules
│   ├── tasks.py              # Celery tasks for bulk upload and email
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── sample_bulk_upload.json  # Sample JSON for bulk upload
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
   
   # Run command in container 
   docker compose exec <service_name> <command>
   eg: docker compose exec celery celery -A projectmanagement worker -l info
   
   # Restart services
   docker compose restart
   
   # Stop everything
   docker compose down
```
## 📡 API Endpoints

### Authentication Endpoints

- `POST /auth/register/` - User registration
- `POST /auth/login/` - User login (returns JWT tokens)
- `POST /auth/logout/` - User logout (blacklist refresh token)
- `POST /auth/token/refresh/` - Refresh access token
- `POST /auth/forgot-password/` - Request password reset email
- `POST /auth/reset-password/` - Reset password with reset-token

### User Management Endpoints

- `PATCH /auth/update-user/` - Update user profile (requires authentication)

### Product Management Endpoints

#### Categories
- `GET /category/` - List all active categories (public)
- `POST /category/` - Create new category (admin only)
- `GET /category/{id}/` - Retrieve specific category (public)
- `PUT /category/{id}/` - Update category (admin only)
- `PATCH /category/{id}/` - Partial update category (admin only)
- `DELETE /category/{id}/` - Soft delete category (admin only)

#### Products
- `GET /product/` - List all active products (public)
- `POST /product/` - Create new product (admin only)
- `GET /product/{id}/` - Retrieve specific product (public)
- `PUT /product/{id}/` - Update product (admin only)
- `PATCH /product/{id}/` - Partial update product (admin only)
- `DELETE /product/{id}/` - Soft delete product (admin only)

#### Bulk Operations
- `POST /upload/` - Upload products and categories via JSON file (admin only)

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

## 📊 Data Models

### Category Model
```json
{
  "id": "integer",
  "category_name": "string (max 255 chars)",
  "description": "text",
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_deleted": "boolean (default: false)"
}
```

### Product Model
```json
{
  "id": "integer",
  "category_id": "integer (foreign key to Category)",
  "product_name": "string (max 255 chars)",
  "product_description": "text",
  "product_price": "decimal (max 10 digits, 2 decimal places)",
  "currency": "string (max 3 chars, default: INR)",
  "stock_quantity": "integer",
  "sku": "string (max 20 chars, unique)",
  "image_url": "url",
  "created_at": "datetime",
  "updated_at": "datetime",
  "is_deleted": "boolean (default: false)"
}
```

## 🔄 Bulk Upload Feature

The system supports bulk uploading of categories and products through a JSON file. This process is handled asynchronously by Celery.

### Bulk Upload Format

Upload a JSON file with the following structure:

```json
{
  "categories": [
    {
      "id": 1,
      "category_name": "Electronics",
      "description": "Devices including smartphones, laptops, and accessories",
      "created_at": "2025-02-20T12:00:00Z",
      "updated_at": "2025-02-20T12:00:00Z"
    },
    {
      "id": 2,
      "category_name": "Clothing",
      "description": "Fashion items including shirts, pants, and accessories",
      "created_at": "2025-02-20T12:00:00Z",
      "updated_at": "2025-02-20T12:00:00Z"
    }
  ],
  "products": [
    {
      "id": 101,
      "category_id": 1,
      "category_name": "Electronics",
      "product_name": "Smartphone",
      "product_description": "Latest model with high-resolution camera and OLED display",
      "product_price": 699.99,
      "currency": "INR",
      "stock_quantity": 50,
      "sku": "ELEC-SMART-001",
      "image_url": "https://example.com/smartphone.jpg",
      "created_at": "2025-02-20T12:00:00Z",
      "updated_at": "2025-02-20T12:00:00Z"
    },
    {
      "id": 102,
      "category_id": 2,
      "category_name": "Clothing",
      "product_name": "T-Shirt",
      "product_description": "100% cotton, comfortable fit",
      "product_price": 19.99,
      "currency": "INR",
      "stock_quantity": 200,
      "sku": "CLOTH-TSHIRT-001!",
      "image_url": "https://example.com/tshirt.jpg",
      "created_at": "2025-02-20T12:00:00Z", 
      "updated_at": "2025-02-20T12:00:00Z"
    }
  ]
}
```

### How to Use Bulk Upload

1. **Prepare your JSON file** following the format above
2. **Authenticate as admin** using JWT tokens
3. **Upload the file** to `/upload/` endpoint
4. **Monitor the process** through Flower at http://localhost:5555

### Bulk Upload Behavior

- **Categories**: Created or updated using `update_or_create` based on `category_name`
- **Products**: Created or updated using `update_or_create` based on `sku`
- **Transaction Safety**: All operations are wrapped in a database transaction
- **Logging**: Detailed logs are created for each created/updated item
- **Error Handling**: Errors are logged but don't stop the entire process

## 📝 API Usage Examples

### Create a New Category (Admin Only)
```bash
curl -X POST http://localhost:8000/category/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "category_name": "Books",
    "description": "Fiction and non-fiction books"
  }'
```

### List All Products (Public)
```bash
curl -X GET http://localhost:8000/product/
```

### Create a New Product (Admin Only)
```bash
curl -X POST http://localhost:8000/product/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "category_id": 1,
    "product_name": "Laptop",
    "product_description": "High-performance laptop",
    "product_price": 1299.99,
    "currency": "INR",
    "stock_quantity": 25,
    "sku": "ELEC-LAPTOP-001",
    "image_url": "https://example.com/laptop.jpg"
  }'
```

### Bulk Upload (Admin Only)
```bash
curl -X POST http://localhost:8000/upload/ \
  -H "Authorization: Bearer <access_token>" \
  -F "file=@bulk_data.json"
```

## 🛡️ Security Features

- **Soft Delete**: Products and categories are never permanently deleted
- **Role-based Access**: Public read access, admin-only write operations
- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: All inputs are validated using DRF serializers
- **SQL Injection Protection**: Django ORM provides built-in protection
