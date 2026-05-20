import streamlit as st 
from db_c import conn,cursor
import cloudinary
import cloudinary.uploader


cloudinary.config(
    cloud_name=st.secrets["c_database"],
    api_key= st.secrets["c_api_key"],
    api_secret=st.secrets["c_password"]
)

st.title("Media Platform")

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
            st.session_state.user =loggedin_user
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
    opt=st.sidebar.selectbox("choose :-- ",["Dashboard","uploadFiles","viewFiles","Logout"])
    if opt == "Dashboard":
        st.header("Dashboard")
    elif opt == "uploadFiles":
        st.header("uploadFiles")
        u_file=st.file_uploader("upload file",type=["pdf","jpg","jpeg","png","mp3","mp4"])

        if u_file :
            st.success("file selected successfully..")

            st.write("file_name",u_file.name)
            st.write("file_type",u_file.type)
            st.write("file_name",u_file.size)

            if u_file.type == "application/pdf":
                st.info("Pdf file uploaded")
            elif "image" in u_file.type:
                st.image(u_file,width=300)
            elif "video" in u_file.type:
                st.video(u_file)  
            elif "audio" in u_file.type:
                st.audio(u_file) 

            if st.button("Upload to Cloudinary"):

                with st.spinner("Uploading..."):

                    uploaded_file = cloudinary.uploader.upload(
                    u_file,
                    resource_type="auto"
                    )

                    file_url = uploaded_file["secure_url"]
                    query = "insert into files2(file_name,file_type,file_url) values(%s,%s,%s)"
                    values = (u_file.name,u_file.type,file_url)
                    cursor.execute(query,values)

                    conn.commit()

                    st.success(
                    "File Uploaded Successfully"
                    )

                    st.code(file_url)


    elif opt == "viewFiles":

        st.header("View Files")

        # ---------------- FETCH FILES ----------------

        query = """
        SELECT * FROM files2
        ORDER BY upload_date DESC
        """

        cursor.execute(query)

        files = cursor.fetchall()
        print(files)


        if len(files)  == 0:
            st.error("no files in db")
        else:
            for file in files:

            st.write("---")

            st.write(
                "File Name:",
                file["file_name"]
            )

            st.write(
                "File Type:",
                file["file_type"]
            )

            file_url = file["file_url"]

            # ---------------- IMAGE ----------------

            if "image" in file["file_type"]:

                st.image(
                    file_url,
                    width=300
                )

            # ---------------- VIDEO ----------------

            elif "video" in file["file_type"]:

                st.video(file_url)

            # ---------------- AUDIO ----------------

            elif "audio" in file["file_type"]:

                st.audio(file_url)

            # ---------------- PDF ----------------

            elif "pdf" in file["file_type"]:

                st.link_button(
                    "Open PDF",
                    file_url
                )

            # ---------------- URL ----------------

            st.code(file_url)    


    elif opt == "Logout":
        st.session_state.user=None 
        st.success("user loggedout successfully")
        st.rerun()       

if st.session_state.user is None :

    login,signup = st.tabs(
    ["Login","SignUp"]
    )

    with signup:
        signup_function()
    with login:
        login_function()    
else:
    dashboard()            