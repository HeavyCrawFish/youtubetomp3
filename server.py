from flask import Flask,send_from_directory,abort
from flask import request
from flask_cors import CORS, cross_origin
from pytube import YouTube
from flask import send_file
import os

app = Flask(__name__,static_folder='app/build',static_url_path='')
cors = CORS(app)
# members api route

@app.route("/convert",methods=['GET'])
@cross_origin()
def convert():
    link = request.args.get('link')
    if link == '':
        return {"msg":"Please provide a valid youtube video url","code":"failed"}
    else:
        video = YouTube(link)
        print('Title: ',video.title)

        # clearing out files
        print('Clearing out files if present...')
        files = os.listdir('downloads')
        for file in files:
            file_path = os.path.join('downloads',file)
            if(os.path.isfile(file_path)):
                os.remove(file_path)
        
        print('Downloading.....')
        out_path =video.streams.filter(only_audio=True).first().download('downloads')
        new_name = os.path.splitext(out_path)
        os.rename(out_path,new_name[0]+'.mp3')
        new_path = new_name[0]+'.mp3'
        print(new_path)
        print('Done...')
        return {"msg":"Converted SuccessFully", "code":"success","name":video.title}
        


@app.route("/getfiles",methods=['GET'])
@cross_origin()
def get_files():
    file_name = request.args.get('file_name')
    file_name = file_name.replace('%20',' ')
    files = os.listdir('downloads')
    print(file_name)
    try:
        for file in files:
            file_path = os.path.join('downloads',file)
            if(os.path.isfile(file_path)):
                 return send_file(file_path,as_attachment=True)
            else:
                 return {"msg":"could not find file"+file_path+" in "+file, "code":"failure"}
    except Exception as e:
        abort(404)

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')

