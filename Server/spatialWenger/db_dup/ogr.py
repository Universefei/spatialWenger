from django.shortcuts import render
from osgeo import ogr
from django.template import RequestContext
import os


###############################################################################
# Default Connection info
host = 'localhost'
# host = '10.61.126.175'
port = '5432'
user = 'postgres'
password = 'postgres'
dbname = 'dc'
# global Data Source list
DS_Manager = [ {    'id': 0 ,
            'name': 'PostGIS_dc',
            'ConnInfo': "PG: host={} port={} user={} password={} dbname='dc'".format(\
                    host, port, user, password, dbname), },
            {   'id': 1,
                'name': 'PostGIS_dc_dup',
                'ConnInfo': "PG: host={} port={} user={} password={} dbname='dc_dup'".format(\
                        host, port, user, password), },
            {   'id': 2,
                'name': 'ODBC_DM',
                'ConnInfo': "ODBC:SYSDBA/SYSDBA@dm", }, ]

DS_facade = [ {    'id': 0 ,
            'name': 'PostGIS_dc', },
            {   'id': 1,
                'name': 'PostGIS_dc_dup', },
            {   'id': 2,
                'name': 'ODBC_DM', }, ]

SRC_DS_index = 0
DST_DS_index = 0

###############################################################################

def _connPG(host, port, user, password, dbname):
    pgDriver = ogr.GetDriverByName("PostgreSQL")
    pgConnInfo = "PG: host={} port={} user={} password={} dbname={}".format(\
            host, port, user, password, dbname)
    try:
        pgDS = pgDriver.Open(pgConnInfo)
    except:
        sys.exit("Error: Open PostgreSQL failed!")
    else:
        return pgDS


def _openDSByIndex(idx):
    connInfo = DS_Manager[idx].get('ConnInfo')
    return ogr.Open(connInfo)


def _list_layers(req, template, ds_index):
    layerList = []
    DS = _openDSByIndex(ds_index)
    print DS.GetName()
    for iLayer in DS:
        layerList.append(iLayer.GetName())
    layerList.sort()

    print DS.GetName()
    return render(req, template, {'layerList':layerList}, context_instance=RequestContext(req)) 

###############################################################################

# homepage prept for asking select datasource
def db_homepage_view(req):
    return render(req, 'index.html',{'DS_facade': DS_facade})


# List all layers in a specific Data Source
def select_layer_view(req):
    global SRC_DS_index, DST_DS_index
    SRC_DS_index = int( req.POST.get('src_ds') )
    DST_DS_index = int( req.POST.get('dst_ds') )

    return _list_layers(req, 'select_layer.html', SRC_DS_index)


# Duplicate Layer from user's request demand
def dup_layer_view(req):
    # get ds from req.POST
    if req.method == 'POST':

        srcDS = _openDSByIndex(SRC_DS_index)
        dstDS = _openDSByIndex(DST_DS_index)

        srcLayers = req.POST.getlist('srcLayers')
        dstLayers = []
        
        print srcLayers
        for i in range(len(srcLayers)):
            # read srclayers into memory
            print srcLayers[i]
            layer = srcDS.GetLayerByName(str(srcLayers[i]))
            print "getlayerbyname: "+layer.GetName()
            # copy into dstlayers
            dstDS.CopyLayer(layer,str( srcLayers[i] + '_dup'), ['OVERWRITE=YES',])
            pass

        srcDS.Destroy()
        dstDS.Destroy()

    # return render(req, 'layer_list.html',context_instance=RequestContext(req))
    return _list_layers(req, 'list_layer.html', DST_DS_index)


# deamon timer executor
def receive_task(req):
    # get task info from req.POST

    # generate new task dict and add into global task queue
    # not to use multithread first
    # new_task = {}
    # task.append(new_task)

    return render(req, 'index.html')
