from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}

#Example code from template

# @app.route("/about", methods=['POST'])
# def about():
#     return render_template('www.intellipaat.com')


# @app.route("/addemp", methods=['POST'])
# def AddEmp():
#     emp_id = request.form['emp_id']
#     first_name = request.form['first_name']
#     last_name = request.form['last_name']
#     pri_skill = request.form['pri_skill']
#     location = request.form['location']
#     emp_image_file = request.files['emp_image_file']

#     insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
#     cursor = db_conn.cursor()

#     if emp_image_file.filename == "":
#         return "Please select a file"

#     try:

#         cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
#         db_conn.commit()
#         emp_name = "" + first_name + " " + last_name
#         # Uplaod image file in S3 #
#         emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
#         s3 = boto3.resource('s3')

#         try:
#             print("Data inserted in MySQL RDS... uploading image to S3...")
#             s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
#             bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
#             s3_location = (bucket_location['LocationConstraint'])

#             if s3_location is None:
#                 s3_location = ''
#             else:
#                 s3_location = '-' + s3_location

#             object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
#                 s3_location,
#                 custombucket,
#                 emp_image_file_name_in_s3)

#         except Exception as e:
#             return str(e)

#     finally:
#         cursor.close()

#     print("all modification done...")
#     return render_template('AddEmpOutput.html', name=emp_name)





# Home page
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('StudentSignUp.html')

# START CODING HERE

#------------------------------------------------------------------------------Student Sign Up(Jia Shun)
students = {}
# Redirect index
@app.route('/')
def toIndex():
    return render_template('index.html')

# Redirect index (signup)
@app.route('/')
def toStdSignUp():
    return render_template('StudentSignUp.html')

# Redirect to login
@app.route('/StudLoginPage')
def toStdLogin():
    return render_template('StudLogin.html')
    
# Redirect to StudentHomePage
@app.route('/StudHomePage')
def toStdHomePage():
    return render_template('StudentHomePage.html')

# Redirect to StudentHomePage
@app.route('/StudViewCompany')
def toStdViewCompPage():
    return render_template('StudentViewCompany.html')

    
#----------------------------------------------------------------------------global variable

student_id = ""
std_company_id = ""
std_cmpDetails = ""
std_jobDetails = ""



#-----------------------------------------------------------------------------
#database route

@app.route('/studentsignup', methods=['GET', 'POST'])
def signup():
    student_id = request.form.get('std_id')
    first_name = request.form.get('std_first_name')
    last_name = request.form.get('std_last_name')
    password = request.form.get('std_pass')
    confirm_password = request.form.get('confirm_std_pass')
    intern_status = "None"

    # Check if passwords match
    if password != confirm_password:
        return "Password confirmation does not match."

    # Store student data in the dictionary
    students[student_id] = {
        'first_name': first_name,
        'last_name': last_name,
        'password': password
    }
    insert_sql = "INSERT INTO studentInformation VALUES (%s, %s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (student_id, first_name, last_name, password))
    db_conn.commit()
    cursor.close()

    return render_template('StudLogin.html')


#------------------------------------------------------------signin

# Student login function
@app.route('/studlogin', methods=['GET', 'POST'])
def signin_page():
    # return render_template('StudLogin.html')
    global student_id  # Declare student_id as a global variable if not already declared globally
    student_id = request.form.get('std_lg_id')
    password = request.form.get('std_lg_pass')

    select_stmt = "SELECT std_password FROM studentInformation WHERE std_id =%s"
    cursor = db_conn.cursor()
    cursor.execute(select_stmt, (student_id))
    dbPassword = cursor.fetchcall()
    cursor.close()

    
    cursor = db_conn.cursor()
    cursor.execute('SELECT comp_id, comp_name FROM company')
    std_cmpDetails = cursor.fetchcall()
    cursor.close()

    cursor = db_conn.cursor()
    cursor.execute('SELECT job_name FROM internship')
    std_jobDetails = cursor.fetchcall()
    cursor.close()

    global std_cmpDetails
    global std_jobDetails


    # Check if the student exists in the dictionary (for demonstration purposes)
    if dbPassword == password:
        return f"Welcome, Student with ID {student_id}!"
        return render_template('StudentHomePage.html', std_cmpDetails = std_cmpDetails, std_jobDetails = std_jobDetails)
    else:
        return "Invalid student ID or password."

    



    #------------------------StudentHome Page

    # Student home function
