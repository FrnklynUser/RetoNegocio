# Sistema de Promociones

Sistema de gestión de promociones y bonificaciones para pedidos de productos.

## Descripción

Este sistema permite gestionar promociones y aplicar bonificaciones automáticas a pedidos basados en reglas predefinidas. Incluye gestión de clientes, productos, pedidos y un motor de promociones flexible.

## Características

- Gestión de clientes y sus canales de venta
- Catálogo de productos
- Sistema de pedidos
- Motor de promociones configurable
- API REST para integración con otros sistemas
- Interfaz de usuario moderna con Tailwind CSS

## Requisitos

- Python 3.12+
- Django 5.2.1
- Base de datos PostgreSQL (recomendado)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd reto_grupo03_test
```

2. Crear un entorno virtual:
```bash
python -m venv env
```

3. Activar el entorno virtual:
```bash
# En Windows:
env\Scripts\activate
# En Unix o MacOS:
source env/bin/activate
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

5. Configurar la base de datos:
```bash
python manage.py migrate
```

6. Crear un superusuario:
```bash
python manage.py createsuperuser
```

## Uso

1. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

2. Acceder a la aplicación:
- Panel de administración: http://localhost:8000/admin/
- Aplicación principal: http://localhost:8000/
- Documentación de la API: http://localhost:8000/api/docs/

## Estructura del Proyecto

```
reto_grupo03_test/
├── api/                # Aplicación para la API REST
├── core/              # Funcionalidad principal
├── pedidos/           # Gestión de pedidos
├── productos/         # Gestión de productos
├── promociones/       # Motor de promociones
├── static/            # Archivos estáticos
├── templates/         # Plantillas HTML
└── reto_grupo03/      # Configuración del proyecto
```

## Módulos Principales

### Core
- Autenticación y autorización
- Gestión de clientes
- Dashboard principal

### Productos
- Catálogo de productos
- Gestión de precios
- Categorías

### Promociones
- Configuración de reglas de promoción
- Motor de cálculo de bonificaciones
- Gestión de períodos de vigencia

### Pedidos
- Creación y gestión de pedidos
- Aplicación automática de promociones
- Historial de transacciones

## API REST

La API proporciona endpoints para:
- Consulta de productos
- Gestión de pedidos
- Cálculo de promociones
- Información de clientes

Documentación completa disponible en `/api/docs/`

## Contribución

1. Fork del repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 