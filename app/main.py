from fastapi import FastAPI
import uvicorn
from database import init_db
from routes.cards import cards_router
from starlette.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(cards_router)

init_db()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
