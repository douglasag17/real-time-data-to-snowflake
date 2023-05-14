// https://surveyjs.io/create-free-survey
surveyJSON = {
    "title": "Survey App",
    "description": "A Survey Web App created with the purpose of testing out this project https://github.com/douglasag17/real-time-data-to-snowflake",
    "logoPosition": "right",
    "pages": [
        {
            "name": "page1",
            "elements": [
                {
                    "type": "text",
                    "name": "What's your name?",
                    "title": "What's your name?",
                    "isRequired": true,
                    "autocomplete": "name"
                },
                {
                    "type": "dropdown",
                    "name": "From which generation are you?",
                    "title": "From which generation are you?",
                    "isRequired": true,
                    "choices": [
                        "The Silent Generation: Born 1928-1945",
                        {
                            "value": "Baby Boomers: Born 1946-1964Baby Boomers: Born 1946-1964",
                            "text": "Baby Boomers: Born 1946-1964"
                        },
                        "Generation X: Born 1965-1980",
                        "Millennials: Born 1981-1996",
                        "Generation Z: Born 1997-2012"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "I consider myself:",
                    "title": "I consider myself:",
                    "isRequired": true,
                    "choices": [
                        "Extroverted",
                        "Introverted"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "I prefer my pizza:",
                    "title": "I prefer my pizza:",
                    "isRequired": true,
                    "choices": [
                        "With pineapple",
                        "Without pineapple"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "On the weekends I would rather:",
                    "title": "On the weekends I would rather:",
                    "isRequired": true,
                    "choices": [
                        {
                            "value": "Stay at home and chill with a movie",
                            "text": "Go out and party"
                        },
                        "Stay at home and chill with a movie"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "When I eat cereal:",
                    "title": "When I eat cereal:",
                    "isRequired": true,
                    "choices": [
                        "I pour the cereal first",
                        "I pour the milk first"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "What came first:",
                    "title": "What came first:",
                    "isRequired": true,
                    "choices": [
                        "The Egg",
                        "The chicken"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "When it comes to superheroes:",
                    "title": "When it comes to superheroes:",
                    "isRequired": true,
                    "choices": [
                        "I prefer DC",
                        "I prefer Marvel"
                    ],
                    "showNoneItem": true
                },
                {
                    "type": "radiogroup",
                    "name": "When it comes to pets:",
                    "title": "When it comes to pets:",
                    "isRequired": true,
                    "choices": [
                        "I am a Cat person",
                        "I am a Dog person"
                    ],
                    "showNoneItem": true
                },
                {
                    "type": "radiogroup",
                    "name": "What is a better dessert:",
                    "title": "What is a better dessert:",
                    "isRequired": true,
                    "choices": [
                        "Ice Cream",
                        "Cake"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "iOS or Android?",
                    "title": "iOS or Android?",
                    "isRequired": true,
                    "choices": [
                        "iOS",
                        "Android"
                    ]
                },
                {
                    "type": "rating",
                    "name": "From 0-5 how satisfied are you with this survey?",
                    "title": "From 0-5 how satisfied are you with this survey?",
                    "isRequired": true
                }
            ]
        }
    ]
}
