# 🏥 Hospital Online Appointment System

## 📌 Project Overview

The Hospital Online Appointment System is a web-based healthcare application designed to simplify the process of finding hospitals, doctors, and booking medical appointments online.

The project was developed as a UI/UX and software project based on the hospital appointment workflow designed during the internship.

## 🎯 Objectives

* Reduce manual appointment booking.
* Reduce patient waiting time.
* Provide easy doctor and hospital search.
* Allow patients to book appointments online.
* Maintain appointment history.
* Provide an AI-assisted appointment experience.

## ✨ Features

* Patient registration
* Patient login
* Hospital search
* Department-based search
* Doctor search
* Doctor details
* Online appointment booking
* Appointment history
* Appointment cancellation
* AI appointment assistant
* Responsive user interface

## 🤖 AI Appointment Assistant

The AI assistant accepts natural-language requests such as:

> "I need a heart specialist."

The system identifies the required department, searches doctors from the database, and displays suitable doctors with an option to book an appointment.

### AI Workflow

```text
User Request
     ↓
Intent Detection
     ↓
Department Identification
     ↓
Doctor Search
     ↓
Availability
     ↓
Doctor Recommendation
     ↓
Appointment Booking
```

## 🛠️ Technologies

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

### Backend

* Python
* Flask

### Database

* MySQL

### UI/UX

* Figma
* Balsamiq
* Canva

## 📂 Project Modules

1. Authentication Module
2. Patient Module
3. Hospital Module
4. Doctor Module
5. Appointment Module
6. AI Assistant Module
7. Database Module

## 🗃️ Database

The application uses MySQL tables for:

* Patients
* Hospitals
* Doctors
* Appointments

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hospital-online-appointment.git
```

### 2. Open the project

```bash
cd hospital-online-appointment
```

### 3. Create virtual environment

```bash
python -m venv venv
```

### 4. Activate environment – Windows

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Create MySQL database

Open MySQL and run:

```text
database/hospital.sql
```

### 7. Configure database

Update the database configuration in `config.py`.

### 8. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 👩‍💻 Project Author

**I. Afrin Sahana**

Computer Science and Engineering

## 📄 Project Documentation

The internship report is available in the `docs` folder.

## 🔮 Future Enhancements

* Real LLM-based Agentic AI
* Voice-based appointment booking
* Tamil language support
* SMS/email reminders
* Online payment
* Telemedicine
* Hospital queue prediction
* Multi-agent healthcare workflow
* Cloud deployment
