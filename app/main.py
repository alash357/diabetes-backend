from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import auth, user, admin, predict
from app.api.v1.routes import admin_password_reset
app.include_router(admin_password_reset.router, prefix="/api/v1/admin", tags=["Admin Password Reset"])


# Import route files you already created
from app.api.v1.routes import auth, user, admin, predict

app = FastAPI(
    title="Diabetes Prediction API",
    description="Backend for prediction and user management",
    version="1.0.0"
)

# Allow frontend to talk to backend
origins = [
    "http://localhost:5173",  # your frontend during dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allows requests from frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hook up all routes under /api/v1/*
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(predict.router, prefix="/api/v1/predict", tags=["Predict"])



@app.get("/")
def root():
    return {"message": "Diabetes Prediction API running 💉"}