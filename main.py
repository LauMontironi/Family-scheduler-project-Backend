from fastapi import FastAPI
from routes import children_routes, events_routes, families_routes,auth_routes, fmembers_routes
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Para autenticacion

app.include_router(auth_routes.router, prefix='/auth', tags= ['auth'])

#para grupos familiares 

app.include_router(families_routes.router, prefix='/families', tags= ['families'])

#para children 

app.include_router(children_routes.router, prefix='/children', tags= ['children'])

#para events 

app.include_router(events_routes.router, prefix='/events', tags= ['events'])

#para family_members

app.include_router(fmembers_routes.router, prefix='/fmembers', tags= ['fmembers'])