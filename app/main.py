
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from .routers import produce, farms, auth
#
#

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#Linking routes in routers to FastApi
app.include_router(produce.router)
app.include_router(farms.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

