from flask import Flask, send_file, render_template,jsonify, request, send_from_directory
from flask_socketio import SocketIO, emit

import eventlet
import eventlet.wsgi
from model import transcript
from configs import settings
import os

highlighted_user_list=[]

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

#app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins='*')



@app.route('/api/<meetingId>/<user>',methods=['GET'])
def index(meetingId,user):
    transcript_obj=transcript.Transcript()
    transcript_obj.get_transcript(request.view_args)
    print(request.view_args)
    
    return send_file(os.path.join(settings.BASE_DIR, 'temp')+'/'+request.view_args['meetingId']+'.pdf', as_attachment=True)

@socketio.event
def get_transcript(data):
    print(data)
    transcript_obj=transcript.Transcript()
    transcript_obj.push_transcript_chunks(data)

@socketio.event
def highlight(data):
    print(data)
    try:
        highlighted_user_list.index(data['name'])
    except ValueError:
        highlighted_user_list.append(data['name'])
        
    emit('highlight_status',highlighted_user_list)

@socketio.event
def get_highlight_status():
    emit('highlight_status',highlighted_user_list)

@socketio.event
def remove_highlighted_user(data):
    highlighted_user_list.remove(data['name'])
    emit('highlight_status',highlighted_user_list)

if __name__ == '__main__':
    # app.run(port=5000)
    # app.run(debug = True)
   # socketio.run(app)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)