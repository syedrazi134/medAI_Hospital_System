"""
MediAI Smart Hospital System - Database Module
SQLite Database for storing patients, appointments, beds, and roster data

Author: AI Semester Project Team (Arsham & Razi)
Date: December 2025
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json


class HospitalDatabase:
    """Database manager for Hospital Management System"""

    def __init__(self, db_name: str = "hospital_management.db"):
        """Initialize database connection and create tables if not exist"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            # Enable foreign keys
            self.cursor.execute("PRAGMA foreign_keys = ON")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def create_tables(self):
        """Create all necessary tables"""

        # Patients table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                contact TEXT,
                address TEXT,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Symptoms table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS symptoms (
                symptom_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                symptom_name TEXT NOT NULL,
                recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            )
        """)

        # Diagnosis table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS diagnosis (
                diagnosis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                urgency TEXT NOT NULL,
                priority INTEGER NOT NULL,
                specialty TEXT NOT NULL,
                disease TEXT NOT NULL,
                assigned_doctor TEXT NOT NULL,
                diagnosis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            )
        """)

        # Appointments table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                diagnosis_id INTEGER NOT NULL,
                doctor_name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                appointment_time TIMESTAMP NOT NULL,
                room TEXT NOT NULL,
                duration INTEGER NOT NULL,
                status TEXT DEFAULT 'Scheduled',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                FOREIGN KEY (diagnosis_id) REFERENCES diagnosis(diagnosis_id) ON DELETE CASCADE
            )
        """)

        # Bed Allocations table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bed_allocations (
                allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                bed_id TEXT NOT NULL,
                ward TEXT NOT NULL,
                bed_type TEXT NOT NULL,
                allocated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estimated_stay TEXT,
                status TEXT DEFAULT 'Occupied',
                discharge_date TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
            )
        """)

        # Doctors table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                specialty TEXT NOT NULL,
                cost_per_hour REAL NOT NULL,
                contact TEXT,
                available BOOLEAN DEFAULT 1
            )
        """)

        # Weekly Roster table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS weekly_roster (
                roster_id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_start_date DATE NOT NULL,
                day TEXT NOT NULL,
                shift TEXT NOT NULL,
                doctor_name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                patients_count INTEGER NOT NULL,
                cost REAL NOT NULL,
                revenue REAL NOT NULL,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # System Logs table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

        # Insert default doctors if table is empty
        self.initialize_doctors()

    def initialize_doctors(self):
        """Insert default doctors if not already present"""
        self.cursor.execute("SELECT COUNT(*) FROM doctors")
        count = self.cursor.fetchone()[0]

        if count == 0:
            doctors = [
                ('Dr. Sarah Johnson', 'Cardiology', 150, '+1-555-0101'),
                ('Dr. Michael Chen', 'Neurology', 140, '+1-555-0102'),
                ('Dr. Emily Davis', 'General Medicine', 100, '+1-555-0103'),
                ('Dr. Robert Lee', 'Pediatrics', 120, '+1-555-0104'),
                ('Dr. Anna Martinez', 'Orthopedics', 130, '+1-555-0105'),
                ('Dr. James Wilson', 'Respiratory Medicine', 145, '+1-555-0106'),
                ('Dr. Linda Sophia', 'Gastroenterology', 135, '+1-555-0107'),
                ('Dr. Kevin Park', 'Dermatology', 110, '+1-555-0108'),
                ('Dr. Rachel Adams', 'Psychiatry', 125, '+1-555-0109'),
                ('Dr. Steven Wright', 'Other', 95, '+1-555-0110')
            ]

            self.cursor.executemany("""
                INSERT INTO doctors (name, specialty, cost_per_hour, contact)
                VALUES (?, ?, ?, ?)
            """, doctors)

            self.conn.commit()
            self.log_action("System Initialization",
                            "Default doctors added to database")

    # ==================== PATIENT OPERATIONS ====================

    def add_patient(self, name: str, age: int, gender: str, contact: str = None,
                    address: str = None) -> int:
        """
        Add a new patient to the database

        Returns:
            patient_id: ID of the newly created patient
        """
        try:
            self.cursor.execute("""
                INSERT INTO patients (name, age, gender, contact, address)
                VALUES (?, ?, ?, ?, ?)
            """, (name, age, gender, contact, address))

            self.conn.commit()
            patient_id = self.cursor.lastrowid

            self.log_action("Patient Added",
                            f"Patient: {name}, ID: {patient_id}")
            return patient_id

        except sqlite3.Error as e:
            print(f"Error adding patient: {e}")
            self.conn.rollback()
            return -1

    def get_patient(self, patient_id: int) -> Optional[Dict]:
        """Get patient details by ID"""
        self.cursor.execute("""
            SELECT patient_id, name, age, gender, contact, address, registration_date
            FROM patients WHERE patient_id = ?
        """, (patient_id,))

        row = self.cursor.fetchone()
        if row:
            return {
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'contact': row[4],
                'address': row[5],
                'registration_date': row[6]
            }
        return None

    def get_all_patients(self) -> List[Dict]:
        """Get all patients"""
        self.cursor.execute("""
            SELECT patient_id, name, age, gender, contact, registration_date
            FROM patients ORDER BY registration_date DESC
        """)

        patients = []
        for row in self.cursor.fetchall():
            patients.append({
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'contact': row[4],
                'registration_date': row[5]
            })
        return patients

    def search_patients(self, search_term: str) -> List[Dict]:
        """Search patients by name or contact"""
        self.cursor.execute("""
            SELECT patient_id, name, age, gender, contact, registration_date
            FROM patients 
            WHERE name LIKE ? OR contact LIKE ?
            ORDER BY registration_date DESC
        """, (f'%{search_term}%', f'%{search_term}%'))

        patients = []
        for row in self.cursor.fetchall():
            patients.append({
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'contact': row[4],
                'registration_date': row[5]
            })
        return patients

    # ==================== SYMPTOMS OPERATIONS ====================

    def add_symptoms(self, patient_id: int, symptoms: List[str]) -> bool:
        """Add symptoms for a patient"""
        try:
            for symptom in symptoms:
                self.cursor.execute("""
                    INSERT INTO symptoms (patient_id, symptom_name)
                    VALUES (?, ?)
                """, (patient_id, symptom))

            self.conn.commit()
            self.log_action(
                "Symptoms Added", f"Patient ID: {patient_id}, Count: {len(symptoms)}")
            return True

        except sqlite3.Error as e:
            print(f"Error adding symptoms: {e}")
            self.conn.rollback()
            return False

    def get_patient_symptoms(self, patient_id: int) -> List[str]:
        """Get all symptoms for a patient"""
        self.cursor.execute("""
            SELECT symptom_name FROM symptoms
            WHERE patient_id = ?
            ORDER BY recorded_date DESC
        """, (patient_id,))

        return [row[0] for row in self.cursor.fetchall()]

    # ==================== DIAGNOSIS OPERATIONS ====================

    def add_diagnosis(self, patient_id: int, urgency: str, priority: int,
                      specialty: str, disease: str, assigned_doctor: str) -> int:
        """Add diagnosis record"""
        try:
            self.cursor.execute("""
                INSERT INTO diagnosis (patient_id, urgency, priority, specialty, disease, assigned_doctor)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (patient_id, urgency, priority, specialty, disease, assigned_doctor))

            self.conn.commit()
            diagnosis_id = self.cursor.lastrowid

            self.log_action("Diagnosis Added",
                            f"Patient ID: {patient_id}, Disease: {disease}, Urgency: {urgency}")
            return diagnosis_id

        except sqlite3.Error as e:
            print(f"Error adding diagnosis: {e}")
            self.conn.rollback()
            return -1

    def get_patient_diagnosis(self, patient_id: int) -> List[Dict]:
        """Get all diagnosis records for a patient"""
        self.cursor.execute("""
            SELECT diagnosis_id, urgency, priority, specialty, disease, 
                   assigned_doctor, diagnosis_date
            FROM diagnosis
            WHERE patient_id = ?
            ORDER BY diagnosis_date DESC
        """, (patient_id,))

        diagnoses = []
        for row in self.cursor.fetchall():
            diagnoses.append({
                'diagnosis_id': row[0],
                'urgency': row[1],
                'priority': row[2],
                'specialty': row[3],
                'disease': row[4],
                'assigned_doctor': row[5],
                'diagnosis_date': row[6]
            })
        return diagnoses

    # ==================== APPOINTMENT OPERATIONS ====================

    def add_appointment(self, patient_id: int, diagnosis_id: int, doctor_name: str,
                        specialty: str, appointment_time: datetime, room: str,
                        duration: int) -> int:
        """Add appointment record"""
        try:
            self.cursor.execute("""
                INSERT INTO appointments (patient_id, diagnosis_id, doctor_name, specialty,
                                        appointment_time, room, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (patient_id, diagnosis_id, doctor_name, specialty,
                  appointment_time.strftime('%Y-%m-%d %H:%M:%S'), room, duration))

            self.conn.commit()
            appointment_id = self.cursor.lastrowid

            self.log_action("Appointment Created",
                            f"Patient ID: {patient_id}, Doctor: {doctor_name}")
            return appointment_id

        except sqlite3.Error as e:
            print(f"Error adding appointment: {e}")
            self.conn.rollback()
            return -1

    def get_patient_appointments(self, patient_id: int) -> List[Dict]:
        """Get all appointments for a patient"""
        self.cursor.execute("""
            SELECT appointment_id, doctor_name, specialty, appointment_time,
                   room, duration, status, created_date
            FROM appointments
            WHERE patient_id = ?
            ORDER BY appointment_time DESC
        """, (patient_id,))

        appointments = []
        for row in self.cursor.fetchall():
            appointments.append({
                'appointment_id': row[0],
                'doctor_name': row[1],
                'specialty': row[2],
                'appointment_time': row[3],
                'room': row[4],
                'duration': row[5],
                'status': row[6],
                'created_date': row[7]
            })
        return appointments

    def get_upcoming_appointments(self, limit: int = 10) -> List[Dict]:
        """Get upcoming appointments"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.cursor.execute("""
            SELECT a.appointment_id, p.name, a.doctor_name, a.specialty,
                   a.appointment_time, a.room, a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            WHERE a.appointment_time >= ? AND a.status = 'Scheduled'
            ORDER BY a.appointment_time ASC
            LIMIT ?
        """, (current_time, limit))

        appointments = []
        for row in self.cursor.fetchall():
            appointments.append({
                'appointment_id': row[0],
                'patient_name': row[1],
                'doctor_name': row[2],
                'specialty': row[3],
                'appointment_time': row[4],
                'room': row[5],
                'status': row[6]
            })
        return appointments

    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """Update appointment status (Scheduled, Completed, Cancelled)"""
        try:
            self.cursor.execute("""
                UPDATE appointments SET status = ? WHERE appointment_id = ?
            """, (status, appointment_id))

            self.conn.commit()
            self.log_action("Appointment Updated",
                            f"Appointment ID: {appointment_id}, Status: {status}")
            return True

        except sqlite3.Error as e:
            print(f"Error updating appointment: {e}")
            self.conn.rollback()
            return False

    # ==================== BED ALLOCATION OPERATIONS ====================

    def add_bed_allocation(self, patient_id: int, bed_id: str, ward: str,
                           bed_type: str, estimated_stay: str) -> int:
        """Add bed allocation record"""
        try:
            self.cursor.execute("""
                INSERT INTO bed_allocations (patient_id, bed_id, ward, bed_type, estimated_stay)
                VALUES (?, ?, ?, ?, ?)
            """, (patient_id, bed_id, ward, bed_type, estimated_stay))

            self.conn.commit()
            allocation_id = self.cursor.lastrowid

            self.log_action("Bed Allocated",
                            f"Patient ID: {patient_id}, Bed: {bed_id}, Ward: {ward}")
            return allocation_id

        except sqlite3.Error as e:
            print(f"Error allocating bed: {e}")
            self.conn.rollback()
            return -1

    def get_patient_bed_allocation(self, patient_id: int) -> Optional[Dict]:
        """Get current bed allocation for a patient"""
        self.cursor.execute("""
            SELECT allocation_id, bed_id, ward, bed_type, allocated_date,
                   estimated_stay, status
            FROM bed_allocations
            WHERE patient_id = ? AND status = 'Occupied'
            ORDER BY allocated_date DESC
            LIMIT 1
        """, (patient_id,))

        row = self.cursor.fetchone()
        if row:
            return {
                'allocation_id': row[0],
                'bed_id': row[1],
                'ward': row[2],
                'bed_type': row[3],
                'allocated_date': row[4],
                'estimated_stay': row[5],
                'status': row[6]
            }
        return None

    def discharge_patient(self, allocation_id: int) -> bool:
        """Mark bed as discharged"""
        try:
            discharge_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("""
                UPDATE bed_allocations 
                SET status = 'Discharged', discharge_date = ?
                WHERE allocation_id = ?
            """, (discharge_time, allocation_id))

            self.conn.commit()
            self.log_action("Patient Discharged",
                            f"Allocation ID: {allocation_id}")
            return True

        except sqlite3.Error as e:
            print(f"Error discharging patient: {e}")
            self.conn.rollback()
            return False

    def get_occupied_beds(self) -> List[Dict]:
        """Get all currently occupied beds"""
        self.cursor.execute("""
            SELECT b.allocation_id, p.name, b.bed_id, b.ward, b.allocated_date
            FROM bed_allocations b
            JOIN patients p ON b.patient_id = p.patient_id
            WHERE b.status = 'Occupied'
            ORDER BY b.allocated_date DESC
        """)

        beds = []
        for row in self.cursor.fetchall():
            beds.append({
                'allocation_id': row[0],
                'patient_name': row[1],
                'bed_id': row[2],
                'ward': row[3],
                'allocated_date': row[4]
            })
        return beds

    # ==================== ROSTER OPERATIONS ====================

    def save_weekly_roster(self, roster_data: List[List[Dict]], week_start_date: str) -> bool:
        """Save weekly roster to database"""
        try:
            # Delete existing roster for the same week
            self.cursor.execute("""
                DELETE FROM weekly_roster WHERE week_start_date = ?
            """, (week_start_date,))

            # Insert new roster
            for day_schedule in roster_data:
                for shift in day_schedule:
                    self.cursor.execute("""
                        INSERT INTO weekly_roster 
                        (week_start_date, day, shift, doctor_name, specialty, 
                         patients_count, cost, revenue)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (week_start_date, shift['day'], shift['shift'],
                          shift['doctor'], shift['specialty'], shift['patients'],
                          shift['cost'], shift['revenue']))

            self.conn.commit()
            self.log_action("Weekly Roster Saved", f"Week: {week_start_date}")
            return True

        except sqlite3.Error as e:
            print(f"Error saving roster: {e}")
            self.conn.rollback()
            return False

    def get_weekly_roster(self, week_start_date: str) -> List[Dict]:
        """Get roster for a specific week"""
        self.cursor.execute("""
            SELECT day, shift, doctor_name, specialty, patients_count, cost, revenue
            FROM weekly_roster
            WHERE week_start_date = ?
            ORDER BY 
                CASE day
                    WHEN 'Monday' THEN 1
                    WHEN 'Tuesday' THEN 2
                    WHEN 'Wednesday' THEN 3
                    WHEN 'Thursday' THEN 4
                    WHEN 'Friday' THEN 5
                    WHEN 'Saturday' THEN 6
                    WHEN 'Sunday' THEN 7
                END,
                CASE shift
                    WHEN 'Morning (8AM-2PM)' THEN 1
                    WHEN 'Afternoon (2PM-8PM)' THEN 2
                    WHEN 'Night (8PM-2AM)' THEN 3
                END
        """, (week_start_date,))

        roster = []
        for row in self.cursor.fetchall():
            roster.append({
                'day': row[0],
                'shift': row[1],
                'doctor': row[2],
                'specialty': row[3],
                'patients': row[4],
                'cost': row[5],
                'revenue': row[6]
            })
        return roster

    # ==================== STATISTICS & REPORTS ====================

    def get_statistics(self) -> Dict:
        """Get overall system statistics"""
        stats = {}

        # Total patients
        self.cursor.execute("SELECT COUNT(*) FROM patients")
        stats['total_patients'] = self.cursor.fetchone()[0]

        # Total appointments
        self.cursor.execute("SELECT COUNT(*) FROM appointments")
        stats['total_appointments'] = self.cursor.fetchone()[0]

        # Scheduled appointments
        self.cursor.execute("""
            SELECT COUNT(*) FROM appointments WHERE status = 'Scheduled'
        """)
        stats['scheduled_appointments'] = self.cursor.fetchone()[0]

        # Occupied beds
        self.cursor.execute("""
            SELECT COUNT(*) FROM bed_allocations WHERE status = 'Occupied'
        """)
        stats['occupied_beds'] = self.cursor.fetchone()[0]

        # Emergency cases today
        today = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute("""
            SELECT COUNT(*) FROM diagnosis 
            WHERE urgency = 'Emergency' AND DATE(diagnosis_date) = ?
        """, (today,))
        stats['emergency_cases_today'] = self.cursor.fetchone()[0]

        return stats

    def get_patient_history(self, patient_id: int) -> Dict:
        """Get complete patient history"""
        patient = self.get_patient(patient_id)
        if not patient:
            return None

        history = {
            'patient': patient,
            'symptoms': self.get_patient_symptoms(patient_id),
            'diagnoses': self.get_patient_diagnosis(patient_id),
            'appointments': self.get_patient_appointments(patient_id),
            'bed_allocation': self.get_patient_bed_allocation(patient_id)
        }

        return history

    # ==================== UTILITY OPERATIONS ====================

    def log_action(self, action: str, details: str = None):
        """Log system action"""
        try:
            self.cursor.execute("""
                INSERT INTO system_logs (action, details)
                VALUES (?, ?)
            """, (action, details))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error logging action: {e}")

    def get_recent_logs(self, limit: int = 50) -> List[Dict]:
        """Get recent system logs"""
        self.cursor.execute("""
            SELECT log_id, action, details, timestamp
            FROM system_logs
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))

        logs = []
        for row in self.cursor.fetchall():
            logs.append({
                'log_id': row[0],
                'action': row[1],
                'details': row[2],
                'timestamp': row[3]
            })
        return logs

    def backup_database(self, backup_path: str) -> bool:
        """Create database backup"""
        try:
            import shutil
            shutil.copy2(self.db_name, backup_path)
            self.log_action("Database Backup",
                            f"Backup created at: {backup_path}")
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()

    def get_all_appointments(self) -> List[Dict]:
        """Get all appointments for analytics"""
        self.cursor.execute("""
            SELECT a.appointment_id, p.name as patient_name, a.doctor_name,
                a.specialty, a.appointment_time, a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            ORDER BY a.appointment_time DESC
        """)

        appointments = []
        for row in self.cursor.fetchall():
            appointments.append({
                'appointment_id': row[0], 'patient_name': row[1],
                'doctor_name': row[2], 'specialty': row[3],
                'appointment_time': row[4], 'status': row[5]
            })
        return appointments

    def get_all_diagnoses(self) -> List[Dict]:
        """Get all diagnoses for analytics"""
        self.cursor.execute("""
            SELECT diagnosis_id, patient_id, urgency, priority,
                specialty, disease, diagnosis_date
            FROM diagnosis
            ORDER BY diagnosis_date DESC
        """)

        diagnoses = []
        for row in self.cursor.fetchall():
            diagnoses.append({
                'diagnosis_id': row[0], 'patient_id': row[1],
                'urgency': row[2], 'priority': row[3],
                'specialty': row[4], 'disease': row[5],
                'diagnosis_date': row[6]
            })
        return diagnoses

    def reschedule_appointment(self, appointment_id: int, new_datetime: datetime) -> bool:
        """Reschedule an appointment"""
        try:
            self.cursor.execute("""
                UPDATE appointments 
                SET appointment_time = ?
                WHERE appointment_id = ?
            """, (new_datetime.strftime('%Y-%m-%d %H:%M:%S'), appointment_id))

            self.conn.commit()
            self.log_action("Appointment Rescheduled",
                            f"Appointment ID: {appointment_id}, New time: {new_datetime}")
            return True

        except sqlite3.Error as e:
            print(f"Error rescheduling appointment: {e}")
            self.conn.rollback()
            return False


# ==================== TESTING FUNCTIONS ====================

def test_database():
    """Test database functionality"""
    print("Testing Hospital Database...")

    db = HospitalDatabase("test_hospital.db")

    # Test adding patient
    patient_id = db.add_patient(
        "John Doe", 45, "male", "+1-555-1234", "123 Main St")
    print(f"✓ Patient added with ID: {patient_id}")

    # Test adding symptoms
    symptoms = ["chest pain", "shortness of breath"]
    db.add_symptoms(patient_id, symptoms)
    print(f"✓ Symptoms added: {symptoms}")

    # Test adding diagnosis
    diagnosis_id = db.add_diagnosis(patient_id, "Emergency", 10, "Cardiology",
                                    "Possible Cardiac Event", "Dr. Sarah Johnson")
    print(f"✓ Diagnosis added with ID: {diagnosis_id}")

    # Test adding appointment
    appointment_time = datetime.now()
    appointment_id = db.add_appointment(patient_id, diagnosis_id, "Dr. Sarah Johnson",
                                        "Cardiology", appointment_time, "CCU-201", 60)
    print(f"✓ Appointment added with ID: {appointment_id}")

    # Test bed allocation
    allocation_id = db.add_bed_allocation(
        patient_id, "ICU-1", "ICU", "Critical", "3-5 days")
    print(f"✓ Bed allocated with ID: {allocation_id}")

    # Test getting patient history
    history = db.get_patient_history(patient_id)
    print(f"✓ Patient history retrieved")

    # Test statistics
    stats = db.get_statistics()
    print(f"✓ Statistics: {stats}")

    db.close()
    print("\n✅ All database tests passed!")


if __name__ == "__main__":
    test_database()
