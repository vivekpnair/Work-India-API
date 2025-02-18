from datetime import datetime, timedelta
import jwt
from flask import Flask, request, jsonify, redirect, url_for, render_template
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os
import random


app = Flask(__name__)

# Database connection parameters (replace with your actual values)
DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "django_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "django_password")
DB_NAME = os.environ.get("DB_NAME", "irctc_clone_db")

SECRET_KEY = "this is a top secret...shhh"

# Function to jwt token with user ID and expiration time
def generate_token(user_id):
    expiration_time = datetime.utcnow() + timedelta(minutes=10)  # Token expiration in 10 minutes
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration_time
    }, SECRET_KEY, algorithm='HS256')
    return token

# Function to verify the JWT token and decode it to get user data
def verify_token(token):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_data
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def get_logged_in_uid(token):

    if not token:
        return None  # Token is missing
    
    # Remove "Bearer " prefix if it's present
    if token.startswith('Bearer '):
        token = token[7:]
    
    try:
        # Decode the token and verify its validity
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # Extract and return the user_id
        user_id = decoded_token.get('user_id')

        if user_id is None:
            return None  # User ID is not in the token, return None

        return user_id  # Successfully retrieved user_id from the token
    
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    

# Function to connect to the database
def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

# Serve the register page on GET request
@app.route('/register', methods=['GET'])
def serve_register_page():
    return render_template('register.html')  # Ensure register.html is in the templates folder

