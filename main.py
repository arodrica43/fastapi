from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

# SETTINGS

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGODB_URI = "mongodb+srv://lexws33_db_user:aJ5GxjUnDtDigpdW@cluster0.vnl39cy.mongodb.net/?appName=Cluster0"
mongodb_client = MongoClient(MONGODB_URI)
db = mongodb_client["Exercises"]
user_collection = db["User"]

# DATA MODEL

class User(BaseModel):
    name: str
    email: str
    password: str

# HELPER FUNCTIONS

def convert_item(item):
    item["_id"] = str(item["_id"])  # Convert ObjectId to string
    return item

# API ENDPOINTS

@app.get("/")
async def root():
    return {"endpoints": {
        "/user": "CRUD user"
    }}

@app.post("/user", response_model=User)
def create_user(user: User):
    user_dict = user.dict()
    user_collection.insert_one(user_dict)
    return user

@app.get("/user")
async def list_items():
    users = list(user_collection.find())
    return [convert_item(user) for user in users]

@app.get("/user/{user_email}")
def search_users(user_email: str):
    users = user_collection.find({
        "name": {"$regex": user_email}
        }).to_list(length=100)
    return [convert_item(user) for user in users]
