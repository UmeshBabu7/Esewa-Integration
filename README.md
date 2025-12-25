### Esewa-Integration (Django)

Esewa-Integration is a Django e-commerce app with eSewa payment integration. Users can register, browse products with search/filter, view details, add to cart, place orders, and pay via eSewa (RC test) or Cash on Delivery. They can view order history and manage their profile. Admins have a dashboard to manage products (add, update, delete) and categories (add, update, delete), with staff-only access.

### Tech stack
- **Backend**: Django
- **DB**: SQLite
- **UI**: Django templates, Tailwind via `crispy-forms` + `crispy-tailwind`
- **Filters**: `django-filter`

### Project layout (apps)
- `product`: Product and Category models, listing, filters, product detail
- `user`: Auth (register/login), cart, order, profile, Esewa payment flow
- `adminpage`: Simple admin dashboards and product/category management
- `esewa`: Project settings, URLs

### Installation
1) Clone or download the repository

2) Create and activate a virtual environment
```powershell
py -m venv .venv
.\.venv\Scripts\Activate
```

3) Install dependencies
```powershell
pip install -r requirements.txt
```

4) Run migrations and create a superuser
```powershell
py esewa\manage.py migrate
py esewa\manage.py createsuperuser
```

5) Start the dev server
```powershell
py esewa\manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

### Default configuration
Key settings are in `esewa/esewa/settings.py`:
- `DEBUG=True`, SQLite database
- Templates root: `BASE_DIR / 'templates'` and app templates
- Static served from `static/` during dev

### URLs (high level)
- User flows (see `esewa/user/urls.py` and views):
  - `/` or `/homepage/`: Home, product carousel
  - `/products/`: Product listing with filters
  - `/product/<id>/`: Product detail
  - `/cart/`: Cart list
  - `/order/<product_id>/<cart_id>/`: Place order
  - `/esewa/`: eSewa payment form (auto‑submit)
  - `/esewaverify/<order_id>/<cart_id>/`: eSewa return handler
  - `/login/`, `/register/`, `/logout/`, `/profile/`
- Admin pages in `adminpage` app (plus default Django admin)

### eSewa integration (RC test)
This project uses the RC (test) gateway at `https://rc-epay.esewa.com.np/api/epay/main/v2/form`.

Flow summary:
1) User places an order and chooses "Esewa"
2) `EsewaView` builds signed fields and renders `user/esewa_payment.html`
3) The form auto‑submits to eSewa
4) eSewa redirects to the success or failure URLs with a `data` param (base64 JSON)
5) `esewa_verify` decodes the payload and marks the order paid if `status == 'COMPLETE'`

Important implementation points (see `esewa/user/views.py`):
- HMAC SHA256 signature with a test secret key and `product_code=EPAYTEST`
- Signed fields: `total_amount,transaction_uuid,product_code`
- `success_url` example (update host/port if needed):
  - `http://localhost:8000/esewaverify/<order_id>/<cart_id>/`
- `failure_url` example:
  - `http://127.0.0.1:8000/esewa/failure/`

Test credentials
- `product_code`: `EPAYTEST`
- `secret_key`: Provided for RC testing in the code. For production, move credentials to environment variables and rotate keys.

### How to test the payment
1) Add a product to the cart (login required)
2) Go to cart and click order; fill the order form
3) Choose "Esewa" as the payment method
4) You will be redirected to eSewa RC; complete the flow
5) On success, you’ll return to the app and the order status becomes completed and the cart item is removed
