import streamlit as st 
from db_c import conn,cursor
st.title("Media Platform")

login,signup = st.tabs(
    ["Login","SignUp"]
)

if "user" not in st.session_state:
    st.session_state.user=None

with login:
    st.header("Login")
    with st.form("Login_Form"):
        email = st.text_input("Email")
        password = st.text_input("Password",type="password")
        btn=st.form_submit_button("Login")


with signup:
    st.header("SignUp")

    with st.form("SignUp_Form"):

        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        btn = st.form_submit_button("SignUp")

        if btn:
            query="insert into user2(name,email,password) values (%s,%s,%s)"

            values=(name,email,password)

            cursor.execute(query,values)
            conn.commit()
            st.success("user added successfully..")
            st.session_state.user=True
            st.rerun()

        cursor.execute("show tables")
        tables=cursor.fetchall()
        st.write(tables)



def dashboard():
    st.sidebar.success(f"welcome to Dashboard") 
    opt=st.sidebar.selectbox("choose :-- ",["Dashboard","uploadFiles","Logout"])
    if opt == "Dashboard":
        st.header("Dashboard")
    elif opt == "uploadFiles":
        st.header("uploadFiles")
    elif opt == "Logout":
        st.session_state.user=None 
        st.success("user loggedout successfully")
        st.rerun()       

if st.session_state.user == True :
    pass 
else:
    dashboard()            