from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("students_data.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS students (student_id int(11) NOT NULL,student_fname varchar(100) NOT NULL,student_lname varchar(100) NOT NULL,gender varchar(1) NOT NULL,class varchar(11) NOT NULL,dob date NOT NULL, PRIMARY KEY(student_id))")
cur.execute("CREATE TABLE IF NOT EXISTS student_attendance_map(id int(11) NOT NULL,attendance_date date NOT NULL,status char(1) NOT NULL,remarks varchar(1000) DEFAULT NULL,student_id int(10) NOT NULL,updated_by varchar(50) NOT NULL,updated_on timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (id),CONSTRAINT student_atts FOREIGN KEY (student_id) REFERENCES students (student_id))")
conn.commit()
conn.close()


@app.route('/')
def hello():
    return "Hello there!"


# route to add data in the students table through this api


# @app.route('/students_table', methods=['POST'])
# def insert_val_in_Stud():
#     conn = sqlite3.connect("students_data.db")
#     cur = conn.cursor()
#     data = request.get_json()
#     student_id = data['student_id']
#     student_fname = data['student_fname']
#     student_lname = data['student_lname']
#     gender = data['gender']
#     stud_class = data['class']
#     dob = data['dob']
#     cur.execute("INSERT INTO students values(?,?,?,?,?,?)", (student_id,
#                                                              student_fname, student_lname, gender, stud_class, dob))
#     conn.commit()
#     conn.close()
#     ret_json = {
#         'Message': "Value has been added",
#         "Status Code": 200
#     }
#     return jsonify(ret_json)


# The below code is used to add attendance to the student_attendance map


@app.route('/attendance_table', methods=['POST'])
def insert_val_in_att():
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
    cur.execute("INSERT INTO student_attendance_map values(?,?,?,?,?,?,?)",
                (att_id, attendance_date, status, remarks, stud_id, updated_by, updated_on))
    conn.commit()
    conn.close()
    ret_json = {
        'Message': "Value has been added",
        "Status Code": 200
    }
    return jsonify(ret_json)


# The below code is used to get students by class


@app.route('/get_students/<string:class_of_student>', methods=['GET'])
def get_student_by_class(class_of_student):
    conn = sqlite3.connect("students_data.db")
    cur = conn.cursor()
    #data = request.get_json()
    #class_of_student = data['class']
    cur.execute("SELECT student_fname,student_lname from students where class={}".format(
        class_of_student))
    rows = cur.fetchall()
    dicts = {}
    if len(rows) == 0:
        dicts = {
            "Message": "There is no entry in the sql table",
            "Status Code": 500
        }
        return jsonify(dicts)
    for i in range(len(rows)):
        dicts['stud' + str(i+1)] = rows[i][0] + rows[i][1]
    dicts['Status Code'] = 200
    conn.commit()
    conn.close()
    return jsonify(dicts)


# The below code is used to get udpade attendance of a student on a particular date


@app.route('/update/<string:attendance_date>', methods=['PUT'])
def update_attendace(attendance_date):
    conn = sqlite3.connect("students_data.db")
    cur = conn.cursor()
    data = request.get_json()
    attendance_date = "'" + attendance_date + "'"
    #attendance_date = data['attendance_date']
    status_ = "'" + data['status'] + "'"
    stud_id = data['student_id']
    cur.execute("UPDATE student_attendance_map SET status={} where attendance_date={} and student_id={}".format(
        status_, attendance_date, stud_id))
    conn.commit()
    conn.close()
    ret_json = {
        'Message': "Attendance has been updated.",
        "Status Code": 200
    }
    return jsonify(ret_json)


# Get the attendance for a given date


@app.route('/get_attendance/<string:dates>', methods=['GET'])
def get_attendance(dates):
    conn = sqlite3.connect("students_data.db")
    cur = conn.cursor()
    #data = request.get_json()
    #dates = data['attendance_date']
    dates = "'" + dates + "'"
    cur.execute(
        "Select student_id,status from student_attendance_map where attendance_date={}".format(str(dates)))
    rows = cur.fetchall()
    dicts = {}
    if len(rows) == 0:
        dicts = {
            "Message": "There is no entry in the sql table",
            "Status Code": 500
        }
        return jsonify(dicts)
    for i in range(len(rows)):
        dicts['student id ' + str(rows[i][0])] = rows[i][1]
    dicts['Status Code'] = 200
    conn.commit()
    conn.close()
    return jsonify(dicts)


if __name__ == "__main__":
    app.run(debug=True)
