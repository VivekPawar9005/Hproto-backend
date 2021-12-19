from flask import Flask, render_template,jsonify, request 
from flask_socketio import SocketIO, emit

import eventlet
import eventlet.wsgi
from model import transcript

highlighted_user_list=[]

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

#app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins='*')



@app.route('/api/<meetingId>',methods=['GET'])
def index(meetingId):
    transcript_obj=transcript.Transcript()
    transcript_obj.get_transcript(request.view_args)
    print(request.view_args)
    return 'sucessfull pdf generation'

@socketio.event
def get_transcript(data):
    print(data)
    transcript_obj=transcript.Transcript()
    transcript_obj.push_transcript_chunks(data)

@socketio.event
def highlight(data):
    print(data)
    highlighted_user_list.push(data['name'])

@socketio.event
def get_highlight_status():
    emit('highlight_status',highlighted_user_list)

@socketio.event
def remove_highlighted_user(data):
    highlight_user_list.remove(data['name'])
    emit('highlight_status',highlighted_user_list)

if __name__ == '__main__':
    # app.run(port=5000)
    # app.run(debug = True)
   # socketio.run(app)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)