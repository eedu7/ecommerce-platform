import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

USER_SERVICE_PORT: int = 8007

app = FastAPI()

# Backend service URLs with specific routes
SERVICES = {
    "user": {
        "auth": f"http://localhost:{USER_SERVICE_PORT}/v1/auth",
        "users": f"http://localhost:{USER_SERVICE_PORT}/v1/users",
        "profile": f"http://localhost:{USER_SERVICE_PORT}/v1/profile",
        "address": f"http://localhost:{USER_SERVICE_PORT}/v1/address",
    }
}


@app.get("/")
async def root():
    return {"message": "Welcome to the API Gateway"}


@app.api_route(
    "/{service}/{sub_service}/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
)
async def proxy_request(service: str, sub_service: str, path: str, request: Request):
    # Validate the service and sub_service
    for service in SERVICES:
        if sub_service in SERVICES[service]:
            break
    else:
        raise HTTPException(
            status_code=404, detail=f"Route {service} - {sub_service} not found"
        )

    # Construct the backend URL
    backend_url = f"{SERVICES[service][sub_service]}/{path}"
    try:
        # Forward the incoming request
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=backend_url,
                headers=request.headers.raw,
                content=await request.body(),
                params=request.query_params,
            )

        # Pass back the response to the client
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
            headers=response.headers,
        )

    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {e}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
