from bs4 import BeautifulSoup
import requests
import csv
import os 
import time 
#from WebCrawler_APIs import *

excel_date_list = [

'110/07/01' ,
'110/07/02' ,
'110/07/05' ,
'110/07/06' ,
'110/07/07' ,
'110/07/08' ,
'110/07/09' ,
'110/07/12' ,
'110/07/13' ,
'110/07/14' ,
'110/07/15' ,
'110/07/16' ,
'110/07/19' ,
'110/07/20' ,
'110/07/21' ,
'110/07/22' ,
'110/07/23' ,
'110/07/26' ,
'110/07/27' ,
'110/07/28' ,
'110/07/29' ,
'110/07/30' ,
'110/08/02' ,
'110/08/03' ,
'110/08/04' ,
'110/08/05' ,
'110/08/06' ,
'110/08/09' ,
'110/08/10' ,
'110/08/11' ,
'110/08/12' ,
'110/08/13' ,
'110/08/16' ,
'110/08/17' ,
'110/08/18' ,
'110/08/19' ,
'110/08/20' ,
'110/08/23' ,
'110/08/24' ,
'110/08/25' ,
'110/08/26' ,
'110/08/27' ,
'110/08/30' ,
'110/08/31' ,
'110/09/01' ,
'110/09/02' ,
'110/09/03' ,
'110/09/06' ,
'110/09/07' ,
'110/09/08' ,
'110/09/09' ,
'110/09/10' ,
'110/09/13' ,
'110/09/14' ,
'110/09/15' ,
'110/09/16' ,
'110/09/17' ,
'110/09/22' ,
'110/09/23' ,
'110/09/24' ,
'110/09/27' ,
'110/09/28' ,
'110/09/29' ,
'110/09/30' ,
'110/10/01' ,
'110/10/04' ,
'110/10/05' ,
'110/10/06' ,
'110/10/07' ,
'110/10/08' ,
'110/10/12' ,
'110/10/13' ,
'110/10/14' ,
'110/10/15' ,
'110/10/18' ,
'110/10/19' ,
'110/10/20' ,
'110/10/21' ,
'110/10/22' ,
'110/10/25' ,
'110/10/26' ,
'110/10/27' ,
'110/10/28' ,
'110/10/29' ,
'110/11/01' ,
'110/11/02' ,
'110/11/03' ,
'110/11/04' ,
'110/11/05' ,
'110/11/08' ,
'110/11/09' ,
'110/11/10' ,
'110/11/11' ,
'110/11/12' ,
'110/11/15' ,
'110/11/16' ,
'110/11/17' ,
'110/11/18' ,
'110/11/19' ,
'110/11/22' ,
'110/11/23' ,
'110/11/24' ,
'110/11/25' ,
'110/11/26' ,
'110/11/29' ,
'110/11/30' ,
'110/12/01' ,
'110/12/02' ,
'110/12/03' ,
'110/12/06' ,
'110/12/07' ,
'110/12/08' ,
'110/12/09' ,
'110/12/10' ,
'110/12/13' ,
'110/12/14' ,
'110/12/15' ,
'110/12/16' ,
'110/12/17' ,
'110/12/20' ,
'110/12/21' ,
'110/12/22' ,
'110/12/23' ,
'110/12/24' ,
'110/12/27' ,
'110/12/28' ,
'110/12/29' ,
'110/12/30' ,
'111/01/03' ,
'111/01/04' ,
'111/01/05' ,
'111/01/06' ,
'111/01/07' ,
'111/01/10' ,
'111/01/11' ,
'111/01/12' ,
'111/01/13' ,
'111/01/14' ,
'111/01/17' ,
'111/01/18' ,
'111/01/19' ,
'111/01/20' ,
'111/01/21' ,
'111/01/24' ,
'111/01/25' ,
'111/01/26' ,
'111/02/07' ,
'111/02/08' ,
'111/02/09' ,
'111/02/10' ,
'111/02/11' ,
'111/02/14' ,
'111/02/15' ,
'111/02/16' ,
'111/02/17' ,
'111/02/18' ,
'111/02/21' ,
'111/02/22' ,
'111/02/23' ,
'111/02/24' ,
'111/02/25' ,
'111/03/01' ,
'111/03/02' ,
'111/03/03' ,
'111/03/04' ,
'111/03/07' ,
'111/03/08' ,
'111/03/09' ,
'111/03/10' ,
'111/03/11' ,
'111/03/14' ,
'111/03/15' ,
'111/03/16' ,
'111/03/17' ,
'111/03/18' ,
'111/03/21' ,
'111/03/22' ,
'111/03/23' ,
'111/03/24' ,
'111/03/25' ,
'111/03/28' ,
'111/03/29' ,
'111/03/30' ,
'111/03/31' ,
'111/04/01' ,
'111/04/06' ,
'111/04/07' ,
'111/04/08' ,
'111/04/11' ,
'111/04/12' ,
'111/04/13' ,
'111/04/14' ,
'111/04/15' ,
'111/04/18' ,
'111/04/19' ,
'111/04/20' ,
'111/04/21' ,
'111/04/22' ,
'111/04/25' ,
'111/04/26' ,
'111/04/27' ,
'111/04/28' ,
'111/04/29' ,
'111/05/03' ,
'111/05/04' ,
'111/05/05' ,
'111/05/06' ,
'111/05/09' ,
'111/05/10' ,
'111/05/11' ,
'111/05/12' ,
'111/05/13' ,
'111/05/16' ,
'111/05/17' ,
'111/05/18' ,
'111/05/19' ,
'111/05/20' ,
'111/05/23' ,
'111/05/24' ,
'111/05/25' ,
'111/05/26' ,
'111/05/27' ,
'111/05/30' ,
'111/05/31' ,
'111/06/01' ,
'111/06/02' ,
'111/06/06' ,
'111/06/07' ,
'111/06/08' ,
'111/06/09' ,
'111/06/10' ,
'111/06/13' ,
'111/06/14' ,
'111/06/15' ,
'111/06/16' ,
'111/06/17' ,
'111/06/20' ,
'111/06/21' ,
'111/06/22' ,
'111/06/23' ,
'111/06/24' ,
'111/06/27' ,
'111/06/28' ,
'111/06/29' ,
'111/06/30' ,
'111/07/01' ,
'111/07/04' ,
'111/07/05' ,
'111/07/06' ,
'111/07/07' ,
'111/07/08' ,
'111/07/11' ,
'111/07/12' ,
'111/07/13' ,
'111/07/14' ,
'111/07/15' ,
'111/07/18' ,
'111/07/19' ,
'111/07/20' ,
'111/07/21' ,
'111/07/22' ,
'111/07/25' ,
'111/07/26' ,
'111/07/27' ,
'111/07/28' ,
'111/07/29' ,
'111/08/01' ,
'111/08/02' ,
'111/08/03' ,
'111/08/04' ,
'111/08/05' ,
'111/08/08' ,
'111/08/09' ,
'111/08/10' ,
'111/08/11' ,
'111/08/12' ,
'111/08/15' ,
'111/08/16' ,
'111/08/17' ,
'111/08/18' ,
'111/08/19' ,
'111/08/22' ,
'111/08/23' ,
'111/08/24' ,
'111/08/25' ,
'111/08/26' ,
'111/08/29' ,
'111/08/30' ,
'111/08/31' ,
'111/09/01' ,
'111/09/02' ,
'111/09/05' , 
'111/09/06' , 
'111/09/07' , 
'111/09/08'
]

