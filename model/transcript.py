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


    def get_html(self, data, users):
        doc = dominate.document()
        transcriptData=data['transcriptArray']
        print("transcriptData")
        print(transcriptData,users)
        with doc:
            with body():
                h1(users['user'][0].upper()+users['user'][1:len(users['user'])]+"'s transcript",style="text-align:center;")
                for j in range(len(transcriptData)):
                    with div(style="display:flex;flex-direction:row;justify-content: space-evenly;border: 1px solid gainsboro;padding: 1rem;margin-bottom: 1rem;"):
                        with div(style="flex:2; display:flex; flex-direction:column;padding-right:2rem"):
                            h3(transcriptData[j]['name'])
                            i(transcriptData[j]['time'],style="font-size: small;")
                        with div(style="flex:6"):
                            highlight_index=-1
                            try:
                                highlight_index=transcriptData[j]['highlightedUsers'].index(users['user'])
                            except ValueError:
                                pass
                            if(highlight_index == -1):                        
                                p(transcriptData[j]['data'])
                            else:
                                p(b(transcriptData[j]['data'],style="background:#fffb89"))

                    
                    

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
        'margin-right':'1cm'
        }
        print("base dir")
        print(settings.BASE_DIR)
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