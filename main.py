from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import events_routes, families_routes, auth_routes, fmembers_routes

app = FastAPI()

ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "https://family-scheduler-front.netlify.app",   # Netlify (viejo)
    "https://family-scheduler-project.vercel.app",  # Vercel (nuevo)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Para autenticacion

app.include_router(auth_routes.router, prefix='/auth', tags= ['auth'])

#para grupos familiares 

app.include_router(families_routes.router, prefix='/families', tags= ['families'])


#para events 

app.include_router(events_routes.router, prefix='/events', tags= ['events'])

#para family_members

app.include_router(fmembers_routes.router, prefix='/fmembers', tags= ['fmembers'])