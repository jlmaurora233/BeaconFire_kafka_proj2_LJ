# BeaconFire_kafka_proj2_LJ
This is Kafka project 2. It uses Kafka CDC pipeline to replicate DML operations from a source PostgreSQL database (db_source) to a destination database (db_dst). <br>

**The workflow is as follows:** <br>
db_source (PostgreSQL) <br>
   ↓ <br>
trigger (PostgreSQL) <br>
   ↓ <br>
emp_cdc (PostgreSQL) <br>
   ↓ <br>
producer (Python file) <br>
   ↓ <br>
Kafka <br>
   ↓ <br>
consumer (Python file) <br>
   ↓ <br>
db_dst (PostgreSQL) <br>
