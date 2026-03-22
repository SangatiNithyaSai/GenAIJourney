'''uvicorn FastApi:app --reload
need to use the uvicorn server to run the app

Pro: will get the swagger in built

Use this for post 
{
  "id": 4,
  "name": "pen",
  "description": "Useful for writing",
  "quantity": 23,
  "price": 12
}
'''
from  fastapi import FastAPI
from models import Product

app=FastAPI()


@app.get("/")
def greet():
    return " Hello ! Hi"

products=[
    Product(1,"Stool","Useful for Household",2,199.5),
    Product(2,"Chair","Useful for Household",2,200),
    Product(3,"Fan","Useful for Household",2,150.5)
]


@app.get("/products")
def getproduct():
    return products

@app.get("/products/{id}")
def get_product_by_id(id:int):
    for product in products:
        if product.id==id:
            return product
    else:
        return "Product not found"
        
@app.post("/products")
def add_product(product:Product):
    products.append(product)
    return product

@app.put("/products")
def update_product(id:int, product:Product):
    for i in range(len(products)):
        if products[i].id==id:
            products[i]=product
            return "Product updated successfully"
    else:
        return "No product found"
        
@app.delete("/products")
def delete_product(id:int):
    for i in range(len(products)):
        if products[i].id==id:
            del products[i]
            return "Product deleted successfully"
    else:
        return "No product found"

