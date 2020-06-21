from flask import Flask,request,jsonify
from flask_restful import Api,Resource
import sqlite3

app = Flask(__name__)
api = Api(app)

conn = sqlite3.connect("students_data.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS students (student_id int(11) NOT NULL,student_fname varchar(100) NOT NULL,student_lname varchar(100) NOT NULL,gender varchar(1) NOT NULL,class varchar(11) NOT NULL,dob date NOT NULL, PRIMARY KEY(student_id))")
cur.execute("CREATE TABLE IF NOT EXISTS student_attendance_map(id int(11) NOT NULL,attendance_date date NOT NULL,status char(1) NOT NULL,remarks varchar(1000) DEFAULT NULL,student_id int(10) NOT NULL,updated_by varchar(50) NOT NULL,updated_on timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (id),CONSTRAINT student_atts FOREIGN KEY (student_id) REFERENCES students (student_id))")
conn.commit()
conn.close()

class insert_val_in_students(Resource):
    def post(self):
        conn = sqlite3.connect("students_data.db")
        cur = conn.cursor()
        data = request.get_json()
        student_id = data['student_id']
        student_fname = data['student_fname']
        student_lname = data['student_lname']
        gender = data['gender']
        stud_class = data['class']
        dob = data['dob']
        cur.execute("INSERT INTO students values(?,?,?,?,?,?)",(student_id,student_fname,student_lname,gender,stud_class,dob))
        conn.commit()
        conn.close()
        ret_json = {
            'Message' : "Value has been added",
            "Status Code": 200
        }
        return jsonify(ret_json)

class insert_val_in_attendance(Resource):
    def post(self):
        conn = sqlite3.connect("students_data.db")
        cur = conn.cursor()
        data = request.get_json()
        att_id = data['id']
        attendance_date = data['attendance_date']
        status = data['status']
        remarks = data['remarks']
        stud_id = data['student_id']
        updated_by = data['updated_by']
        updated_on = data['updated_on']
        cur.execute("INSERT INTO student_attendance_map values(?,?,?,?,?,?,?)",(att_id,attendance_date,status,remarks,stud_id,updated_by,updated_on))
        conn.commit()
        conn.close()
        ret_json = {
            'Message' : "Value has been added",
            "Status Code": 200
        }
        return jsonify(ret_json)

class update_attendance(Resource):
    def post(self):
        conn = sqlite3.connect("students_data.db")
        cur = conn.cursor()
        data = request.get_json()
        attendance_date = data['attendance_date']
        status = data['status']
        stud_id = data['student_id']
        cur.execute("UPDATE student_attendance_map SET status={} where attendance_date={} and student_id={}".format(status,attendance_date,stud_id))
        conn.commit()
        conn.close()
        ret_json = {
            'Message' : "Attendance has been updated.",
            "Status Code": 200
        }
        return jsonify(ret_json)


class get_students_by_class(Resource):
    def post(self):
        conn = sqlite3.connect("students_data.db")
        cur = conn.cursor()
        data = request.get_json()
        class_of_student = data['class']
        cur.execute("SELECT student_fname,student_lname from students where class={}".format(class_of_student))
        rows = cur.fetchall()
        dicts = {}
        if len(rows) == 0:
            dicts = {
                "Message": "There is no entry in the sql table",
                "Status Code": 500
            }
        for i in range(len(rows)):
            dicts['stud' + str(i+1)] = rows[i][0] + rows[i][1]
            dicts['Status Code'] = 200
        conn.commit()
        conn.close()
        return jsonify(dicts)

class get_attendace_by_date(Resource):
    def post(self):
        conn = sqlite3.connect("students_data.db")
        cur = conn.cursor()
        data = request.get_json()
        dates = data['attendance_date']
        cur.execute("Select status from student_attendance_map where attendance_date = {}".format(dates))
        rows = cur.fetchall()
        dicts = {}
        if len(rows) == 0:
            dicts = {
                "Message": "There is no entry in the sql table",
                "Status Code": 500
            }
        for i in range(len(rows)):
            dicts['Attendance'] = rows[i][0]
            dicts['Status Code'] = 200
        conn.commit()
        conn.close()
        return jsonify(dicts)


api.add_resource(get_students_by_class,"/get_by_class")
api.add_resource(insert_val_in_students,"/insert_stud")
api.add_resource(get_attendace_by_date,"/get_attendance")
api.add_resource(insert_val_in_attendance,"/insert_att")
api.add_resource(update_attendance,"/update_attendance")