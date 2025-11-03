"""
Locust Performance Tests para Ecommerce Microservices
Simula casos de uso reales con carga y estrés
"""
from locust import HttpUser, task, between
import random
import json
from datetime import datetime

# Base URL del API Gateway (se configurará desde variable de entorno o CLI)
HOST = "http://20.15.17.8:8080"


class EcommerceUser(HttpUser):
    """Usuario simulado que interactúa con el sistema e-commerce"""
    
    wait_time = between(1, 3)  # Espera entre 1 y 3 segundos entre requests
    
    def on_start(self):
        """Se ejecuta al inicio de cada usuario simulado"""
        self.user_id = None
        self.product_ids = []
        self.category_ids = []
        self.cart_id = None
        self.order_id = None
        
        # Intentar obtener IDs existentes (para evitar crear demasiados)
        self._load_existing_ids()
    
    def _load_existing_ids(self):
        """Cargar IDs existentes de productos y categorías"""
        try:
            # Obtener algunos productos existentes
            response = self.client.get("/product-service/api/products", name="GET Products List")
            if response.status_code == 200:
                data = response.json()
                if 'collection' in data and len(data['collection']) > 0:
                    self.product_ids = [p['productId'] for p in data['collection'][:10]]
            
            # Obtener algunas categorías existentes
            response = self.client.get("/product-service/api/categories", name="GET Categories List")
            if response.status_code == 200:
                data = response.json()
                if 'collection' in data and len(data['collection']) > 0:
                    self.category_ids = [c['categoryId'] for c in data['collection'][:5]]
        except Exception as e:
            print(f"⚠️ Error cargando IDs existentes: {e}")
    
    # ==================== PRODUCT SERVICE ====================
    
    @task(10)  # Peso 10: muy frecuente
    def list_products(self):
        """Listar productos - operación más común"""
        with self.client.get(
            "/product-service/api/products",
            name="GET Products List",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(5)  # Peso 5: frecuente
    def get_product_by_id(self):
        """Obtener producto por ID"""
        if not self.product_ids:
            return
        
        product_id = random.choice(self.product_ids)
        with self.client.get(
            f"/product-service/api/products/{product_id}",
            name="GET Product by ID",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(3)  # Peso 3: moderado
    def list_categories(self):
        """Listar categorías"""
        with self.client.get(
            "/product-service/api/categories",
            name="GET Categories List",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(2)  # Peso 2: menos frecuente
    def create_product(self):
        """Crear nuevo producto"""
        if not self.category_ids:
            return
        
        # Generar datos únicos para evitar duplicados
        timestamp = int(datetime.now().timestamp() * 1000)
        product_data = {
            "productTitle": f"Performance Test Product {timestamp}",
            "imageUrl": "https://via.placeholder.com/300",
            "sku": f"PERF-TEST-{timestamp}",
            "priceUnit": round(random.uniform(10.0, 1000.0), 2),
            "quantity": random.randint(1, 100),
            "category": {
                "categoryId": random.choice(self.category_ids)
            }
        }
        
        with self.client.post(
            "/product-service/api/products",
            json=product_data,
            name="POST Create Product",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if 'productId' in data:
                    self.product_ids.append(data['productId'])
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    # ==================== USER SERVICE ====================
    
    @task(8)  # Peso 8: muy frecuente
    def list_users(self):
        """Listar usuarios"""
        with self.client.get(
            "/user-service/api/users",
            name="GET Users List",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(3)  # Peso 3: moderado
    def create_user(self):
        """Crear nuevo usuario"""
        timestamp = int(datetime.now().timestamp() * 1000)
        user_data = {
            "firstName": f"TestUser{timestamp}",
            "lastName": "Performance",
            "email": f"perf.test.{timestamp}@example.com",
            "phone": f"+57-300-{random.randint(1000000, 9999999)}",
            "imageUrl": "https://bootdey.com/img/Content/avatar/avatar7.png"
        }
        
        with self.client.post(
            "/user-service/api/users",
            json=user_data,
            name="POST Create User",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if 'userId' in data:
                    self.user_id = data['userId']
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    # ==================== ORDER SERVICE ====================
    
    @task(6)  # Peso 6: frecuente
    def list_orders(self):
        """Listar órdenes"""
        with self.client.get(
            "/order-service/api/orders",
            name="GET Orders List",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(2)  # Peso 2: menos frecuente (requiere cart y user)
    def create_order(self):
        """Crear orden completa (flujo de compra)"""
        # Este es un flujo complejo que requiere:
        # 1. Usuario
        # 2. Carrito
        # 3. Orden
        
        if not self.user_id:
            # Intentar crear usuario primero
            timestamp = int(datetime.now().timestamp() * 1000)
            user_data = {
                "firstName": f"OrderUser{timestamp}",
                "lastName": "Test",
                "email": f"order.user.{timestamp}@example.com",
                "phone": f"+57-300-{random.randint(1000000, 9999999)}",
                "imageUrl": "https://bootdey.com/img/Content/avatar/avatar7.png"
            }
            
            user_response = self.client.post(
                "/user-service/api/users",
                json=user_data,
                name="POST Create User (for Order)"
            )
            
            if user_response.status_code != 200:
                return
            
            user_data = user_response.json()
            self.user_id = user_data.get('userId')
        
        # Crear carrito
        cart_data = {"userId": self.user_id}
        cart_response = self.client.post(
            "/order-service/api/carts",
            json=cart_data,
            name="POST Create Cart (for Order)"
        )
        
        if cart_response.status_code != 200:
            return
        
        cart_data = cart_response.json()
        self.cart_id = cart_data.get('cartId')
        
        # Crear orden
        now = datetime.now()
        order_date = now.strftime("%d-%m-%Y__%H:%M:%S:") + str(now.microsecond).zfill(6)
        
        order_data = {
            "orderDate": order_date,
            "orderDesc": "Performance Test Order",
            "orderFee": round(random.uniform(10.0, 500.0), 2),
            "cart": {
                "cartId": self.cart_id,
                "userId": self.user_id
            }
        }
        
        with self.client.post(
            "/order-service/api/orders",
            json=order_data,
            name="POST Create Order",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if 'orderId' in data:
                    self.order_id = data['orderId']
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")

