from middleware import ypmongo_pool #,mailer,template_compiler
from datetime import date
import dominate
from dominate.tags import *
import requests
import pdfkit
import os

import os

class Transcript():
    def __init__(self):
        print('APi Obj created')
    def get_html(self,data):
        doc = dominate.document()
        transcriptData=data['transcriptArray']
        print(transcriptData)
        with doc:
            with body(style="text-align:center;width:100%;"):
                for i in range(len(transcriptData)):
                    with table(style="width: 90%;border: 1px solid black;border-collapse: collapse;margin-top: 5%;margin-left: auto;margin-right: auto;font-family: 'Roboto';").add(tbody()):
                        l1=tr()
                        with l1.add(td(style="")):
                            div(transcriptData[i]['name'],style='padding-top:0!important;margin-block-start: 0!important;margin-block-end: 0!important;')
                            div(transcriptData[i]['time'],style='padding-top:0!important;margin-block-start: 0!important;margin-block-end: 0!important;')
                        with l1.add(td(style="padding-top: 5px;padding-left: 10px;padding-bottom: 10px;text-align: left;")):
                            div(transcriptData[i]['data'],style='padding-top:0!important;margin-block-end: 0!important;')
                    # if index+1<len(transcriptData) and transcriptData[index]['name'] != transcriptData[index+1]['name'] :
                    #     with div(style="width:100%;display:flex;flex-direction:row"):
                    #         with div(style="flex:0;display:flex;flex-direction:column;"):
                    #             h3(transcriptData[index]['name'])
                    #             p(transcriptData[index]['time'])
                    #         with div(style="flex:1;"):
                    #             with p():
                    #                 if(transcriptData[index]['remark'] == 'highlight'):
                    #                     b(transcriptData[index]['data'])
                    #                 else:
                    #                     p(transcriptData[index]['data'])
                    #     index += 1
                    # elif index+1<len(transcriptData) and transcriptData[index]['name'] == transcriptData[index+1]['name']:
                    #     with div(style="width:100%;display:flex;flex-direction:row"):
                    #         with div(style="flex:0;display:flex;flex-direction:column;"):
                    #             h3(transcriptData[index]['name'])
                    #             p(transcriptData[index]['time'])
                    #         with div(style="flex:1;"):
                    #             temp=transcriptData[ index : len(transcriptData)]
                    #             mono=''
                    #             for j in range(len(temp)):
                    #                 try:
                    #                     if (j+1<len(temp) and temp[j]['name'] != temp[j+1]['name']):
                    #                         p(mono)
                    #                         break
                    #                     else:
                    #                         if(temp[j]['remark']=='highlight'):
                    #                             mono += "<b>"+temp[j]['data']+"</b>"
                    #                         else:
                    #                             mono += temp[j]['data']
                    #                 except:
                    #                     print("execption raised")
                    #                 finally:
                    #                     p(mono)
                    #                     break
  
                    #     index += 1

            return doc.render()


    def get_transcript(self,data):
        db = ypmongo_pool.get_db_connection()
        collection = db['room-meta']
        query={'meetingId':data['meetingId']}
        res=collection.find_one(query)
        #print(res)
        
        print(self.get_html(res))
        return 'pdf generated'

    def push_transcript_chunks(self,data):
        db = ypmongo_pool.get_db_connection()
        collection = db['room-meta']
        query={'meetingId':data['meetingId']}
        res=collection.find_one(query)
       # print(res)
        push_data={'name':data['name'],'data':data['data'],'time':data['date'],'remark':data['remark']}
        if res is None:
            collection.insert({'meetingId':data['meetingId'],'transcriptArray':[push_data]})
        else:
            collection.update(query,{'$addToSet':{'transcriptArray':push_data}})


     
        return 'Successfully chunks is PUSHED!'