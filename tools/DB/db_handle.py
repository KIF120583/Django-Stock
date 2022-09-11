import os
import sys
import time
import codecs
import csv
import logging
import datetime
try:
    import pymysql
except:
    os.system("pip install pymysql")
    import pymysql

db_setting = {
  "host" : "192.168.23.137",
  "port" : 3306,
  "user" : "root",
  "password" : "svteam",
  "db":"stock",
  "charset":"utf8"
}

class dbhandle:

    def __init__(self,db_setting=None):

        self.db_setting = db_setting
        self.conn = None
        self.db_connect_state = None
        self.insert_db_data_state = None

        try:
            self.conn = pymysql.connect(**self.db_setting)
            self.db_connect_state = True
        except Exception as err:
            self.db_connect_state = False

    def create_table(self , table_name = None):
        try:
            with self.conn.cursor() as cursor:
                command = "CREATE TABLE `{}`.`{}` (`Date` VARCHAR(45) NOT NULL,`Open` VARCHAR(45) NULL,`High` VARCHAR(45) NULL,`Low` VARCHAR(45) NULL,`Close` VARCHAR(45) NULL,`Volume` VARCHAR(45) NULL,PRIMARY KEY (`Date`));".format(db_setting["db"],table_name)
                print(command)
                cursor.execute(command)
        except Exception as err:
            print(err)

    def insert_db_data(self , stock_num , stock_date , stock_data):
        #logger.info("insert_db_data for {} on {}".format(stock_num,stock_date))
        self.insert_db_data_state = None
        try:
            with self.conn.cursor() as cursor:

                Open = stock_data['Open']
                High = stock_data['High']
                Low  = stock_data['Low']
                Close = stock_data['Close']
                Volume = stock_data['Volume'].replace(",","")

                command = "INSERT INTO stock.{}(Date,Open,High,Low,Close,Volume)VALUES('{}','{}','{}','{}','{}','{}')".format(stock_num,stock_date,Open,High,Low,Close,Volume)
                #logger.info("insert_db_data command : {}".format(command))
                cursor.execute(command)
                self.conn.commit()
                #logger.info("Insert stock data of {} successfully on {}!!!".format(stock_num,stock_date))
                self.insert_db_data_state = True
                self.insert_db_data_state_count_pass += 1
        except Exception as err:
            logger.error("Insert stock data of {} failed on {}!!!".format(stock_num,stock_date))
            logger.error(err)
            self.insert_db_data_state = False
            self.insert_db_data_state_count_fail += 1

    def get_insert_db_data_state_count(self):
        return self.insert_db_data_state_count_pass , self.insert_db_data_state_count_fail

    def reset_insert_db_data_state_count(self):
        self.insert_db_data_state_count_pass = 0
        self.insert_db_data_state_count_fail = 0


def mylogging():
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
        datefmt='%Y%m%d %H:%M:%S')

    # Output to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # Output to Log file
    log_filename = datetime.datetime.now().strftime("db_handle/%Y-%m-%d_%H_%M_%S.log")
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

def read_stock_data(file_dir):
    try:
        ret = {}
        with open(file_dir, newline='',encoding='utf8') as csvfile:
            rows = csv.reader(csvfile)
            print(rows)
            rows = list(rows)
            #print(rows)
            for i in range(1,len(rows)):
                ret[rows[i][0]] = {
                                    "Open":rows[i][1],
                                    "High":rows[i][2],
                                    "Low":rows[i][3],
                                    "Close":rows[i][4],
                                    "Volume":rows[i][5]
                }
        return ret
    except Exception as err:
        logger.error(err)
        return None

def delays(seconds, reason = ""):
    print("----- delays() -----")
    print("Waiting for %s seconds due to %s..." %(seconds, reason))
    seconds = int(seconds)

    while seconds > 0:
        time.sleep(1)
        seconds -= 1
        second_str = "%d seconds...\r" %seconds
        print(second_str, end='')

def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "#"*x, "."*(size-x), j, count),
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)

if __name__ == '__main__':

    # Enable log function
    mylogging()

    my_db = dbhandle(db_setting=db_setting)
    time_start = time.time()
    #----------------------------------

    stock_id = "2317"

    time_1 = time.time()
    my_db.create_table(table_name=stock_id)
    stock_data = read_stock_data(r"..\StockData\everyday\All\{}.csv".format(stock_id))

    """
    {
        '110/07/01': {'Open': '112.50', 'High': '112.50', 'Low': '111.50', 'Close': '112.00', 'Volume': '15,992'},
        '110/07/02': {'Open': '112.00', 'High': '112.50', 'Low': '111.50', 'Close': '111.50', 'Volume': '16,613'}
    }
    """

    # Convert stock_data to list type
    stock_data_list = []
    for key,value in stock_data.items():
        temp = []
        temp.append(key)
        temp.append(value)
        stock_data_list.append(temp)
    """
    [
      ['110/07/01', {'Open': '112.50', 'High': '112.50', 'Low': '111.50', 'Close': '112.00', 'Volume': '15,992'}],
      ['110/07/02', {'Open': '112.00', 'High': '112.50', 'Low': '111.50', 'Close': '111.50', 'Volume': '16,613'}]
    ]
    """

    # add progress bar
    my_db.reset_insert_db_data_state_count()
    for i in progressbar(range(len(stock_data)), "{} : ".format(stock_id), 40):
        my_db.insert_db_data(stock_id,stock_data_list[i][0],stock_data_list[i][1])
    logger.info("Update {} stock data , total {} , pass {} , fail {}".format(stock_id,len(stock_data),my_db.get_insert_db_data_state_count()[0],my_db.get_insert_db_data_state_count()[1]))

    time_2 = time.time()
    time_interval = time_2 - time_1
    logger.info("Time cost for {} is {} sec".format(stock_id,time_interval))

    #----------------------------------
    time_end = time.time()
    time_total_interval = time_2 - time_1
    logger.info("Total Time cost : {} sec".format(time_total_interval))


