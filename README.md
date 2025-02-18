# IRCTC Clone Project

This project is a very simple basic clone of the IRCTC website.

## How to Run

This project is built using Docker containers for easy setup and execution.

### Technologies Used
- Frontend/Middleware : Python Flask
- Backend Database : MySQL

### Steps to Run the Project

1. Copy the Project Folder :
   - Copy the entire folder to your desired location.

2. Run the Docker Command :
   - Open a terminal in the folder location and run the following command:
     ```bash
     docker-compose up --build
     ```
   - This will:
     - Create a MySQL database container.
     - Create a Python Flask app server container.

3. Access the Application:
   - Register a user by visiting: [http://localhost:5000/register](http://localhost:5000/register).
   - Once registered, log in using your `User ID` and `Password` to make reservations.
   - The home page can be accessed at: [http://localhost:5000/home](http://localhost:5000/home).

---

### Notes
- Ensure Docker is installed and running on your system.
- If you encounter any issues, make sure the required ports (`5000` for Flask and `3306` for MySQL) are not already in use.

Enjoy using the IRCTC Clone!
