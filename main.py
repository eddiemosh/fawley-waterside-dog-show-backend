import random

from fastapi import FastAPI
from starlette import status

app = FastAPI(title="Beer-as-a-Service (BaaS)")

top_uk_lagers = [
    "Stella Artois",
    "Budweiser",
    "Foster’s",
    "Carling",
    "San Miguel",
    "Carlsberg",
    "Heineken",
    "Peroni Nastro Azzurro",
    "Corona",
    "Desperados",
    "Kronenbourg 1664",
    "Beck’s",
    "Staropramen",
    "John Smith’s",
    "Tennent’s Lager",
    "Asahi Super Dry",
    "Tyskie",
    "Birra Moretti",
    "Madri Excepcional",
    "Coors"
]


@app.get("/", tags=["Beer"],
         responses={
             status.HTTP_200_OK: {"description": "I love beer!"}
         }
         )
def get_beer():
    return {"beer": top_uk_lagers[random.randint(0, len(top_uk_lagers) - 1)]}
