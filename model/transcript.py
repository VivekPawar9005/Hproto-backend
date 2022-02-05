from middleware import ypmongo_pool #,mailer,template_compiler
from datetime import date
import dominate
from dominate.tags import *
import requests
import pdfkit
import os
from configs import settings


from server import highlight

class Transcript():
    def __init__(self):
        print('APi Obj created')
        self.absolute_path=os.path.abspath(__file__)
        if (os.path.isdir(os.path.join(settings.BASE_DIR, 'temp')) ) == False:
            os.mkdir(os.path.join(settings.BASE_DIR, 'temp'))

    # def stitch(self,data):
    #     mainIndex = []
    #     i=0
    #     print(len(data))
    #     while i< len(data):
    #         temp=[]
    #         for j in range(i, len(data)):

    #             try:
    #                 if (data[j]['name'] == data[j+1]['name']):
    #                     temp.append(j)
    #                 else:
    #                     temp.append(j)
    #                     print(temp)
    #                     mainIndex.append(temp)
    #                     i=j+1
    #                     break
    #             except:
    #                 if len(data) != 1 and len(temp) != 0:
    #                     # print(temp)
    #                     # print(data[temp[len(temp)-1]]['name'])
    #                     # print(data[temp[len(temp)-1]+1]['name'])
    #                     if data[temp[len(temp)-1]]['name'] == data[temp[len(temp)-1]+1]['name']:
    #                         temp.append(temp[len(temp)-1]+1)
    #                         mainIndex.append(temp)
    #                     else:
    #                         mainIndex.append(temp)
    #                         mainIndex.append([temp[len(temp)-1]+1])
    #                     i=len(data)
    #                 else:
    #                     mainIndex.append([i])
    #                     i=len(data)
    #     return mainIndex

    def stitch(self,data):
        mainIndex = []
        i=0
        print(len(data))
        while i< len(data)-1:
            temp=[]
            for j in range(i, len(data)-1):

                try:
                    if (data[j]['name'] == data[j+1]['name']):
                        temp.append(j)
                    else:
                        temp.append(j)
                        print(temp)
                        mainIndex.append(temp)
                        i=j+1
                        break
                except:
                    print("execption!")
        return mainIndex



    def get_html(self, data, users):
        doc = dominate.document()
        transcriptData=data['transcriptArray']
        print("transcriptData")
        print(transcriptData)
        sticher=self.stitch(transcriptData)
        print("sticher indexs")
        print(sticher)
        with doc:
            with body():
                h1(users['user'][0].upper()+users['user'][1:len(users['user'])]+"'s transcript",style="text-align:center;")
                for j in range(len(sticher)):
                    with div(style="display:flex;flex-direction:row;justify-content: space-evenly;border: 1px solid gainsboro;padding: 1rem;margin-bottom: 1rem;"):
                        with div(style="flex:2; display:flex; flex-direction:column;padding-right:2rem"):
                            h3(transcriptData[sticher[j][0]]['name'])
                            i(transcriptData[sticher[j][0]]['time'],style="font-size: small;")
                        with div(style="flex:6"):
                            
                            for k in range(len(sticher[j])):
                                print(sticher[j][k])
                                try:
                                    highlight_index=transcriptData[sticher[j][k]]['highlightedUsers'].index(users['user'])
                                except ValueError:
                                    highlight_index= -1

                                if(highlight_index == -1):                        
                                    p(transcriptData[sticher[j][k]]['data'])
                                else:
                                    p(b(transcriptData[sticher[j][k]]['data'],style="background:#fffb89"))

                    
                    

        return doc.render()


    def get_transcript(self,data):
        db = ypmongo_pool.get_db_connection()
        collection = db['room-meta']
        query = { 'meetingId': data['meetingId'] }
        res = collection.find_one(query)
        pdfkit_options = {
        'page-size':'Letter',
        'encoding':'utf-8', 
        'margin-top':'1.2cm',
        'margin-bottom':'1cm',
        'margin-left':'1cm',
        'margin-right':'1cm',
        'encoding':'UTF-8',
        'custom-header' : [
            ('Accept-Encoding','gzip')
        ]
        }
        print("base dir")
        print(settings.BASE_DIR)
        print("********res*******")
        print(res)
        if  res is None or len(res['transcriptArray']) == 0:
            notFound="""<!DOCTYPE html> <html> <head> <title>Dominate</title> </head> <body> <body> <div style="display:flex;flex-direction:row;justify-content:center;"> <h1> TRANSCRIPT DATA NOT FOUND </h1> </div> </body> </body> </html>"""
            pdfkit.from_string(notFound, os.path.join(settings.BASE_DIR, 'temp')+'/'+data['meetingId']+'.pdf',options=pdfkit_options)
        else:
            pdfkit.from_string(self.get_html(res,data), os.path.join(settings.BASE_DIR, 'temp')+'/'+data['meetingId']+'.pdf',options=pdfkit_options)

        return 'pdf generated'

    def push_transcript_chunks(self,data):
        db = ypmongo_pool.get_db_connection()
        collection = db['room-meta']
        query={'meetingId':data['meetingId']}
        res=collection.find_one(query)
        push_data={'name':data['name'],'data':data['data'],'time':data['date'],'highlightedUsers':data['highlightedUsers']}
        if res is None:
            collection.insert({'meetingId':data['meetingId'],'transcriptArray':[push_data]})
        else:
            collection.update(query,{'$addToSet':{ 'transcriptArray': push_data }})


     
        return 'Successfully chunks is PUSHED!'