# from flask import Flask,render_template,request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# import requests
#Reference https://stackoverflow.com/questions/19697846/how-to-convert-csv-file-to-multiline-json
#https://www.youtube.com/watch?v=s_ht4AKnWZg
#swagger:https://www.youtube.com/watch?v=iZ2Tah3IxQc
#https://editor.swagger.io/
#for installing flask, Reference :http://flask.pocoo.org/docs/1.0/installation/
import csv
from flask_swagger_ui import get_swaggerui_blueprint	
# with open('/Users/msdaram/Downloads/dailyweather.csv','r') as csv_file:
#   csv_reader = csv.reader(csv_file)

from flask import Flask, jsonify,render_template,request,send_from_directory,Blueprint
from flask_restplus import Api, Resource, fields
import requests
import pandas as pd
import numpy as np
# from routes import request_api
app = Flask(__name__)
csv_file1 = pd.DataFrame(pd.read_csv("/Users/msdaram/Downloads/dailyweathernew.csv", sep = ",", header = 0, index_col = False))
csv_file = pd.DataFrame(pd.read_csv("/Users/msdaram/Downloads/dailyweather.csv", sep = ",", header = 0, index_col = False))
#x = csv_file.to_dict('records')


@app.route("/historical/", methods=['GET','POST']) 
def get_data():
	# jsonf = request.json
	list1 =[]
	#csv_file = pd.DataFrame(pd.read_csv("/Users/msdaram/Downloads/dailyweather.csv", sep = ",", header = 0, index_col = False))
	#csv_file1 = pd.DataFrame(pd.read_csv("/Users/msdaram/Downloads/dailyweathernew.csv", sep = ",", header = 0, index_col = False))
	#f=csv_file.to_json(orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)     
	#csv1=csv_file.drop(['TMAX','TMIN'],axis=1)
	
	#csv_dict=csv1.to_dict('records')
	global csv_file
	global csv_file1
	if(request.method=='GET'):

		list1=csv_file1.values.tolist()
		list3=[]
		for i in list1:
			list3.append(str(i[0]))
		columns=['DATE']
		dframe=pd.DataFrame(np.array(list3),columns=columns)

		return dframe.to_json(orient = "records", double_precision = 10, force_ascii = True, default_handler = None)
	if(request.method=='POST'):
		
		x1={'DATE':request.json['DATE'],'TMAX':request.json['TMAX'],'TMIN':request.json['TMIN']}
		l1=[[int(request.json['DATE'])]]
		l2=[[int(request.json['DATE']),int(request.json['TMAX']),int(request.json['TMIN'])]]
		print(l1)
		print(l2)
		df1=pd.DataFrame(np.array(l1),columns=['DATE'])
		csv_file1=csv_file1.append(df1,ignore_index=True)
		l3=csv_file1.values.tolist()
		df2=pd.DataFrame(np.array(l2),columns=['DATE','TMAX','TMIN'])
		csv_file=csv_file.append(df2,ignore_index=True)
		return jsonify({'DATE':request.json['DATE']}),201



@app.route("/historical/<int:num>",methods=['GET'])
def get_specdate(num):
	global csv_file
	global csv_file1
	#df = pd.read_csv('/Users/msdaram/Downloads/dailyweather.csv')
	print('csv',csv_file,'csvend')
	print(num)
	#df1=pd.DataFrame(pd.read_csv("/Users/msdaram/Downloads/dailyweathernew.csv", sep = ",", header = 0, index_col = False))
	# if(request.method == 'DELETE'):
	# 	csv_file=csv_file.drop(csv_file[csv_file['DATE']==num].index.item(),axis=0)

	# 	csv_file1=csv_file1.drop(csv_file1[csv_file1['DATE']==num].index.item(),axis=0)
	# 	return csv_file1.to_json(orient = "records", double_precision = 10, force_ascii = True, default_handler = None),200
	if(request.method=='GET'):
		#print(csv_file['DATE'])
		#print('inside get')
		l4=[]
		for i in csv_file['DATE']:
			#print(i)
			#print('before if')
			if(i==num):
				df2 = csv_file.loc[csv_file['DATE'] == num].to_json()
				break
				# lnew=df2.values.tolist()
				# lnew1=[]
				# #b=','.join(map(str, lnew))
				# #print(b)
				# lnew2=[]
				# lnew3=[]
				# print(lnew)
				# lnew2.append(str(lnew[0][0]))
				# lnew2.append(lnew[0][1])
				# lnew2.append(lnew[0][2])

				# lnew3.append(lnew2)
				# print(lnew2)	
				# df3=pd.DataFrame(np.array(lnew3),columns=['DATE','TMAX','TMIN'])
				# len(df3.to_json(orient = "records", double_precision = 10, force_ascii = True, default_handler = None))
			else:
				df2 = page_not_found()
		return df2
	
	else:
		return page_not_found()	
		
@app.errorhandler(404)
def page_not_found():
	return render_template('404.html'), 404

@app.route("/historical/<int:num>",methods=['DELETE'])
def del_date(num):
	global csv_file
	global csv_file1

	# csv_file=csv_file.drop(csv_file[csv_file['DATE']==num].index.item(),axis=0)
	# csv_file1=csv_file1.drop(csv_file1[csv_file1['DATE']==num].index.item(),axis=0)
	# df2=csv_file1.drop(csv_file1[csv_file1['DATE']==num].index.item(),axis=0)
	for i in csv_file['DATE']:
		if(i==num):
			x=csv_file1[csv_file1['DATE']==num].index.values.astype(int)[0]
			y=csv_file[csv_file['DATE']==num].index.values.astype(int)[0]		
			csv_file=csv_file.drop([x],axis=0)
			csv_file1=csv_file1.drop([y],axis=0)		
			df2=csv_file.to_json(orient = "records", double_precision = 10, force_ascii = True, default_handler = None)
		else:
			df2=page_not_found()
	return df2			



@app.route("/forecast/<int:num>",methods=['GET'])
def forcast_weather(num):
	tmax=30
	tmin=20
	list2=[]
	list2.append([str(num),tmax,tmin])
	for i in range(0,6):
		num=num+1
		tmax=tmax+2
		tmin=tmax-5
		list2.append([str(num),tmax,tmin])
	columns=['DATE','TMAX','TMIN']
	df2 = pd.DataFrame(np.array(list2),columns=columns)
	#print(df2.to_json(orient = "records", double_precision = 10, force_ascii = True, default_handler = None))
	return df2.to_json(orient = "records", double_precision = 10, force_ascii = True, default_handler = None),200

# swagger ui
@app.route("/static/<path:path>")
def send_static(path):
	return send_from_directory('static', path)

SWAGGER_URL = '/swaggerui'
API_URL = '/static/swaggerui.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
	SWAGGER_URL,
	API_URL,
	config={
		'app_name' : 'Python-FLask-SwaggerAPI-WeatherApp'
	}
)
app.register_blueprint(swaggerui_blueprint,url_prefix=SWAGGER_URL)
# app.register_blueprint(request_api.get_blueprint())


if __name__ == '__main__':
	app.run(debug=True)