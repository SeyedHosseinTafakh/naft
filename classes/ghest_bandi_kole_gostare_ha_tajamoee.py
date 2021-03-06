from DB import *
import os
import werkzeug
from flask import Flask , jsonify
from flask_restful import Api, Resource, reqparse
import pandas
import json
from timeFunctions import *
from dateutil.relativedelta import *
from datetime import timedelta
from khayyam import JalaliDate


class ghest_bandi_kole_gostare_ha_tajamoee(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('time',required=True)
        args = parser.parse_args()
        retSum = {}
        n = 1
        while n < 11:
            mycursor.execute("select * from gostare where id = %s ",(n,))
            gostare_data = mycursor.fetchall()
            mydb.commit()
            query = "select * from gostare_pishraft where gostare_id = %s and malg =1"
            values = (n ,)
            mycursor.execute(query , values)
            gostare_pishrafts = mycursor.fetchall()
            df = self.opencsv()
            column = df.loc[0:29 , str(gostare_data[0][0])]
            ret = {}
            i = 0
            for gostare_pishraft in gostare_pishrafts:
                ret[gostare_pishraft[5]] = {}

                d = gostare_pishraft[3].split('-')
                time = JalaliDate(d[0], d[1], d[2])
                month = int(d[1])
                while i < 29:
                    if month > 12 :
                        month = 1
                        d[0] = str(int(d[0])+1)
                    column[i]= column[i].replace(',', '')
                    ret[gostare_pishraft[5]][i] = [
                        float(gostare_pishraft[2])/float(gostare_data[0][2]) * float(column[i]),
                        str(JalaliDate(d[0], str(month) , d[2]))
                    ]
                    i +=1
                    month +=1

                i = 0
            dataFrame = self.makeDataFrame(ret)
            # print (dataFrame)

            dataFrame= self.searchInDataframeToTop(dataFrame,args['time']+"-17")

            sum = self.sumTheDataframe(dataFrame)
            n +=1
            # print (sum)
            retSum[gostare_data[0][1]] = sum
        return retSum


    def opencsv(self):
        model_mali_csv = pandas.read_csv('model_mali2.csv')

        df = pandas.DataFrame(model_mali_csv)
        return df

    def makeDataFrame(self , inputs):
        i = 0
        n = 0
        time = []
        columns = []
        init = []
        data_fin = {}
        for input in inputs:

            data_fin[input] = []
            while i < 29:
                full_time = inputs[input][i][1]
                year_and_month = full_time.split('-')

                if year_and_month[0]+"-"+year_and_month[1] not in time:
                    full_time = inputs[input][i][1]
                    year_and_month = full_time.split('-')
                    time.append(year_and_month[0]+"-"+year_and_month[1])
                init.append(inputs[input][i][0])
                data_fin[input].append(inputs[input][i][0])
                i += 1
            columns.append(str(input))
            i = 0
            # if n == 0:
            #     n = 1
        # print(data_fin)
        # print (time)
        #///////////////
        for input in inputs:
            i = len(data_fin[input])
            full_time = inputs[input][0][1]
            year_and_month = full_time.split('-')

            x = time.index(year_and_month[0]+"-"+year_and_month[1])
            # x = time.index(inputs[input][0][1])
            print (x)
            while n < x:
                data_fin[input].insert(0,0)
                n +=1
            n = 0
            full_time = inputs[input][28][1]
            year_and_month = full_time.split('-')

            x = time.index(year_and_month[0]+"-"+year_and_month[1])
            # x = time.index(inputs[input][28][1])
            x = abs(x - (len(time)-1))
            print(x)
            while n <x:
                data_fin[input].append(0)
                n += 1
            n = 0
        dataframe_init = pandas.DataFrame(index=time , data = data_fin,columns=columns)
        # print (dataframe_init)
        return dataframe_init

    def searchInDataframeToButtom(self,df , index):
        df = df.loc[str(index):]
        return df
    def searchInDataframeToTop(self,df , index):
        df = df.loc[:str(index)]
        return df
    def sumTheDataframe(self,df):

        sum = 0
        for index , data in df.iterrows():
            # print (data)
            for d in data:
                sum += d
        # print(sum)
        return sum