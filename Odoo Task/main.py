import streamlit as st
import mysql.connector
import bcrypt

# Connect to MySQL database
db = mysql.connector.connect(
    host="your_host",
    user="your_user",
    password="your_password",
    database="your_database"
)
cursor = db.cursor()

# Function to hash passwords
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# Function to check if username exists
def username_exists(username):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    return cursor.fetchone() is not None

# Streamlit app
def main():
    st.title("Login Registration App")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            query = "SELECT password FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                hashed_password = result[0].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    st.success("Logged in as {}".format(username))
                else:
                    st.warning("Incorrect username or password")
            else:
                st.warning("Incorrect username or password")

    elif choice == "Register":
        st.subheader("Register")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Register"):
            if username_exists(new_username):
                st.warning("Username already exists. Please choose another.")
            else:
                hashed_password = hash_password(new_password)
                insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(insert_query, (new_username, hashed_password))
                db.commit()
                st.success("Successfully registered. You can now login.")

if __name__ == "__main__":
    main()
