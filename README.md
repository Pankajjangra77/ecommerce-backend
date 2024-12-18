# E-Commerce Backend

Django REST API backend for the e-commerce store.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:

On Windows:
```bash
.\venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in the backend directory with the following content:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
DISCOUNT_ORDER_INTERVAL=3
DISCOUNT_PERCENTAGE=10
```

5. Run migrations:
```bash
python manage.py migrate
```


## Running the Server

Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

- `GET /api/products/`: List all products
- `POST /api/cart/checkout/`: Process checkout
- `POST /api/discount/validate/`: Validate discount code
- `GET /api/admin/stats/`: Get admin statistics

## Testing

Run the tests:
```bash
python manage.py test
```