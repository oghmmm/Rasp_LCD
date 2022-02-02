# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_file, jsonify, redirect, session

try:
	from werkzeug.utils import secure_filename
except:
	from werkzeug import secure_filename

import os
import shutil
app = Flask(__name__)

FILE_PATH = "C:/test/elevator"
#FILE_PATH = "/home/pi/FilePlus/upload"
LOGIN_ID = 'admin'
PASSWD = 'admin2356'

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error(error)
	return render_template('404.html'), 404

@app.route('/')
def home_page():
	session.clear()
	return render_template('login.html')

@app.route('/login_check', methods = ['GET', 'POST'])
def login_check():
	if request.method == 'POST':
		loginId = request.form['loginId']
		passwd = request.form['passwd']

		if(loginId == LOGIN_ID and passwd == PASSWD):
			session['login_id'] = loginId
			return jsonify(result = 'success')
		else:
			return jsonify(result = 'fail')
	else:
		return render_template('404.html')

# File list page
@app.route('/filelist')
def file_list():
	try:
		if not os.path.exists(FILE_PATH):
			os.makedirs(FILE_PATH)
			os.makedirs(FILE_PATH + "/temp")
			for i in range(1, 6):
				os.makedirs(FILE_PATH + "/" + str(i))

	except OSError:
		print("Error: Failed to create the directory.")

	directories = os.listdir(FILE_PATH)
	directories.remove('temp')
	directories.sort(key=int)
	file_dict = {}

	for directory in directories:
		full_file_path = os.path.join(FILE_PATH, directory)
		sub_files = os.listdir(full_file_path)
		#print(sub_files)
		file_dict[directory] = sub_files

	#print(file_dict)
	return render_template('file_list.html', directories=directories, files=file_dict)

# File upload
@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		chk_list = request.form.getlist('uploadChk')

		if not os.path.exists(FILE_PATH + "/temp"):
			os.makedirs(FILE_PATH + "/temp")

		file_list = request.files['file']
		file_list.save(FILE_PATH + "/temp/" + secure_filename(file_list.filename))

		upload_files = os.listdir(FILE_PATH + "/temp/")
		for file in upload_files:
			src = FILE_PATH + "/temp/" + file
			for i in chk_list:
				dst = FILE_PATH + "/" + i + "/" + file
				shutil.copy2(src, dst)
			os.remove(src)

		return "success"
	else:
		return render_template('404.html')

# File delete
@app.route('/fileDelete', methods = ['GET', 'POST'])
def delete_file():
	if request.method == 'POST':
		hogi = request.form['hogi']
		fName = request.form['fName']

		src = FILE_PATH + "/" + hogi + "/" + fName

		try:
			os.remove(src)
			return jsonify(result = 'success')
		except:
			return jsonify(result = 'fail')

	else:
		return render_template('404.html')
'''
#파일 다운로드 처리
@app.route('/fileDown', methods = ['GET', 'POST'])
def down_file():
	if request.method == 'POST':
		sw=0
		files = os.listdir("./uploads")
		for x in files:
			if(x==request.form['file']):
				sw=1
				path = "./uploads/"
				return send_file(path + request.form['file'],
						attachment_filename = request.form['file'],
						as_attachment=True)

		return render_template('page_not_found2.html')
	else:
		return render_template('page_not_found2.html')
'''


def register_interceptor(app: Flask):
    @app.before_request
    def before_request():
        if '/static' in request.path:
            pass
        elif '/login_check' in request.path:
            pass
        else:
            if 'login_id' not in session:
                return render_template('login.html')


if __name__ == '__main__':
	app.secret_key = "c90dcd7d-5321-4fa6-88eb-8c2687663dbc"
	register_interceptor(app)
	app.run(host='0.0.0.0', port=8888, debug=True, threaded=True)