@app.route('/std_homepage', methods=['GET', 'POST'])
def std_home_page():
    global std_company_id
    std_company_id = request.form.get('cmp_id')
    

    search_cmp = "SELECT comp_name, comp_industry, comp_address FROM company WHERE comp_id=%s"
    cursor = db_conn.cursor()
    cursor.execute(search_cmp, (company_id))
    cmpdetails = cursor.fetchcall()
    cursor.close()

    search_intern = "SELECT job_id, job_name, job_description FROM internship WHERE comp_id=%s"
    cursor = db_conn.cursor()
    cursor.execute(search_intern, (company_id))   
    std_internDetails = cursor.fetchcall()
    cursor.close()

    return render_template('StudentViewCompany.html', cmpdetails = cmpdetails, std_internDetails = std_internDetails)



        #------------------------Student View Company Page

    # Student apply intern function
@app.route('/stdapplyintern', methods=['GET', 'POST'])
def std_viewCompany(cmp_id):
    
    global std_cmpDetails
    global std_jobDetails

    global student_id

    global company_id

    search_cmp = "SELECT comp_name FROM company WHERE comp_id=%s"
    cursor = db_conn.cursor()
    cursor.execute(search_cmp, (company_id))
    cmpName = cursor.fetchcall()
    cursor.close()

    company_name = cmpName
    intern_status = "pending"



    apply_intern = "INSERT INTO student VALUES (%s, %s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(apply_intern, (student_id, company_id, company_name, intern_status))
    db_conn.commit()
    cursor.close()

    

    return render_template('StudentHomePage.html', std_cmpDetails = std_cmpDetails, std_jobDetails = std_jobDetails)

            #------------------------Student View Profile Page

    # Student View Profile function
@app.route('/viewProfile', methods=['GET', 'POST'])
def std_viewCompany(cmp_id):
    
    global student_id

    search_cmp = "SELECT std_first_name, std_last_name FROM studentInformation WHERE std_id=%s"
    cursor = db_conn.cursor()
    cursor.execute(search_cmp, (student_id))
    stdInfor = cursor.fetchcall()
    cursor.close()

    

    search_cmp = "SELECT * FROM student"
    cursor = db_conn.cursor()
    cursor.execute(search_cmp)
    cmpName = cursor.fetchcall()
    cursor.close()

    return render_template('StudentProfile.html', stdInfor = stdInfor, student_id = student_id, cmpName = cmpName)


     #------------------------ Profile Page

    # Student Upload forder function
# @app.route('/viewProfile', methods=['GET', 'POST'])
# def std_viewCompany(cmp_id):

#     std_letter_file = request.files['std_letter_A']
#     std_form_file = request.files['std_letter_B']

#         # if std_letter_file.filename == "" or std_form_file.filename == "":
#         #   return "Please select a file"


    
#         #Uplaod image file in S3 #
#         std_letter_file = "std-id-" + str(global student id) + "_letter_file"
#         std_form_file = "std-id-" + str(global student id) + "_form_file"
#         s3 = boto3.resource('s3')

#         try:
#             # Upload the first file (std_letter_file)
#             print(f"Uploading {std_letter_file} to S3...")
#             s3.upload_file(std_letter_file, custombucket, std_letter_file)
#             print(f"{std_letter_file} uploaded successfully!")

#             # Upload the second file (std_form_file)
#             print(f"Uploading {std_form_file} to S3...")
#             s3.upload_file(std_form_file, custombucket, std_form_file)
#             print(f"{std_form_file} uploaded successfully!")

#             # Get the S3 bucket location
#             bucket_location = s3.get_bucket_location(Bucket=custombucket)
#             s3_location = bucket_location.get('LocationConstraint', '')

#             # Construct URLs for both files
#             letter_object_url = f"https://s3{s3_location}.amazonaws.com/{custombucket}/{std_letter_file}"
#             form_object_url = f"https://s3{s3_location}.amazonaws.com/{custombucket}/{std_form_file}"

#         except Exception as e:
#             return str(e) 
    


    return render_template('StudentProfile.html', student_id = student_id, cmpName = cmpName)





#-------------------------------------------------------------------------------------------------------






# Company sign up
company = {}

# @app.route('/')
# def index():
#     return render_template('CompanyRegister.html')

# @app.route("/companyregister", methods=['POST'])
# def signup():
#     company_id = request.form.get('comp_id')
#     company_name = request.form.get('comp_name')
#     company_industry = request.form.get('comp_industry')
#     company_password = request.form.get('comp_password')
#     company_confirm_password = request.form.get('comp_confirm_password')
#     company_address = request.form.get('comp_address')

#     # Check if password matches
#     if company_password !=company_confirm_password:
#         return "Password does not match"
    
#     # Store company data
#     company[company_id] {

#         'company_name' : company_name,
#         'company_industry' : company_industry,
#         'company_password' : company_password,
#         'company_address' : company_address
#     }

#     return f"Company {company_name} have signed up successfully!"





# END OF CODING
# Establish connection
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)