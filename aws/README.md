Documentation of API Gateway, AWS Lambda, RDS


## RDS

Select us-east-1 
-> postgres 
-> free tier 
-> [public access enabled](https://docs.confluent.io/cloud/current/connectors/cc-postgresql-cdc-source-debezium.html#:~:text=Services%20is%20enabled.-,Public,-access%20may%20be) 
-> add port to security group [access rules](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html#USER_ConnectToPostgreSQLInstance.psql:~:text=By%20far%20the-,most%20common,-connection%20problem%20is)
-> A [parameter group](https://docs.confluent.io/cloud/current/connectors/cc-postgresql-cdc-source-debezium.html#:~:text=A%20parameter-,group,-with%20the%20property) with the property rds.logical_replication=1 is required 
-> create a new one (don't use the defaul one) 
-> [associate](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithDBInstanceParamGroups.html#:~:text=RDS%20API-,Associating,-a%20DB%20parameter) it with the DB instance 
-> reboot the database.


TODO: how to connect to rds https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html#USER_ConnectToPostgreSQLInstance.psql

### Connect to database via Terminal:
```bash
brew install postgresql
```

Connect to db
``` bash
psql --host=database-postgres-1.c0lxvocrw0de.us-east-1.rds.amazonaws.com --port=5432 --username=douglaspostgres --password --dbname=postgres
```
### Set up database
Create tables and set up CDC by running this script:
[Script](/aws/postgres-rds/create_tables.sql)

List tables, [see more](https://dbschema.com/2020/04/14/postgresql-show-tables/)
```SQL
 \dt
```

### Mock transactions in real-time

```bash
sudo pip3 install virtualenv

virtualenv pyvenv

source pyvenv/bin/activate

pip3 install requirements.txt
pip3 freeze

python3 aws/postgres-rds/generate_mock-data.py 

deactivate
```

run this [script](/aws/postgres-rds/generate_mock-data.py) to emulate transactions in real-time
...

### Use Web App to create transactions
TODO: