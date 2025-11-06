from flask import Flask, request, jsonify, session, render_template_string
import time
import random
import logging
from datetime import datetime
import hashlib
from functools import wraps

app = Flask(__name__)
app.secret_key = 'demo-secret-key-2024'

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Demo users
users = {
    'intern': hashlib.sha256('password123'.encode()).hexdigest(),
    'admin': hashlib.sha256('admin123'.encode()).hexdigest()
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return render_template_string('''
            <script>
                alert('Please login first!');
                window.location.href = '/login-page';
            </script>
            '''), 401
        return f(*args, **kwargs)
    return decorated_function

# Simple HTML templates
LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login - ECS Demo</title>
    <style>
        body { font-family: Arial; max-width: 400px; margin: 100px auto; padding: 20px; }
        .container { background: #f8f9fa; padding: 30px; border-radius: 10px; border: 1px solid #ddd; }
        input { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #007bff; color: white; padding: 12px; border: none; border-radius: 5px; width: 100%; cursor: pointer; }
        button:hover { background: #0056b3; }
        .error { color: red; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔐 ECS Demo Login</h2>
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        <form action="/login" method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div style="margin-top: 20px; font-size: 14px; color: #666;">
            <p><strong>Demo Users:</strong></p>
            <p>👨‍💻 intern / password123</p>
            <p>👑 admin / admin123</p>
        </div>
    </div>
</body>
</html>
'''

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - ECS Demo</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background: #007bff; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; margin: 15px 0; border-radius: 8px; border: 1px solid #ddd; }
        .btn { background: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }
        .btn-logout { background: #dc3545; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat-box { flex: 1; background: #e9ecef; padding: 15px; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 ECS Demo Dashboard</h1>
        <p>Welcome, <strong>{{ username }}</strong> ({{ role }})</p>
        <a href="/logout" class="btn btn-logout">Logout</a>
    </div>

    <div class="stats">
        <div class="stat-box">
            <h3>📈 Orders</h3>
            <p>{{ total_orders }} Total</p>
        </div>
        <div class="stat-box">
            <h3>👥 Users</h3>
            <p>{{ total_users }} Registered</p>
        </div>
        <div class="stat-box">
            <h3>🕒 Uptime</h3>
            <p>{{ uptime }}s</p>
        </div>
    </div>

    <div class="card">
        <h2>Quick Actions</h2>
        <a href="/orders-page" class="btn">View Orders</a>
        <a href="/create-order" class="btn">Create Order</a>
        <a href="/metrics" class="btn">System Metrics</a>
        <a href="/profile" class="btn">My Profile</a>
    </div>
</body>
</html>
'''

ORDERS_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Orders - ECS Demo</title>
    <style>
        body { font-family: Arial; max-width: 1000px; margin: 0 auto; padding: 20px; }
        .header { background: #007bff; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .order-card { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; border: 1px solid #ddd; }
        .btn { background: #28a745; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 5px; }
        .btn-back { background: #6c757d; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📋 Orders</h1>
        <p>Total Orders: {{ total_orders }}</p>
        <a href="/dashboard" class="btn btn-back">← Dashboard</a>
        <a href="/create-order" class="btn">➕ Create Order</a>
    </div>

    {% for order in orders %}
    <div class="order-card">
        <h3>🆔 Order #{{ order.id }} - {{ order.product }}</h3>
        <p><strong>Quantity:</strong> {{ order.quantity }}</p>
        <p><strong>Price:</strong> ${{ order.price }}</p>
        <p><strong>Created by:</strong> {{ order.created_by }}</p>
        <p><strong>Date:</strong> {{ order.created_at }}</p>
    </div>
    {% endfor %}

    {% if not orders %}
    <div class="order-card">
        <p>No orders found. <a href="/create-order">Create your first order!</a></p>
    </div>
    {% endif %}
</body>
</html>
'''

orders = []
order_id = 1
start_time = time.time()

@app.route('/')
def home():
    logger.info("Home page accessed")
    return jsonify({
        "message": "ECS Demo API",
        "status": "running",
        "login_page": "/login-page",
        "docs": "/docs"
    })

@app.route('/login-page')
def login_page():
    error = request.args.get('error')
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template_string(LOGIN_HTML, error="Please enter both username and password"), 400

        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        
        if username in users and users[username] == hashed_pw:
            session['user'] = username
            session['role'] = 'admin' if username == 'admin' else 'intern'
            session['login_time'] = datetime.now().isoformat()
            session['session_id'] = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()[:8]
            
            logger.info(f"User {username} logged in successfully")
            return '''
            <script>
                alert('Login successful!');
                window.location.href = '/dashboard';
            </script>
            '''
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            return render_template_string(LOGIN_HTML, error="Invalid username or password"), 401

    except Exception as e:
        logger.error(f"Login error: {e}")
        return render_template_string(LOGIN_HTML, error="Login failed"), 500

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template_string(DASHBOARD_HTML,
        username=session.get('user'),
        role=session.get('role'),
        total_orders=len(orders),
        total_users=len(users),
        uptime=int(time.time() - start_time)
    )

@app.route('/logout')
@login_required
def logout_user():
    user = session.get('user')
    session.clear()
    logger.info(f"User {user} logged out")
    return '''
    <script>
        alert('Logged out successfully');
        window.location.href = '/login-page';
    </script>
    '''

@app.route('/profile')
@login_required
def user_profile():
    return jsonify({
        "user": session.get('user'),
        "role": session.get('role'),
        "login_time": session.get('login_time'),
        "status": "success"
    })

@app.route('/create-order')
@login_required
def create_order_page():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Create Order</title>
        <style>
            body { font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }
            .container { background: #f8f9fa; padding: 30px; border-radius: 10px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
            button { background: #28a745; color: white; padding: 12px; border: none; border-radius: 5px; width: 100%; cursor: pointer; }
            .back { background: #6c757d; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>➕ Create New Order</h2>
            <form action="/orders" method="post">
                <input type="text" name="product" placeholder="Product Name" required>
                <input type="number" name="quantity" placeholder="Quantity" value="1" min="1">
                <input type="number" name="price" placeholder="Price" step="0.01" required>
                <button type="submit">Create Order</button>
            </form>
            <a href="/dashboard"><button class="back">← Back to Dashboard</button></a>
        </div>
    </body>
    </html>
    '''
    return html

@app.route('/orders', methods=['POST'])
@login_required
def create_order():
    global order_id
    
    try:
        product = request.form.get('product')
        quantity = int(request.form.get('quantity', 1))
        price = float(request.form.get('price', 10.0))

        order = {
            "id": order_id,
            "product": product,
            "quantity": quantity,
            "price": price,
            "created_by": session.get('user'),
            "created_at": datetime.now().isoformat(),
            "status": "completed"
        }

        orders.append(order)
        order_id += 1

        logger.info(f"Order created: {product} by {session.get('user')}")
        
        return f'''
        <script>
            alert('Order #{order["id"]} created successfully!');
            window.location.href = '/orders-page';
        </script>
        ''', 201

    except Exception as e:
        logger.error(f"Order creation failed: {e}")
        return "Order creation failed", 500

@app.route('/orders-page')
@login_required
def orders_page():
    user_orders = [o for o in orders if o['created_by'] == session.get('user')] 
    if session.get('user') == 'admin':
        user_orders = orders
    
    return render_template_string(ORDERS_HTML,
        orders=user_orders,
        total_orders=len(user_orders)
    )

@app.route('/orders-api')
@login_required
def get_orders_api():
    user_orders = [o for o in orders if o['created_by'] == session.get('user')] 
    if session.get('user') == 'admin':
        user_orders = orders
    
    return jsonify({
        "orders": user_orders,
        "total": len(user_orders),
        "user": session.get('user')
    })

@app.route('/metrics')
@login_required
def system_metrics():
    if session.get('user') != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    return jsonify({
        "system": {
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": int(time.time() - start_time),
            "total_orders": len(orders),
            "active_users": len(users)
        },
        "status": "success"
    })

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "ecs-demo",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/docs')
def api_docs():
    return jsonify({
        "endpoints": {
            "GET /": "API info",
            "GET /login-page": "Web login",
            "POST /login": "Login endpoint",
            "GET /dashboard": "Main dashboard",
            "GET /orders-page": "Web orders page",
            "GET /orders-api": "JSON orders API",
            "POST /orders": "Create order",
            "GET /metrics": "System metrics (admin)",
            "GET /health": "Health check"
        }
    })

if __name__ == '__main__':
    logger.info("🚀 Starting ECS Demo Application")
    logger.info("📍 Login: http://localhost:5000/login-page")
    app.run(host='0.0.0.0', port=5000, debug=True)