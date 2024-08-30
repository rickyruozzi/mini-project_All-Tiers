from fastapi import FastAPI
from pydantic import BaseModel, validator
from typing import Optional
import pymongo.errors
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import pymongo
from fastapi.responses import JSONResponse
import logging
from bson import ObjectId
from starlette.responses import HTMLResponse
from starlette.requests import Request

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a secure MongoDB connection string
MONGO_URI = 'mongodb://localhost:27017'

# Create a templates directory
templates = Jinja2Templates(directory='templates')

origins = [
    "http://localhost:8000",
    "http://localhost:3000",  
]                               #to pass the CORS policy

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str
    description: str
    price: float

    @validator('name')      #validazione del campo name
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Name must not be empty')
        return v

    @validator('description')
    def description_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Description must not be empty')
        return v

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v


class item_id(BaseModel):
    id : str

    @validator('id')      #validazione del campo id
    def id_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('id must not be empty')
        return v


@app.post('/add_item')
def add_item(item: Item):
    try:
        with pymongo.MongoClient(MONGO_URI) as client:
            db = client['NewDB']
            col = db['NewCol']
            data = {"name": item.name, 'description': item.description, 'price': item.price}
            result = col.insert_one(data)
            inserted_id = str(result.inserted_id)
            return JSONResponse(content={'stato inserimento':'dato inserito', 'id': inserted_id}, media_type='application/json')
    except pymongo.errors.PyMongoError as e:
        logger.error(f"Error adding item: {str(e)}")
        return JSONResponse(content={'stato inserimento' : 'dato NON inserito' , 'error': str(e)}, media_type='application/json', status_code=500)

@app.get('/items')
def see_items():
    try:
        with pymongo.MongoClient(MONGO_URI) as client:
            db = client['NewDB']
            col = db['NewCol']
            items = col.find()
            items_list=[]
            for item in items:
                item['_id'] = str(item['_id'])
                items_list.append(item)
            return JSONResponse(content={'items': list(items_list)}, media_type='application/json')
    except pymongo.errors.PyMongoError as error:
        return JSONResponse(content={'stato' : 'Impossibile visualizzare items' , 'error': str(error)},media_type='application/json', status_code=500)


@app.post('/remove_item')
def remove_item(item_id: item_id):
    try:
        with pymongo.MongoClient(MONGO_URI) as client:
            db = client['NewDB']
            col = db['NewCol']
            col.delete_one({'_id': ObjectId(item_id.id)})
            return JSONResponse(content={'stato': 'Item eliminato'}, media_type='application/json')
    except pymongo.errors.PyMongoError as error:
        return JSONResponse(content={'stato': 'Impossibile eliminare item', 'error': str(error)}, media_type='application/json', status_code=500)

@app.get('/')
def render_page(r : Request):
    return templates.TemplateResponse('page.html', {'request':r})
    
if __name__ == '__main__':
    try:
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except Exception as e:
        logger.error(f"Error running app: {str(e)}")