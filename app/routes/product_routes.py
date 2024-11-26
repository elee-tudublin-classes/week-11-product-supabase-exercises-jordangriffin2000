from typing import Annotated
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# import service functions
from app.services.product_service import *
from app.services.category_service import getAllCategories

from app.models.product import Product

router = APIRouter()

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# handle http get requests for the site root /
# return the todos page
@router.get("/", response_class=HTMLResponse)
async def getProducts(request: Request, filter : str | None = "all"):

    products = getAllProducts()
    categories = getAllCategories()

    # note passing of parameters to the page
    return templates.TemplateResponse("product/products.html", {"request": request, "products": products, "categories": categories, "filter": "all" })


@router.get("/filter/{filter}", response_class=HTMLResponse)
async def getProductsFilter(request: Request, filter: str):
    if filter == "all":
        products = getAllProducts()
    else:
        # Filter products by the category name
        products = [product for product in getAllProducts() if product['category']['name'] == filter]

    return templates.TemplateResponse(
        "product/partials/product_list.html",
        {"request": request, "products": products, "filter": filter}
    )

@router.get("/update/{id}", response_class=HTMLResponse)
async def getProfuctUpdateForm(request: Request, id: int):

    # note passing of parameters to the page
    return templates.TemplateResponse("product/partials/product_update_form.html", {"request": request, "product": getProduct(id) })

# https://fastapi.tiangolo.com/tutorial/request-form-models/#pydantic-models-for-forms
@router.put("/")
def putProduct(request: Request, productData: Annotated[Product, Form()]) :
    # get item value from the form POST data
    update_product = updateProduct(productData)
    return templates.TemplateResponse("product/partials/product_tr.html", {"request": request, "product": update_product})

@router.post("/")
def postProduct(request: Request, productData: Annotated[Product, Form()]) :
    # get item value from the form POST data
    new_product = newProduct(productData)
    return templates.TemplateResponse("product/partials/product_tr.html", {"request": request, "product": new_product})

# https://fastapi.tiangolo.com/tutorial/request-form-models/#pydantic-models-for-forms

@router.delete("/{id}")
def delProduct(request: Request, id: int):
    deleteProduct(id)
    return templates.TemplateResponse("product/partials/product_list.html", {"request": request, "products": getAllProducts()})

