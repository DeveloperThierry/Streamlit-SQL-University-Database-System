import streamlit as st
import pymysql

conn = pymysql.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"],
    port=st.secrets["mysql"]["port"]
)
cursor = conn.cursor()


def register():
    st.header("📝 Register Student")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    dob = st.date_input("Date of Birth")
    address = st.text_input("Address")
    phone = st.text_input("Phone Number")

    if st.button("Register"):
        try:
            cursor.execute("""
                INSERT INTO student (first_name, last_name, email, password, date_of_birth, address, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, email, password, dob, address, phone))
            conn.commit()
            student_id = cursor.lastrowid
            st.success(f"✅ Registration successful! Your Student ID is: {student_id}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def login():
    st.header("🔐 Student Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM student WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        if user:
            st.success(f"✅ Welcome, {user[1]} {user[2]}!")
            st.write("Your Student ID:", user[0])
        else:
            st.error("❌ Invalid email or password.")


def update_student():
    st.header("✏️ Update Student Info")
    student_id = st.number_input("Enter Student ID to Update", min_value=1, step=1)

    if st.button("Load Student Info"):
        cursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
        user = cursor.fetchone()

        if user:
            st.session_state["update_data"] = {
                "first_name": user[1],
                "last_name": user[2],
                "address": user[3],
                "phone_number": user[4],
                "email": user[5],
                "dob": str(user[6])
            }
        else:
            st.error("❌ Student not found.")

    if "update_data" in st.session_state:
        st.subheader("Update Fields Below")

        new_first = st.text_input("First Name", value=st.session_state["update_data"]["first_name"])
        new_last = st.text_input("Last Name", value=st.session_state["update_data"]["last_name"])
        new_address = st.text_input("Address", value=st.session_state["update_data"]["address"])
        new_phone = st.text_input("Phone", value=st.session_state["update_data"]["phone_number"])

        if st.button("Update Info"):
            try:
                cursor.execute("""
                    UPDATE student 
                    SET first_name = %s, last_name = %s, address = %s, phone_number = %s
                    WHERE student_id = %s
                """, (new_first, new_last, new_address, new_phone, student_id))
                conn.commit()

                if cursor.rowcount:
                    st.success("✅ Student information updated successfully!")
                    del st.session_state["update_data"]  # Clear after update
                else:
                    st.warning("⚠️ No changes made.")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")



def delete_student():
    st.header("🗑️ Delete Student")
    student_id = st.number_input("Enter Student ID to Delete", min_value=1, step=1)

    if st.button("Delete"):
        try:
            cursor.execute("DELETE FROM student WHERE student_id = %s", (student_id,))
            conn.commit()
            if cursor.rowcount:
                st.success("✅ Student deleted successfully!")
            else:
                st.warning("⚠️ No student found with that ID.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")



def view_students():
    st.header("📄 All Registered Students")
    cursor.execute("SELECT student_id, first_name, last_name, email FROM student")
    data = cursor.fetchall()

    if data:
        for row in data:
            st.write(f"🧑 ID: {row[0]}, Name: {row[1]} {row[2]}, Email: {row[3]}")
    else:
        st.info("No students found.")


st.sidebar.title("Thierry Tech University System")
option = st.sidebar.radio("Choose Action", ["Register", "Login", "Update Student", "Delete Student", "View All Students"])

if option == "Register":
    register()
elif option == "Login":
    login()
elif option == "Update Student":
    update_student()
elif option == "Delete Student":
    delete_student()
elif option == "View All Students":
    view_students()

