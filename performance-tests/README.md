# Pruebas de Rendimiento y Estrés con Locust

##  Descripción

Este directorio contiene las pruebas de rendimiento y estrés para el sistema e-commerce usando **Locust**.

Las pruebas simulan casos de uso reales con diferentes niveles de carga para validar:
- **Rendimiento**: Tiempo de respuesta bajo carga normal
- **Estrés**: Comportamiento bajo carga extrema
- **Escalabilidad**: Capacidad de manejar múltiples usuarios simultáneos

##  Estructura

```
performance-tests/
├── locustfile.py         # Script principal de Locust con escenarios
├── requirements.txt      # Dependencias Python
└── README.md            # Este archivo
```

##  Escenarios Implementados

### Product Service (Peso 20)
- **Listar productos** (10x): Operación más frecuente
- **Obtener producto por ID** (5x): Consulta individual
- **Listar categorías** (3x): Consulta de categorías
- **Crear producto** (2x): Operación de escritura

### User Service (Peso 11)
- **Listar usuarios** (8x): Consulta frecuente
- **Crear usuario** (3x): Operación de escritura

### Order Service (Peso 8)
- **Listar órdenes** (6x): Consulta frecuente
- **Crear orden completa** (2x): Flujo complejo (user → cart → order)

---

##  Cómo Ejecutar Localmente

### Prerrequisitos

#### 1. Verificar Python instalado

```powershell
# En PowerShell (Windows)
python --version
# Debe mostrar: Python 3.x.x

# Si no está instalado, descarga desde: https://www.python.org/downloads/
```

#### 2. Instalar Locust

```powershell
# Navegar a la carpeta de performance tests
cd ecommerce-api-gateway/performance-tests

# Instalar dependencias
pip install -r requirements.txt

# O si pip no está en PATH:
python -m pip install -r requirements.txt

# Verificar instalación
python -m locust --version
```

---

##  Modos de Ejecución

### Modo 1: Con Interfaz Web (Recomendado para pruebas)

#### Pasos:

1. **Navegar a la carpeta**:
   ```powershell
   cd ecommerce-api-gateway/performance-tests
   ```

2. **Ejecutar Locust con UI**:
   ```powershell
   # Opción 1: Si locust está en PATH
   locust -f locustfile.py --host=http://20.15.17.8:8080
   
   # Opción 2: Si locust NO está en PATH (recomendado para Windows)
   python -m locust -f locustfile.py --host=http://20.15.17.8:8080
   ```

