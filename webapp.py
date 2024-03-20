import streamlit as st
import re
import sqlite3 
import pickle
import pandas as pd
import bz2

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()


menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice=="Home":
    st.subheader("Welcome To covid_19 Prediction System")
    
    
if choice=="Login":
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password",type="password")
    b1=st.sidebar.checkbox("Login")
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            if Email=='a@a.com' and Password=='123':
                st.success("Logged In as {}".format("Admin"))
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)
            else:
                if login_user(Email,Password):
                    menu2 = ["K-Nearest Neighbors", "SVM",
                             "Decision Tree", "Random Forest",
                             "Naive Bayes","ExtraTreesClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)

                    USMER=int(st.slider('Usmer', 1, 2))
                    MEDICAL_UNIT=int(st.slider('Medical_unit', 1, 13))
                    SEX=int(st.slider('sex', 1, 2))
                    PATIENT_TYPE=int(st.slider('Patient_type', 1, 2))
                    INTUBED=int(st.slider('Intubed', 1, 99))
                    PNEUMONIA=int(st.slider('Pneumonia',1, 99))
                    AGE=int(st.slider('Age',0, 121))
                    PREGNANT =int(st.slider('Pregnant',1, 98))
                    COPD=int(st.slider('COPD',1, 98))
                    DIABETES =int(st.slider('Diabetes',1, 98))
                    ASTHMA =int(st.slider('Asthma',1, 98))
                    INMSUPR =int(st.slider('Inmsupr',1, 98))
                    HIPERTENSION =int(st.slider('Hipertension',1, 98))
                    OTHER_DISEASE =int(st.slider('Other_disease',1, 98))
                    CARDIOVASCULAR =int(st.slider('Cardiovascular',1, 98))
                    OBESITY =int(st.slider('Obesity',1, 98))
                    RENAL_CHRONIC =int(st.slider('Renal_chronic',1, 98))
                    TOBACCO =int(st.slider('Tobacco',1, 98))
                    ICU=int(st.slider('Icu',1, 98))
                    my_array=[USMER,MEDICAL_UNIT,SEX,PATIENT_TYPE,INTUBED,
                              PNEUMONIA,AGE,PREGNANT,DIABETES,COPD,ASTHMA,INMSUPR,HIPERTENSION,
                              OTHER_DISEASE,CARDIOVASCULAR,OBESITY,RENAL_CHRONIC,TOBACCO,ICU] 
                    b2=st.button("Predict")
                    sfile = bz2.BZ2File('model.pkl', 'rb')
                    model=pickle.load(sfile)                               
                    if b2:     
                        tdata=[my_array]
                        #st.write(tdata)
                        if choice2=="K-Nearest Neighbors":
                            test_prediction = model[0].predict(tdata)  
                            query=test_prediction[0]
                            #st.success(query)
                        if choice2=="SVM":
                            test_prediction = model[1].predict(tdata)
                            query=test_prediction[0]
                            #st.success(query)                 
                        if choice2=="Decision Tree":
                            test_prediction = model[2].predict(tdata)
                            query=test_prediction[0]
                            #st.success(query)
                        if choice2=="Random Forest":
                            test_prediction = model[3].predict(tdata)
                            query=test_prediction[0]
                            #st.success(query)
                        if choice2=="Naive Bayes":
                            test_prediction = model[4].predict(tdata)
                            query=test_prediction[0]
                            #st.success(query)
                        if choice2=="ExtraTreesClassifier":
                             test_prediction = model[5].predict(tdata)
                             query=test_prediction[0]
                             #st.success(query)
                        if str(query)=="1":
                            st.error("Covid Positive")
                        else:
                            st.success("Covid Negative")
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
                
           
if choice=="SignUp":
    Fname = st.text_input("First Name")
    Lname = st.text_input("Last Name")
    Mname = st.text_input("Mobile Number")
    Email = st.text_input("Email")
    City = st.text_input("City")
    Password = st.text_input("Password",type="password")
    CPassword = st.text_input("Confirm Password",type="password")
    b2=st.button("SignUp")
    if b2:
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if Password==CPassword:
            if (pattern.match(Mname)):
                if re.fullmatch(regex, Email):
                    create_usertable()
                    add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")         
            else:
                st.warning("Not Valid Mobile Number")
        else:
            st.warning("Pass Does Not Match")
            
        

    