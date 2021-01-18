import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from datetime import datetime
import processor as processor

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/json/")
def get_potreros_stats(initial_date: str = Query(None, description="Initial date of the interval of time.\n"
                                                                   "Leave empty if you want to consider "
                                                                   "from the oldest date",
                                                 regex=r'\d{4}-\d{2}-\d{2}'),
                       final_date: str = Query(None, description="Final date of the interval of time.\n"
                                                                 "Leave empty if you want to consider "
                                                                 "to the most recent date",
                                               regex=r'\d{4}-\d{2}-\d{2}'),
                       potrero: List[str] = Query(None, description="Potrero to consider in the information."
                                                                    "Leave emtpy if you want to consider all of them")):

    initial_date_ = None
    if initial_date is not None:
        initial_date_ = datetime.strptime(initial_date, "%Y-%m-%d").date()
    final_date_ = None
    if final_date is not None:
        final_date_ = datetime.strptime(final_date, "%Y-%m-%d").date()

    res = processor.get_potreros_info(names=potrero, initial_date=initial_date_, final_date=final_date_)
    return res


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app)
