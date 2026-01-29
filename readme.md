👨‍👩‍👧‍👦 Family Scheduler API

Backend – FastAPI + MySQL (Railway)
API para gestionar familias, miembros y eventos familiares.

🧱 Stack

FastAPI

MySQL (Railway)

aiomysql

passlib (argon2)

python-jose (JWT)

🔐 Variables de entorno (.env)
SECRET_KEY=tu_clave
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

DB_HOST=tu_host_railway
DB_PORT=tu_puerto
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=railway

🗄️ Base de Datos

| Campo       | Tipo      |
| ----------- | --------- |
| id          | INT PK    |
| family_name | VARCHAR   |
| created_at  | TIMESTAMP |

members

Adultos y niños en la misma tabla

| Campo        | Tipo           |
| ------------ | -------------- |
| id           | INT PK         |
| family_id    | INT FK         |
| full_name    | VARCHAR        |
| email        | VARCHAR        |
| password     | VARCHAR (hash) |
| relationship | VARCHAR        |
| is_child     | BOOL           |
| birthdate    | DATE           |
| gender       | VARCHAR        |
| city         | VARCHAR        |
| hobbys       | TEXT           |
| is_admin     | BOOL           |

events

| Campo       | Tipo        |
| ----------- | ----------- |
| id          | INT PK      |
| family_id   | INT FK      |
| member_id   | INT FK NULL |
| title       | VARCHAR     |
| description | TEXT        |
| location    | VARCHAR     |
| type        | VARCHAR     |
| start_at    | DATETIME    |
| end_at      | DATETIME    |

🔑 Auth

| Método | Ruta             | Descripción    |
| ------ | ---------------- | -------------- |
| POST   | `/auth/register` | Crear usuario  |
| POST   | `/auth/login`    | Login y JWT    |
| GET    | `/auth/me`       | Usuario actual |

👪 Families

| Método | Ruta                    |
| ------ | ----------------------- |
| GET    | `/families/my`          |
| POST   | `/families/`            |
| GET    | `/families/{family_id}` |
| PUT    | `/families/{family_id}` |
| DELETE | `/families/{family_id}` |

👥 Members

| Método | Ruta                             |
| ------ | -------------------------------- |
| GET    | `/fmembers/summary/all`          |
| GET    | `/fmembers/families/{family_id}` |
| POST   | `/fmembers/`                     |
| PUT    | `/fmembers/{member_id}`          |
| DELETE | `/fmembers/{member_id}`          |

📅 Events

| Método | Ruta                                                      | Descripción               |
| ------ | --------------------------------------------------------- | ------------------------- |
| POST   | `/events/families/{family_id}/members/{member_id}/events` | Crear evento              |
| GET    | `/events/families/{family_id}`                            | Listar eventos de familia |
| GET    | `/events/families/{family_id}/events/{event_id}`          | Ver evento                |
| PUT    | `/events/families/{family_id}/events/{event_id}`          | Editar evento             |
| DELETE | `/events/families/{family_id}/events/{event_id}`          | Eliminar evento           |

🧪 Usuario de prueba

| Email                                             | Password  |
| ------------------------------------------------- | --------- |
| [ana.rivera@demo.com](mailto:ana.rivera@demo.com) | Demo1234! |

🚀 Flujo Frontend

Login

Guardar token

GET /auth/me

GET /families/my

GET /fmembers/summary/all

CRUD eventos vía /events/families/{id}
