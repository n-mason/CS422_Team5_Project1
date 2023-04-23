"""
Script to take CSV file sent from front-end and package data in InfluxDB format, then send to InfluxDB
"""

#command to run InfluxDB in docker: docker run -p 8086:8086 -v myInfluxVolume:/var/lib/influxdb2 influxdb:latest

#Test that can create InfluxDB from Python and store data
#pip3 install influxdb-client

#working with python: https://www.influxdata.com/blog/import-csv-data-influxdb-using-influx-cli-python-java-client-libraries/

from influxdb_client import InfluxDBClient, WriteOptions, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time, os
from datetime import datetime
import pandas as pd # pandas makes data analysis/manipulation easy
# Pandas has a read_csv function that reads column names based on CSV header and then chunks file

bucket = "Time_Series_Data"
org = "Project1"
token = "iBp9mU2tIlEF88e3cg2VClBELSjvQyOFT8OhatPg3-ULVAbmF1sctfGyr8Cr3a2gdg_DbJzJsQYC6Umg8_XtUw=="
url="https://us-east-1-1.aws.cloud2.influxdata.com"

# instantiate InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)

# useful API reference: https://influxdb-client.readthedocs.io/en/stable/api.html#writeapi

# send data in chunks of 1000 rows
for chunk in pd.read_csv("/home/nmason/CS422_Software_Methodologies_1/InfluxDBTest/GOOG_Testing.csv", chunksize=1_000):
    # need to create points to send to InfluxDB, so will convert chunk to a dict of dicts (called records), and then each inner dict will be a point (which is a row in the csv file)
    records = chunk.to_dict(orient='records') # records is a list of dicts, need to create point for each dict

    for record in records:
        #Date should be the timestamp that is store in influxDB and creates the graphs that we can observe over time
        date_str = record["Date"]
        ts_string = date_str + "T00:00:00.000Z"
        timestamp = datetime.strptime(ts_string, "%Y-%m-%dT%H:%M:%S.%fZ")

        #print(timestamp)
        #test = datetime.fromtimestamp(timestamp)
        #nice_str = test.strftime('%Y-%m-%d %H:%M:%S')
        #print(nice_str)

        p = Point("GOOG_Testing_Tags")

        # one record has structure: {'Date': xxx, 'Open': xxx, 'High': xxx, 'Low': xxx, 'Close': x, 'Adj Close': x, 'Volume': xx}
        for key, val in record.items():
            #if(key != "Date"): # will store Date as a field along with its timestamp form in InfluxDB
            p.field(key, val)
        
        # Assign tags to point
        """TS Metadata required from PDF: TS Name, Description, Domain(s), Units, Keywords, 
        Scalar/Vector(univariate/multivariate), Vector size, Length, Sampling Period"""
        # All metadata info can be stored as tags in InfluxDB

        # TS data required from PDF: Date, Time, Magnitude, other non-magnitude features?
        
        # This is for our test example, code will be changed so that the system gets this info POSTed from the contributor
        p.tag("TS Name", "GOOG_Testing") # Name of the file
        p.tag("Description", "Stock data for Google") # Description of the file
        p.tag("Domain(s)", "Finance") # Domain of the file
        p.tag("Units", "Days, USD, Number Of Shares") # Units of the file, for a stock case would be USD, Days (unit for YYYY-MM-DD) and Number of shares (Volume)
        # Keywords are stored as fields above (keywords like Open, High, Low, Volume etc), 
        p.tag("Scalar/Vector", "Vector")
        p.tag("Vector Size", "14")
        p.tag("Length", "14 Days") # limited data to test with, data retention limited to last 30 days with the free InfluxDB plan
        p.tag("Sampling Period", "One Day") 


        p.time(timestamp)

        # now write the point to influxdb
        with client.write_api(write_options=SYNCHRONOUS) as write_client:
            write_client.write(bucket=bucket, record=p)
        
        
    # tags (optional) should be used for columns that will be commonly queried
    # tag is like SQL indexed column and value
    # So in this case, good tags would be Author, Company Name along with other metadata tags

    