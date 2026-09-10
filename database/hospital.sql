pip install -r requirements.txt
CREATE DATABASE hospital_appointment;

USE hospital_appointment;

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hospitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    department VARCHAR(100) NOT NULL,
    location VARCHAR(150),
    description TEXT
);

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    hospital_id INT,
    experience INT DEFAULT 0,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
);

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status VARCHAR(30) DEFAULT 'Confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

INSERT INTO hospitals
(name, department, location, description)
VALUES
('The Eye Foundation', 'Eye', 'Madurai',
 'Specialized eye care hospital'),

('Aravind Eye Hospital', 'Eye', 'Madurai',
 'Eye care and ophthalmology services'),

('Zaara Dental', 'Dental', 'Madurai',
 'Dental care and treatment'),

('Velammal Hospital', 'Cardiology', 'Madurai',
 'Cardiology and multispecialty services'),

('Velammal Hospital', 'Neurology', 'Madurai',
 'Neurology specialist services');


INSERT INTO doctors
(name, specialization, hospital_id, experience)
VALUES
('Dr. Arun Kumar', 'Ophthalmologist', 1, 10),
('Dr. Priya', 'Ophthalmologist', 2, 8),
('Dr. Meena', 'Dentist', 3, 7),
('Dr. Rajesh', 'Cardiologist', 4, 12),
('Dr. Kumar', 'Neurologist', 5, 15);
