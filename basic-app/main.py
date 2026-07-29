from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/scalar")
async def scalar_html():
    return get_scalar_api_reference()