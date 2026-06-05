# BeaconFire_kafka_proj2_LJ
This is Kafka project 2. It uses Kafka CDC pipeline to replicate DML operations from a source PostgreSQL database (db_source) to a destination database (db_dst).

**The workflow is as follows:**
db_source (PostgreSQL)
   ↓
trigger (PostgreSQL)
   ↓
emp_cdc (PostgreSQL)
   ↓
producer (Python file)
   ↓
Kafka 
   ↓
consumer (Python file)
   ↓
db_dst (PostgreSQL)
