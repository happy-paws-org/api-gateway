from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="Happy Paws API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = {
    "users": "http://user-service:8001",
    "pets": "http://pet-service:8002",
    "appointments": "http://appointment-service:8003",
    "orders": "http://order-service:8004",
    "notifications": "http://notification-service:8005",
}

@app.get("/")
def root():
    return {"message": "API Gateway Running"}

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_request(service: str, path: str, request: Request):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"{SERVICES[service]}/{path}"

    async with httpx.AsyncClient() as client:
        body = await request.body()

        response = await client.request(
            method=request.method,
            url=url,
            content=body,
            headers=dict(request.headers)
        )

        return response.json()