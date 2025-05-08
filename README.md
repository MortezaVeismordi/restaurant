# Restaurant Management System API

A Django-based REST API for restaurant management with an admin panel.

## Features

- User authentication with JWT
- Menu management
- Order processing
- Table reservations
- Customer feedback
- Analytics dashboard
- Custom admin panel

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd restaurant-api
```

2. Create a .env file:
```bash
cp .env.example .env
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

5. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Accessing the Application

- API Documentation: http://localhost:8000/api/docs/
- Admin Panel: http://localhost:8000/admin/
- API Base URL: http://localhost:8000/api/

## Development

To run tests:
```bash
docker-compose exec web python manage.py test
```

## API Endpoints

### Authentication
- POST /api/auth/token/ - Get JWT token
- POST /api/auth/token/refresh/ - Refresh JWT token

### Menu
- GET /api/menu/ - List all menu items
- POST /api/menu/ - Create menu item (admin/staff only)
- GET /api/menu/{id}/ - Get menu item details
- PUT /api/menu/{id}/ - Update menu item (admin/staff only)
- DELETE /api/menu/{id}/ - Delete menu item (admin/staff only)

### Orders
- GET /api/orders/ - List orders
- POST /api/orders/ - Create order
- GET /api/orders/{id}/ - Get order details
- PATCH /api/orders/{id}/ - Update order status (staff only)

### Reservations
- GET /api/reservations/ - List reservations
- POST /api/reservations/ - Create reservation
- GET /api/reservations/{id}/ - Get reservation details
- PATCH /api/reservations/{id}/ - Update reservation status

### Feedback
- GET /api/feedback/ - List feedback
- POST /api/feedback/ - Create feedback
- GET /api/feedback/{id}/ - Get feedback details

## License

MIT 