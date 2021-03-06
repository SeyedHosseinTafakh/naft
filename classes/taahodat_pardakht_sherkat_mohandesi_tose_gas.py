from DB import *
import os
import werkzeug
from flask import Flask , jsonify
from flask_restful import Api, Resource, reqparse
import secrets

class taahodat_pardakht_sherkat_mohandesi_tose_gas(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_ghest',required = True)
        args = parser.parse_args()
        mycursor.execute("select * from taahodat_pardakht_sherkat_mohandesi_tose_gas where id_ghest =%s",(args['id_ghest'],))
        data = mycursor.fetchall()
        return data
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tarikh')
        parser.add_argument('sharh')
        parser.add_argument('mablagh_dollar')
        parser.add_argument('tozihat')
        parser.add_argument('id_ghest',required=True)
        parser.add_argument("file_peyvast", type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        file = args['file_peyvast']
        if file:
            dirname = secrets.dirname
            file.save(os.path.join(dirname, 'files', file.filename))
            fileName = file.filename
        else:
            fileName = None
        sql = "INSERT INTO taahodat_pardakht_sherkat_mohandesi_tose_gas (tarikh , sharh,mablagh_dollari,tozihat,file_peyvast,id_ghest) VALUES (%s,%s,%s,%s,%s,%s)"
        values = (args['tarikh'] , args['sharh'] , args['mablagh_dollar'] , args['tozihat'] , fileName,args['id_ghest'])
        mycursor.execute(sql,values)
        mydb.commit()
        return True

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',required=True)
        args = parser.parse_args()
        mycursor.execute("delete from taahodat_pardakht_sherkat_mohandesi_tose_gas where id = "+args['id'])
        mydb.commit()
        return True

