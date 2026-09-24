from fastapi import APIRouter

app = APIRouter(prefix="/multi", tags=["Miscellaneous"])


# create decorator function
@app.get("/hello")
async def hello(): # asynchronous
    return "Hello Deepseeds!"

"""uvicorn app:app --reload" "where 'app' b4 : is filename, 'app' after : is class name, --reload reloads browser automatically"""


@app.get("/sentiment-analysis")
def analyze_sentiment():
    # after logic here
    # then return the data
    return {
        "sentiment_score":"score-0.7",
        "platform":"huggingface",
        "sentiment":"Positive",
        "model":"distilbert-id"
    }

# create a point: that returns information about you(name, email, favmeal, age)

# TOPIC2: PATH PARAMETERS

@app.get("/sentiment/{text}")
def analyze_sentiment(text):
    if text.lower() in ["good", "nice", "great"]:
        return {
            "sentiment":"positive",
            "score":"positive score",
            "model":"model"
        }
    else:
        return {
            "sentiment":"negative",
            "score":"negative score",
            "model":"model"
        }

# Similar endpoint(with endpoints having the same identifier, hierarchy is crucial)

@app.get("/get-config/{response}")
def get_config(response: str):
    return {
        "data": "my data",
        "response": response
    }

# Another Endpoint
@app.get("/get-config/{temperature}")
def get_config(temperature: float):
    if temperature<0 or temperature>1:
        print("Temperature cannot be less than 0 or more than 1...")
        return { "error": "temperature should be between 0 and 1" }
    return { "temperature":temperature}


from pydantic import BaseModel

# REQUEST BODY
# define the type of data or the structure of data to be stored
class UserData(BaseModel):
    name: str
    age: int
    favMeal: str
    isSleepy: bool

@app.post("/posting-data", response_model=UserData)
def posting_data(request:UserData): # (...) -> ellipses syntax
    # expecting data from client
    return UserData(name=request.name, age=request.age, favMeal=request.favMeal, isSleepy=request.isSleepy)

# Exercise
class AiData(BaseModel):
    name:str
    prompt:str
    id:int

@app.post("/ai-post")
def post_ai(request:AiData):
    return {
        "data": request.name
    }
