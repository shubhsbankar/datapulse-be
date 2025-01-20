import datetime
from app.endpoints.adhoc import *
from pydantic import BaseModel

class FormData(BaseModel):
    py_id: str
    execution_date: str
    input_1: str
    input_2: str
    input_3: str

# BigQuery Files
@router.post("/execute")
async def execute(data: FormData):
    try:
        print(data)
        return response(200, "Adhoc Execution Successful")
    except Exception as e:
        return response(400, str(e))