#current_date = "2019/09/03"
date_list = [ 
"2022/09/01",
"2022/08/01",
"2022/07/01",
"2022/06/01",
"2022/05/01",
"2022/04/01",
"2022/03/01",
"2022/02/01",
"2022/01/01",
"2021/12/01",
"2021/11/01",
"2021/10/01",
"2021/09/01",
"2021/08/01",
"2021/07/01"
            ]


def get_current_date():
    from datetime import datetime

    now = datetime.now()

    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")    
    
    return str(int(year)-1911) , str(month) , str(day)


def Get_Pig_Strong(stocknumber , current_date):
    #print("# stocknumber : " + stocknumber + " - " + current_date + " #")
    #year , month , day= get_current_date()
    current_date_list = current_date.split("/")

    year = str(int(current_date_list[0]) - 1911)
    month = current_date_list[1]
    day = current_date_list[2]
    current_date = year + "/" + month + "/" + day
    
    timeout_count = 1

    while timeout_count > 0:
    
        try:
            url ="https://stock.wearn.com/cdata.asp?year=" + year + "&month=" + month + "&kind=" + stocknumber
            res = requests.get(url, timeout=120)


              
            soup = BeautifulSoup(res.text, 'html.parser')            
            #print(soup)
            #print(type(soup)) #<class 'bs4.BeautifulSoup'>
            div_tag = soup.find('div', {'class':'stockalllist'})
            #print(div_tag)  
            #print(type(div_tag)) # <class 'bs4.element.Tag'>
            
            soup2 = BeautifulSoup(str(div_tag), 'html.parser')
            #print(type(soup2)) # <class 'bs4.BeautifulSoup'>
            a_tags = soup2.find_all('table')
            #print(a_tags)  
            #print(type(a_tags)) # <class 'bs4.element.ResultSet'>
            
            soup3 = BeautifulSoup(str(a_tags), 'html.parser')
            #print(type(soup3)) # <class 'bs4.BeautifulSoup'>
            div_tag = soup.find_all('tr', {'class':["stockalllistbg1" , "stockalllistbg2"]})
            #print(div_tag)  
            #print(type(div_tag)) # <class 'bs4.element.ResultSet'>
            
            temp_dict = {}
            for i in div_tag:
                #print("-"*50)
                #print(i)
                #print(type(i))
                #print(i.text)
                #print(type(i.text))
                #for j in i:
                #    print("j = " + str(j))
                
                data_dict = {}
                
                soup4 = BeautifulSoup(str(i), 'html.parser')
                #print(soup4)
                today = soup4.find_all('td' , {'class' : ["center" , "table-first-child"]})
                #print(today)
                today = today[0].text
                #print(today)
                div_tag2 = soup4.find_all('td' , {'align' : ["center" , "right"]})
                #print(div_tag2)  
                
                
                
                
                data_dict["open"] = div_tag2[0].text.replace("\xa0","")
                #print(data_dict["open"])
                data_dict["high"] = div_tag2[1].text.replace("\xa0","")
                #print(data_dict["high"])
                data_dict["low"] = div_tag2[2].text.replace("\xa0","")
                #print(data_dict["low"])
                data_dict["close"] = div_tag2[3].text.replace("\xa0","")
                #print(data_dict["close"])
                data_dict["volume"] = div_tag2[4].text.replace("\xa0","")

                
                
                
                #print(data_dict["volume"])
                
                
                #print(today)
                #print(data_dict)
                temp_dict[today] = data_dict
                #print(temp_dict)
                #print("-"*50)
            
            #print(temp_dict)
            #return [ current_date , stocknumber , temp_dict[current_date]["open"] , temp_dict[current_date]["high"] , temp_dict[current_date]["low"] , temp_dict[current_date]["close"] , temp_dict[current_date]["volume"]] 
            return temp_dict
            
        except Exception as e:
            #print(e)
            return [ current_date , stocknumber , 0 , 0 , 0 , 0 , 0]  
            #return_list = [ stocknumber , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] 
            #return return_list
            
        timeout_count-=1

