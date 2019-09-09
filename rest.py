from flask import Flask,jsonify,request
import pandas as pd
app = Flask(__name__)
csv_file = pd.DataFrame(pd.read_csv("/Users/msdaram/Downloads/dailyweather.csv", sep = ",", header = 0, index_col = False))

x = csv_file.to_dict('records')
#url = "http://127.0.0.1:5000/historical"
@app.route('/historical/',methods=['POST'])
def addweather():
	x1={'DATE':request.json['DATE'],'TMAX':request.json['TMAX'],'TMIN':request.json['TMIN']}
	x.append(x1)
	return jsonify({'x':x})
import csvmapper



if __name__ == '__main__':
	app.run(debug=True)
for i in csv_file['DATE']:
	print(i)
	if(i==num):
			#jsonify({"DATE":num})
		print(i==num)
				#df2=csv_file.loc[csv_file['DATE'] == num].to_json()
		df2=csv_file.loc[csv_file['DATE'] == num]	
			#print(df2)
		l3=df2.values.tolist()
		dfl3=pd.DataFrame(np.array(l3),columns=['DATE','TMAX','TMIN'])
		return dfl3.to_json(orient = "records", double_precision = 10, force_ascii = True, default_handler = None)
		break
	else:
		return page_not_found()
		break 