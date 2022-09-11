from bs4 import BeautifulSoup
import requests
import csv
import os 
import time 
#from WebCrawler_APIs import *

excel_date_list = [
'111/09/06' ,
'111/09/07' ,
'111/09/08' ,
'111/09/09'
]

#current_date = "2019/09/03"
date_list = [ 
"2022/09/01",
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

        
stocklist = ["2317"]
#stocklist = Get_Stock_Number_List("stocknumber - full.txt")        

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
        
for item in range(len(stocklist)):  

    try:
        stocknumber = stocklist[item]
        print("#### {} ".format(stocknumber))
        output_file_dir = "everyday/All/"+stocknumber + ".csv"
        
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
        
        Output_Stock_Data_a(output_file_dir , result)
        
    except Exception as err:
        print(err)
    
