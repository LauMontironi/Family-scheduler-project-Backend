# 👨‍👩‍👧‍👦 Family Scheduler API

**Backend – FastAPI + MySQL**

API para una aplicación de organización familiar: gestión de familias, miembros, hijos/as y eventos (calendario familiar).  
Incluye autenticación con contraseñas hasheadas y JWT.

---

## ✍️ Autora

**Laura Montironi**  
Proyecto personal de aprendizaje y desarrollo full-stack.

---

## 🧱 Stack Tecnológico

- **FastAPI**
- **MySQL 8**
- **aiomysql**
- **passlib (argon2)** – hash de contraseñas
- **python-jose** – JWT
- **python-dotenv**

---

## 📦 Instalación

### 1. Crear entorno virtual

```bash
python -m venv .venv

2. Instalar dependencias

pip install -r requirements.txt

🔐 Variables de entorno (.env)

Crear un archivo .env en la raíz del proyecto:
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=family_schedule

🗄️ Base de Datos

Schema principal: family_schedule

Tablas

users

families

family_members

children

events

Relaciones clave

family_members vincula users ↔ families

children.family_id → families.id

events.family_id → families.id

events.child_id → children.id (ON DELETE SET NULL)

family_members guarda:

role (admin / parent)

relationship_label (madre, padre, abuelo…)

avatar_url

🔑 Autenticación (Auth)
Registro
POST /auth/register

Login (devuelve JWT)
POST /auth/login

Usuario autenticado
GET /auth/me
Authorization: Bearer <TOKEN>

🧠 Flujo de Seguridad

Passwords hasheados con argon2

JWT contiene:

id
️

email

full_name

Validación por:

get_current_user

pertenencia a familia vía family_members

👪 Families
Familias del usuario logado (cards del frontend)
GET /families/my
Authorization: Bearer <TOKEN>

Obtener una familia (requiere pertenecer)
GET /families/{family_id}
Authorization: Bearer <TOKEN>

Crear familia (crea membership admin automáticamente)
POST /families
Authorization: Bearer <TOKEN>

Actualizar / eliminar familia (solo admin)
PUT /families/{family_id}
DELETE /families/{family_id}

👥 Family Members
GET /fmembers/families/{family_id}
PUT /fmembers/families/{family_id}/users/{user_id}

👶 Children
GET    /children/families/{family_id}/children
GET    /children/families/{family_id}/children/{child_id}
POST   /children/families/{family_id}/children
PUT    /children/families/{family_id}/children/{child_id}
DELETE /children/families/{family_id}/children/{child_id}

📅 Events
GET    /events/families/{family_id}
GET    /events/families/{family_id}/events/{event_id}
POST   /events/families/{family_id}/children/{child_id}/events
PUT    /events/families/{family_id}/events/{event_id}
DELETE /events/families/{family_id}/events/{event_id}


Incluye:

validación de fechas

filtros por tipo

eventos por hijo o familiares

🧩 Estado actual del proyecto

✔ CRUD completo (families, members, children, events)
✔ Auth + JWT
✔ Protección por pertenencia a familia
✔ Endpoint listo para frontend (/families/my)

🚀 Próximo paso: Frontend (Angular)

Flujo previsto:

Landing page (join the family / welcome back)

Login / Register

Guardar token

GET /auth/me

GET /families/my → cards de familias

Dashboard por familia (miembros + children + calendario)

Proyecto educativo desarrollado paso a paso para aprender backend real con FastAPI y MySQL.
```
