from flask import Blueprint, abort, request
import json
from watchDB import watchManager, watchSession, zone
from setting import areas

webAPI = Blueprint('webAPI', __name__,
                        template_folder='templates')

@webAPI.route('/')
def show():
    return 'web API here'

@webAPI.route('/maps')
def getAreas():
    return json.dumps(areas)

@webAPI.route('/watch/list')
def getWatchs():
    fullData = []
    for watch in watchManager.watchs():
        name = watchManager.getName(watch)
        fullData.append( {'name': name, 'ID': watch} )
    return json.dumps(fullData)

@webAPI.route('/watch/list/act')
def getActWatchs():
    fullData = []
    for watch in watchManager.actWatchs():
        name = watchManager.getName(watch)
        fullData.append( {'name': name, 'ID': watch} )
    return json.dumps(fullData)

@webAPI.route('/watch/Act/<ID>')
def ctWatch(ID):
    return json.dumps(watchSession.new(ID,"2016-06-06"))

@webAPI.route('/watch/loc/<ID>')
@webAPI.route('/watch/loc/<ID>/<NUMBER>')

def locs(ID,NUMBER=1):
    return json.dumps(watchManager.getPos(ID,NUMBER))

@webAPI.route('/zone/list/<mapID>')
def listZone(mapID):
    return json.dumps(zone.listZone(mapID))

@webAPI.route('/zone/new',methods=['POST'])
def newZone():
    MapID = request.form.get('MapID')
    zoneName = request.form.get('Name')
    LT = request.form.get('LT')
    RB = request.form.get('RB')

    x1 = eval(LT)[0]
    y1 = eval(LT)[1]
    x2 = eval(RB)[0]
    y2 = eval(RB)[1]

    if ( x1 > x2 or y1 > y2 or len(zoneName) < 2 ):
        return json.dumps([-2,'Data wrong!!']), 400
    else:
        dbOP = zone.newZone(MapID,zoneName,LT,RB)
        if dbOP[0] >= 0:
            return json.dumps(dbOP), 200
        else:
            return json.dumps(dbOP), 500

@webAPI.route('/zone/rename',methods=['POST'])
def renameZone():
    MapID = request.form.get('MapID')
    zoneName = request.form.get('Name')
    zoneNewName = request.form.get('NewName')

    dbOP = zone.renameZone(MapID,zoneName,zoneNewName)
    if dbOP[0] >= 0:
        return json.dumps(dbOP), 200
    else:
        return json.dumps(dbOP), 500

@webAPI.route('/zone/setAlert',methods=['POST'])
def setAlertZone():
    MapID = request.form.get('MapID')
    zoneName = request.form.get('Name')
    zoneAlert = request.form.get('Alert')

    dbOP = zone.setAlertZone(MapID,zoneName,zoneAlert)
    if dbOP[0] >= 0:
        return json.dumps(dbOP), 200
    else:
        return json.dumps(dbOP), 500

@webAPI.route('/zone/del',methods=['POST'])
def delZone():
    MapID = request.form.get('MapID')
    zoneName = request.form.get('Name')

    dbOP = zone.delZone(MapID,zoneName)
    if dbOP[0] >= 0:
        return json.dumps(dbOP), 200
    else:
        return json.dumps(dbOP), 500

