from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers import analytics_router, feedback_router, order_router, payment_router, test_router

app = FastAPI(title="Dogshow Backend")

app.include_router(payment_router.router)
app.include_router(order_router.router)
app.include_router(analytics_router.router)
app.include_router(test_router.router)
app.include_router(feedback_router.router)

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
