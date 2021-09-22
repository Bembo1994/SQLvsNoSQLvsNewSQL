import mysql.connector
import time
import sys

files=["1K","100K","1M","3M","10M","historical_stock_prices"]
if len(sys.argv) < 2:
  host = 'localhost'
else :
  host = sys.argv[1]
mydb = mysql.connector.connect(host=host, user="root", password="password", db="example", port=3306, allow_local_infile=True)
mycursor = mydb.cursor()
with open("Result_query/report_sql_singlenode.txt","a") as report:
  for f in files:
    start_query = time.time()
    print("init query {}".format(start_query))
    mycursor.execute("DROP TABLE IF EXISTS stockprices;")
    mycursor.execute("CREATE TABLE IF NOT EXISTS stockprices ( ticker VARCHAR(255), open FLOAT, close FLOAT, adj_close FLOAT, low FLOAT, high FLOAT, volume INT, data DATE);")
    mycursor.execute("LOAD DATA LOCAL INFILE 'dataset/"+f+".csv' INTO TABLE stockprices  FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES;")
    mycursor.execute("CREATE OR REPLACE VIEW appoggio AS (SELECT ticker AS ticker, MIN(data) AS min_data, MAX(data) AS max_data FROM stockprices GROUP BY ticker);")
    mycursor.execute("CREATE OR REPLACE VIEW ticker_close_min AS (SELECT stockprices.ticker,close FROM stockprices JOIN appoggio ON stockprices.ticker = appoggio.ticker WHERE stockprices.data = appoggio.min_data);")
    mycursor.execute("CREATE OR REPLACE VIEW ticker_close_max as (select stockprices.ticker,close from stockprices join appoggio on stockprices.ticker = appoggio.ticker where stockprices.data = appoggio.max_data);")
    mycursor.execute("CREATE OR REPLACE VIEW ticker_variation as (select ticker_close_max.ticker, (ticker_close_max.close-ticker_close_min.close)/ticker_close_min.close as variation from ticker_close_max join ticker_close_min on ticker_close_max.ticker = ticker_close_min.ticker);")
    mycursor.execute("SELECT stockprices.ticker, min(stockprices.data) AS first_data, MAX(stockprices.data) AS last_data, cast(ticker_variation.variation*100  as decimal(15,3)) AS variation_percentage, cast(MIN(stockprices.low)as decimal(15,3)) AS min_price, cast(MAX(stockprices.high) as decimal(15,3)) AS max_price\
                        FROM stockprices join ticker_variation on stockprices.ticker = ticker_variation.ticker\
                        GROUP BY stockprices.ticker, ticker_variation.variation\
                        ORDER BY last_data DESC;")

    myresult = mycursor.fetchall()
    end_query = time.time()
    query_time = end_query - start_query
    print("query eseguita in {}".format(query_time))
    report.write("{}\t{}\n".format(f,query_time))
