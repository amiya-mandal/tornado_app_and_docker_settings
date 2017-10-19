# author : amiya mandal
"""
this is an api for fetching data from cleartrip hotel
using tornado as a web frame work and mongodb as db
"""


import tornado.ioloop
import tornado.web
import motor.motor_tornado
import config
import ujson
from Model.model_db_connection import InsertObject
from tornado.gen import *
from tornado.concurrent import run_on_executor, futures
import tornado.gen
import math
import requests


con = motor.motor_tornado.MotorClient(config.host, config.port)


class ParserInsert(object):
    def __init__(self):
        self._dbObject = InsertObject(con=con)
        self.executor = futures.ThreadPoolExecutor(10)
    @coroutine
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
        raise tornado.gen.Return(tempdict)

    @run_on_executor
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
            return parseddata





class MainHandler(tornado.web.RequestHandler):
    def _requestmodule(self):
        try:
            self._childerntemp = int(self._childern)
            self._adultstemp = int(self._adults)
            print("*")
            if self._source == "cleartrip":
                no_rooms = int(math.ceil(self._adultstemp / 2))
                print(no_rooms)
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

                re = requests.get(url=mainurl, headers = headers)
                return re.text
            elif self._source == "makemytrip":
                pass
        except:
            print("error>>", sys.exc_info()[1])
    def get(self):
        try:
            self._start_date = self.get_argument("startDate")
            self._end_date = self.get_argument("endDate")
            self._adults = self.get_argument("adults")
            self._state = self.get_argument("State")
            self._city = self.get_argument("City")
            self._childern = self.get_argument("children")
            self._source = self.get_argument("source")
            self.write(self._requestmodule())
        except:
            self.write_error(400)


def make_app():
    return tornado.web.Application([
        (r"/hotel/api", MainHandler),
    ])

if __name__ == "__main__":
    print("server start")
    app = make_app()
    app.listen(8888)
    loop = tornado.ioloop.IOLoop.current().start()