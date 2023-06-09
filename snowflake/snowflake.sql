USE ROLE ACCOUNTADMIN;

CREATE DATABASE KAFKA_DB;

USE DATABASE KAFKA_DB;

ALTER USER DOUGLASCONFLUENT SET RSA_PUBLIC_KEY = ''
;

USE WAREHOUSE COMPUTE_WH;


DESC STAGE SNOWFLAKE_KAFKA_CONNECTOR_LCC_W5RG05_1406118471_STAGE_TOPIC_SURVEY_RESPONSES_ENRICHED;
LIST @SNOWFLAKE_KAFKA_CONNECTOR_LCC_W5RG05_1406118471_STAGE_TOPIC_SURVEY_RESPONSES_ENRICHED;

DESC PIPE SNOWFLAKE_KAFKA_CONNECTOR_LCC_W5RG05_1406118471_PIPE_TOPIC_SURVEY_RESPONSES_ENRICHED_0;
SELECT SYSTEM$PIPE_STATUS('SNOWFLAKE_KAFKA_CONNECTOR_LCC_W5RG05_1406118471_PIPE_TOPIC_SURVEY_RESPONSES_ENRICHED_0');

SELECT
    TO_TIMESTAMP_NTZ(RECORD_CONTENT:CREATED_AT::VARCHAR) AS CREATED_AT,
    RECORD_CONTENT,
    RECORD_METADATA
FROM TOPIC_SURVEY_RESPONSES_ENRICHED
ORDER BY CREATED_AT DESC
LIMIT 1000
;

CREATE OR REPLACE VIEW TOPIC_SURVEY_RESPONSES_ENRICHED_VIEW AS
SELECT
    RECORD_METADATA:key::VARCHAR AS RESPONDENT_ID,
    RECORD_CONTENT:RESPONSE_ID::NUMBER AS RESPONSE_ID,
    RECORD_CONTENT:NAME::VARCHAR AS NAME,
    RECORD_CONTENT:GENERATION::VARCHAR AS GENERATION,
    RECORD_CONTENT:SATISFACTION::NUMBER AS SATISFACTION,
    RECORD_CONTENT:QUESTION::VARCHAR AS QUESTION,
    RECORD_CONTENT:ANSWER::VARCHAR AS ANSWER,
    RECORD_CONTENT:IS_REAL::BOOLEAN IS_REAL,
    CONVERT_TIMEZONE('UTC', 'America/Bogota', TO_TIMESTAMP_NTZ(RECORD_CONTENT:CREATED_AT::VARCHAR)) AS CREATED_AT
FROM TOPIC_SURVEY_RESPONSES_ENRICHED
;

SELECT * FROM TOPIC_SURVEY_RESPONSES_ENRICHED_VIEW ORDER BY CREATED_AT DESC LIMIT 1000;

SELECT * FROM TOPIC_SURVEY_RESPONSES_ENRICHED_VIEW WHERE IS_REAL = TRUE ORDER BY CREATED_AT DESC;

SELECT
    GENERATION,
    ANSWER,
    COUNT(*) AS AMOUNT
FROM TOPIC_SURVEY_RESPONSES_ENRICHED_VIEW
WHERE QUESTION = 'When it comes to superheroes:'
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC
;

SELECT
    ANSWER,
    COUNT(*) AS AMOUNT
FROM TOPIC_SURVEY_RESPONSES_ENRICHED_VIEW
WHERE QUESTION = 'What came first:'
GROUP BY 1
;

SELECT
    GENERATION,
    AVG(SATISFACTION) AS AMOUNT
FROM TOPIC_SURVEY_RESPONSES_ENRICHED_VIEW
GROUP BY 1
ORDER BY 2 DESC
;
