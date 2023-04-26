# Streaming data to your data warehouse using Kafka (Confluent) and Snowflake
Continuously loading data to your data warehouse with Snowflake + Declarative data pipelines with Dynamic tables.

TODO: insert table of contents

## Architecture Overview
TODO: insert here architecture, https://drive.google.com/file/d/1CSzKirj17dDpR_8SdR-nojX7Ivfypph9/view?usp=sharing


TODO: Insert Images for everything
## Setting up AWS RDS (PostgreSQL)

## Setting up Snowflake
- Sign up, etc
- Create database
    ```
    USE ROLE ACCOUNTADMIN;

    CREATE DATABASE KAFKA_DB;

    USE DATABASE KAFKA_DB;
    ```

## Setting up Confluent Cloud
- Sign up, etc

- Generate a new API Key for your Kafka Cluster
- Download it and keep it

## Setting up Postgres CDC Source connector

## Setting up ksqlDB

## Setting up Snowflake Sink Kafka Connector

Steps:
- [Overview of the Kafka Connector](https://docs.snowflake.com/en/user-guide/kafka-connector-overview) 
- Go to Confluent Cloud -> Connectors -> Snowflake Sink
- Select the Topic from where you want to consume messages
- Use your existing API key of your Kafka Cluster
- [Generate a Snowflake key pair](https://docs.confluent.io/cloud/current/connectors/cc-snowflake-sink.html#generate-a-snowflake-key-pair)
  - Open up a Terminal and generate a private and public key using OpenSSL.
  - `openssl genrsa -out snowflake_key.pem 2048`
  - `openssl rsa -in snowflake_key.pem  -pubout -out snowflake_key.pub`
  - `ls -l snowflake_key*`
- Fill out required parameters
  - Connection URL: Go to Snowflake -> Admin -> Accounts -> Locator
  - Connection User Name: Snowflake username
    - Add public key to the Snowflake user by running:
      - `grep -v "BEGIN PUBLIC" snowflake_key.pub | grep -v "END PUBLIC"|tr -d '\r\n'`
      - `ALTER USER DOUGLASCONFLUENT SET RSA_PUBLIC_KEY = '<public-key>'`
  - Private Key
    - `grep -v "BEGIN RSA PRIVATE KEY" snowflake_key.pem | grep -v "END RSA PRIVATE KEY"|tr -d '\r\n'`
  - Database Name: KAFKA_DB
  - Schema Name: PUBLIC
- A Stage, Pipe, and a Table should be created by the Kafka connector within seconds.
    ```
    USE WAREHOUSE COMPUTE_WH;

    DESC STAGE SNOWFLAKE_KAFKA_CONNECTOR_LCC_PRZ15M_1550001102_STAGE_TOPIC_PAYROLL;
    LIST @SNOWFLAKE_KAFKA_CONNECTOR_LCC_PRZ15M_1550001102_STAGE_TOPIC_PAYROLL;

    DESC PIPE KAFKA_DB.PUBLIC.SNOWFLAKE_KAFKA_CONNECTOR_LCC_PRZ15M_1550001102_PIPE_TOPIC_PAYROLL_0;

    SELECT * FROM TOPIC_PAYROLL;

    CREATE OR REPLACE VIEW TOPIC_PAYROLL_VIEW AS
    SELECT 
        RECORD_CONTENT,
        RECORD_CONTENT:employee_id::NUMBER AS EMPLOYEE_ID,

        TO_TIMESTAMP_NTZ(RECORD_METADATA:CreateTime::VARCHAR) as CREATED_AT
    FROM TOPIC_PAYROLL
    ;

    SELECT * FROM TOPIC_PAYROLL_VIEW ORDER BY CREATED_AT DESC;
    ```