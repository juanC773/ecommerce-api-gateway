# API Gateway

## 📋 Descripción

API Gateway es el **punto de entrada único** para todas las peticiones HTTP que llegan a los microservicios. Implementa el patrón de API Gateway usando **Spring Cloud Gateway**, proporcionando enrutamiento, balanceo de carga, CORS y circuit breaker.

## 🎯 Propósito

- **Punto de Entrada Único**: Un solo puerto (8080) para acceder a todos los servicios
- **Enrutamiento Inteligente**: Enruta peticiones según el path (`/product-service/**`, `/order-service/**`, etc.)
- **Service Discovery**: Usa Eureka para encontrar instancias de servicios
- **Load Balancing**: Distribuye carga entre múltiples instancias
- **CORS**: Configurado para permitir peticiones desde frontend
- **Circuit Breaker**: Protege contra fallos en cascada

## 🏗️ Arquitectura

```
┌─────────────┐
│   Cliente   │
│ (Postman,   │
│  Browser)   │
└──────┬──────┘
       │ HTTP Request
       │
       ▼
┌─────────────┐      ┌─────────────┐      ┌──────────────┐
│ API Gateway │─────>│   Eureka    │─────>│ Product Svc  │
│  Puerto:    │      │ (discovers) │      │ Order Svc    │
│   8080      │      └─────────────┘      │ User Svc     │
└─────────────┘                            └──────────────┘
```

## ⚙️ Configuración

### Puerto
- **Puerto**: `8080`
- **URL Local**: `http://localhost:8080`
- **URL Kubernetes**: `http://api-gateway.ecommerce-dev.svc.cluster.local:8080`
- **URL Pública (LoadBalancer)**: `http://20.15.17.8:8080` (IP asignada por Azure)

### Application Name
- **Nombre**: `API-GATEWAY`

### Rutas Configuradas

El gateway enruta las peticiones según el path:

| Path | Destino | Descripción |
|------|---------|-------------|
| `/product-service/**` | `lb://PRODUCT-SERVICE` | Microservicio de Productos |
| `/order-service/**` | `lb://ORDER-SERVICE` | Microservicio de Órdenes |
| `/user-service/**` | `lb://USER-SERVICE` | Microservicio de Usuarios |
| `/payment-service/**` | `lb://PAYMENT-SERVICE` | Microservicio de Pagos |
| `/shipping-service/**` | `lb://SHIPPING-SERVICE` | Microservicio de Envíos |
| `/favourite-service/**` | `lb://FAVOURITE-SERVICE` | Microservicio de Favoritos |
| `/app/**` | `lb://PROXY-CLIENT` | Proxy Client (Frontend) |

**Nota**: `lb://` significa "Load Balancer" y usa Eureka para descubrir las instancias.

## 🔌 Ejemplos de Uso

### Product Service
```bash
# Obtener todos los productos
GET http://20.15.17.8:8080/product-service/api/products

# Obtener producto por ID
GET http://20.15.17.8:8080/product-service/api/products/1
```

### Order Service
```bash
# Obtener todas las órdenes
GET http://20.15.17.8:8080/order-service/api/orders

# Crear orden
POST http://20.15.17.8:8080/order-service/api/orders
```

### User Service
```bash
# Obtener todos los usuarios
GET http://20.15.17.8:8080/user-service/api/users

# Crear usuario
POST http://20.15.17.8:8080/user-service/api/users
```

## 🌐 CORS Configuration

El gateway está configurado para permitir peticiones CORS desde:

```yaml
allowed-origins: "${CLIENT_HOST:http://localhost:4200}"
allowed-methods: [GET, POST, PUT, DELETE, PATCH, OPTIONS]
allowed-headers: "*"
allow-credentials: true
```

## ⚡ Timeouts

```yaml
httpclient:
  connect-timeout: 5000        # 5 segundos para conectar
  response-timeout: 30s         # 30 segundos para respuesta
```

## 🛡️ Circuit Breaker

El gateway usa **Resilience4j** para proteger contra fallos:

```yaml
resilience4j:
  circuitbreaker:
    failure-rate-threshold: 50           # Abre circuit si 50% falla
    minimum-number-of-calls: 5          # Mínimo 5 llamadas para evaluar
    wait-duration-in-open-state: 5s     # Espera 5s antes de reintentar
```

## 🔗 Integración con Eureka

El gateway se registra en Eureka y usa Eureka para descubrir servicios:

```yaml
eureka:
  client:
    service-url:
      defaultZone: http://service-discovery.ecommerce-dev.svc.cluster.local:8761/eureka/
```

### Configuración en Kubernetes

El ConfigMap define las variables de entorno:

```yaml
EUREKA_CLIENT_SERVICE_URL_DEFAULTZONE: "http://service-discovery.ecommerce-dev.svc.cluster.local:8761/eureka/"
EUREKA_INSTANCE_PREFER_IP_ADDRESS: "true"
EUREKA_INSTANCE_HOSTNAME: "api-gateway.ecommerce-dev.svc.cluster.local"
```

## 🚀 Despliegue

### Desarrollo Local

```bash
./mvnw spring-boot:run
```

Servicio disponible en: `http://localhost:8080`

### Docker

```bash
docker build -t api-gateway:0.1.0 .
docker run -p 8080:8080 api-gateway:0.1.0
```

### Kubernetes

El servicio se despliega automáticamente mediante el pipeline CI/CD en el namespace `ecommerce-dev`.

**Tipo de Servicio**: `LoadBalancer` (expone una IP pública)

Para obtener la IP pública:
```bash
kubectl get svc api-gateway -n ecommerce-dev
```

## 📝 Notas Importantes

### Paths y Context Paths

Los microservicios tienen context paths (ej: `/product-service`), por lo tanto:

✅ **Correcto**: `GET /product-service/api/products`  
❌ **Incorrecto**: `GET /api/products`

El gateway NO elimina el prefijo (`/product-service`), lo pasa completo al servicio.

### Estrategia de Despliegue

- **Namespace**: Siempre `ecommerce-dev` (mismo para dev/stage/prod)
- **Tags de Imagen**:
  - `dev-latest` (branches dev/develop)
  - `stage-latest` (branch stage)
  - `prod-0.1.0` (branches main/master)
- **Tipo de Servicio**: LoadBalancer (expone IP pública)
- **Replicas**: 1

### Orden de Arranque

El API Gateway debe iniciar después de:
1. Service Discovery
2. Cloud Config (opcional)
3. Microservicios de negocio (Product, Order, User)

**Razón**: El gateway necesita que los servicios estén registrados en Eureka para poder enrutar peticiones.

### Health Check

```
GET http://20.15.17.8:8080/actuator/health
```

## 🧪 Testing

Este servicio tiene un intento de pruebas unitarias pero puede ejecutarse sin ellas (configurado con `|| true` en el pipeline).

No requiere pruebas E2E complejas ya que es principalmente enrutamiento.

## 📚 Referencias

- [Spring Cloud Gateway Documentation](https://spring.io/projects/spring-cloud-gateway)
- [Resilience4j Circuit Breaker](https://resilience4j.readme.io/docs/circuitbreaker)

---

**Estado**: ✅ Servicio de Infraestructura - Estable y Documentado
