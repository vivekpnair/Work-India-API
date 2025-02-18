-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS irctc_clone_db;

-- Use the database
USE irctc_clone_db;

-- Create the Passengers table
CREATE TABLE IF NOT EXISTS Passengers (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    mobile VARCHAR(15) UNIQUE ,
    isadmin BOOLEAN DEFAULT FALSE,
    reg_code VARCHAR(100) NOT NULL
);

-- Create the Trains table
CREATE TABLE IF NOT EXISTS Trains (
    train_id INT AUTO_INCREMENT PRIMARY KEY,
    train_name VARCHAR(100) NOT NULL,
    train_number VARCHAR(20) UNIQUE NOT NULL
);

-- Create the Stations table
CREATE TABLE IF NOT EXISTS Stations (
    station_id INT AUTO_INCREMENT PRIMARY KEY,
    station_name VARCHAR(100) NOT NULL
);

-- Create the Train_Stops table
CREATE TABLE IF NOT EXISTS Train_Stops (
    stop_id INT AUTO_INCREMENT PRIMARY KEY,
    train_id INT,
    station_id INT,
    arrival_time TIME NOT NULL,
    departure_time TIME NOT NULL,
    stop_number INT NOT NULL,
    FOREIGN KEY (train_id) REFERENCES Trains(train_id) ON DELETE CASCADE,
    FOREIGN KEY (station_id) REFERENCES Stations(station_id) ON DELETE CASCADE
);

-- Create the Seats table
CREATE TABLE IF NOT EXISTS Seats (
    seat_id INT AUTO_INCREMENT PRIMARY KEY,
    train_id INT,
    seat_number INT NOT NULL,
    is_reserved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (train_id) REFERENCES Trains(train_id) ON DELETE CASCADE
);

-- Create the Reservations table
CREATE TABLE IF NOT EXISTS Reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    train_id INT,
    seat_id INT,
    passenger_id INT,
    journey_date DATE NOT NULL,
    source_station INT,
    destination_station INT,
    FOREIGN KEY (train_id) REFERENCES Trains(train_id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES Seats(seat_id) ON DELETE CASCADE,
    FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id) ON DELETE CASCADE,
    FOREIGN KEY (source_station) REFERENCES Stations(station_id) ON DELETE CASCADE,
    FOREIGN KEY (destination_station) REFERENCES Stations(station_id) ON DELETE CASCADE
);

-- Insert sample stations
INSERT INTO Stations (station_name) VALUES
('Trivandrum'),
('Kollam'),
('Kayamkulam'),
('Kottayam'),
('Ernakulam'),
('Thrissur'),
('Shoranur'),
('Alleppey'),
('Kozhikode'),
('Kannur'),
('Kasargode'),
('Palakkad'),
('Coimbatore'),
('Arakkonam'),
('Chennai');

-- Insert sample trains
INSERT INTO Trains (train_name, train_number) VALUES
('Venad Express', '16302'),
('Vande Bharat', '20632'),
('Chennai Express', '12696');

-- Insert sample train stops
INSERT INTO Train_Stops (train_id, station_id, arrival_time, departure_time, stop_number) VALUES
(1, 1, '05:30:00', '05:45:00', 1), -- Trivandrum Venad Express (Train 1)
(1, 2, '06:00:00', '06:05:00', 2), -- Kollam
(1, 3, '06:30:00', '06:35:00', 3), -- Kayamkulam
(1, 4, '07:00:00', '07:05:00', 4), -- Kottayam
(1, 5, '07:30:00', '07:35:00', 5), -- Ernakulam
(1, 6, '08:00:00', '08:05:00', 6), -- Thrissur
(1, 7, '08:30:00', '08:35:00', 7), -- Shoranur

(2, 1, '05:30:00', '05:45:00', 1), -- Trivandrum Vande Bharat (Train 2)
(2, 2, '06:00:00', '06:05:00', 2), -- Kollam
(2, 3, '06:30:00', '06:35:00', 3), -- Alleppey
(2, 4, '07:00:00', '07:05:00', 4), -- Ernakulam
(2, 5, '07:30:00', '07:35:00', 5), -- Thrissur
(2, 6, '08:00:00', '08:05:00', 6), -- Shoranur
(2, 7, '08:30:00', '08:35:00', 7), -- Kozhikode
(2, 8, '09:00:00', '09:05:00', 8), -- Kannur
(2, 9, '09:30:00', '09:35:00', 9), -- Kasargode

(3, 1, '05:30:00', '05:45:00', 1), -- Trivandrum Chennai Express (Train 3)
(3, 2, '06:00:00', '06:05:00', 2), -- Kollam
(3, 3, '06:30:00', '06:35:00', 3), -- Alleppey
(3, 4, '07:00:00', '07:05:00', 4), -- Ernakulam
(3, 5, '07:30:00', '07:35:00', 5), -- Thrissur
(3, 6, '08:00:00', '08:05:00', 6), -- Palakkad
(3, 7, '08:30:00', '08:35:00', 7), -- Coimbatore
(3, 8, '09:00:00', '09:05:00', 8), -- Arakkonam
(3, 9, '09:30:00', '09:35:00', 9); -- Chennai

-- Insert seats for all trains (1-30 seats for each train)
-- Insert seats for Venad Express (Train 1)
INSERT INTO Seats (train_id, seat_number) VALUES 
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), 
(1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), 
(1, 21), (1, 22), (1, 23), (1, 24), (1, 25), (1, 26), (1, 27), (1, 28), (1, 29), (1, 30);

-- Insert seats for Vande Bharat (Train 2)
INSERT INTO Seats (train_id, seat_number) VALUES 
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), 
(2, 11), (2, 12), (2, 13), (2, 14), (2, 15), (2, 16), (2, 17), (2, 18), (2, 19), (2, 20), 
(2, 21), (2, 22), (2, 23), (2, 24), (2, 25), (2, 26), (2, 27), (2, 28), (2, 29), (2, 30);

-- Insert seats for Chennai Express (Train 3)
INSERT INTO Seats (train_id, seat_number) VALUES 
(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), 
(3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 19), (3, 20), 
(3, 21), (3, 22), (3, 23), (3, 24), (3, 25), (3, 26), (3, 27), (3, 28), (3, 29), (3, 30);
