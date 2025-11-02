# Pruebas E2E (End-to-End) - Ecommerce Microservices

## 📋 Descripción

Este directorio contiene las pruebas E2E que validan flujos completos de usuario a través de múltiples microservicios. Las pruebas están diseñadas para ejecutarse en el ambiente Stage usando Postman y Newman.

## 📁 Estructura

```
e2e-tests/
├── postman/
│   ├── e2e-tests.postman_collection.json    # Colección principal de pruebas E2E
│   └── environment-stage.json               # Variables de entorno para Stage
└── README.md                                 # Este archivo
```

## 🎯 Flujos E2E Implementados

### Flujo 1: Compra Completa ✅
**Propósito**: Valida el flujo completo de una compra desde la creación de usuario hasta la orden.

**Pasos**:
1. Crear Usuario → Guarda `userId`
2. Listar Productos → Selecciona un producto
3. Crear Carrito → Guarda `cartId`
4. Crear Orden → Guarda `orderId`
5. Verificar Orden Creada → Valida que todo esté correcto

**Validaciones**:
- ✅ Usuario creado correctamente
- ✅ Productos disponibles
- ✅ Carrito creado con userId correcto
- ✅ Orden creada con status CREATED
- ✅ Orden tiene cartId y userId correctos

---

### Flujo 2: Gestión de Productos ✅
**Propósito**: Valida el flujo completo de gestión de productos y categorías.

**Pasos**:
1. Crear Categoría → Guarda `categoryId`
2. Crear Producto → Guarda `productId`
3. Verificar Producto → Valida que existe
4. Actualizar Producto → Valida cambios

**Validaciones**:
- ✅ Categoría creada correctamente
- ✅ Producto creado con categoría correcta
- ✅ Producto tiene todos los campos requeridos
- ✅ Producto se actualiza correctamente

---

### Flujo 3: Validación entre Servicios ✅
**Propósito**: Valida que los servicios se comunican correctamente entre sí.

**Pasos**:
1. Crear Usuario → Guarda `validationUserId`
2. Crear Carrito → Guarda `validationCartId`
3. Verificar Comunicación → GET del carrito debe traer datos del usuario

**Validaciones**:
- ✅ Order Service llama a User Service correctamente
- ✅ El carrito trae información completa del usuario
- ✅ Los datos del usuario son correctos (firstName, lastName, email)

**Importante**: Este flujo valida que `ORDER-SERVICE` usa `RestTemplate` para llamar a `USER-SERVICE`.

---

### Flujo 4: Actualización de Estado de Orden ✅
**Propósito**: Valida el flujo completo de creación y actualización de estado de una orden.

**Pasos**:
1. Crear Usuario → Para la orden
2. Crear Carrito → Para el usuario
3. Crear Orden → Con el carrito
4. Actualizar Estado de Orden → PATCH endpoint

**Validaciones**:
- ✅ Orden creada con status CREATED
- ✅ Estado se actualiza correctamente
- ✅ Estado cambia de CREATED a otro valor

---

### Flujo 5: Listar Recursos ✅
**Propósito**: Valida que todos los endpoints de listado funcionan correctamente.

**Pasos**:
1. Listar Usuarios
2. Listar Productos
3. Listar Categorías
4. Listar Órdenes

**Validaciones**:
- ✅ Todos los endpoints retornan status 200
- ✅ Todos retornan arrays en formato `collection`
- ✅ Los servicios están accesibles a través del API Gateway

---

## 🚀 Cómo Usar

### 1. Importar en Postman

1. Abre Postman
2. Click en **Import**
3. Selecciona:
   - `e2e-tests.postman_collection.json`
   - `environment-stage.json`
4. Activa el environment **"E2E Tests - Stage"**

### 2. Probar Manualmente

1. Selecciona el ambiente **"E2E Tests - Stage"** en Postman
2. Ejecuta cada flujo completo (click en la carpeta → **Run**)
3. Verifica que todas las pruebas pasan (tests en verde)

