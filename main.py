import os

import stripe
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers import payment_router

secret_key = os.getenv("STRIPE_SECRET_TEST_KEY")

stripe.api_version = "2025-03-31.basil"
stripe.api_key = secret_key

app = FastAPI(title="Dog Show Backend")
app.include_router(payment_router.router)

origins = [
    "http://localhost:3000",  # Local frontend (React dev server)
    "https://fawleydogshow.com",  # Your deployed frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def get_health():
    return True


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
