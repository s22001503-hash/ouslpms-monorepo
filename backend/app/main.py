from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, admin, dean

app = FastAPI(title='OUSPMS Backend')

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5177",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5177",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth.router, prefix='/auth')
app.include_router(admin.router, prefix='/admin')
app.include_router(dean.router, prefix='/dean')

@app.get('/')
def root():
    return {'status': 'ok'}
