# author : amiya mandal
"""
this is an api for fetching data from cleartrip hotel
using tornado as a web frame work and mongodb as db
"""


import tornado.ioloop
import tornado.web
import pymongo
import app.config as config
import ujson
from tornado.gen import *
import tornado.gen
from tornado.concurrent import run_on_executor
from app.Model.model_db_connection import InsertObject
from concurrent.futures import ThreadPoolExecutor
import math
import requests


con = pymongo.MongoClient(host=config.host, port=config.port)


class ParserInsert(object):
    def __init__(self):
        global con
        self._dbObject = InsertObject(con=con)

    def parserdatAtype_cleartrip(self, ddata):
        tempdict = {}
        tempdict["images"] = ddata["im"]
        tempdict["hotel_name"] = ddata["nm"]
        tempdict["location"] = ddata["ar"] + ":"+ ddata["ad"]
        tempdict["price"] = ddata["low"]
        try:
            tempdict["facility"] = ddata["rnm"]
        except:
            tempdict["facility"] = None
        tempdict["source"] = "cleartrip"
        self._dbObject.InsertOne(data=tempdict.copy())
        return tempdict

    def _clertripFucntion(self,data):
        templist = []
        htlist = data["ht"]
        for i in htlist:
            templist.append(self.parserdatAtype_cleartrip(i))
        return templist

    def sender_funtion(self, data, type):
        ddata = ujson.loads(data)
        if type == "cleartrip":
            parseddata = self._clertripFucntion(data=ddata)
            return ujson.dumps(parseddata)



class MainHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)

    @run_on_executor
    def _Blocking_task(self, data):
        obj = ParserInsert()
        parseddata = obj.sender_funtion(data=data, type=self._source)
        return parseddata


    @coroutine
    def _requestmodule(self):
        try:
            self._childerntemp = int(self._childern)
            self._adultstemp = int(self._adults)
            if self._source == "cleartrip":
                no_rooms = int(math.ceil(self._adultstemp / 2))
                appurl = ""
                for i in range(0, no_rooms):
                    if self._childerntemp != 0:
                        if self._childerntemp != 1:
                            appurl += "&adults" + str(i + 1) + "=2&children" + str(i + 1) + "=2&ca1=10&ca1=10"
                            self._adultstemp -= 2
                            self._childerntemp -= 2
                        else:
                            appurl += "&adults" + str(i + 1) + "=2&children" + str(i + 1) + "=1"
                            self._adultstemp -= 2
                            self._childerntemp -= 1
                    elif self._childerntemp == 0:
                        if self._adultstemp == 1:
                            appurl += "&adults" + str(i + 1) + "=1&children" + str(i + 1) + "=0"
                            self._adultstemp -= 1
                        else:
                            appurl += "&adults" + str(i + 1) + "=2&children" + str(i + 1) + "=0"
                            self._adultstemp -= 2

                mainurl = "https://www.cleartrip.com/hotels/jsonservice/hotel-content?city={0}&state={1}&country=IN&chk_in={2}&chk_out={3}&num_rooms={4}".format(self._city,self._start_date,self._start_date,self._end_date,no_rooms)
                mainurl += appurl
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

                re = requests.get(url=mainurl, headers=headers)
                # code here
                data = yield self._Blocking_task(data=re.text)
                return (data)
            elif self._source == "makemytrip":
                pass
        except:
            print("error>>", sys.exc_info()[1])
    @coroutine
    def get(self):
        try:
            # self._start_date = "27/10/2017"
            # self._end_date = "14/11/2017"
            # self._adults = "4"
            # self._childern = "2"
            # self._state = "Goa"
            # self._city = "Goa"
            # self._source = "cleartrip"
            # localhost:8888/hotel/api?startDate=27/10/2017&endDate=14/11/2017&adults=3&children=2&source=cleartrip&City=Goa&State=Goa
            self._start_date = self.get_argument("startDate")
            self._end_date = self.get_argument("endDate")
            self._adults = self.get_argument("adults")
            self._state = self.get_argument("State")
            self._city = self.get_argument("City")
            self._childern = self.get_argument("children")
            self._source = self.get_argument("source")
        except:
            self.write_error(400)
        data = yield self._requestmodule()
        self.write(str(data))


class MainHandler2(tornado.web.RequestHandler):
    def get(self):
        items = ["Item 1", "Item 2", "Item 3"]
        self.render("abc.html", title="My title", items=items)

def make_app():
    return tornado.web.Application([
        (r"/hotel/api", MainHandler),
        (r"/webpage", MainHandler2),
    ])

if __name__ == "__main__":
    print("server start")
    app = make_app()
    app.listen(8888)
    loop = tornado.ioloop.IOLoop.current().start()