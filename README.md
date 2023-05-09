# Streaming data from a transactional database to a data warehouse using Kafka (Confluent), Snowflake, and PostgreSQL.

TODO:

Watch a demo on youtube here.

Read the Medium blog post here.

## Architecture Overview
![architecture](/images/architecture.png)

## Project Description
This is a Data Engineering end to end project meant to demonstrate how to unlock real-time insights from a transactional database in real-time. 

Unlocking real-time insights requires a streaming architecture that’s continuously ingesting, processing, and provisioning data in real time. This is where Kafka (Confluent) comes into play. Finally, a data warehouse like Snowflake comes in handy to run your analytical queries and dashboards from where you can extract insights.

### Why Streaming data pipelines? 
Analyzing the events in real-time ​as opposed to batch ​gives the flexibility to see outcomes as they occur or in a windowed fashion depending on the consuming application.

### Stream Processing vs Batch Processing
[Here](https://www.confluent.io/learn/batch-vs-real-time-data-processing/#:~:text=Key%20Differences%20and%20Considerations) you can find some of the key differences and considerations. Many companies are finding that they need a modern, real-time data architecture to unlock the full potential of their data, regardless where it resides. Where some real-time data processing is required for real-time insights, persistent storage is required to enable advanced analytical functions like predictive analytics or machine learning. This is where a full-fledged data streaming platform like Confluent comes in.

## Tutorial
### 1. Store credentials
Create an environment file (.env) to manage all the values you'll need through the setup. [This](.env.example) is an example of a .env file.
### 2. Prerequisites
#### AWS
[Amazon Web Services](https://aws.amazon.com/what-is-aws/) (AWS) is the world’s most comprehensive and broadly adopted cloud, offering over 200 fully featured services from data centers globally.

AWS Offers a [Free Tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all) on each new AWS account. This will be enough to accomplish this project.

Make sure to select AWS us-east-1 when creating new resources. You can also use any other region and availavility zone as long as you create all the resorces needed in this project in the same ones.

#### Confluent
[Confluent Cloud](https://www.confluent.io/confluent-cloud/) is a fully managed service for Apache Kafka, a distributed streaming platform technology. It provides a single source of truth across event streams that mission-critical applications can rely on.

With Confluent Cloud, developers can easily get started with serverless Kafka and the related services required to build event streaming applications, including fully managed connectors, Schema Registry, and ksqlDB for stream processing

Confluent offers a 30 day [free trial](https://www.confluent.io/confluent-cloud/tryfree/) account. Then, follow the following:

- Provision a new [Kafka Cluster](https://docs.confluent.io/cloud/current/get-started/index.html#:~:text=Internet%20connectivity-,Step%201,-%3A%20Create%20a%20Kafka) in Confluent Cloud and make sure to select AWS us-east-1.

- Go to the API Keys section and create a new one with Global access, store them safely in your .env file for later use.

#### Snowflake
[Snowflake’s](https://docs.snowflake.com/en/user-guide/intro-key-concepts) Data Cloud is powered by an advanced data platform provided as a self-managed service. Snowflake enables data storage, processing, and analytic solutions that are faster, easier to use, and far more flexible than traditional offerings.

Snowflake offers a 30 day [free trial](https://docs.snowflake.com/en/user-guide/admin-trial-account) account, and you can use the same email after it ends to renew your free trial.

Make sure to select AWS us-east-1. Then, follow the following:

- [Generate a Snowflake key pair](https://docs.confluent.io/cloud/current/connectors/cc-snowflake-sink.html#generate-a-snowflake-key-pair): Open up a Terminal in your local and generate a private and public key using OpenSSL.
    ```bash
    openssl genrsa -out snowflake_key.pem 2048
    ```
    ```bash
    openssl rsa -in snowflake_key.pem  -pubout -out snowflake_key.pub
    ```
    ```bash
    ls -l snowflake_key*
    ```
- Add Public Key to the Snowflake user by running:
    ```bash
    grep -v "BEGIN PUBLIC" snowflake_key.pub | grep -v "END PUBLIC"|tr -d '\r\n'
    ```
- Open up a SQL worksheet inside Snowsight and run the following.
    ```SQL
    ALTER USER <SNOWFLAKE_USERNAME> SET RSA_PUBLIC_KEY = '<SNOWFLAKE_PUBLIC_KEY>'
    ```
- Create a new database.
    ```
    USE ROLE ACCOUNTADMIN;

    CREATE DATABASE KAFKA_DB;

    USE DATABASE KAFKA_DB;
    ```
- Then, Go to Snowsight -> Admin -> Accounts -> Locator. Copy and paste the URL in the .env file for later use.
- Let's do the same with the username, you can find it by going to Snowsight -> Admin -> Accounts -> Users & Roles.
- Finally, go back to the terminal and store the Private Key in the .env file for later use.
    ```bash
    grep -v "BEGIN RSA PRIVATE KEY" snowflake_key.pem | grep -v "END RSA PRIVATE KEY"|tr -d '\r\n'
    ```
### 3. AWS
#### Create RDS PostgreSQL Database

[PostgreSQL](https://aws.amazon.com/rds/postgresql/) has become the preferred open source relational database for many enterprise developers and startups, powering leading business and mobile applications. Amazon RDS makes it easier to set up, operate, and scale PostgreSQL deployments on the cloud. With Amazon RDS, you can deploy scalable PostgreSQL deployments in minutes with cost-efficient and resizable hardware capacity. Amazon RDS manages complex and time-consuming administrative tasks such as PostgreSQL software installation and upgrades, storage management, replication for high availability and read throughput, and backups for disaster recovery.

First, let's create a new [parameter group](https://docs.confluent.io/cloud/current/connectors/cc-postgresql-cdc-source-debezium.html#:~:text=A%20parameter-,group,-with%20the%20property) with the property rds.logical_replication set to 1. This is required is required to be able to connect to Kafka.

Let's create a new database on AWS by following these steps:
- First, make sure you are on US East 1.
- Secondly, navigate to RDS (Managed Relational Database Service).
- Then, click on Create database.
  - **Engine type:** select PostgreSQL.
  - **Templates:** select Free tier.
  - **DB instance identifier:** postgres-cdc.
  - **Master username:** Type a username and store it in the .env file for later use.
  - **Master password:** Type a password or let AWS create one for you and store it in the .env file for later use.
  - **DB instance class:** Select a micro type of instance.
  - **Public access:** Yes. It is important to have the [public access enabled](https://docs.confluent.io/cloud/current/connectors/cc-postgresql-cdc-source-debezium.html#:~:text=Services%20is%20enabled.-,Public,-access%20may%20be) to be able to connect to Kafka.
  - **Database port:** Type 5432 and store it in the .env file for later use.
  - **DB parameter group:** Select the one we just created, it is called `cdc`.
  - Leave the rest of the configuration as they appear by default.
  - Finally, click on Create database, and wait a few minutes while it gets created.
  - You should be able to see the Endpoint which should be something similar to `database-postgres-1.c0lxvocrw0de.us-east-1.rds.amazonaws.com`. Store it on the .env file for later use.
- Now, to connect to a DB instance from outside its VPC, the DB instance must be publicly accessible. Also, access must be granted using the [inbound rules](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html#USER_ConnectToPostgreSQLInstance.psql:~:text=By%20far%20the-,most%20common,-connection%20problem%20is) of the DB instance's security group.
  - Go to Security Groups
  - Select the DB instance's security group.
  - Click on `Edit inbound rules`.
  - Add a new rule for the port `5432` and source `Anywhere-IPv4`.
  - Click on save rules, and you are all set.

Connect to database via Terminal:
```bash
brew install postgresql
```

Connect to database
``` bash
psql --host=database-postgres-1.c0lxvocrw0de.us-east-1.rds.amazonaws.com --port=5432 --username=douglaspostgres --password --dbname=postgres
```

Set up database
Create tables by running this script: [Script](/aws/postgres-rds/create_tables.sql)

Verify that the tables were created by listing them with the following command (see more commands [here](https://dbschema.com/2020/04/14/postgresql-show-tables/)):
```SQL
 \dt
```

Data model of the transactional database

![datamodel](/images/transactional-data-model.png)

The data model we are going to use in this project was inspired by [this](https://developer.confluent.io/tutorials/survey-responses/ksql.html). Basically, this project is based on a Survey Web Application as surveys are great ways for businesses to capture insights from their customers and even their employees. But these insights go stale and lose value the longer they take to be analyzed. This recipe makes survey analysis real-time, allowing you to see results as survey responses happen.

#### Generate Mock Data
Run this [Python Script](/aws/postgres-rds/generate_mock-data.py) to emulate transactions in real-time.

```bash
sudo pip3 install virtualenv

virtualenv pyvenv

source aws/pyvenv/bin/activate

pip3 install requirements.txt

pip3 freeze

python3 aws/postgres-rds/generate_mock-data.py 

deactivate
```

#### Generate Real data with a Web App
TODO:

##### Deploy Web App with API Gateway and Lambda
TODO:

### 4. Kafka (Confluent Cloud)
[Confluent Platform](https://docs.confluent.io/platform/current/platform.html#what-is-confluent-used-for) lets you focus on how to derive business value from your data rather than worrying about the underlying mechanics, such as how data is being transported or integrated between disparate systems. Specifically, Confluent Platform simplifies connecting data sources to Kafka, building streaming applications, as well as securing, monitoring, and managing your Kafka infrastructure.

#### Postgres CDC Source connector
Now, let's countinuously send the transactions created in PostgreSQL to the Kafka cluster using Kafka Connect.

[Kafka Connect](https://docs.confluent.io/platform/current/connect/index.html#:~:text=Kafka%20Connect%20is%20a%20free,search%20indexes%2C%20and%20file%20systems.) is a tool for scalably and reliably streaming data between Apache Kafka® and other data systems. It makes it simple to quickly define connectors that move large data sets in and out of Kafka. Kafka Connect can ingest entire databases or collect metrics from all your application servers into Kafka topics, making the data available for stream processing with low latency.

In order to do this, let's set up a new Kafka Connector called [Postgres CDC Source connector](https://docs.confluent.io/cloud/current/connectors/cc-postgresql-cdc-source-debezium.html).

This Kafka connector leverages Change Data Capture (CDC) to obtain a snapshot of the existing data in a PostgreSQL database and then monitor and record all subsequent row-level changes to the database. All of the events for each table are recorded in a separate Kafka Topic.

Let's set up the connector by following these steps:
- Open Confluent Cloud.
- Go to the Connectors section on the left pane side.
- Select Postgres CDC Source connector
  - **Kafka Credentials:** Use your existing API key of your Kafka Cluster.
  - **Authentication:** Fill out the required parameters by using your .env file.
  - **Configuration:** Set both value and key format as `JSON_SR`.
  - **Sizing:** 1.
  - **Review and launch:** Set a connector name and compare the JSON cinfiguration given with the expected [here](confluent/source_connector.json).

- A Kafka topic should be created per each PostgreSQL table by the Kafka connector within seconds. Verify that messages are populating your Kafka topic by going to the topic section on the left pane side. You should see the following topics:
  - `postgres_cdc.public.survey_respondents`
  - `postgres_cdc.public.survey_responses`

Output example:

![messages topic](/images/topic_postgres.png)

#### Stream processing - KsqlDB
[Streaming data processing](https://www.confluent.io/learn/batch-vs-real-time-data-processing/#:~:text=weekly%20or%20monthly.-,Streaming%20data%20processing,-happens%20as%20the) happens as the data flows through a system. This results in analysis and reporting of events as it happens. An example would be fraud detection or intrusion detection. Streaming data processing means that the data will be analyzed and that actions will be taken on the data within a short period of time or near real-time, as best as it can.

Create a [KsqlDB Cluster](https://docs.confluent.io/cloud/current/get-started/index.html#section-2-add-ksql-cloud-to-the-cluster:~:text=Confluent%20Cloud.-,Step%201,-%3A%20Create%20a%20ksqlDB) in Confluent Cloud by selecting ksqlDb in the left side pane. Wait a few minutes while the Cluster is provisioned.

Navigate to the ksqlDB editor, ksqlDB supports SQL language for extracting, transforming, and loading events within your Kafka cluster. ksqlDB processes data in realtime, and in this case we want to enrich the Suvey Responses with the Survey Respondent data.

First, let's create a Stream per each Kafka topic. You can do it using the editor or by going to the Streams tab and clicking on `import topics as streams`.

![import topics as streams](/images/import_topics.png)

You should see that 2 streams were created called:
- `POSTGRES_CDCPUBLICSURVEY_RESPONSES`
- `POSTGRES_CDCPUBLICSURVEY_RESPONDENTS`

Finally, let's join both streams and create a new Stream called `SURVEY_RESPONSES_ENRICHED` that is going to be producing messages to a new Kafka topic called `topic_survey_responses_enriched`

```SQL
CREATE STREAM SURVEY_RESPONSES_ENRICHED
WITH (
    KAFKA_TOPIC = 'topic_survey_responses_enriched',
    VALUE_FORMAT = 'JSON_SR',
    KEY_FORMAT = 'JSON_SR',
    PARTITIONS = 1
) AS
SELECT
    R.RESPONDENT_ID AS RESPONDENT_ID,
    R.RESPONSE_ID AS RESPONSE_ID,
    T.NAME AS NAME,
    T.GENERATION AS GENERATION,
    R.QUESTION AS QUESTION,
    R.ANSWER AS ANSWER,
    R.IS_REAL AS IS_REAL,
    R.CREATED_AT AS CREATED_AT
FROM POSTGRES_CDCPUBLICSURVEY_RESPONSES R
INNER JOIN POSTGRES_CDCPUBLICSURVEY_RESPONDENTS T WITHIN 10 MINUTES GRACE PERIOD 2 MINUTES
    ON R.RESPONDENT_ID = T.RESPONDENT_ID
EMIT CHANGES;
```

You can verify the resulting set by running the following query:

```SQL
SELECT *
FROM SURVEY_RESPONSES_ENRICHED
EMIT CHANGES;
```

Output example:

![ksql query](/images/ksql_output.png)

Push queries are identified by the **EMIT CHANGES** clause. By running a push query, the client will receive a message for every change that occurs on the stream (that is, every new message).

View entire script [here](confluent/ksql.sql)

If you want to learn more about 
#### Snowflake Sink Kafka Connector
Now, let's send the resulting data from the Kafka Topic `topic_survey_responses_enriched` to our Data Warehouse in Snowflake unlocking real-time analytics and decision-making.

In order to do this, let's set up a new Kafka Connector called [Snowflake Sink Kafka Connector](https://docs.snowflake.com/en/user-guide/kafka-connector-overview) by following these steps.
- Open Confluent Cloud.
- Go to the Connectors section on the left pane side.
- Select Snowflake Sink
  - **Topic Selection:** Select the Topic from where you want to consume messages.
  - **Kafka Credentials:** Use your existing API key of your Kafka Cluster.
  - **Authentication:** Fill out the required parameters by using your .env file.
  - **Configuration:** Set both value and key format as `JSON_SR`.
  - **Sizing:** 1.
  - **Review and launch:** Set a connector name and compare the JSON cinfiguration given with the expected [here](confluent/sink_connector.json).
- A Stage, Pipe, and a Table should be created by the Kafka connector within seconds in Snowflake.

#### Stream Lineage
[Stream lineage](https://docs.confluent.io/cloud/current/stream-governance/stream-lineage.html) in Confluent Cloud is represented visually to show the movement of data from source to destination, and how it is transformed as it moves. The lineage graph always shows the activity of producers and consumers of data for the last 10 minutes.

You should see something like this at this point.

![lineage](/images/stream_lineage.png)

### 5. Snowflake
Let's review the objects created in Snowflake by the Kakfa Sink Connector. Open up a SQL Worksheet in Snowsight and look at the objects created in the left side pane view. You should see a internal stage, a pipe, and a table.

Every Snowflake table loaded by the Kafka connector has a schema consisting of two VARIANT columns:
- RECORD_CONTENT. This contains the Kafka message.
- RECORD_METADATA. This contains metadata about the message, for example, the topic from which the message was read.

```SQL
DESC STAGE SNOWFLAKE_KAFKA_CONNECTOR_LCC_8WXGX5_1146345676_STAGE_TOPIC_SURVEY_RESPONSES_ENRICHED;

DESC PIPE SNOWFLAKE_KAFKA_CONNECTOR_LCC_8WXGX5_1146345676_PIPE_TOPIC_SURVEY_RESPONSES_ENRICHED_0;

SELECT 
    TO_TIMESTAMP_NTZ(RECORD_CONTENT:CREATED_AT::VARCHAR) AS CREATED_AT,
    RECORD_CONTENT,
    RECORD_METADATA
FROM TOPIC_SURVEY_RESPONSES_ENRICHED
ORDER BY CREATED_AT DESC
LIMIT 1000
;
```

Output example:
![datamodel_analytical](/images/snowflake_table.png)

Now, let's create a view on top of the original table by mapping the attributes inside the [Variant](https://docs.snowflake.com/en/user-guide/querying-semistructured.html) columns.

```SQL
CREATE OR REPLACE VIEW TOPIC_SURVEY_RESPONSES_ENRICHED_VIEW AS
SELECT
    RECORD_METADATA:key::VARCHAR AS RESPONDENT_ID,
    RECORD_CONTENT:RESPONSE_ID::NUMBER AS RESPONSE_ID,
    RECORD_CONTENT:NAME::VARCHAR AS NAME,
    RECORD_CONTENT:GENERATION::VARCHAR AS GENERATION,
    RECORD_CONTENT:QUESTION::VARCHAR AS QUESTION,
    RECORD_CONTENT:ANSWER::VARCHAR AS ANSWER,
    RECORD_CONTENT:IS_REAL::BOOLEAN IS_REAL,
    CONVERT_TIMEZONE('UTC', 'America/Bogota', TO_TIMESTAMP_NTZ(RECORD_CONTENT:CREATED_AT::VARCHAR)) AS CREATED_AT
FROM TOPIC_SURVEY_RESPONSES_ENRICHED
;
```

Data model of the analytical database

![datamodel_analytical](/images/analytical-data-model.png)

Finally, let's answer some business questions by creating analytical queries. For example: which superheroes does each generation preffer?

```SQL
SELECT
    GENERATION,
    ANSWER,
    COUNT(*) AS AMOUNT
FROM TOPIC_SURVEY_RESPONSES_ENRICHED_VIEW
WHERE QUESTION = 'When it comes to superheroes:'
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC
;
```

Output example:
![datamodel_analytical](/images/snowflake_query.png)

View entire script [here](snowflake/snowflake.sql)

### Learnings, and next steps.
- Data Streaming is now easier and more accesible for everyone to learn and use.
- You can create awesome Data Engineering projects without paying anything as most services offer a free trial.
- This project was intended as a PoC and it is not recommended for production environments as we are not taking care of security actions such as granular access and networking.
- Use Terraform as Infrastructure-as-Code (IaC) tool. Use Terraform to spin up cloud resources in the cloud.
