"""
Script to take file sent from upload python script and package data in InfluxDB format, then send to InfluxDB
"""

#command to run InfluxDB in docker: docker run -p 8086:8086 -v myInfluxVolume:/var/lib/influxdb2 influxdb:latest

#working with python: https://www.influxdata.com/blog/import-csv-data-influxdb-using-influx-cli-python-java-client-libraries/

from influxdb_client import InfluxDBClient, WriteOptions, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time, os
from datetime import datetime
import pandas as pd # pandas makes data analysis/manipulation easy
# Pandas has a read_csv function that reads column names based on CSV header and then chunks file



# useful API reference: https://influxdb-client.readthedocs.io/en/stable/api.html#writeapi


# Edit code so that have a function that takes in a Panda dataframe and then submits into the DB
# will consider pandas dataframe as df in function

def send_to_DB(df): # once we have the user form, function should take in a df and then a dictionary containing the other form data
    # InfluxDB client vars
    bucket = "Time_Series_Data"
    org = "Project1"
    token = "iBp9mU2tIlEF88e3cg2VClBELSjvQyOFT8OhatPg3-ULVAbmF1sctfGyr8Cr3a2gdg_DbJzJsQYC6Umg8_XtUw=="
    url="https://us-east-1-1.aws.cloud2.influxdata.com"

    # instantiate InfluxDB client
    client = InfluxDBClient(url=url, token=token, org=org)


    # need to create points to send to InfluxDB, so will convert chunk to a dict of dicts (called records), and then each inner dict will be a point (which is a row in the csv file)
    records = df.to_dict(orient='records') # records is a list of dicts, need to create point for each dict

    for record in records:
        #Date should be the timestamp that is store in influxDB and creates the graphs that we can observe over time
        date_str = record["Date"]
        ts_string = date_str + "T00:00:00.000Z"
        timestamp = datetime.strptime(ts_string, "%Y-%m-%dT%H:%M:%S.%fZ")

        #print(timestamp)
        #test = datetime.fromtimestamp(timestamp)
        #nice_str = test.strftime('%Y-%m-%d %H:%M:%S')
        #print(nice_str)

        p = Point("GOOG_Testing_func")

        # one record has structure: {'Date': xxx, 'Open': xxx, 'High': xxx, 'Low': xxx, 'Close': x, 'Adj Close': x, 'Volume': xx}
        for key, val in record.items():
            #if(key != "Date"): # will store Date as a field along with its timestamp form in InfluxDB
            p.field(key, val)
        
        # Assign tags to point
        """TS Metadata required from PDF: TS Name, Description, Domain(s), Units, Keywords, 
        Scalar/Vector(univariate/multivariate), Vector size, Length, Sampling Period"""

        """
        # All metadata info can be stored as tags in InfluxDB
        TS_name = info_dict['TS_name']
        desc = info_dict['description']
        domain = info_dict['domain']
        units = info_dict['domain']
        # Keywords are stored as fields above (keywords like Open, High, Low, Volume etc) 
        scalvec_val = info_dict['scalvec']
        vec_size = info_dict['vector_size']
        ts_len = info_dict['ts_length']
        samp_per = info_dict['sampling_period']
        """

        # TS data required from PDF: Date, Time, Magnitude, other non-magnitude features?
        
        # This is for our test example, code will be changed so that the system gets this info POSTed from the contributor
        # These tags will be defined based on what is entered into the contributor FORM
        p.tag("TS Name", "GOOG_Testing_func") # Name of the file
        p.tag("Description", "Stock data for Google") # Description of the file
        p.tag("Domain(s)", "Finance") # Domain of the file
        p.tag("Units", "Days, USD, Number Of Shares") # Units of the file, for a stock case would be USD, Days (unit for YYYY-MM-DD) and Number of shares (Volume)
        
        p.tag("Scalar/Vector", "Vector")
        p.tag("Vector Size", "14")
        p.tag("Length", "14 Days") # limited data to test with, data retention limited to last 30 days with the free InfluxDB plan
        p.tag("Sampling Period", "One Day") 


        p.time(timestamp)

        # now write the point to influxdb
        with client.write_api(write_options=SYNCHRONOUS) as write_client:
            write_client.write(bucket=bucket, record=p)

    return True 
        
    # tags (optional) should be used for columns that will be commonly queried
    # tag is like SQL indexed column and value
    # So in this case, good tags would be Author, Company Name along with other metadata tags

    