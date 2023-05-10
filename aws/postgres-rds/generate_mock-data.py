import psycopg2
import time
import os
from dotenv import load_dotenv
from faker import Faker
import random


# From which generation are you?
GENERATIONS = [
    "The Silent Generation: Born 1928-1945",
    "Baby Boomers: Born 1946-1964",
    "Generation X: Born 1965-1980",
    "Millennials: Born 1981-1996",
    "Generation Z: Born 1997-2012",
]

# From 0-5 how satisfied are you with this survey?
SATISFACTION_GRADE = [0, 1, 2, 3, 4, 5]

QUESTIONS = {
    "Q1": {"Q": "I consider myself:", "A": ["Extroverted", "Introverted"]},
    "Q2": {"Q": "I prefer my pizza:", "A": ["With pineapple", "Without pineapple"]},
    "Q3": {
        "Q": "On the weekends I would rather:",
        "A": ["Go out and party", "Stay at home and chill with a movie"],
    },
    "Q4": {
        "Q": "When I eat cereal:",
        "A": ["I pour the cereal first", "I pour the milk first"],
    },
    "Q5": {"Q": "What came first:", "A": ["The Egg", "The chicken"]},
    "Q6": {"Q": "A hot dog is a sandwich?", "A": ["Yes", "No"]},
    "Q7": {
        "Q": "When it comes to superheroes:",
        "A": ["I prefer DC", "I prefer Marvel"],
    },
    "Q8": {
        "Q": "When it comes to pets:",
        "A": ["I am a Cat person", "I am a Dog person", "Other"],
    },
    "Q9": {"Q": "What is a better dessert:", "A": ["Ice Cream", "Cake"]},
    "Q10": {
        "Q": "iOS or Android?",
        "A": ["iOS", "Android"],
    },
}


def add_row(cursor, fake):
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
            '{fake.name()}',
            '{GENERATIONS[random.randint(0, len(GENERATIONS)-1)]}',
            {SATISFACTION_GRADE[random.randint(0, len(SATISFACTION_GRADE)-1)]},
            DEFAULT
        )
        RETURNING RESPONDENT_ID
        ;
    """
    cursor.execute(dml_survey_respondents)
    respondent_id = cursor.fetchone()[0]
    print(f"\nrespondent_id: {respondent_id}")

    # Insert into SURVEY_RESPONSES
    for key, value in QUESTIONS.items():
        value["Q"]
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
                '{value['Q']}',
                '{value['A'][random.randint(0, len(value['A'])-1)]}',
                FALSE,
                DEFAULT
            )
            RETURNING RESPONSE_ID
            ;
        """
        cursor.execute(dml_survey_responses)
        response_id = cursor.fetchone()[0]
        print(f"\t{key} -> response_id: {response_id}")


def main():
    load_dotenv()
    fake = Faker()
    with psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        host=os.getenv("POSTGRES_HOST"),
        user=os.getenv("POSTGRES_MASTER_USERNAME"),
        password=os.getenv("POSTGRES_MASTER_PASSWORD"),
        port=os.getenv("POSTGRES_PORT"),
    ) as conn:
        cursor = conn.cursor()
        print("connection established")
        try:
            while True:
                add_row(cursor, fake)
                conn.commit()
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nclosing")


if __name__ == "__main__":
    main()
