from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg2
import os
from dotenv import load_dotenv


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

load_dotenv()
conn = psycopg2.connect(
    database=os.getenv("POSTGRES_DB"),
    host=os.getenv("POSTGRES_HOST"),
    user=os.getenv("POSTGRES_MASTER_USERNAME"),
    password=os.getenv("POSTGRES_MASTER_PASSWORD"),
    port=os.getenv("POSTGRES_PORT"),
)

questions = [
    "I consider myself:",
    "I prefer my pizza:",
    "On the weekends I would rather:",
    "When I eat cereal:",
    "What came first:",
    "When it comes to superheroes:",
    "When it comes to pets:",
    "What is a better dessert:",
    "iOS or Android?",
]


@app.get("/")
async def survey(request: Request):
    return templates.TemplateResponse("survey.html", {"request": request})


@app.post("/")
def save_survey(*, request=Body(...)):
    cursor = conn.cursor()

    # Insert into SURVEY_RESPONDENTS
    dml_survey_respondents = f"""
        INSERT INTO SURVEY_RESPONDENTS (
            RESPONDENT_ID,
            NAME,
            GENERATION,
            SATISFACTION,
            CREATED_AT
        ) VALUES (
            DEFAULT,
            '{request["What's your name?"]}',
            '{request["From which generation are you?"]}',
            {request["From 0-5 how satisfied are you with this survey?"]},
            DEFAULT
        )
        RETURNING RESPONDENT_ID
        ;
    """
    cursor.execute(dml_survey_respondents)
    respondent_id = cursor.fetchone()[0]
    print(f"respondent_id: {respondent_id}\n")

    # Insert into SURVEY_RESPONSES
    for question in questions:
        dml_survey_responses = f"""
            INSERT INTO SURVEY_RESPONSES (
                RESPONSE_ID,
                RESPONDENT_ID,
                QUESTION,
                ANSWER,
                IS_REAL,
                CREATED_AT
            ) VALUES (
                DEFAULT,
                {respondent_id},
                '{question}',
                '{request[question]}',
                TRUE,
                DEFAULT
            )
            RETURNING RESPONSE_ID
            ;
        """
        cursor.execute(dml_survey_responses)

    # Commit DMLs to db
    conn.commit()