# Handle register POST request
@app.route('/register', methods=['POST'])
def register():
    try:
        # Extract form data
        name = request.json.get('name')
        password = request.json.get('password')
        mobile = request.json.get('mobile')
        reg_code = None

        # Check if all fields are provided
        if not name or not password or not mobile:
            return jsonify({"error": "All fields are required!"}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)
        # get a random code for reg
        reg_code = random.randint(1000000000, 9999999999)

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the passenger into the database
        cursor.execute(
            "INSERT INTO Passengers (name, password, mobile, reg_code) VALUES (%s, %s, %s, %s)",
            (name, hashed_password, mobile, reg_code)
        )
        conn.commit()
        userid = cursor.lastrowid


        # Close the connection
        cursor.close()
        conn.close()

        return jsonify({
                    "message": "Registration successful!",
                    "redirect": "/home",
                    "uid": userid
                }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve the login page on GET request
@app.route('/login', methods=['GET'])
def serve_login_page():
    return render_template('login.html')  # Ensure login.html is in the templates folder

# Handle login POST request
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # Get form data
        passenger_id = request.json['passenger_id']
        password = request.json['password']

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if passenger exists and fetch the hashed password and isadmin flag
        cursor.execute('SELECT password, isadmin FROM Passengers WHERE passenger_id = %s', (passenger_id,))
        passenger = cursor.fetchone()

        cursor.close()
        conn.close()

        if passenger and check_password_hash(passenger[0], password):
            # Password is correct, generate the JWT token
            token = generate_token(passenger_id)

            # Check if passenger is admin
            if passenger[1]:  # If isadmin is True
                return jsonify({
                    "message": "Login successful!",
                    "redirect": "/admin",
                    "token": token
                }), 200
            else:
                return jsonify({
                    "message": "Login successful!",
                    "redirect": "/home",
                    "token": token
                }), 200
        else:
            # Invalid login attempt, return error message
            return jsonify({"error": "Invalid credentials. Please try again."}), 400

    return render_template('login.html')  # Login form template

@app.route('/home')
def home():
    logged_in_uid = get_logged_in_uid(request.args.get('t'))
    app.logger.info(f"{logged_in_uid}")

    if logged_in_uid is None:
        return redirect(url_for('login'))

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to get reservations for the user
    query = """
        SELECT r.reservation_id, s.seat_number, t.train_name, r.journey_date, 
            s1.station_name AS source, s2.station_name AS destination
        FROM Reservations r
        JOIN Trains t ON r.train_id = t.train_id
        JOIN Seats s ON r.seat_id = s.seat_id
        JOIN Stations s1 ON r.source_station = s1.station_id
        JOIN Stations s2 ON r.destination_station = s2.station_id
        WHERE r.passenger_id = %s
    """

    cursor.execute(query, (logged_in_uid,))
    reservations = cursor.fetchall()
    app.logger.info(f"{reservations}")

    # Close the database connection
    cursor.close()
    conn.close()

    return render_template('home.html', reservations=reservations)

@app.route('/admin')
def admin():
    return render_template('admin.html')  # Admin page template


# Reservation page (GET request)
@app.route('/reserve', methods=['GET'])
def reservation():
    try:
        logged_in_uid = get_logged_in_uid(request.args.get('t'))
        app.logger.info(f"{logged_in_uid}")
        
        if logged_in_uid is None:
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        # Fetch all stations from the database
        cursor.execute("SELECT station_id, station_name FROM Stations")
        stations = cursor.fetchall()
        app.logger.info(f"{stations}")

        # Pass stations to the HTML page for dynamic selection
        return render_template('reservation.html', stations=stations, trains=None)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

# Reservation handling (POST request)
@app.route('/reserve', methods=['POST'])
def find_trains():
    logged_in_uid = get_logged_in_uid(request.form['token'])
    app.logger.info(f"find_trains : {logged_in_uid}")

    if logged_in_uid is None:
        return redirect(url_for('login'))
    
    from_station_id = request.form['from_station']
    to_station_id = request.form['to_station']
    journey_date = request.form['journey_date']
    app.logger.info(f"{journey_date}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        

        # Query to find trains based on the selected 'from_station' and 'to_station'
        cursor.execute("""
            SELECT 
                t.train_id, 
                t.train_number, 
                t.train_name, 
                ts1.arrival_time, 
                ts1.departure_time,
                (ts2.stop_number - ts1.stop_number) AS num_stops,
                COUNT(s.seat_id) - COUNT(r.reservation_id) AS available_seats
            FROM Trains t
            JOIN Train_Stops ts1 ON t.train_id = ts1.train_id
            JOIN Train_Stops ts2 ON t.train_id = ts2.train_id
            JOIN Seats s ON t.train_id = s.train_id
            LEFT JOIN Reservations r ON s.seat_id = r.seat_id AND r.journey_date = %s
            WHERE ts1.station_id = %s
            AND ts2.station_id = %s
            AND ts2.stop_number > ts1.stop_number
            GROUP BY t.train_id, t.train_number, t.train_name, ts1.arrival_time, ts1.departure_time, num_stops;
        """, (journey_date, from_station_id, to_station_id))

        trains = cursor.fetchall()

        # Convert timedelta to HH:MM:SS string format
        cost = 0
        formatted_trains = [
            (train_id, train_number, train_name, str(arrival_time), str(departure_time), cost, available_seats)
            for train_id, train_number, train_name, arrival_time, departure_time, num_stops, available_seats in trains
            for cost in [num_stops * 100]  # simple cost...no of stop * 100 :)
        ]
        cursor.close()
        conn.close()

        # Pass stations and available trains to the HTML page
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT station_id, station_name FROM Stations")
        stations = cursor.fetchall()

        station_dict = dict(stations)
        
        app.logger.info(f"{stations}")
        app.logger.info(f"{formatted_trains}")


        # return render_template('reserve.html', stations=stations, selected_from=selected_from, selected_to=selected_to, trains=trains)

        return render_template('reservation.html',journey_date=journey_date, stations=stations, selected_from=station_dict.get(int(from_station_id)),selected_from_id=from_station_id, selected_to=station_dict.get(int(to_station_id)), selected_to_id=to_station_id, trains=formatted_trains)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    

@app.route('/book', methods=['POST'])
def book_train():
    # Retrieve form data
    logged_in_uid = get_logged_in_uid(request.form['token'])
    app.logger.info(f"book_train : {logged_in_uid}")

    if logged_in_uid is None:
        return redirect(url_for('login'))
    
    train_id = request.form.get('train_id')
    train_number = request.form.get('train_number')
    train_name = request.form.get('train_name')
    arrival_time = request.form.get('arrival_time')
    departure_time = request.form.get('departure_time')
    cost = request.form.get('cost')
    available_seats = request.form.get('available_seats')
    selected_from_id = request.form.get('selected_from_id')
    selected_to_id = request.form.get('selected_to_id')
    journey_date = request.form.get('journey_date')




    # Render the booking page with the train details
    return render_template('book.html', 
                           train_id=train_id, 
                           train_number=train_number, 
                           train_name=train_name, 
                           arrival_time=arrival_time, 
                           departure_time=departure_time,
                           cost=cost,
                           available_seats=available_seats,
                           selected_from_id=selected_from_id,
                           selected_to_id=selected_to_id,
                           journey_date=journey_date)


@app.route('/make_booking', methods=['POST'])
def make_booking():
    
    logged_in_uid = get_logged_in_uid(request.form.get('token'))
    app.logger.info(f"make_booking : {logged_in_uid}")

    if logged_in_uid is None:
        return redirect(url_for('login'))

    train_id = request.form.get('train_id')
    source_station = request.form.get('source_station')
    destination_station = request.form.get('destination_station')
    journey_date = request.form.get('journey_date')

    if not all([logged_in_uid, train_id, source_station, destination_station, journey_date]):
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Find the first available seat
        cursor.execute("""
            SELECT seat_id FROM Seats 
            WHERE train_id = %s AND is_reserved = FALSE 
            LIMIT 1
        """, (train_id,))
        
        seat = cursor.fetchone()

        if not seat:
            return jsonify({"error": "No available seats"}), 400
        
        seat_id = seat['seat_id']

        # Insert into Reservations table
        cursor.execute("""
            INSERT INTO Reservations (train_id, seat_id, passenger_id, journey_date, source_station, destination_station)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (train_id, seat_id, logged_in_uid, journey_date, source_station, destination_station))

        # Mark seat as reserved
        cursor.execute("""
            UPDATE Seats SET is_reserved = TRUE WHERE seat_id = %s
        """, (seat_id,))

        conn.commit()
        return jsonify({"message": "Booking successful", "seat_id": seat_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
