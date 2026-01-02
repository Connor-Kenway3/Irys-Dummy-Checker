from app.allocation import get_address_allocation, get_kaito_allocation
from fastapi import FastAPI, Form, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "..", "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "static")), name="static")

@app.get("/")
async def homepage(request: Request):
    print('rendered')
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/allocation")
async def quantize_image(request: Request, address: str = Form(...), role: str = Form(...), username: str = Form(...)):
    print('posted')
    Address_allocation=0
    print(role)
    X_allocation=0
    X_allocation = await get_kaito_allocation(username)
    Address_allocation = get_address_allocation(address,role)
    print(Address_allocation)
    if isinstance(Address_allocation, str):
        Address_allocation=0

    return JSONResponse({
        "x_allocation": X_allocation,
        "address_allocation": Address_allocation,
        "total_allocation": X_allocation + Address_allocation
    })