3. **Abrir en el navegador**:
   - URL: http://localhost:8089
   - Te mostrará una interfaz web donde puedes configurar:
     - **Number of users**: 10-50 (empieza con 10)
     - **Spawn rate**: 2 (usuarios por segundo)
     - **Host**: Ya está configurado (http://20.15.17.8:8080)

4. **Hacer clic en "Start swarming"**

5. **Ver resultados en tiempo real**:
   - Estadísticas por endpoint
   - Gráficos de response time
   - Número de requests por segundo
   - Errores si los hay

6. **Detener el test**:
   - **Con tiempo límite**: El test terminará automáticamente si configuraste `--run-time`
   - **Sin tiempo límite**: El test correrá **indefinidamente** hasta que:
     - Hagas clic en el botón **"STOP"** (rojo) en la interfaz web
     - O presiones **Ctrl+C** en la terminal

7. **Cuándo detener**:
   - **Mínimo recomendado**: Deja correr al menos 2-5 minutos para tener datos significativos
   - **Ideal**: 5-10 minutos para obtener métricas estables
   - **Observar**: Revisa las métricas en tiempo real y detén cuando:
     - Veas que las métricas se estabilizan (RPS constante, response time estable)
     - O cuando hayas alcanzado el número de requests que necesitas probar

---

### Modo 2: Headless (Sin UI, con parámetros)

Ejecutar directamente con parámetros desde la línea de comandos:

```powershell
cd ecommerce-api-gateway/performance-tests

# Usar python -m locust si locust no está en PATH
python -m locust -f locustfile.py `
  --host=http://20.15.17.8:8080 `
  --users=10 `
  --spawn-rate=2 `
  --run-time=2m `
  --headless `
  --html=locust-report.html `
  --csv=locust-results
```

**Parámetros**:
- `--users=10`: 10 usuarios concurrentes (empieza con pocos)
- `--spawn-rate=2`: 2 usuarios por segundo (ritmo de inicio)
- `--run-time=2m`: Duración de 2 minutos
- `--headless`: Sin interfaz web
- `--html=locust-report.html`: Genera reporte HTML
- `--csv=locust-results`: Genera CSV con datos

**Ver resultados**:

Después de ejecutar, tendrás:
- `locust-report.html` → Abre en el navegador para ver gráficos
- `locust-results_stats.csv` → Datos estadísticos
- `locust-results_failures.csv` → Errores si los hay

---

##  Ejemplos de Configuración de Carga

### Carga Ligera (Prueba inicial)
```powershell
python -m locust -f locustfile.py --host=http://20.15.17.8:8080 --users=5 --spawn-rate=1 --run-time=1m --headless
```

### Carga Media (Stage simulation)
```powershell
python -m locust -f locustfile.py --host=http://20.15.17.8:8080 --users=50 --spawn-rate=5 --run-time=5m --headless --html=report.html
```

### Carga Extrema (Stress test)
```powershell
python -m locust -f locustfile.py --host=http://20.15.17.8:8080 --users=100 --spawn-rate=10 --run-time=10m --headless --html=stress-report.html
```

### Parámetros Recomendados por Ambiente

| Ambiente | Usuarios | Spawn Rate | Duración |
|----------|----------|------------|----------|
| Desarrollo | 10-20 | 2 usuarios/seg | 2 minutos |
| Stage | 50-100 | 5 usuarios/seg | 5 minutos |
| Estrés | 200-500 | 10 usuarios/seg | 10 minutos |

---

## 📈 Cómo Leer los Resultados

### Estado del Test

**Cuando está Corriendo**:
- **Status**: RUNNING (en verde)
- **Users**: Número de usuarios concurrentes simulados
- **RPS**: Requests por segundo
- **Failures**: Porcentaje de errores (idealmente 0%)

**Cuándo Detener el Test**:

- **Modo Manual (UI)**: El test corre **indefinidamente** hasta que hagas clic en **"STOP"** o presiones **Ctrl+C**
- **Con Tiempo Límite**: Ejecuta con `--run-time` y terminará automáticamente

**Tiempo Recomendado**:
- **Mínimo**: 2-3 minutos (para datos básicos)
- **Recomendado**: 5-10 minutos (para métricas estables)
- **Extendido**: 10-30 minutos (para pruebas de resistencia)

---

### Métricas Importantes

#### En la Tabla de Estadísticas:

1. **Response Times (ms)**
   - **Median (p50)**: Tiempo mediano - el 50% de requests son más rápidos
   - **95%ile (p95)**: El 95% de requests son más rápidos - **métrica clave**
   - **99%ile (p99)**: El 99% de requests son más rápidos
   - **Average**: Promedio
   - **Min/Max**: Tiempos mínimo y máximo

2. **# Requests**
   - Total de requests ejecutados por endpoint

3. **# Fails**
   - Número de requests que fallaron
   - **Ideal**: 0

4. **Current RPS**
   - Requests por segundo en ese momento
   - Debe mantenerse estable

5. **Current Failures/s**
   - Errores por segundo
   - **Ideal**: 0

### Criterios de Éxito

 **GET Requests (Lecturas)**:
- p95 < 500ms
- p99 < 1000ms
- Failure rate = 0%

 **POST Requests (Escrituras)**:
- p95 < 1000ms
- p99 < 2000ms
- Failure rate = 0%

 **Sistema Estable**:
- RPS constante (no decreciendo)
- Response times estables (no incrementando)
- Sin errores

---

### Qué Observar en Tiempo Real

1. **Estabilización de Métricas**
   - Durante los primeros 30-60 segundos, las métricas pueden variar
   - Después deberían estabilizarse
   - **Espera** hasta ver métricas constantes antes de detener

2. **Tasa de Errores**
   - Si ves errores (> 0% failures), detén el test
   - Revisa los logs en la pestaña "Failures"
   - **Acción**: Investigar qué endpoints fallan y por qué

3. **Degradación de Performance**
   - Si los response times aumentan con el tiempo → problema
   - Si RPS decrece → el sistema está sobrecargado
   - **Acción**: Detener el test y revisar recursos (CPU, memoria)

4. **RPS Consistente**
   - El RPS debe mantenerse estable
   - Si baja mucho → el sistema no puede manejar la carga
   - **Acción**: Reducir número de usuarios o revisar configuración

---

### Qué Hacer Después del Test

1. **Revisar Tabla de Estadísticas**
   - Identifica endpoints con mayor tiempo de respuesta
   - Revisa si algún endpoint tiene errores
   - Anota los p95 y p99 para documentación

2. **Descargar Reportes** (si ejecutaste con `--html` y `--csv`)
   - **HTML Report**: Gráficos visuales y estadísticas detalladas
   - **CSV Files**: Datos para análisis en Excel o herramientas de BI

3. **Revisar Gráficos**
   - En la pestaña "Charts" verás:
     - Response times a lo largo del tiempo
     - RPS a lo largo del tiempo
     - Número de usuarios

4. **Interpretar Resultados**
   - **Todo en verde (0% failures)**:  Sistema funciona bien
   - **Response times bajos**:  Sistema responde rápido
   - **RPS alto y estable**:  Sistema maneja la carga bien
   - **Errores o timeouts**:  Investigar qué falla

---

###  Señales de Alerta (Detener Inmediatamente)

Si ves alguno de estos, **detén el test**:

1. **Failure rate > 5%**: Demasiados errores
2. **Response times > 5000ms** constantemente: Sistema muy lento
3. **RPS cayendo constantemente**: Sistema sobrecargado
4. **Errores de conexión**: Problema de red o servicios caídos

---

###  Ejemplo de Resultados Exitosos

```
Status: RUNNING → Status: STOPPED
Users: 10
Total Requests: 1500
Failures: 0 (0%)
Median Response Time: 88ms
95%ile Response Time: 234ms
Average Response Time: 110ms
RPS: 5 (estable)
```

**Interpretación**:  Sistema funciona perfectamente bajo esta carga

---

##  Debugging

### Error: "pip no se reconoce"
```powershell
# Usar python -m pip en su lugar
python -m pip install -r requirements.txt
```

### Error: "locust no se reconoce" (Común en Windows)
```powershell
# Siempre usar python -m locust en lugar de solo locust:
python -m locust -f locustfile.py --host=http://20.15.17.8:8080
```

### Error: "Connection refused"
- Verificar que el API Gateway está accesible:
  ```powershell
  curl http://20.15.17.8:8080/actuator/health
  ```

### Error: "No module named 'locust'"
```powershell
# Reinstalar
pip install locust>=2.20.0
```

### Verificar servicios mientras corre Locust:
```powershell
# Ver logs en tiempo real
kubectl logs -n ecommerce-dev deployment/product-service --tail=50 -f

# Ver uso de recursos
kubectl top pods -n ecommerce-dev

# Ver detalles de un pod
kubectl describe pod -n ecommerce-dev -l app=product-service
```

---

##  Ejecutar desde Pipeline CI/CD

El pipeline de Stage ejecutará automáticamente las pruebas después del deploy:

```yaml
- name: Run Performance Tests
  run: |
    cd api-gateway/performance-tests
    pip install -r requirements.txt
    locust -f locustfile.py \
      --host=http://20.15.17.8:8080 \
      --users=50 \
      --spawn-rate=5 \
      --run-time=5m \
      --headless \
      --html=locust-report.html \
      --csv=locust-results
```

Los pipelines de `product-service`, `user-service`, y `order-service` incluyen este job cuando se ejecutan en la rama `stage`.

---

##  Notas Importantes

- **Datos de Prueba**: Las pruebas crean datos reales (productos, usuarios, órdenes)
- **SKU Únicos**: Se generan SKUs únicos con timestamps para evitar duplicados
- **Cleanup**: No hay cleanup automático (aceptable para Stage)
- **Host Configurable**: El host se puede cambiar vía parámetro `--host`
- **Primera vez**: Empieza con carga ligera (5-10 usuarios, 1 minuto)
- **Pruebas incrementales**: Aumenta usuarios gradualmente (10 → 25 → 50)

---

##  Consejos

1. **Primera prueba**: Empieza con pocos usuarios (5-10) y tiempo corto (2 min)
2. **Pruebas incrementales**: Aumenta usuarios gradualmente (10 → 25 → 50)
3. **Monitoreo paralelo**: Mientras corre Locust, revisa logs de Kubernetes
4. **Recursos**: Verifica uso de CPU/memoria en Kubernetes durante las pruebas

---

##  Próximos Pasos

1.  Locustfile con escenarios básicos
2.  Integrar en pipeline de Stage
3.  Configurar reportes HTML/CSV
4.  Agregar métricas avanzadas (percentiles, gráficos)

---
