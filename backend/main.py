from fastapi import FastAPI
from routers.users import userApp
from routers.leads import leadApp
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

@app.middleware("http")
async def add_process_time_header(request, call_next):
    curr = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - curr
    response.headers["X-Process-Time"] = str(process_time)
    return response



app.include_router(userApp, tags=["Users"])
app.include_router(leadApp, tags=["Leads"])