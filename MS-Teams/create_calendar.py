from flask import Flask, jsonify, render_template, request, redirect
import json as js
from datetime import datetime, timedelta
from O365 import Account, MSGraphProtocol
import os

app = Flask(__name__)

f = open('data.json','r')
data = js.load(f)
emp_data = data['Employees']

def datetime_range(start, end, delta):
    current = start
    while current <= end:
        yield current
        current += delta

def create_time_slots(arr, mint):
	timestamps = []
	for x in arr:
		start,end = x[0],x[1]
		dts = [dt.strftime('%H:%M') for dt in datetime_range(datetime(2021, 8, 23, start), datetime(2021, 8, 23, end), timedelta(minutes=mint))]
		res = [[dts[i], dts[i + 1]] for i in range(len(dts) - 1)]
		timestamps.extend(res)
	return timestamps

@app.route('/get_data',methods =["GET", "POST"])
def get_data():
	if request.method == "POST":
		sub = request.form.get('sub')
		name = request.form.get('nm')
		email = request.form.get('email')
		dte = request.form.get('date')
		time = request.form.get('time')
		tl = [int(i) for i in ":".join(list(map(str,time.split(' ')))).split(":") if i.isdigit()]
		dl = list(map(int,dte.split('/')))
		file1 = open("appointment.txt",'a')
		file1.write(dte + " " + time + "\n")
		file1.close()
		os.system('python readwrite_calendar.py ' + '"' + sub + '"' + ' ' + '"' +name + '"' + " " + '"' +email + '"' + " " + str(dl[0]) + ' ' + str(dl[1]) + ' ' + str(dl[2]) + ' ' + str(tl[0]) + ' ' + str(tl[1]) + ' ' + str(tl[-2]) + ' ' + str(tl[-1]))
		msg = "Meeting arranged successfully..."
		return msg
	else:
		msg = "Something went wrong! Try again..."
		return msg

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/date_form_',methods =["GET", "POST"])
def date_form_():
	if request.method == "POST":
		dt7 = request.form.get('get_date')
		cat = request.form.get('category')
		file1 = open("appointment.txt",'r')
		lines = [line[:-1] for line in file1.readlines()]
		file1.close()
		arr = emp_data["Suamya_Agrawal"]
		if cat[-4:] == "view":
			timestamps = create_time_slots(arr, 30)
		elif cat[-4:] == "sion":
			timestamps = create_time_slots(arr, 60)
		else:
			file2 = open("time.txt","r")
			dur = int(file2.read())
			file2.close()
			timestamps = create_time_slots(arr, dur)
		#print(timestamps)
		for x in timestamps:
			#print(x)
			if dt7 + " " + x[0] + " - " + x[1] in lines:
				timestamps.remove(x)
			for y in lines:
				if dt7 == y.split(" ")[0] and (x[0] >= y.split(" ")[1] and x[0] < y.split(" ")[3]):
					timestamps.remove(x)
		#print(timestamps)
		return render_template('calendar1.html',data=timestamps)

@app.route('/set_interview')
def set_interview():
	return render_template('calendar.html')

@app.route('/set_discussion')
def set_discussion():
	return render_template('calendar.html')

@app.route('/set_meeting',methods =["GET", "POST"])
def set_meeting():
	if request.method == "POST":
		time_str = request.form.get('hrmin')
		time_arr = list(map(int,time_str.split(':')))
		dur = time_arr[0] * 60 + time_arr[-1]
		file2 = open("time.txt",'w')
		file2.write(str(dur))
		file2.close()
	return render_template('calendar.html')


if __name__ == '__main__':
	app.run(debug=True)