### 3. Ejecutar con Newman (CLI)

```bash
# Instalar Newman globalmente
npm install -g newman

# Ejecutar todas las pruebas
newman run e2e-tests/postman/e2e-tests.postman_collection.json \
  --environment e2e-tests/postman/environment-stage.json \
  --reporters cli,html,json \
  --reporter-html-export e2e-report.html \
  --reporter-json-export e2e-results.json
```

### 4. Ejecutar desde Pipeline CI/CD

El pipeline de Stage ejecutará automáticamente estas pruebas después del despliegue:

```yaml
- name: Run E2E Tests
  run: |
    npm install -g newman
    newman run e2e-tests/postman/e2e-tests.postman_collection.json \
      --environment e2e-tests/postman/environment-stage.json \
      --reporters cli,html,json \
      --reporter-html-export e2e-report.html \
      --reporter-json-export e2e-results.json
```

---

## 📊 Variables de Entorno

El environment `environment-stage.json` define:

| Variable | Valor | Descripción |
|---------|-------|-------------|
| `baseUrl` | `http://20.15.17.8:8080` | URL del API Gateway |
| `userId` | (automático) | Se guarda después de crear usuario |
| `productId` | (automático) | Se guarda después de crear producto |
| `categoryId` | (automático) | Se guarda después de crear categoría |
| `cartId` | (automático) | Se guarda después de crear carrito |
| `orderId` | (automático) | Se guarda después de crear orden |

**Nota**: Las variables se llenan automáticamente durante la ejecución de los flujos.

---

## ✅ Validaciones Implementadas

Cada request tiene **tests (assertions)** que validan:

1. **Status Code**: Que la respuesta sea 200 OK
2. **Estructura de Datos**: Que los campos requeridos existan
3. **Valores Correctos**: Que los IDs y datos coincidan
4. **Comunicación entre Servicios**: Que los servicios se comuniquen correctamente

**Ejemplo de test**:
```javascript
pm.test("Order was created successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.orderId).to.exist;
    pm.environment.set("orderId", jsonData.orderId);
});
```

---

## 🔍 Debugging

Si una prueba falla:

1. **Revisa los logs en Postman Console**:
   - Click en **Console** (bottom bar)
   - Verás mensajes como `✅ User created with ID: 123`

2. **Verifica el API Gateway**:
   ```bash
   curl http://20.15.17.8:8080/actuator/health
   ```

3. **Verifica servicios en Eureka**:
   ```bash
   kubectl port-forward -n ecommerce-dev svc/service-discovery 8761:8761
   # Abre http://localhost:8761
   ```

4. **Revisa logs de servicios**:
   ```bash
   kubectl logs -n ecommerce-dev deployment/product-service --tail=50
   kubectl logs -n ecommerce-dev deployment/order-service --tail=50
   ```

---

## 📝 Notas Importantes

### Formato de Fecha para Órdenes

Las órdenes requieren fecha en formato: `dd-MM-yyyy__HH:mm:ss:SSSSSS`

Ejemplo: `02-11-2025__15:30:45:123456`

Los scripts de pre-request generan esta fecha automáticamente.

### Variables Compartidas

Las variables se comparten entre requests del mismo flujo usando:
- `pm.environment.set("variableName", value)` → Guardar
- `{{variableName}}` → Usar en URL o Body

### Limpieza de Datos

**⚠️ IMPORTANTE**: Estos tests crean datos reales en la base de datos. Para Stage:
- Es aceptable crear datos de prueba
- Los datos pueden acumularse después de múltiples ejecuciones
- Considera limpiar datos antiguos periódicamente

---

## 🎯 Próximos Pasos

1. ✅ Colecciones Postman creadas
2. ⏳ Integrar Newman en pipeline de Stage
3. ⏳ Configurar ejecución automática después del deploy
4. ⏳ Agregar reportes HTML para visualización

---

**Estado**: ✅ Colecciones E2E Listas para Usar

