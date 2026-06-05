"""
Copyright (C) 2024 BeaconFire Staffing Solutions
Author: Ray Wang

This file is part of Oct DE Batch Kafka Project 1 Assignment.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import csv
import json
import os
from confluent_kafka import Producer
from employee import Employee
import confluent_kafka
from pyspark.sql import SparkSession
import pandas as pd
from confluent_kafka.serialization import StringSerializer
import psycopg2

employee_topic_name = "bf_employee_cdc"

class cdcProducer(Producer):
    #if running outside Docker (i.e. producer is NOT in the docer-compose file): host = localhost and port = 29092
    #if running inside Docker (i.e. producer IS IN the docer-compose file), host = 'kafka' or whatever name used for the kafka container, port = 9092
    def __init__(self, host="localhost", port="29092"):
        self.host = host
        self.port = port
        producerConfig = {'bootstrap.servers':f"{self.host}:{self.port}",
                          'acks' : 'all'}
        super().__init__(producerConfig)
        self.running = True
        # tracks the last CDC row already published
        self.last_offset = 0
    
    def fetch_cdc(self,):
        rows = []
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                port = '5434', # the ports are 5434 for source and 5433 for destination
                password="postgres")
            conn.autocommit = True
            cur = conn.cursor()
            #your logic should go here
            query = """
                SELECT
                    cdc_id,
                    "Employee ID",
                    "First Name",
                    "Last Name",
                    "Date of Birth",
                    City,
                    "Action"
                FROM emp_cdc
                WHERE cdc_id > %s
                ORDER BY cdc_id;
            """
            cur.execute(query, (self.last_offset,))
            # update last offset
            rows = cur.fetchall() # get all returned results
            if rows:
                # retrieve the cdc_id
                self.last_offset = rows[-1][0]


            cur.close()
            conn.close()
        except Exception as err:
            print("Error retrieving CDC records:", err)
        
        return rows # if you need to return sth, modify here
    

if __name__ == '__main__':
    encoder = StringSerializer('utf-8')
    producer = cdcProducer()
    
    while producer.running:
        # your implementation goes here
        # takes in the records and sends them to Kafka
        records = producer.fetch_cdc()
        for row in records:
            load = {
                    "cdc_id": row[0],
                    "emp_id": row[1],
                    "emp_FN": row[2],
                    "emp_LN": row[3],
                    "emp_dob": str(row[4]),
                    "emp_city": row[5],
                    "action": row[6]
                }
            producer.produce(
                topic=employee_topic_name,
                key=encoder(str(row[1])),
                value=encoder(json.dumps(load))
                )
            print("Sending:", load)

        producer.flush()
    
