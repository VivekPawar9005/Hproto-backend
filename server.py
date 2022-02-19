from numpy import delete
from flask import Flask, send_file, render_template,jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
import eventlet
import eventlet.wsgi
from model import transcript
from configs import settings
import os

highlighted_user_list=[]
room_dict={}


app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

#app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins='*')



@app.route('/api/<meetingId>/<user>',methods=['POST'])
@cross_origin()
def index(meetingId,user):
    transcript_obj=transcript.Transcript()
    transcript_obj.get_transcript(request.view_args)
    print(request.view_args)
    
    return send_file(os.path.join(settings.BASE_DIR, 'temp')+'/'+request.view_args['meetingId']+'_'+request.view_args['user']+'.pdf', as_attachment=True, mimetype='application/pdf')

@socketio.event
def get_transcript(data):
    print(data)
    data['highlightedUsers'] = highlighted_user_list
    transcript_obj=transcript.Transcript()
    transcript_obj.push_transcript_chunks(data)

@socketio.event
def highlight(data):
    print(data)
    try:
        highlighted_user_list.index(data['name'])
    except ValueError:
        highlighted_user_list.append(data['name'])
        
    #emit('highlight_status',highlighted_user_list)
    print("****************")
    print(highlighted_user_list)

@socketio.event
def get_highlight_status():
    emit('highlight_status',highlighted_user_list)

@socketio.event
def remove_highlighted_user(data):
    try:
        highlighted_user_list.remove(data['name'])
    except ValueError:
        pass
    emit('highlight_status',highlighted_user_list, broadcast=True)

@socketio.event
def join(data):
    # username = data['name']
    # room = data['room']
    # join_room(room)
    # print(room)
    # send(username + ' has entered the room.', to=room)
    print("***enter room***")
    print(data)
    try:
     room_dict[data['meetingId']].append(data['name'])
    except:
        room_dict[data['meetingId']]=[]
        room_dict[data['meetingId']].append(data['name'])
    print(room_dict[data['meetingId']])
    emit('numberOfClients',room_dict[data['meetingId']],broadcast=True)

@socketio.event
def leave(data):
    room_dict[data['meetingId']].remove(data['name'])
    print("***left room***")
    print(data)
    print(room_dict[data['meetingId']])
    if(len(room_dict[data['meetingId']]) == 0):
        del room_dict[data['meetingId']]
    emit('numberOfClients',room_dict[data['meetingId']],broadcast=True)

@socketio.event
def remove_generated_file(data):
    os.remove(os.path.join(settings.BASE_DIR, 'temp')+'/'+data['meetingId']+'_'+data['user']+'.pdf')
    

if __name__ == '__main__':
    # app.run(port=5000)
    # app.run(debug = True)
   # socketio.run(app)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)