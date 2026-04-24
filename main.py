from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = {
    "users": "http://localhost:8001",
    "pets": "http://localhost:8002",
    "appointments": "http://localhost:8003",
    "orders": "http://localhost:8004",
    "notifications": "http://localhost:8005",
}

@app.get("/")
def root():
    return {"message": "API Gateway is running"}

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def route_request(service: str, path: str, request: Request):
    if service not in SERVICES:
        return {"error": "Service not found"}
    
    url = f"{SERVICES[service]}/{path}"
    
    async with httpx.AsyncClient() as client:
        body = await request.body()
        response = await client.request(
            method=request.method,
            url=url,
            headers=dict(request.headers),
            content=body
        )
        return response.json()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
