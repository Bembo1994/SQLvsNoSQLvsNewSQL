import psycopg2
import time
import sys
import socket

files=["1K","100K","1M","3M","10M","historical_stock_prices"]

if len(sys.argv) < 2:
  host = 'localhost'
else :
  host = sys.argv[1]

conn = psycopg2.connect(
        user='root',
        host=host,
        port=26257
    )
conn.set_session(autocommit=True)
cursor = conn.cursor()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_server_dataset = s.getsockname()[0]
s.close()

with open("Result_query/report_newsql_singlenode.txt","a") as report:
  for f in files:
    cursor.execute("DROP DATABASE IF EXISTS mytest CASCADE;")
    cursor.execute("CREATE DATABASE IF NOT EXISTS mytest;")
    cursor.execute("USE mytest;")
    cursor.execute("IMPORT TABLE hsp ( ticker STRING, open FLOAT, close FLOAT, adj_close FLOAT, low FLOAT, high FLOAT, volume FLOAT, data DATE ) CSV DATA ('http://"+ip_server_dataset+":8000/dataset/"+f+".csv') WITH skip = '1';")
    start_query = time.time()
    print("init query {}".format(start_query))
    cursor.execute("CREATE OR REPLACE VIEW appoggio AS (SELECT ticker AS ticker, MIN(data) AS min_data, MAX(data) AS max_data FROM hsp GROUP BY ticker);")
    cursor.execute("CREATE OR REPLACE VIEW ticker_close_min AS (SELECT hsp.ticker,close FROM hsp JOIN appoggio ON hsp.ticker = appoggio.ticker WHERE hsp.data = appoggio.min_data);")
    cursor.execute("CREATE OR REPLACE VIEW ticker_close_max as (select hsp.ticker,close from hsp join appoggio on hsp.ticker = appoggio.ticker where hsp.data = appoggio.max_data);")
    cursor.execute("CREATE OR REPLACE VIEW ticker_variation as (select ticker_close_max.ticker, (ticker_close_max.close-ticker_close_min.close)/ticker_close_min.close as variation from ticker_close_max join ticker_close_min on ticker_close_max.ticker = ticker_close_min.ticker);")
    cursor.execute("SELECT hsp.ticker, min(hsp.data) AS first_data, MAX(hsp.data) AS last_data, cast(ticker_variation.variation*100  as decimal(15,3)) AS variation_percentage, cast(MIN(hsp.low)as decimal(15,3)) AS min_price, cast(MAX(hsp.high) as decimal(15,3)) AS max_price\
                        FROM hsp join ticker_variation on hsp.ticker = ticker_variation.ticker\
                        GROUP BY hsp.ticker, ticker_variation.variation\
                        ORDER BY last_data DESC;")

    myresult = cursor.fetchall()
    end_query = time.time()
    query_time = end_query - start_query
    print("query eseguita in {}".format(query_time))
    report.write("{}\t{}\n{}\n\n".format(f,query_time,myresult))
cursor.close()
conn.close()