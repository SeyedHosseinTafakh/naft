import os
import werkzeug
from flask import Flask , jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from timeFunctions import *
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
import DB as db
import mysql.connector
import json

class gostare(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_gostare')
        args = parser.parse_args()
        if args['id_gostare']:
            db.mycursor.execute("SELECT * FROM gostare_pishraft WHERE gostare_id =%s ",(args['id_gostare'],))
            pihraft_with_id = db.mycursor.fetchall()
            return pihraft_with_id
        db.mycursor.execute("""SELECT * FROM gostare""")
        gostare = db.mycursor.fetchall()
        db.mycursor.execute("""SELECT * FROM gostare_pishraft""")
        pishraft = db.mycursor.fetchall()
        res= {}
        res["gostareha"] = gostare
        res["pishraft"] = pishraft
        mydb.commit()
        return res


    def post(selfs):
        parser = reqparse.RequestParser()
        parser.add_argument('tarikh')
        parser.add_argument('darsade_bardari')
        parser.add_argument('id_gostare')
        parser.add_argument('id_ghest')
        parser.add_argument('tozihat')
        parser.add_argument('malg')
        args = parser.parse_args()
        #if args['mahe_khali'] and args['id_gostare']:
            #values =  ( float(args['id_gostare']) ,0 ,args['mahe_khali'] ,)
            ## print(values)
            #db.mycursor.execute("INSERT INTO gostare_pishraft(gostare_id , darsad , tarikh) values (%s , %s , %s)", values)
            #db.mydb.commit()
            #return True
        if args['darsade_bardari'] and args['tarikh'] and args['id_gostare']:
            values = (args['id_gostare'],args['darsade_bardari'] , args['tarikh'] ,args['id_ghest'] , args['tozihat'], args['malg'])
            # print(values)
            db.mycursor.execute("INSERT INTO gostare_pishraft(gostare_id , darsad , tarikh , id_ghest , tozihat,malg) values (%s , %s , %s , %s ,%s,%s)", values)
            db.mydb.commit()
            return True
        return False

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_pishraft')
        args = parser.parse_args()
        # if args['id_gostare']:
        #     db.mycursor.execute("DELETE FROM gostare WHERE id = %s" , (args['id_gostare'] ,))
        #     db.mycursor.execute("DELETE FROM gostare_pishraft WHERE gostare_id = %s",(args['id_gostare'],))
        #     db.mydb.commit()
        #     return "gostare deleted"
        if args['id_pishraft']:
            db.mycursor.execute("DELETE FROM gostare_pishraft where id = %s" , (args['id_pishraft'],))
            db.mydb.commit()
            return "pishraft deleted"
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('darsad')
        args = parser.parse_args()
        db.mycursor.execute("UPDATE gostare_pishraft SET darsad = %s WHERE id = %s " , (args['darsad'], args['id'],))
        db.mydb.commit()
        return "salam"
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',required=True)
        parser.add_argument('malg',required=True)
        args = parser.parse_args()
        db.mycursor.execute('UPDATE gostare_pishraft SET malg = %s where id = %s' , (args['malg'] , args['id']))
        db.mydb.commit()
        return True

class peymankaran(Resource):
    def get(self):
        db.mycursor.execute("SELECT * FROM peymankaran")
        ret = db.mycursor.fetchall()
        return ret;
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('check_id')
        parser.add_argument('money')
        parser.add_argument('tarikh')
        parser.add_argument('tozih')
        parser.add_argument('name')

        args = parser.parse_args()
        db.mycursor.execute("INSERT INTO peymankaran (peymankar_name,check_id , check_money , tarikh , tozihat) VALUES (%s,%s , %s ,%s , %s)" , (args['name'],args['check_id'],args['money'],args['tarikh'] , args['tozih'] , ))
        db.mydb.commit()
        return True
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        db.mycursor.execute("DELETE FROM peymankaran WHERE id = %s " , (args['id'],))
        db.mydb.commit()
        return "delete"

class arazi(Resource):
    def get(self):
        db.mycursor.execute("SELECT * FROM arazi")
        ret = db.mycursor.fetchall()
        return ret
    def post(self):
        #//TODO: have to add peyvast FIles
        parser = reqparse.RequestParser()
        parser.add_argument("sharh")
        parser.add_argument("mablaghe_darkhasti_naftanir")
        parser.add_argument("mablaghe_hoghooghi")
        parser.add_argument("tarikh_hoghooghi")
        parser.add_argument("mablaghe_taeed_mali")
        parser.add_argument("tarikh_taeed_omoor_mali")
        parser.add_argument("stateDate")
        parser.add_argument("peyvast",type=werkzeug.datastructures.FileStorage,location = 'files')
        args = parser.parse_args()
        file = args['peyvast']
        if file:
            dirname = os.path.dirname(__file__)
            file.save(os.path.join(dirname,'files',file.filename))
            fileName = file.filename
        else:
            fileName = None
        sql = "INSERT INTO arazi (sharh , mablaghe_darkhasti_naftanir , mablaghe_hoghooghi,tarikh_hoghooghi ,mablaghe_taeed_mali ,tarikh_taeed_omoor_mali ,tarikh , peyvast) VALUES (%s , %s , %s, %s,%s,%s,%s,%s)"
        values = (args['sharh'] , args['mablaghe_darkhasti_naftanir'] , args['mablaghe_hoghooghi'] ,args['tarikh_hoghooghi'],args['mablaghe_taeed_mali'],args['tarikh_taeed_omoor_mali'],args['stateDate'],fileName)
        db.mycursor.execute(sql , values)
        db.mydb.commit()
        return True
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        args = parser.parse_args()
        db.mycursor.execute("DELETE FROM arazi WHERE id = %s " , (args['id'],))
        db.mydb.commit()
        return "delete"

    
class pipeLinesF(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tarikh')
        parser.add_argument('zekhamat')
        parser.add_argument('metraj')
        parser.add_argument('tonaj')
        parser.add_argument('tarikhTahvil')
        parser.add_argument('typeKalaTahvili')
        parser.add_argument('shomareHavaleAnbar')
        parser.add_argument('shomareTaghaza')
        parser.add_argument('shomareGhalam')
        parser.add_argument('nerkhBank')
        parser.add_argument('hazineAnbar')
        parser.add_argument('hazineSodoorBime')
        parser.add_argument('hazineBime')
        parser.add_argument('Inch36')
        parser.add_argument('tarikh')
        parser.add_argument('adam_ghatiyat')
        args = parser.parse_args()
        # mysql = "INSERT INTO pipelinesf (tarikh ,zekhamat , metraj , tonaj , tarikhTahvil,typeKalaTahvil ,shomareHavaleAnbar , shomareTaghaza,shomareGhalam ,nerkhTashilBankMarkazi ,hazineAnbar , hazineSodoor, hazineBime , mablagheVaragh , avarezGomrok , hazineSakhteLoole , hazinePooshesh , maliatVaragh, maliatSakht )"
        mysql = "INSERT INTO pipelinesf (" \
                "zekhamat , " \
                "metraj , " \
                "tonaj , " \
                "tarikhTahvil," \
                "typeKalaTahvili ," \
                "shomareHavaleAnbar , " \
                "shomareTaghaza," \
                "shomareGhalam ," \
                "nerkhTashilBankMarkazi ," \
                "hazineAnbar , " \
                "hazineSodoorBime , se , tarikh , adam_ghatiyat) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s ,%s ,%s)"
        values = (
                  args['zekhamat'],
                  args['metraj'],
                  args['tonaj'],
                  args['tarikhTahvil'],
                  args['typeKalaTahvili'],
                  args['shomareHavaleAnbar'],
                  args['shomareTaghaza'],
                  args['shomareGhalam'],
                  args['nerkhBank'],
                  args['hazineAnbar'],
                  args['hazineSodoorBime'],
                  args['Inch36'],args['tarikh'],args['adam_ghatiyat'])
        db.mycursor.execute(mysql ,values)
        db.mydb.commit()
        return True
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("inch36")
        args = parser.parse_args()
        if args['inch36']:
            db.mycursor.execute("SELECT * FROM pipelinesf WHERE se IS NOT NULL ")
        else:
            db.mycursor.execute("SELECT * FROM pipelinesf WHERE se IS NULL")
        data = db.mycursor.fetchall()
        ret = {}
        i = 0
        for record in data:
            mablaghe_varagh = float(record[3])*1033
            avarez_gomrok = mablaghe_varagh * float(record[9]) * 4/100
            # maliyat_bar_arzesh_afzoode_varagh = avarez_gomrok * 1/10
            hazine_sakht_loole = 0
            if record[5] == "ورق" :
                hazine_sakht_loole = 0
                hazine_pooshesh = 0
            else :
                hazine_sakht_loole = float(record[3]) * 125
                hazine_pooshesh = 0
            if record[5] == "پوشش داده شده":
                hazine_sakht_loole = float(record[3])*95
                hazine_pooshesh = float(record[3]) * 125
            maliyat_bar_arzesh_afzoode_sakht_pooshesh = (hazine_sakht_loole + hazine_pooshesh) *  float(record[9]) * 10/100
            # maliyat_bar_arzesh_afzoode_varagh = ((mablaghe_varagh * float(record[9])) + float(record[10]) + float(record[11]) + avarez_gomrok) * 1 / 10
            # maliyat_bar_arzesh_afzoode_varagh = ((mablaghe_varagh * float(record[9])) + float(record[10]) + avarez_gomrok ) * 0.1
            # maliyat_bar_arzesh_afzoode_varagh = mablaghe_varagh * float(record[9]) * (1.04) *(1/10)
            maliyat_bar_arzesh_afzoode_varagh = ((mablaghe_varagh * float(record[9])) + float(record[11]) + avarez_gomrok + float(record[10]) ) *(1/10)
            motalebate_riyali = float(record[10]) + float(record[11]) + avarez_gomrok + maliyat_bar_arzesh_afzoode_varagh + maliyat_bar_arzesh_afzoode_sakht_pooshesh
            motalebat_arzi = hazine_pooshesh + hazine_sakht_loole

            ret[i] ={'dataBase' : record ,
                             'mablaghe_varagh':mablaghe_varagh,
                             'avarez_gomrok':avarez_gomrok,
                             'maliyat_bar_arzesh_varagh':maliyat_bar_arzesh_afzoode_varagh,
                             'hazine_sakhte_loole':hazine_sakht_loole,
                             'hazine_pooshesh':hazine_pooshesh,
                             'maliyat_bara_arzesh_afzoode_sakhte_pooshesh':maliyat_bar_arzesh_afzoode_sakht_pooshesh,
                             'motalebat_riyali':motalebate_riyali,
                             'motalebat_arzi':motalebat_arzi,
                    'arzi_sakht_va_pooshesh':hazine_pooshesh + hazine_sakht_loole}
            i = i+ 1
        db.mydb.commit()
        return ret

    def get2(self,ghatiyat , s_inch = 'NULL'):
        if ghatiyat=="true":
            db.mycursor.execute("SELECT * FROM pipelinesf WHERE se is NULL and adam_ghatiyat = %s AND se = %s",('before',s_inch,))
            data =  db.mycursor.fetchall()
        else :
            db.mycursor.execute("SELECT * FROM pipelinesf WHERE se is NULL and adam_ghatiyat = %s",('after',))
            data = db.mycursor.fetchall()
        ret = {}
        i = 0
        for record in data:
            mablaghe_varagh = float(record[3])*1033
            avarez_gomrok = mablaghe_varagh * float(record[9]) * 4/100
            # maliyat_bar_arzesh_afzoode_varagh = avarez_gomrok * 1/10
            hazine_sakht_loole = 0
            if record[5] == "ورق" :
                hazine_sakht_loole = 0
                hazine_pooshesh = 0
            else :
                hazine_sakht_loole = float(record[3]) * 125
                hazine_pooshesh = 0
            if record[5] == "پوشش داده شده":
                hazine_sakht_loole = float(record[3])*95
                hazine_pooshesh = float(record[3]) * 125
            maliyat_bar_arzesh_afzoode_sakht_pooshesh = (hazine_sakht_loole + hazine_pooshesh) *  float(record[9]) * 10/100
            maliyat_bar_arzesh_afzoode_varagh = ((mablaghe_varagh * float(record[9])) + float(record[11]) + avarez_gomrok + float(record[10]) ) *(1/10)
            motalebate_riyali = float(record[10]) + float(record[11]) + avarez_gomrok + maliyat_bar_arzesh_afzoode_varagh + maliyat_bar_arzesh_afzoode_sakht_pooshesh
            motalebat_arzi = hazine_pooshesh + hazine_sakht_loole

            ret[i] ={'dataBase' : record ,
                             'mablaghe_varagh':mablaghe_varagh,
                             'avarez_gomrok':avarez_gomrok,
                             'maliyat_bar_arzesh_varagh':maliyat_bar_arzesh_afzoode_varagh,
                             'hazine_sakhte_loole':hazine_sakht_loole,
                             'hazine_pooshesh':hazine_pooshesh,
                             'maliyat_bara_arzesh_afzoode_sakhte_pooshesh':maliyat_bar_arzesh_afzoode_sakht_pooshesh,
                             'motalebat_riyali':motalebate_riyali,
                             'motalebat_arzi':motalebat_arzi,
                    'tarikh':record[4]}
            i = i+ 1
        return ret

    def get36inch(self,ghatiyat ):
        if ghatiyat=="true":
            # db.mycursor.execute("SELECT * FROM pipelinesf WHERE se IS NULL and adam_ghatiyat = %s",('before',))
            db.mycursor.execute("SELECT * FROM pipelinesf WHERE se is NOT NULL and adam_ghatiyat = %s ",('before',))
            data =  db.mycursor.fetchall()
            db.mydb.commit()
        else :
            db.mycursor.execute("SELECT * FROM pipelinesf WHERE se is NOT NULL AND adam_ghatiyat = %s",('after',))
            data = db.mycursor.fetchall()
            db.mydb.commit()
        ret = {}
        i = 0
        for record in data:
            mablaghe_varagh = float(record[3])*1033
            avarez_gomrok = mablaghe_varagh * float(record[9]) * 4/100
            # maliyat_bar_arzesh_afzoode_varagh = avarez_gomrok * 1/10
            hazine_sakht_loole = 0
            if record[5] == "ورق" :
                hazine_sakht_loole = 0
                hazine_pooshesh = 0
            else :
                hazine_sakht_loole = float(record[3]) * 125
                hazine_pooshesh = 0
            if record[5] == "پوشش داده شده":
                hazine_sakht_loole = float(record[3])*95
                hazine_pooshesh = float(record[3]) * 125
            maliyat_bar_arzesh_afzoode_sakht_pooshesh = (hazine_sakht_loole + hazine_pooshesh) *  float(record[9]) * 10/100
            maliyat_bar_arzesh_afzoode_varagh = ((mablaghe_varagh * float(record[9])) + float(record[10]) + float(record[11]) + avarez_gomrok) * 1 / 10
            motalebate_riyali = float(record[10]) + float(record[11]) + avarez_gomrok + maliyat_bar_arzesh_afzoode_varagh + maliyat_bar_arzesh_afzoode_sakht_pooshesh
            motalebat_arzi = hazine_pooshesh + hazine_sakht_loole

            ret[i] ={'dataBase' : record ,
                             'mablaghe_varagh':mablaghe_varagh,
                             'avarez_gomrok':avarez_gomrok,
                             'maliyat_bar_arzesh_varagh':maliyat_bar_arzesh_afzoode_varagh,
                             'hazine_sakhte_loole':hazine_sakht_loole,
                             'hazine_pooshesh':hazine_pooshesh,
                             'maliyat_bara_arzesh_afzoode_sakhte_pooshesh':maliyat_bar_arzesh_afzoode_sakht_pooshesh,
                             'motalebat_riyali':motalebate_riyali,
                             'motalebat_arzi':motalebat_arzi,
                    'tarikh':record[4]}
            i = i+ 1
        return ret

class pardakht_naftanir(Resource):
    def get(self):
        ret = {}
        db.mycursor.execute("SELECT * FROM pardakht_naftanir WHERE softDelete is NULL ")
        ready = db.mycursor.fetchall()
        db.mycursor.execute("SELECT * FROM pardakht_naftanir WHERE softDelete is NOT NULL ")
        softDeletes = db.mycursor.fetchall()
        ret['softDeletes'] = softDeletes
        ret['ready'] = ready
        return ret

    def post(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument("peyvast",type=werkzeug.datastructures.FileStorage)
        parser = reqparse.RequestParser()
        parser.add_argument("date")
        parser.add_argument("sharh")
        parser.add_argument("dollar")
        parser.add_argument("riyal")
        parser.add_argument("tozihat")
        parser.add_argument("peyvast",type=werkzeug.datastructures.FileStorage,location = 'files')
        args = parser.parse_args()
        file = args['peyvast']
        dirname = os.path.dirname(__file__)
        file.save(os.path.join(dirname,'files',file.filename))
        db.mycursor.execute("INSERT INTO pardakht_naftanir ( tarikh ,sharh , dollar , riyal, peyvast_address , tozihat ) VALUES (%s,%s,%s,%s,%s,%s)" ,
                            (args['date'],args['sharh'] , args['dollar'] , args['riyal'] , file.filename ,args['tozihat'], ))
        db.mydb.commit()

        return True
    #TODO: add update and delete
    #def delete(self):
        #parser = 

class pardakht_tose_gas(Resource):
    def get(self):
        ret = {}
        db.mycursor.execute("SELECT * FROM pardakht_gas WHERE softDelete is NULL ")
        ready = db.mycursor.fetchall()
        db.mycursor.execute("SELECT * FROM pardakht_gas WHERE softDelete is NOT NULL ")
        softDeletes = db.mycursor.fetchall()
        ret['softDeletes'] = softDeletes
        ret['ready'] = ready
        return ret
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("peyvast",type=werkzeug.datastructures.FileStorage,location = 'files')
        parser.add_argument("date")
        parser.add_argument("sharh")
        parser.add_argument("dollar")
        parser.add_argument("riyal")
        parser.add_argument("tozihat")
        args = parser.parse_args()
        file = args['peyvast']
        dirname = os.path.dirname(__file__)
        file.save(os.path.join(dirname,'files',file.filename))
        db.mycursor.execute("INSERT INTO pardakht_gas ( tarikh ,sharh , dollar , riyal, peyvast_address , tozihat ) VALUES (%s,%s,%s,%s,%s,%s)" ,
                            (args['date'],args['sharh'] , args['dollar'] , args['riyal'] , file.filename ,args['tozihat'], ))
        db.mydb.commit()


class comper(Resource):
    def get(self):
        db.mycursor.execute("SELECT * FROM comper")
        data = db.mycursor.fetchall()
        ret = {}
        for record in data:
            ret[record[0]] = {'dataBase': record ,
                              'natayej_motalebat': (float(record[4]) * (float(record[5])/float(record[6])))}
        return ret
    def post(self):
        parser = reqparse.RequestParser()
        #//TODO:: have to add peyvast file 
        parser.add_argument("name")
        parser.add_argument("type")
        parser.add_argument("dollar")
        parser.add_argument("euro")
        parser.add_argument("nerkh_dollar")
        parser.add_argument("nerkh_euro")
        parser.add_argument("tarikh_shoroo_tahvil")
        parser.add_argument("tarikh_pardakht")
        parser.add_argument("tozihat")
        parser.add_argument("peyvast",type=werkzeug.datastructures.FileStorage,location = 'files')
        args = parser.parse_args()
        file = args['peyvast']
        if file:
            dirname = os.path.dirname(__file__)
            file.save(os.path.join(dirname, 'files', file.filename))
            fileName = file.filename
        else:
            fileName = None
        db.mycursor.execute('INSERT INTO comper (name , type , dollar , euro , nerkh_dollar , nerkh_euro , tarikh_shoroo_tahvil , tarikh_pardakht , tozihat,peyvast) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            (args['name'],args['type'],args['dollar'],args['euro'],args['nerkh_dollar'],args['nerkh_euro'],args['tarikh_shoroo_tahvil'],args['tarikh_pardakht'],args['tozihat'],fileName))
        db.mydb.commit()
        return True
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        args = parser.parse_args()
        db.mycursor.execute('DELETE FROM comper WHERE id = %s' , (args['id'],))
        db.mydb.commit()
        return True


#// taraz mali
class pardakht_shode_tavasote_naftanir(Resource):
    def get(self):
        db.mycursor.execute("SELECT * FROM pardakht_shode_tavasote_naftanir_tm ")
        ret = db.mycursor.fetchall()
        return ret
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("tarikh")
        parser.add_argument("mablagh")
        parser.add_argument("pardakht_shod_babate")
        parser.add_argument("shomare_sanad")
        parser.add_argument("tozihat")
        parser.add_argument("state")
        args = parser.parse_args()
        db.mycursor.execute("INSERT INTO pardakht_shode_tavasote_naftanir_tm (tarikh , mablagh , pardakht_shod_babate,shomare_sanad, tozihat , state) VALUES (%s,%s,%s,%s,%s,%s)",
                            (args['tarikh'] , args['mablagh'],args['pardakht_shod_babate'],args['shomare_sanad'],args['tozihat'],args['state']))
        db.mydb.commit()
        return True
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id")
        parser.add_argument("tarikh")
        args = parser.parse_args()
        if args['id'] and args['tarikh']:
            db.mycursor.execute("UPDATE pardakht_shode_tavasote_naftanir_tm SET softdelete = %s WHERE id = %s" , (args['id'] , args['tarikh'],))
            db.mydb.commit()
            return True
        if args['id']:
            db.mycursor.execute("DELETE FROM pardakht_shode_tavasote_naftanir_tm where id = %s" ,(args['id'],))
            db.mydb.commit()
            return True
        return False

class kala_30(Resource):
    def get(self):
        db.mycursor.execute("select * from kala_30_inch ")
        data = db.mycursor.fetchall()
        ret = {}
        # ret['miyangin']=(float(data[0][1])+float(data[0][2])+float(data[0][3])) / 3
        # ret['shandool']= "shandool"
        miyangin = {}
        # return data
        for record in data:
            ret['database_record'+str(record[0])] = float(record[1]),float(record[2]),float(record[3])
            ret['miyangin__'+str(record[0])] = (float(record[1]) + float(record[2]) + float(record[3])) / 3
            ret['maliayt__'+str(record[0])] = ((float(record[1]) + float(record[2]) + float(record[3])) / 3) * 1/10
        return ret
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('estelam1')
        parser.add_argument('estelam2')
        parser.add_argument('estelam3')
        args = parser.parse_args()
        db.mycursor.execute("INSERT INTO kala_30_inch (estelam_1 , estelam_2, estelam_3) VALUES (%s , %s ,%s )",
                            (args['estelam1'],args['estelam2'],args['estelam3'],))
        db.mydb.commit()
        return True

class sadid_mahshahr(Resource):
    def get(self):
        db.mycursor.execute("SELECT * FROM sadid_mahshahr")
        ret = db.mycursor.fetchall()
        return ret
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument("money")
        parse.add_argument("asl_dar_mohasebat")
        parse.add_argument("tarikh")
        parse.add_argument("jarime")
        args = parse.parse_args()
        db.mycursor.execute("INSERT INTO sadid_mahshahr(money , asl_dar_mohasebat , tarikh , jarime)  VALUES(%s , %s ,%s , %s) " , (args['money'] , args['asl_dar_mohasebat'],args['tarikh'],args['jarime'],))
        db.mydb.commit()
        return True
from operator import itemgetter
import operator
class jadval56(Resource):
    def get(self):
        # sql = "SELECT * FROM pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate =  %s AND state = %s"
        # values = ('پیمانکاران', 'after')
        db.mycursor.execute("select * from pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate = %s" ,("لوله",))
        naftanir = db.mycursor.fetchall()
        db.mycursor.execute("SELECT * FROM pipelinesf")
        p56 = db.mycursor.fetchall()
        merger ={}
        i = 0
        for record in p56:
            mablaghe_varagh = float(record[3]) * 1033
            avarez_gomrok = mablaghe_varagh * float(record[9]) * 4 / 100
            hazine_sakht_loole = 0
            if record[5] == "ورق":
                hazine_sakht_loole = 0
                hazine_pooshesh = 0
            else:
                hazine_sakht_loole = float(record[3]) * 125
                hazine_pooshesh = 0
            if record[5] == "پوشش داده شده":
                hazine_sakht_loole = float(record[3]) * 95
                hazine_pooshesh = float(record[3]) * 125
            maliyat_bar_arzesh_afzoode_sakht_pooshesh = (hazine_sakht_loole + hazine_pooshesh) * float(
                record[9]) * 10 / 100
            maliyat_bar_arzesh_afzoode_varagh = ((mablaghe_varagh * float(record[9])) + float(record[10]) + float(
                record[11]) + avarez_gomrok) * 1 / 10
            motalebate_riyali = float(record[10]) + float(record[
                                                              11]) + avarez_gomrok + maliyat_bar_arzesh_afzoode_varagh + maliyat_bar_arzesh_afzoode_sakht_pooshesh
            motalebat_arzi = hazine_pooshesh + hazine_sakht_loole

            ret = {'dataBase': record,
                      'mablaghe_varagh': mablaghe_varagh,
                      'avarez_gomrok': avarez_gomrok,
                      'maliyat_bar_arzesh_varagh': maliyat_bar_arzesh_afzoode_varagh,
                      'hazine_sakhte_loole': hazine_sakht_loole,
                      'hazine_pooshesh': hazine_pooshesh,
                      'maliyat_bara_arzesh_afzoode_sakhte_pooshesh': maliyat_bar_arzesh_afzoode_sakht_pooshesh,
                      'motalebat_riyali': motalebate_riyali,
                      'motalebat_arzi': motalebat_arzi}

            d1 = moment.date(record[13]).strftime("%Y-%m-%d")
            d2 = moment.date("1350-1-1").strftime("%Y-%m-%d")
            d1 = moment.date(d1).locale("Asia/Tehran").date
            d2 = moment.date(d2).locale("Asia/Tehran").date
            ekh = d1 - d2
            ekh = str(ekh)
            ekh = ekh.split(' ')
            merger[i] = {
                'pool':ret['motalebat_riyali'],
                'tarikh': record[13],
                'ekhtelaf': int(ekh[0]),
                'sharh':"loole"
            }
            i = i+1
        for n in naftanir:
            d1 = moment.date(n[1]).strftime("%Y-%m-%d")
            d2 = moment.date("1350-1-1").strftime("%Y-%m-%d")
            d1 = moment.date(d1).locale("Asia/Tehran").date
            d2 = moment.date(d2).locale("Asia/Tehran").date
            ekh = d1 - d2
            ekh = str(ekh)
            ekh = ekh.split(' ')
            merger[i] = {
                'pool':n[2],
                'tarikh':n[1],
                'ekhtelaf': int(ekh[0]),
                'sharh':'naftanir'
            }
            i = i +1
        db.mycursor.execute("select * from jadval56")
        jadvals = db.mycursor.fetchall()
        for i in jadvals:
            db.mycursor.execute('delete from jadval56 where id =%s',(i[0],))
        db.mydb.commit()
        for i in merger:
            db.mycursor.execute("insert into jadval56 (pool , tarikh , ekhtelaf,sharh ) VALUES (%s , %s ,%s ,%s)" , (merger[i]['pool'],
                                                                                                                     merger[i]['tarikh'],
                                                                                                                     merger[i]['ekhtelaf'],
                                                                                                                     merger[i]['sharh']))
            db.mydb.commit()

        db.mycursor.execute("select * from jadval56")
        data = db.mycursor.fetchall()
        jadval = {}
        nerkh_jarime = 0.0180875824835107
        i = 0
        for n in data:
            if i == 0:
                jarime_dore_ghabl =0
                pardakht_nashode_dore_ghabl = 0
                kole_motalebat = 0
            else:
                pardakht_nashode_dore_ghabl = jadval[i-1]['jame_kole_motalebat']
                jarime_dore_ghabl = (pardakht_nashode_dore_ghabl * ( 1 + nerkh_jarime)**(ekhtelaf_date(jadval[i-1]['tarikh'],data[i][2]))) - pardakht_nashode_dore_ghabl
            if data[i][4] == 'naftanir':
                sharh = "پرداخت شده توسط نفتانیر"
                tarikh = data[i][2]
                pool = float(data[i][1]) * -1
            else:
                pool = abs(float(data[i][1]))
                sharh = data[i][4]
            jadval[i] = {
                'sharh':sharh,
                'tarikh':data[i][2],
                'pool':pool,
                'jarime':jarime_dore_ghabl,
                'jame_kole_motalebat': jarime_dore_ghabl + jarime_dore_ghabl + pool
            }
            i = i+1
        return jadval


class jadvalArazi(Resource):
    def get(self):
        # arz = arazi()
        # arz = arz.get()
        # arz = json.dumps(arz)
        # arz = json.loads(arz)
        jarazi = {}
        jarazi['0'] = {
            'sharh' : "مبلغ ریالی پرداخت شده",
            'tarikh' : '1394-12-27',
            'pardakht_shode_tavasote_naftanir': 85747896194,
            'taahod_be_pardakht': 0,
            'pardakht_nashode_dore_ghabl': 0,
            'jarime' : 0,
            'motalebat':-85747896194,
        }
        jarazi['1'] = {
            'sharh' : "مبالغ ریالی در تعهد",
            'tarikh' : '95-02-12',
            'pardakht_shode_tavasote_naftanir': 0,
            'taahod_be_pardakht': 85747896194,
            'pardakht_nashode_dore_ghabl': -85747896194,
            'jarime' : 0,
            'motalebat':0,
        }
        # nerkh_jarime = 1
        # i = 1
        # for id in arz:
        #     jarazi[i] ={}
        #     jarazi[i]['sharh'] = 'مبالغ ریالی در تعهد'
        #     jarazi[i]['tarikh'] = '1394-12-27'
        #     jarazi[i]['pardakht_shode_tavasote_naftanir'] = 0
        #     jarazi[i]['taahod_be_pardakht'] = arz[i-1][3]
        #     jarazi[i]['tarikh_taaid_hoghooghi'] = arz[i-1][4]
        #     taahod = arz[i-1][3]
            # taahod = arz[i-1][3]
            # jarazi[i]['kole_motalebat'] = int(taahod) - 85747896194
            # jarazi[i]['kole_motalebat'] = 0
            # jarazi[i]['jarime'] = 0
            # i = i+1
        return jarazi

class looleSaziSadid(Resource):
    def get(self):
        db.mycursor.execute('SELECT * FROM sadid_mahshahr ORDER BY ID DESC LIMIT 1')
        data = db.mycursor.fetchall()
        if not data:
            return None
        i = 0
        ret = {}
        nerkh = 0.0180875824835107
        while i <= 2:
            print(i)
            ret[i] = {}
            ret[i]['taahod_be_pardakht'] = float(data[0][1])/3
            if i ==0:
                ret[i]['pardakht_nashod_dore_ghabl'] = 0
                ret[i]['jarime'] = 0
                ret[i]['kole_motalebat'] = float(data[0][1])/3
                ret[i]['tarikh']='1394-12-27'
            if i == 1:
                ret[i]['pardakht_nashod_dore_ghabl'] = ret[i-1]['taahod_be_pardakht']
                ret[i]['jarime'] = (ret[i-1]['kole_motalebat'] *(1+nerkh)**(
                    khayam_type('1394-12-27','1395-01-27'))) -ret[i-1]['kole_motalebat']
                ret[i]['kole_motalebat'] = ret[i]['jarime'] + ret[i-1]['kole_motalebat']+(float(data[0][1])/3)
                ret[i]['tarikh'] = '1395-01-27'
            if i ==2:
                ret[i]['pardakht_nashod_dore_ghabl'] = ret[i-1]['taahod_be_pardakht']
                ret[i]['jarime'] = (ret[i-1]['kole_motalebat'] *(1+nerkh)**(
                    khayam_type('1395-01-27','1395-02-27'))) -ret[i-1]['kole_motalebat']
                ret[i]['kole_motalebat'] = ret[i]['jarime'] + ret[i - 1]['kole_motalebat'] + (float(data[0][1]) / 3)
                ret[i]['tarikh'] = '1395-02-27'
            i = i+1
        parser = reqparse.RequestParser()
        parser.add_argument('time_now')
        args = parser.parse_args()
        if args['time_now']:
            ret['end'] = {}
            ret['end']['jarime'] = (ret[2]['kole_motalebat'] * (1+nerkh)**khayam_type('1395-02-27' , args['time_now'])) -  float(ret[2]['kole_motalebat'])
            # ret['end']['jarime'] = (ret[2]['kole_motalebat'] * (1+nerkh)**khayam_type('1395-02-27' , '1396-9-27')) -  float(ret[2]['kole_motalebat'])
            ret['end']['kole_motalebat'] = ret[2]['kole_motalebat'] + ret['end']['jarime']
            ret['end']['taahod_be_pardakht'] = 0
            ret['end']['pardakht_nashod_dore_ghabl'] = ret[2]['kole_motalebat']
        return  ret


import moment
from datetime import datetime
def ekhtelaf_date(date1 , date2):
    d1 =moment.date(date1).strftime("%Y-%m-%d")
    d1 = moment.date(d1).locale("Asia/Tehran").date
    print(d1)
    d2 =moment.date(date2).strftime("%Y-%m-%d")
    d2 = moment.date(d2).locale("Asia/Tehran").date
    print(d2)
    sal = {}
    sal[1] = 31
    sal[2] = 31
    sal[3] = 31
    sal[4] = 31
    sal[5] = 31
    sal[6] = 31
    sal[7] = 30
    sal[8] = 30
    sal[9] = 30
    sal[10] = 30
    sal[11] = 30
    sal[11] = 30
    sal[12] = 29
    ekh = d1 - d2
    print(ekh)
    ekh = ekh.days
    date2 = date2.split('-')
    return float(int(ekh) / int(sal[int(date2[1])]))


def ekhtelaf_dateV2(date1 , date2):
    d1 =moment.date(date1).strftime("%Y-%m-%d")
    d1 = moment.date(d1).locale("Asia/Tehran").date
    # print(d1)
    d2 =moment.date(date2).strftime("%Y-%m-%d")
    d2 = moment.date(d2).locale("Asia/Tehran").date
    # print(d2)
    sal = {}
    sal[1] = 31
    sal[2] = 31
    sal[3] = 31
    sal[4] = 31
    sal[5] = 31
    sal[6] = 31
    sal[7] = 30
    sal[8] = 30
    sal[9] = 30
    sal[10] = 30
    sal[11] = 30
    sal[11] = 30
    sal[12] = 29
    rooz_aval = str(d1).split('-')
    mah_aval = rooz_aval[1]
    rooz_aval = int(str(rooz_aval[2]).split(' ')[0]) - sal[int(mah_aval)]
    # print(rooz_aval)
    rooz_dovom = str(d2).split('-')
    rooz_dovom = str(rooz_dovom[2]).split(' ')[0]
    # print (rooz_dovom)
    # print('finally')
    ekhtelaf_roozha = int(rooz_dovom) - int(rooz_aval-1)
    # print (ekhtelaf_roozha)
    # print( float(ekhtelaf_roozha / int(sal[int(date2[1])])))
    return float(ekhtelaf_roozha / int(sal[int(date2[1])]))

class jadvalPeymankaran(Resource):
    def get(self):
        ret = {}
        nerkh = 0.0180875824835107
        db.mycursor.execute("SELECT * FROM peymankaran")
        jadval_az_db = db.mycursor.fetchall()
        db.mydb.commit()
        i = 0
        sum_kole_peymankaran = 0
        while i < len(jadval_az_db):
            sum_kole_peymankaran = float(jadval_az_db[i][3]) + sum_kole_peymankaran
            i = i + 1

        jadval = list()
        # jadval[0] = []
        n = (
            'بدهی به توسعه گذار',
            'tozihat',
            '1394-12-27',
            str(sum_kole_peymankaran / 3)
        )
        n2 = (
            'بدهی به توسعه گذار',
            'tozihat',
            '1395-1-27',
            str(sum_kole_peymankaran / 3)
        )
        n3 = (
            'بدهی به توسعه گذار',
            'tozihat',
            '1395-2-27',
            str(sum_kole_peymankaran / 3)
        )
        jadval.append(n)
        jadval.append(n2)
        jadval.append(n3)
        sql = "SELECT * FROM pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate =  %s AND state = %s"
        values = ('پیمانکاران' , 'after')
        db.mycursor.execute(sql,values)
        jadval_naftanir = db.mycursor.fetchall()
        # return jadval_naftanir
        i = 0
        while i< len(jadval_naftanir):
            apending = [
                'پرداخت شده توسط نفتانیر',
                'no_check_id',
                jadval_naftanir[i][1],
                '-'+jadval_naftanir[i][2],
                # jadval_naftanir[i][5]
                ]
            i = i+1
            jadval.append(apending)
        # return jadval
        sql = "SELECT * FROM pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate =  %s AND state = %s"
        values = ('پیمانکاران', 'before')
        db.mycursor.execute(sql, values)
        dore_ghable_db = db.mycursor.fetchall()
        n = 0
        dore_ghable = 0
        while n < len(dore_ghable_db):
            dore_ghable = float(dore_ghable_db[n][2]) + float(dore_ghable)
            n = n + 1
        ret['dore_ghable'] = {
            'sharh': 'مبالغ ریالی پرداخت شده توسط نفتانیر تا تاریخ 94/12/27',
            'tarikh': '1394-12',
            'pool':abs(dore_ghable),
            'noe': 'پرداخت شده توسط نفتانیر',
            'pardakht_nashode_dore_ghable':0,
            'jarime':0,
            'kole_motalebat':abs(dore_ghable )* -1
        }
        i = 0
        # return jadval
        while i < len(jadval):
            ret[i]={}
            ret[i]['sharh'] = jadval[i][0]
            # ret[i]['noe'] = jadval[i][1]
            ret[i]['tozihat'] = 'telegram coming'
            ret[i]['tarikh'] = jadval[i][2]
            ret[i]['pool']=jadval[i][3]
            if i == 0:
                ret[i]['pardakht_nashode_dore_ghable'] = abs(dore_ghable )* -1
                ret[i]['jarime'] = 0
            else:
                ret[i]['pardakht_nashode_dore_ghable'] = ret[i-1]['kole_motalebat']
                ret[i]['jarime'] = (float(ret[i]['pardakht_nashode_dore_ghable']) * (1 + nerkh) ** (
                    abs(khayam_type(jadval[i-1][2], jadval[i][2])))) - float(
                    ret[i]['pardakht_nashode_dore_ghable'])
                print (float(ret[i]['pardakht_nashode_dore_ghable']))
                print (abs(khayam_type(jadval[i-1][2], jadval[i][2])))
                print ("\n")
            ret[i]['kole_motalebat'] = float(ret[i]['jarime']) + float(ret[i]['pardakht_nashode_dore_ghable']) + float(ret[i]['pool'])
            ret[i]['pool'] = abs(float(ret[i]['pool']))
            i = i+1
        return ret



class adam_ghateyat_peymankaran(Resource):
    def get(self):
        db.mycursor.execute('select * from naftanir_peymankaran_adam')
        data = db.mycursor.fetchall()
        return data
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tarikh')
        parser.add_argument('mablagh')
        parser.add_argument('pardakht_shod_babate')
        parser.add_argument('shomare_sanad')
        parser.add_argument('tozihat')
        args = parser.parse_args()
        db.mycursor.execute('insert into naftanir_peymankaran_adam (tarikh,mablagh,pardakht_shod_babate,shomare_sanad,tozihat)'
                            'values(%s,%s,%s,%s,%s)',(args['tarikh'],args['mablagh'],args['pardakht_shod_babate'],args['shomare_sanad'],args['tozihat']))
        db.mydb.commit()
        return True

class jadval562(Resource):
    def get(self):
        #HANDELING BEFORE IN PIPELINES
        p56_before = pipeLinesF().get2(ghatiyat="true")
        i = 0
        # return p56_before
        sum_of_adam_ghatiyat_p56 = 0
        while i < len(p56_before):
            sum_of_adam_ghatiyat_p56 = float(p56_before[i]['motalebat_riyali']) + sum_of_adam_ghatiyat_p56
            i = i+1
        # return sum_of_adam_ghatiyat_p56
        # sum_of_adam_ghatiyat_p56 = 834675673780
        db.mydb.commit()
        #end
        db.mycursor.execute("select * from pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate = %s and state = %s",('لوله های 56 اینچ' , 'before'))
        naftanir_pardakht_adam = db.mycursor.fetchall()
        db.mydb.commit()
        i = 0
        final_sum=0
        while i < len(naftanir_pardakht_adam):
            final_sum = float(naftanir_pardakht_adam[i][2]) + final_sum
            i = i +1
        data_b = {}
        data_b={
            'sharh': 'پرداختی شرکت توسعه گاز',
            'tarikh': '1394-11-19',
            'pool': final_sum,
            'kole_motalebat': abs(final_sum) * -1 ,
            'pardakht_nashode_dore_ghabl':0
        }
        data_b_p56={
            'sharh': 'تعهدات پرداخت بابت 56',
            'tarikh': '94/12/12',
            'pool': sum_of_adam_ghatiyat_p56,
            'pardakht_nashode_dore_ghabl':final_sum,
            'kole_motalebat': abs(abs(final_sum) - sum_of_adam_ghatiyat_p56)
        }

        p56 = pipeLinesF().get2(ghatiyat="false")
        db.mycursor.execute('select id from jadval56')
        idies = db.mycursor.fetchall()
        db.mydb.commit()
        i= 0
        values = []
        while i < len(idies):
            # values.append(idies[i][0])
            db.mycursor.execute('delete from jadval56 where id = '+str(idies[i][0]))
            i = i + 1
        db.mydb.commit()
        db.mycursor.execute(
            "select * from pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate = %s and state = %s",
            ('لوله های 56 اینچ', 'after'))
        data = db.mycursor.fetchall()
        db.mydb.commit()
        i = 0
        while i < len(data):
            db.mycursor.execute('INSERT INTO jadval56 (pool , tarikh , ekhtelaf , sharh) values (%s , %s , %s , %s)',
                                (data[i][2], data[i][1],int(khayyam_time_sort(data[i][1])) , "sharh"))

            db.mydb.commit()
            i = i+1
        db.mydb.commit()
        i = 0
        while i < len(p56):
            db.mycursor.execute('INSERT INTO jadval56 (pool , tarikh , ekhtelaf , sharh) values (%s , %s , %s , %s)',
                                (str(p56[i]['motalebat_riyali']),str(p56[i]['tarikh']) , int(khayyam_time_sort(p56[i]['tarikh'])) , str(p56[i]['dataBase'][5])))
            db.mydb.commit()
            i = i + 1
        db.mydb.commit()
        i = 0
        db.mycursor.execute("select * from jadval56 order by ekhtelaf")
        data = db.mycursor.fetchall()
        db.mydb.commit()
        ret ={}
        ret['befor'] = data_b
        ret['befor_p56'] = data_b_p56
        i = 0
        nerkh = 0.0180875824835107
        # return data
        while i <len(data):
            ret[i]={}
            ret[i]['pool'] = data[i][1]
            pool = data[i][1]
            if i == 0 :
                ret[i]['kole_motalebat'] = sum_of_adam_ghatiyat_p56 - data_b['pool']
                # return data[i][2]
                jarime = (data_b_p56['kole_motalebat'] * (1 + nerkh) ** khayam_type(data[i][2], '1394-12-12') -
                          data_b_p56['kole_motalebat'])
                pardakht_nashode_dore_ghabl = data_b['pool']
            else:
                pardakht_nashode_dore_ghabl =ret[i-1]['kole_motalebat']
                jarime = (pardakht_nashode_dore_ghabl * (1 + nerkh) ** khayam_type(data[i][2], data[i - 1][
                    2]) - pardakht_nashode_dore_ghabl)
                ret[i]['kole_motalebat'] = float(pardakht_nashode_dore_ghabl )+ float(pool) + float(jarime)
            #
            ret[i]['jarime'] = jarime
            ret[i]['tarikh'] = data[i][2]
            ret[i]['sharh'] = data[i][4]
            ret[i]['pardakht_nashode_dore_ghabl'] = pardakht_nashode_dore_ghabl
            print (i)
            i = i +1

        return ret

class jadval56dollar(Resource):
    def get(self):
        #HANDELING BEFORE IN PIPELINES
        p56_before = pipeLinesF().get2(ghatiyat="true")
        i = 0
        # return p56_before
        sum_of_adam_ghatiyat_p56 = 0
        while i < len(p56_before):
            sum_of_adam_ghatiyat_p56 = float(p56_before[i]['motalebat_arzi']) + sum_of_adam_ghatiyat_p56
            i = i+1
        # return sum_of_adam_ghatiyat_p56
        # sum_of_adam_ghatiyat_p56 = 834675673780
        db.mydb.commit()
        #end
        db.mycursor.execute("select * from pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate = %s and state = %s",('لوله های 56 اینچ' , 'before'))
        naftanir_pardakht_adam = db.mycursor.fetchall()
        db.mydb.commit()
        i = 0
        final_sum=0
        while i < len(naftanir_pardakht_adam):
            final_sum = float(naftanir_pardakht_adam[i][2]) + final_sum
            i = i +1
        data_b = {}
        data_b={
            'sharh': 'پرداختی شرکت توسعه گاز',
            'tarikh': '1394-11-19',
            'pool': final_sum,
            'kole_motalebat': abs(final_sum) * -1 ,
            'pardakht_nashode_dore_ghabl':0
        }
        data_b_p56={
            'sharh': 'تعهدات پرداخت بابت 56',
            'tarikh': '94/12/12',
            'pool': sum_of_adam_ghatiyat_p56,
            'pardakht_nashode_dore_ghabl':final_sum,
            'kole_motalebat': abs(abs(final_sum) - sum_of_adam_ghatiyat_p56)
        }

        p56 = pipeLinesF().get2(ghatiyat="false")
        db.mycursor.execute('select id from jadval56')
        idies = db.mycursor.fetchall()
        db.mydb.commit()
        i= 0
        values = []
        while i < len(idies):
            # values.append(idies[i][0])
            db.mycursor.execute('delete from jadval56 where id = '+str(idies[i][0]))
            i = i + 1
        db.mydb.commit()
        db.mycursor.execute(
            "select * from pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate = %s and state = %s",
            ('لوله های 56 اینچ', 'after'))
        data = db.mycursor.fetchall()
        db.mydb.commit()
        i = 0
        while i < len(data):
            db.mycursor.execute('INSERT INTO jadval56 (pool , tarikh , ekhtelaf , sharh) values (%s , %s , %s , %s)',
                                (data[i][2], data[i][1],int(khayyam_time_sort(data[i][1])) , "sharh"))

            db.mydb.commit()
            i = i+1
        db.mydb.commit()
        i = 0
        while i < len(p56):
            db.mycursor.execute('INSERT INTO jadval56 (pool , tarikh , ekhtelaf , sharh) values (%s , %s , %s , %s)',
                                (str(p56[i]['motalebat_arzi']),str(p56[i]['tarikh']) , int(khayyam_time_sort(p56[i]['tarikh'])) , str(p56[i]['dataBase'][5])))
            db.mydb.commit()
            i = i + 1
        db.mydb.commit()
        i = 0
        db.mycursor.execute("select * from jadval56 order by ekhtelaf")
        data = db.mycursor.fetchall()
        db.mydb.commit()
        ret ={}
        ret['befor'] = data_b
        ret['befor_p56'] = data_b_p56
        i = 0
        nerkh = 0.0180875824835107
        # return data
        while i <len(data):
            ret[i]={}
            ret[i]['pool'] = data[i][1]
            pool = data[i][1]
            if i == 0 :
                ret[i]['kole_motalebat'] = sum_of_adam_ghatiyat_p56 - data_b['pool']
                # return data[i][2]
                jarime = (data_b_p56['kole_motalebat'] * (1 + nerkh) ** khayam_type(data[i][2], '1394-12-12') -
                          data_b_p56['kole_motalebat'])
                pardakht_nashode_dore_ghabl = data_b['pool']
            else:
                pardakht_nashode_dore_ghabl =ret[i-1]['kole_motalebat']
                jarime = (pardakht_nashode_dore_ghabl * (1 + nerkh) ** khayam_type(data[i][2], data[i - 1][
                    2]) - pardakht_nashode_dore_ghabl)
                ret[i]['kole_motalebat'] = float(pardakht_nashode_dore_ghabl )+ float(pool) + float(jarime)
            #
            ret[i]['jarime'] = jarime
            ret[i]['tarikh'] = data[i][2]
            ret[i]['sharh'] = data[i][4]
            ret[i]['pardakht_nashode_dore_ghabl'] = pardakht_nashode_dore_ghabl
            print (i)
            i = i +1
        return ret
class jadval36(Resource):
    def get(self):
        #HANDELING BEFORE IN PIPELINES
        p56_before = pipeLinesF().get36inch(ghatiyat="true")
        i = 0
        # return p56_before
        sum_of_adam_ghatiyat_p56 = 0
        while i < len(p56_before):
            sum_of_adam_ghatiyat_p56 = float(p56_before[i]['motalebat_riyali']) + sum_of_adam_ghatiyat_p56
            i = i+1
        # return sum_of_adam_ghatiyat_p56
        # sum_of_adam_ghatiyat_p56 = 834675673780
        db.mydb.commit()
        #end
        db.mycursor.execute("select * from pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate = %s and state = %s",('لوله های 56 اینچ' , 'before'))
        naftanir_pardakht_adam = db.mycursor.fetchall()
        db.mydb.commit()
        i = 0
        final_sum=0
        while i < len(naftanir_pardakht_adam):
            final_sum = float(naftanir_pardakht_adam[i][2]) + final_sum
            i = i +1
        data_b = {}
        data_b={
            'sharh': 'پرداختی شرکت توسعه گاز',
            'tarikh': '1394-11-19',
            'pool': final_sum,
            'kole_motalebat': abs(final_sum) * -1 ,
            'pardakht_nashode_dore_ghabl':0
        }
        data_b_p56={
            'sharh': 'تعهدات پرداخت بابت 56',
            'tarikh': '94/12/12',
            'pool': sum_of_adam_ghatiyat_p56,
            'pardakht_nashode_dore_ghabl':final_sum,
            'kole_motalebat': abs(abs(final_sum) - sum_of_adam_ghatiyat_p56)
        }

        p56 = pipeLinesF().get36inch(ghatiyat="false")
        db.mycursor.execute('select id from jadval56')
        idies = db.mycursor.fetchall()
        db.mydb.commit()
        i= 0
        values = []
        while i < len(idies):
            # values.append(idies[i][0])
            db.mycursor.execute('delete from jadval56 where id = '+str(idies[i][0]))
            i = i + 1
        db.mydb.commit()
        db.mycursor.execute(
            "select * from pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate = %s and state = %s",
            ('لوله های 56 اینچ', 'after'))
        data = db.mycursor.fetchall()
        db.mydb.commit()
        i = 0
        while i < len(data):
            db.mycursor.execute('INSERT INTO jadval56 (pool , tarikh , ekhtelaf , sharh) values (%s , %s , %s , %s)',
                                (data[i][2], data[i][1],int(khayyam_time_sort(data[i][1])) , "sharh"))

            db.mydb.commit()
            i = i+1
        db.mydb.commit()
        i = 0
        while i < len(p56):
            db.mycursor.execute('INSERT INTO jadval56 (pool , tarikh , ekhtelaf , sharh) values (%s , %s , %s , %s)',
                                (str(p56[i]['motalebat_riyali']),str(p56[i]['tarikh']) , int(khayyam_time_sort(p56[i]['tarikh'])) , str(p56[i]['dataBase'][5])))
            db.mydb.commit()
            i = i + 1
        db.mydb.commit()
        i = 0
        db.mycursor.execute("select * from jadval56 order by ekhtelaf")
        data = db.mycursor.fetchall()
        db.mydb.commit()
        ret ={}
        ret['befor'] = data_b
        ret['befor_p56'] = data_b_p56
        i = 0
        nerkh = 0.0180875824835107
        # return data
        while i <len(data):
            ret[i]={}
            ret[i]['pool'] = data[i][1]
            pool = data[i][1]
            if i == 0 :
                ret[i]['kole_motalebat'] = sum_of_adam_ghatiyat_p56 - data_b['pool']
                # return data[i][2]
                jarime = (data_b_p56['kole_motalebat'] * (1 + nerkh) ** khayam_type(data[i][2], '1394-12-12') -
                          data_b_p56['kole_motalebat'])
                pardakht_nashode_dore_ghabl = data_b['pool']
            else:
                pardakht_nashode_dore_ghabl =ret[i-1]['kole_motalebat']
                jarime = (pardakht_nashode_dore_ghabl * (1 + nerkh) ** khayam_type(data[i][2], data[i - 1][
                    2]) - pardakht_nashode_dore_ghabl)
                ret[i]['kole_motalebat'] = float(pardakht_nashode_dore_ghabl )+ float(pool) + float(jarime)
            #
            ret[i]['jarime'] = jarime
            ret[i]['tarikh'] = data[i][2]
            ret[i]['sharh'] = data[i][4]
            ret[i]['pardakht_nashode_dore_ghabl'] = pardakht_nashode_dore_ghabl
            print (i)
            i = i +1
        return ret

class jadval36_dollar(Resource):
    def get(self):
        #HANDELING BEFORE IN PIPELINES
        p56_before = pipeLinesF().get36inch(ghatiyat="true")
        i = 0
        sum_of_adam_ghatiyat_p56 = 0
        while i < len(p56_before):
            sum_of_adam_ghatiyat_p56 = float(p56_before[i]['motalebat_arzi']) + sum_of_adam_ghatiyat_p56
            i = i+1
        db.mydb.commit()
        #end
        db.mycursor.execute("select * from pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate = %s and state = %s",('لوله های 56 اینچ' , 'before'))
        naftanir_pardakht_adam = db.mycursor.fetchall()
        db.mydb.commit()
        i = 0
        final_sum=0
        while i < len(naftanir_pardakht_adam):
            final_sum = float(naftanir_pardakht_adam[i][2]) + final_sum
            i = i +1
        data_b = {}
        data_b={
            'sharh': 'پرداختی شرکت توسعه گاز',
            'tarikh': '1394-11-19',
            'pool': final_sum,
            'kole_motalebat': abs(final_sum) * -1 ,
            'pardakht_nashode_dore_ghabl':0
        }
        data_b_p56={
            'sharh': 'تعهدات پرداخت بابت 56',
            'tarikh': '94/12/12',
            'pool': sum_of_adam_ghatiyat_p56,
            'pardakht_nashode_dore_ghabl':final_sum,
            'kole_motalebat': abs(abs(final_sum) - sum_of_adam_ghatiyat_p56)
        }

        p56 = pipeLinesF().get2(ghatiyat="false")
        db.mycursor.execute('select id from jadval56')
        idies = db.mycursor.fetchall()
        db.mydb.commit()
        i= 0
        values = []
        while i < len(idies):
            # values.append(idies[i][0])
            db.mycursor.execute('delete from jadval56 where id = '+str(idies[i][0]))
            i = i + 1
        db.mydb.commit()
        db.mycursor.execute(
            "select * from pardakht_shode_tavasote_naftanir_tm where pardakht_shod_babate = %s and state = %s",
            ('لوله های 56 اینچ', 'after'))
        data = db.mycursor.fetchall()
        db.mydb.commit()
        i = 0
        while i < len(data):
            db.mycursor.execute('INSERT INTO jadval56 (pool , tarikh , ekhtelaf , sharh) values (%s , %s , %s , %s)',
                                (data[i][2], data[i][1],int(khayyam_time_sort(data[i][1])) , "sharh"))

            db.mydb.commit()
            i = i+1
        db.mydb.commit()
        i = 0
        while i < len(p56):
            db.mycursor.execute('INSERT INTO jadval56 (pool , tarikh , ekhtelaf , sharh) values (%s , %s , %s , %s)',
                                (str(p56[i]['motalebat_arzi']),str(p56[i]['tarikh']) , int(khayyam_time_sort(p56[i]['tarikh'])) , str(p56[i]['dataBase'][5])))
            db.mydb.commit()
            i = i + 1
        db.mydb.commit()
        i = 0
        db.mycursor.execute("select * from jadval56 order by ekhtelaf")
        data = db.mycursor.fetchall()
        db.mydb.commit()
        ret ={}
        ret['befor'] = data_b
        ret['befor_p56'] = data_b_p56
        i = 0
        nerkh = 0.0180875824835107
        # return data
        while i <len(data):
            ret[i]={}
            ret[i]['pool'] = data[i][1]
            pool = data[i][1]
            if i == 0 :
                ret[i]['kole_motalebat'] = sum_of_adam_ghatiyat_p56 - data_b['pool']
                # return data[i][2]
                jarime = (data_b_p56['kole_motalebat'] * (1 + nerkh) ** khayam_type(data[i][2], '1394-12-12') -
                          data_b_p56['kole_motalebat'])
                pardakht_nashode_dore_ghabl = data_b['pool']
            else:
                pardakht_nashode_dore_ghabl =ret[i-1]['kole_motalebat']
                jarime = (pardakht_nashode_dore_ghabl * (1 + nerkh) ** khayam_type(data[i][2], data[i - 1][
                    2]) - pardakht_nashode_dore_ghabl)
                ret[i]['kole_motalebat'] = float(pardakht_nashode_dore_ghabl )+ float(pool) + float(jarime)
            #
            ret[i]['jarime'] = jarime
            ret[i]['tarikh'] = data[i][2]
            ret[i]['sharh'] = data[i][4]
            ret[i]['pardakht_nashode_dore_ghabl'] = pardakht_nashode_dore_ghabl
            print (i)
            i = i +1
        return ret

# api.add_resource(adam_ghateyat_peymankaran,"/naftanir_aadam_ghatiyat_peymankaran")
api.add_resource(gostare,"/gostare")
api.add_resource(comper,"/comperosor")
api.add_resource(peymankaran,"/peymankaran")
api.add_resource(pipeLinesF,"/pipeLinesF")
api.add_resource(arazi , "/arazi")
api.add_resource(pardakht_naftanir , "/pardakht_naftanir")
api.add_resource(pardakht_shode_tavasote_naftanir , "/pardakht_shode_tavasote_naftanir_TM")
api.add_resource(kala_30 , "/kala_30")
api.add_resource(sadid_mahshahr , "/sadid_mahshahr")
api.add_resource(jadval562 , "/jadval56")
api.add_resource(jadval56dollar , "/jadval56_dollar")
api.add_resource(jadval36 , "/jadval36")
api.add_resource(jadval36_dollar , "/jadval36_dollar")
api.add_resource(jadvalArazi , "/jadvalArazi")
api.add_resource(looleSaziSadid , "/jadval_loole_sazi_sadid")
api.add_resource(jadvalPeymankaran , "/jadval_peymankaran")

from classes.classes import *
from classes.taahodat_pardakht_sherkat_mohandesi_tose_gas import *
from classes.jaraem_taakhir_dar_bahre_bardari import *
from classes.taahodat_pardakht_sherkat_naftanir import *
from classes.model_mali import *
from classes.mohasebe_aghsat import *
api.add_resource(jarime_takhir_dar_pardakht , "/jarime_takhir_dar_pardakht")
api.add_resource(taahodat_pardakht_sherkat_mohandesi_tose_gas , "/taahodat_pardakht_sherkat_mohandesi_tose_gas")
api.add_resource(taahodat_pardakht_sherkat_naftanir , "/taahodat_pardakht_sherkat_naftanir")
api.add_resource(model_mali , "/model_mali")
api.add_resource(mohasebe_aghsat , "/mohasebe_aghsat")
# UPDATE :: have to make new changes from here
from classes.gereftane_darsade_gostare_ba_shomare_ghest import *
from classes.ghest_bandi_har_pishraft import *
api.add_resource(gereftane_darsade_gostare_ba_shomare_ghest, '/gereftane_darsade_gostare_ba_shomare_ghest')

api.add_resource(ghest_bandi_har_pishraft , '/ghest_bandi_har_pishraft')
from classes.ghest_bandi_har_pishraft_tajamoee import *
api.add_resource(ghest_bandi_har_pishraft_tajamoee , '/ghest_bandi_har_pishraft_tajamoee')
from classes.ghest_bandi_kole_gostare_ha_tajamoee import *
api.add_resource(ghest_bandi_kole_gostare_ha_tajamoee , '/ghest_bandi_kole_gostare_ha_tajamoee')
from classes.jaraem_taakhir_dar_bahre_bardariV2 import *
api.add_resource(jaraem_taakhir_dar_bahre_bardariV2 , '/jaraem_taakhir_dar_bahre_bardariV2')

from classes.jaraem_taakhir_dar_bahre_bardari_tajamoe import *
api.add_resource(jaraem_taakhir_dar_bahre_bardari_tajamoe , "/jaraem_taakhir_dar_bahre_bardari_tajamoe")

from classes.mohasebe_aghsat_tajamoee import *
api.add_resource(mohasebe_aghsat_tajamoee,'/mohasebe_aghsat_tajamoee')

from classes.taakhir_dar_bahre_bardari_tajamoee import *
api.add_resource(taakhir_dar_bahre_bardari_tajamoee ,'/taakhir_dar_bahre_bardari_tajamoee')


api.add_resource(jaraem_taakhir_dar_bahre_bardari,'/jaraem_taakhir_dar_bahre_bardari')
# app.run(host='192.168.43.7',debug=True)
app.run(debug=True)
