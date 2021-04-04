from flask import Flask,jsonify,request
import jwt
from pathlib import Path
from flask_cors import CORS

#creating app

app = Flask(__name__)

#enabling? cors

CORS(app)
#seting app config

app.config['SECRET_KEY'] = 'NOT_SO_SECRET_KEY'

#routes

#login and getting tokens
@app.route('/login',methods=['POST'])
def login():
    
    #getting user info from http request body

    userInfo = request.get_json()

    print(userInfo)

    if 'email' in userInfo and 'password' in userInfo:

            token = jwt.encode(userInfo,app.config['SECRET_KEY'],algorithm='HS256')

            return jsonify({'token':token}),200

    return jsonify({'message':'something went wrong'}),400


#login with token
@app.route('/loginWithToken',methods=['POST'])

def loginWithToken():

        token = request.headers['Authorization'].split(' ')[1]

        if token:

            try:

                userInfo = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])

                print(userInfo)

                return jsonify('success'),200
            
            except:
                
                return jsonify('failed'),400

        else:
            
            return jsonify('failure'),400


#upload handler

@app.route('/upload',methods=['POST'])
def upload():
    
    if request.files and request.args['domain'] :
        
        domain = request.args['domain']

        files = request.files

        #making domain folder path

        domainFolder = Path.cwd() / 'storage' / domain

        #making project directory

        makeFolder(domainFolder)
        

        for pathname in files:

            #removing base folder name 

            splitPathName = pathname.split('/')[2:]

            #getting file

            file = files[pathname]

            #getting file name as it is always the last item in the list

            filename = splitPathName.pop(-1)

            #making files full path name
            #full path name is folder where the current file will be found

            fullPathName = Path.joinpath(domainFolder,'/'.join(splitPathName))

            #making folder with full path name

            makeFolder(fullPathName)

            print(fullPathName)

            #making a path that contains the fullpath and the path name
            #required inorder to save file

            pathWithFile = Path.joinpath(fullPathName,filename)

            print(pathWithFile)

          
            #saving file
            #  
            file.save(pathWithFile)
            
                

        return jsonify('loading'),200

    else:

        return jsonify('errror'),400


#function that makes the domain folder

def makeFolder(folderName):
   
    try:

        folderName.mkdir()
            
    except:
                
        print('folder creation failed')


if __name__ == '__main__':
    
    app.run(debug=True)