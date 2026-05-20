import streamlit as st 
from db_c import conn,cursor
st.title("Media Platform")

login,signup = st.tabs(
    ["Login","SignUp"]
)

if "user" not in st.session_state:
    st.session_state.user=None

def login_function():
    st.header("Login")
    with st.form("Login_Form"):
        email = st.text_input("Email")
        password = st.text_input("Password",type="password")
        btn=st.form_submit_button("Login")

        if btn:
            query="select * from users2 where email=%s and password=%s"
            values=(email,password)
            cursor.execute(query,values)
            loggedin_user=cursor.fetchone()
            st.write(f"welcome {loggedin_user["name"]}")
            st.session_state.user =True
            st.rerun()

def signup_function():
    st.header("SignUp")

    with st.form("SignUp_Form"):

        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        btn = st.form_submit_button("SignUp")

        if btn:
            query="insert into users2(name,email,password) values (%s,%s,%s)"

            values=(name,email,password)

            cursor.execute(query,values)
            conn.commit()
            st.success("user added successfully..")


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

if st.session_state.user is None :
    with signup:
        signup_function()
    with login:
        login_function()    
else:
    dashboard()            