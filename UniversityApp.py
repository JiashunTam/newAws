from flask import Flask, render_template, request, session
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

# Set a secret key for your Flask application
app.secret_key = 'never_gonna_give_you_up_never_gonna_let_you_down_never_gonna_run_around_and_hurt_you'  # Replace with a long and secure secret key

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
    return render_template('StudLogin.html')

# START CODING HERE

#------------------------------------------------------------------------------Student Sign Up(Jia Shun)
students = {}
# # Redirect index
# @app.route('/toIndex')
# def toIndex():
#     return render_template('index.html')

# Redirect index (signup)
@app.route('/toStdSignUp')
def toStdSignUp():
    return render_template('StudentSignUp.html')

# Redirect to login
@app.route('/toStdLogin')
def toStdLogin():
    return render_template('StudLogin.html')
    
# Redirect to StudentHomePage
@app.route('/toStdHomePage')
def toStdHomePage():
    return render_template('StudentHomePage.html')

# Redirect to StudentHomePage
@app.route('/toStdViewCompPage')
def toStdViewCompPage():
    return render_template('StudentViewCompany.html')

# Redirect to StudentHomePage
@app.route('/toStdViewProfilePage')
def toStdViewProfilePage():
    return render_template('StudentProfile.html')

    
#----------------------------------------------------------------------------global variable

student_id = ""
student_password = ""
std_company_id = ""
std_cmpDetails = ""
std_jobDetails = ""



#-----------------------------------------------------------------------------
#database route

@app.route('/studentsignup', methods=['GET', 'POST'])
def signup():
    global student_password
    student_id = request.form.get('std_id')
    first_name = request.form.get('std_first_name')
    last_name = request.form.get('std_last_name')
    student_password = request.form.get('std_pass')
    confirm_password = request.form.get('confirm_std_pass')


    # Check if passwords match
    if student_password != confirm_password:
        return "Password confirmation does not match."

    # Store student data in the dictionary
    students[student_id] = {
        'first_name': first_name,
        'last_name': last_name,
        'password': student_password
    }
    insert_sql = "INSERT INTO studentInformation VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (student_id, first_name, last_name, student_password, ""))
    db_conn.commit()
    cursor.close()

    return render_template('StudLogin.html')


#------------------------------------------------------------signin

# Student login function
@app.route('/studlogin', methods=['GET'])
def student_signin():

    

    cursor = db_conn.cursor()
    cursor.execute("SELECT std_id, std_pass FROM studentInformation")
    dbPassword = cursor.fetchall()
    cursor.close()

    student_id = request.args.get('std_lg_id')
    password = request.args.get('std_lg_pass')
    
  

    show_job = "SELECT comp_id, job_id, job_name, job_description FROM internship"
    cursor = db_conn.cursor()
    cursor.execute(show_job)
    jobName = cursor.fetchall()
    cursor.close()


    if student_id and password:
        for row in dbPassword:
            if row[0] == student_id and row[1] == password:
                # session['std_id'] = student_id  # Store student_id in the session for future uses
                session['student_id'] = student_id  
                return render_template('StudentHomePage.html', jobName = jobName, student_id = student_id)
        
        # If none of the rows matched, return an error message
        return "Wrong username or password"
    
    # If student_id or password is missing, return an error message
    return "Please provide both username and password"



    #------------------------StudentHome Page

    # Student home function
@app.route('/std_homepage', methods=['GET', 'POST'])
def std_home_page():
    student_id = session.get('student_id')
    std_company_id = request.form.get('cmp_id')
    session['std_company_id'] = std_company_id 
    

    search_cmp = "SELECT comp_name, comp_industry, comp_address FROM company WHERE comp_id=%s"
    cursor = db_conn.cursor()
    cursor.execute(search_cmp, (std_company_id))
    cmpdetails = cursor.fetchall()
    cursor.close()


    return render_template('StudentViewCompany.html', cmpdetails = cmpdetails, student_id = student_id, std_company_id = std_company_id)



        #------------------------Student View Company Page

    # Student apply intern function
@app.route('/stdapplyintern', methods=['GET', 'POST'])
def std_viewCompany():
    student_id = session.get('student_id')
    std_company_id = session.get('std_company_id')
  

    search_cmp = "SELECT comp_name FROM company WHERE comp_id=%s"
    cursor = db_conn.cursor()
    cursor.execute(search_cmp, (std_company_id))
    cmpName = cursor.fetchall()
    cursor.close()

    company_name = cmpName[0]
    intern_status = "pending"




    apply_intern = "INSERT INTO student VALUES (%s, %s, %s, %s ,%s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(apply_intern, (student_id, std_company_id, company_name, intern_status, "", ""))
    db_conn.commit()
    cursor.close()


    

    return "You are succeessful to apply!"

            #------------------------Student View Profile Page

    # Student View Profile function
@app.route('/viewProfile', methods=['GET', 'POST'])
def std_viewProfile():
    student_id = session.get('student_id')

    std_company_id = session.get('std_company_id')


    search_std_name = "SELECT std_first_name, std_last_name FROM studentInformation WHERE std_id=%s"
    cursor = db_conn.cursor()
    cursor.execute(search_std_name, (student_id))
    stdInfor = cursor.fetchall()
    cursor.close()

    

    search_cmp = "SELECT cmp_name, intern_status FROM student WHERE std_id =%s"
    cursor = db_conn.cursor()
    cursor.execute(search_cmp, (student_id))
    cmpName = cursor.fetchall()
    cursor.close()

    return render_template('StudentProfile.html', stdInfor = stdInfor, student_id = student_id, cmpName = cmpName, std_company_id = std_company_id)


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
    


    # return render_template('StudentProfile.html', student_id = student_id, cmpName = cmpName)


    @app.route('/studentprofile', methods=['GET', 'POST'])
    def student_upload_file():
    # Retrieve company_log_id from the session
            global student_id

 
            std_letter_file = request.files.get('std_letter_A')
            std_form_file = request.files.get('std_letter_B')
      

            student_file_nameA = str(student_id) + "_" + std_letter_file + ".pdf"
            student_file_nameB = str(student_id) + "_" + std_form_file + ".pdf"

            



            if student_file_nameA == "":
                return "ples selec a file"

            try:
                apply_intern = "INSERT INTO student VALUES (%s, %s, %s, %s，%s, %s)"
                cursor = db_conn.cursor()
                cursor.execute(apply_intern, ("", "", "", "", student_file_nameA, student_file_nameB))
                db_conn.commit()
                cursor.close()
                # Upload image file in S3 
                student_letter_in_s3 = student_file_nameA, student_file_nameB
                s3 = boto3.resource('s3')

                try:
                    print("Data inserted...Uploaded to S3")
                    s3.Bucket(custombucket).put_object(Key=student_letter_in_s3, Body=std_letter)
                    bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
                    s3_location = (bucket_location['LocationConstraint'])

                    if s3_location is None:
                        s3_location = ''
                    else: 
                        s3_location = '-' + s3_location

                    object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                    s3_location,
                    custombucket,
                    student_letter_in_s3)


                except Exception as e:
                    return str(e)

            except Exception as e:
                return str(e)

            finally:
                cursor.close()

            return "Letter posted successfully!"

    # Render the template and pass the company_log_id and show_company_id to it
    return render_template('StudentProfile.html')





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