def Get_Stock_Number_List(file_name):
    lines = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            number = str(line)[:-1]
            lines.append(number)
    return lines
    
#stocklist = ["1101"]
stocklist = Get_Stock_Number_List("stocknumber - full.txt")        

dict_result = {}

def Output_Stock_Data_a(output_file , result):
    # First way : Write to CSV File 
    # newline='' => There is a new line character will be added , use this parameter to skip 
    # encoding = 'utf_8_sig' => Use 'utf_8_sig' code to write .csv file , it can avoid the unexpected character
    # Reference : https://www.zhihu.com/question/34201726
    with open(output_file, 'a+' , newline='' , encoding = 'utf_8_sig') as myfile:
        wr = csv.writer(myfile)
        
        #for i in buy_result:
        wr.writerows(result)

def read_stock_data(file_dir):
    try:
        ret = {}
        try:
            with open(file_dir, newline='') as csvfile:
                rows = csv.reader(csvfile)
                #print(rows)
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
        except:
            with open(file_dir, newline='',encoding="utf8") as csvfile:
                rows = csv.reader(csvfile)
                #print(rows)
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
        #print(err)
        return None
        
for item in range(len(stocklist)):  

    try:
        stocknumber = stocklist[item]
        print("#### {} ".format(stocknumber))
        output_file_dir = "everyday/All/"+stocknumber + ".csv"
        
        try:
            stock_data = read_stock_data(output_file_dir)
            if stock_data == None:
                stock_data = {}
        except:
            stock_data = {}
            
        for current_date in date_list:
            result = []
            
            if not os.path.isfile(output_file_dir):
                result.append(["日期","開盤價","最高價","最低價","收盤價","成交量"])

            test = Get_Pig_Strong(stocknumber , current_date)
            dict_result.update(test)



        for current_date in excel_date_list:
            for key,value in dict_result.items():
                #print("{} : {}".format(key,value))
                if current_date == key:
                
                    #print("{} : {}".format(key,value))
                    result.append([key,value["open"],value["high"],value["low"],value["close"],value["volume"]])
        
        if key not in stock_data:
            Output_Stock_Data_a(output_file_dir , result)
        
    except Exception as err:
        print(err)
    
