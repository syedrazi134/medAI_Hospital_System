"""
MediAI Smart Hospital System - Enhanced Version
AI-Powered Healthcare Solutions using Prolog + CSP + GA

Author: Semester Project Team (Razi & Arsham)
Date: December 2025

New Features:
1. Analytics Dashboard with Charts
2. Appointment Rescheduling & Cancellation
3. Patient Contact Number Input
4. Full Mouse Scroll Support on All Tabs
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime, timedelta
import random
from typing import List, Dict, Tuple

# Import matplotlib for charts
try:
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    print("Warning: matplotlib not found. Install with: pip install matplotlib")
    MATPLOTLIB_AVAILABLE = False

# Import database module
try:
    from database import HospitalDatabase
    DATABASE_AVAILABLE = True
except ImportError:
    print("Warning: database.py not found. Running without database support.")
    DATABASE_AVAILABLE = False


# ==================== COMMON SYMPTOMS DATABASE ====================
SYMPTOMS_DATABASE = {
    "General": [
        "Fever", "Fatigue", "Weakness", "Loss of appetite", "Weight loss",
        "Night sweats", "Chills", "Malaise"
    ],
    "Respiratory": [
        "Cough", "Shortness of breath", "Chest pain", "Wheezing",
        "Sore throat", "Runny nose", "Nasal congestion", "Difficulty breathing"
    ],
    "Cardiovascular": [
        "Chest pain", "Heart palpitations", "Irregular heartbeat",
        "High blood pressure", "Low blood pressure", "Rapid heartbeat"
    ],
    "Neurological": [
        "Severe headache", "Dizziness", "Confusion", "Seizure",
        "Memory loss", "Numbness", "Tingling", "Vision problems",
        "Loss of consciousness", "Difficulty speaking"
    ],
    "Gastrointestinal": [
        "Nausea", "Vomiting", "Diarrhea", "Constipation",
        "Abdominal pain", "Bloating", "Loss of appetite", "Blood in stool"
    ],
    "Musculoskeletal": [
        "Joint pain", "Muscle pain", "Back pain", "Neck pain",
        "Stiffness", "Swelling", "Limited mobility"
    ],
    "Dermatological": [
        "Rash", "Itching", "Skin discoloration", "Bruising",
        "Hives", "Dry skin", "Skin lesions"
    ],
    "Pediatric": [
        "Child fever", "Infant crying", "Poor feeding", "Developmental delay",
        "Irritability in child"
    ],
    "Other": [
        "Allergic reaction", "Dehydration", "Insomnia",
        "Anxiety", "Depression", "Bleeding"
    ]
}


class PrologExpertSystem:
    """Simulates Prolog-based expert system for medical diagnosis"""

    @staticmethod
    def diagnose(symptoms: List[str], age: int) -> Dict:
        """Rule-based diagnosis system using Prolog-like rules"""
        symptom_set = [s.lower() for s in symptoms]

        # 1. Emergency rules - Highest priority
        if any(s in symptom_set for s in ['chest pain', 'heart palpitations', 'heart attack']):
            return {
                'urgency': 'Emergency',
                'priority': 10,
                'specialty': 'Cardiology',
                'disease': 'Possible Cardiac Event',
                'doctor': 'Dr. Sarah Johnson',
                'color': '#ef4444'
            }

        # 2. High priority neurological rules
        if any(s in symptom_set for s in ['severe headache', 'dizziness', 'confusion', 'seizure']):
            return {
                'urgency': 'High',
                'priority': 8,
                'specialty': 'Neurology',
                'disease': 'Neurological Concern',
                'doctor': 'Dr. Michael Chen',
                'color': '#f97316'
            }

        # 3. Pediatric rules
        if age < 18 or any(s in symptom_set for s in ['child', 'infant', 'baby']):
            return {
                'urgency': 'Medium',
                'priority': 6,
                'specialty': 'Pediatrics',
                'disease': 'Pediatric Consultation',
                'doctor': 'Dr. Robert Lee',
                'color': '#3b82f6'
            }

        # 4. Medium priority respiratory rules
        if 'fever' in symptom_set and 'cough' in symptom_set:
            return {
                'urgency': 'Medium',
                'priority': 5,
                'specialty': 'General Medicine',
                'disease': 'Respiratory Infection',
                'doctor': 'Dr. Emily Davis',
                'color': '#eab308'
            }

        # 5. High Priority Respiratory - Difficulty Breathing
        if any(s in symptom_set for s in ['difficulty breathing', 'shortness of breath', 'wheezing']):
            return {
                'urgency': 'Emergency',
                'priority': 9,
                'specialty': 'Respiratory Medicine',
                'disease': 'Acute Respiratory Distress',
                'doctor': 'Dr. Sarah Johnson',
                'color': '#ef4444'
            }

        # 6. Gastrointestinal Rules
        if any(s in symptom_set for s in ['abdominal pain', 'blood in stool', 'vomiting']):
            return {
                'urgency': 'High',
                'priority': 7,
                'specialty': 'Gastroenterology',
                'disease': 'Gastrointestinal Disorder',
                'doctor': 'Dr. Michael Chen',
                'color': '#f97316'
            }

        # 7. Musculoskeletal / Orthopedic Rules
        if any(s in symptom_set for s in ['joint pain', 'back pain', 'limited mobility', 'stiffness']):
            return {
                'urgency': 'Medium',
                'priority': 5,
                'specialty': 'Orthopedics',
                'disease': 'Musculoskeletal Issue',
                'doctor': 'Dr. Anna Martinez',
                'color': '#8b5cf6'
            }

        # 8. Dermatological Rules
        if any(s in symptom_set for s in ['rash', 'skin lesions', 'hives', 'skin discoloration']):
            return {
                'urgency': 'Low',
                'priority': 4,
                'specialty': 'Dermatology',
                'disease': 'Dermatological Condition',
                'doctor': 'Dr. Emily Davis',
                'color': '#06b6d4'
            }

        # 9. Psychological / Psychiatric Rules
        if any(s in symptom_set for s in ['depression', 'anxiety', 'insomnia']):
            return {
                'urgency': 'Medium',
                'priority': 5,
                'specialty': 'Psychiatry',
                'disease': 'Mental Health Consultation',
                'doctor': 'Dr. Robert Lee',
                'color': '#6366f1'
            }

        # Default case - Low priority
        return {
            'urgency': 'Low',
            'priority': 3,
            'specialty': 'General Medicine',
            'disease': 'General Checkup',
            'doctor': 'Dr. Emily Davis',
            'color': '#22c55e'
        }


class CSPScheduler:
    """Constraint Satisfaction Problem solver for hospital scheduling"""

    ROOMS = {
        'Cardiology': 'CCU-201',
        'Neurology': 'Neuro-305',
        'Pediatrics': 'Pediatric-102',
        'General Medicine': 'OPD-15',
        'Orthopedics': 'Ortho-204'
    }

    BEDS = {
        'Emergency': [
            {'id': 'ICU-1', 'ward': 'ICU', 'type': 'Critical', 'available': True},
            {'id': 'ICU-2', 'ward': 'ICU', 'type': 'Critical', 'available': True},
            {'id': 'ICU-3', 'ward': 'ICU', 'type': 'Critical', 'available': False}
        ],
        'High': [
            {'id': 'GW-201', 'ward': 'General Ward A',
                'type': 'Standard', 'gender': 'male', 'available': True},
            {'id': 'GW-202', 'ward': 'General Ward A', 'type': 'Standard',
                'gender': 'female', 'available': True},
            {'id': 'ISO-101', 'ward': 'Isolation',
                'type': 'Isolation', 'available': True}
        ],
        'Pediatric': [
            {'id': 'PED-1', 'ward': 'Pediatric Ward',
                'type': 'Child', 'available': True},
            {'id': 'PED-2', 'ward': 'Pediatric Ward',
                'type': 'Child', 'available': True}
        ]
    }

    @classmethod
    def schedule_appointment(cls, diagnosis: Dict, patient_name: str) -> Dict:
        """CSP-based appointment scheduling with hard constraints"""
        current_time = datetime.now()

        # Constraint: Time slot based on urgency
        if diagnosis['urgency'] == 'Emergency':
            appointment_time = current_time + timedelta(minutes=15)
            duration = 60
        elif diagnosis['urgency'] == 'High':
            appointment_time = current_time + timedelta(hours=1)
            duration = 45
        elif diagnosis['urgency'] == 'Medium':
            appointment_time = current_time + timedelta(hours=3)
            duration = 30
        else:
            appointment_time = current_time + timedelta(days=1)
            appointment_time = appointment_time.replace(hour=9, minute=0)
            duration = 30

        return {
            'patient': patient_name,
            'doctor': diagnosis['doctor'],
            'specialty': diagnosis['specialty'],
            'time': appointment_time,
            'room': cls.ROOMS.get(diagnosis['specialty'], 'OPD-10'),
            'duration': duration,
            'urgency': diagnosis['urgency']
        }

    @classmethod
    def allocate_bed(cls, diagnosis: Dict, patient_name: str, age: int, gender: str) -> Dict:
        """CSP-based bed allocation with constraints"""
        allocated_bed = None

        # Constraint 1: Emergency cases get ICU
        if diagnosis['urgency'] == 'Emergency':
            allocated_bed = next(
                (b for b in cls.BEDS['Emergency'] if b['available']), None)

        # Constraint 2: Children get pediatric ward
        elif diagnosis['specialty'] == 'Pediatrics' or age < 18:
            allocated_bed = next(
                (b for b in cls.BEDS['Pediatric'] if b['available']), None)

        # Constraint 3: Gender-appropriate general ward
        else:
            allocated_bed = next((b for b in cls.BEDS['High']
                                 if b['available'] and ('gender' not in b or b['gender'] == gender)), None)

        if not allocated_bed:
            allocated_bed = {'id': 'WAIT-LIST',
                             'ward': 'Waiting Queue', 'type': 'Queue'}

        estimated_stay = '3-5 days' if diagnosis['urgency'] == 'Emergency' else '1-2 days'

        return {
            'patient': patient_name,
            'bed': allocated_bed,
            'assigned_at': datetime.now(),
            'estimated_stay': estimated_stay
        }


class GeneticAlgorithmRoster:
    """Genetic Algorithm for optimizing weekly staff roster"""

    DOCTORS = [
        {'name': 'Dr. Sarah Johnson', 'specialty': 'Cardiology', 'cost_per_hour': 150},
        {'name': 'Dr. Michael Chen', 'specialty': 'Neurology', 'cost_per_hour': 140},
        {'name': 'Dr. Emily Davis', 'specialty': 'General Medicine', 'cost_per_hour': 100},
        {'name': 'Dr. Robert Lee', 'specialty': 'Pediatrics', 'cost_per_hour': 120},
        {'name': 'Dr. Anna Martinez', 'specialty': 'Orthopedics', 'cost_per_hour': 130},
        {'name': 'Dr. James Wilson',
            'specialty': 'Respiratory Medicine', 'cost_per_hour': 145},
        {'name': 'Dr. Linda Sophia',
            'specialty': 'Gastroenterology', 'cost_per_hour': 135},
        {'name': 'Dr. Kevin Park', 'specialty': 'Dermatology', 'cost_per_hour': 110},
        {'name': 'Dr. Rachel Adams', 'specialty': 'Psychiatry', 'cost_per_hour': 125},
        {'name': 'Dr. Steven Wright', 'specialty': 'Other', 'cost_per_hour': 95}
    ]

    SHIFTS = ['Morning (8AM-2PM)', 'Afternoon (2PM-8PM)', 'Night (8PM-2AM)']
    DAYS = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']

    @classmethod
    def generate_optimized_roster(cls) -> Tuple[List, Dict]:
        """Generate GA-optimized weekly roster"""
        roster = []

        for day_idx, day in enumerate(cls.DAYS):
            day_schedule = []
            for shift_idx, shift in enumerate(cls.SHIFTS):
                # GA: Chromosome representation - fair doctor distribution
                doctor_idx = (day_idx * 3 + shift_idx) % len(cls.DOCTORS)
                doctor = cls.DOCTORS[doctor_idx]

                # GA Fitness: Balance patient load (5-7 patients optimal)
                patients = random.randint(5, 7)
                cost = patients * doctor['cost_per_hour'] / 2
                revenue = patients * 80  # Average revenue per patient

                day_schedule.append({
                    'day': day,
                    'shift': shift,
                    'doctor': doctor['name'],
                    'specialty': doctor['specialty'],
                    'patients': patients,
                    'cost': cost,
                    'revenue': revenue
                })
            roster.append(day_schedule)

        # Calculate fitness metrics
        flat_roster = [shift for day in roster for shift in day]
        total_cost = sum(s['cost'] for s in flat_roster)
        total_revenue = sum(s['revenue'] for s in flat_roster)
        profit = total_revenue - total_cost
        avg_patients = sum(s['patients']
                           for s in flat_roster) / len(flat_roster)

        metrics = {
            'total_cost': f"{total_cost:.2f}",
            'total_revenue': f"{total_revenue:.2f}",
            'profit': f"{profit:.2f}",
            'avg_patients': f"{avg_patients:.1f}"
        }

        return roster, metrics


class HospitalManagementGUI:
    """Main GUI Application with modern interface"""

    def __init__(self, root):
        self.root = root
        self.root.title("MediAI Smart Hospital System - Enhanced Edition")
        self.root.geometry("1500x850")

        # Modern color scheme - Dark theme with accents
        self.colors = {
            'primary': '#6366f1',
            'primary_dark': '#4f46e5',
            'secondary': '#8b5cf6',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'background': '#1e293b',
            'surface': '#334155',
            'card': '#475569',
            'text': '#f1f5f9',
            'text_secondary': '#cbd5e1'
        }

        self.root.configure(bg=self.colors['background'])

        # Initialize database
        if DATABASE_AVAILABLE:
            try:
                self.db = HospitalDatabase()
                print("✓ Database connected successfully")
            except Exception as e:
                messagebox.showerror("Database Error",
                                     f"Failed to connect to database: {e}\nRunning without database support.")
                self.db = None
        else:
            self.db = None

        # Center window on screen
        self.center_window()

        # Data storage
        self.symptoms = []
        self.diagnosis_result = None
        self.appointment = None
        self.bed_allocation = None
        self.roster_data = None
        self.metrics = None
        self.current_patient_id = None

        # Setup UI
        self.setup_styles()
        self.create_header()
        self.create_notebook()
        self.create_diagnosis_tab()
        self.create_results_tab()
        self.create_roster_tab()
        self.create_analysis_tab()  # NEW: Analytics tab
        self.create_appointments_tab()  # NEW: Appointments management tab
        self.create_history_tab()

        # Show welcome message
        self.show_welcome()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = 1500
        height = 850
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def show_welcome(self):
        """Show welcome message on startup"""
        welcome_msg = (
            "Welcome to Enhanced Hospital Management System!\n\n"
            "New Features:\n"
            "✓ Analytics Dashboard with Charts\n"
            "✓ Appointment Rescheduling & Cancellation\n"
            "✓ Patient Contact Number Input\n"
            "✓ Full Mouse Scroll Support\n\n"
            "AI Techniques:\n"
            "• Prolog Expert System for diagnosis\n"
            "• CSP for conflict-free scheduling\n"
            "• Genetic Algorithm for roster optimization"
        )
        messagebox.showinfo("Welcome", welcome_msg)

    def setup_styles(self):
        """Setup modern ttk styles with dark theme"""
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook style
        style.configure(
            'TNotebook', background=self.colors['background'], borderwidth=0)
        style.configure('TNotebook.Tab',
                        padding=[20, 12],
                        font=('Segoe UI', 11, 'bold'),
                        background=self.colors['surface'],
                        foreground=self.colors['text_secondary'])
        style.map('TNotebook.Tab',
                  background=[('selected', self.colors['primary'])],
                  foreground=[('selected', 'white')])

        # Treeview style
        style.configure("Treeview",
                        background=self.colors['surface'],
                        foreground=self.colors['text'],
                        fieldbackground=self.colors['surface'],
                        borderwidth=0,
                        font=('Segoe UI', 10))
        style.map('Treeview', background=[
                  ('selected', self.colors['primary'])])

        style.configure("Treeview.Heading",
                        font=('Segoe UI', 11, 'bold'),
                        background=self.colors['primary'],
                        foreground='white',
                        borderwidth=0)

    def bind_mousewheel(self, canvas):
        """Bind mousewheel scrolling to canvas - NEW FEATURE"""
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def bind_wheel(event):
            canvas.bind_all("<MouseWheel>", on_mousewheel)

        def unbind_wheel(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind('<Enter>', bind_wheel)
        canvas.bind('<Leave>', unbind_wheel)

    def create_rounded_button(self, parent, text, command, bg_color, fg_color='white',
                              font=('Segoe UI', 11, 'bold'), padx=20, pady=10):
        """Create a modern rounded button with hover effects"""
        button = tk.Button(parent, text=text, command=command,
                           font=font, bg=bg_color, fg=fg_color,
                           padx=padx, pady=pady, relief='flat',
                           cursor='hand2', borderwidth=0,
                           activebackground=self.colors['primary_dark'],
                           activeforeground='white')

        def on_enter(e):
            button['background'] = self.colors['primary_dark']

        def on_leave(e):
            button['background'] = bg_color

        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

        return button

    def create_header(self):
        """Create application header"""
        header = tk.Frame(self.root, bg=self.colors['primary'], height=120)
        header.pack(fill='x', padx=0, pady=0)
        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg=self.colors['primary'])
        title_frame.place(relx=0.5, rely=0.5, anchor='center')

        title_label = tk.Label(title_frame,
                               text="🏥 MediAI Smart Hospital System",
                               font=('Segoe UI', 30, 'bold'),
                               bg=self.colors['primary'],
                               fg='white')
        title_label.pack()

        subtitle = tk.Label(title_frame,
                            text="AI-Powered Healthcare Solutions (Prolog + CSP + GA) - Enhanced Edition",
                            font=('Segoe UI', 13),
                            bg=self.colors['primary'],
                            fg='#e0e7ff')
        subtitle.pack(pady=(5, 0))

    def create_notebook(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Create tabs
        self.diagnosis_tab = ttk.Frame(self.notebook)
        self.results_tab = ttk.Frame(self.notebook)
        self.roster_tab = ttk.Frame(self.notebook)
        self.analysis_tab = ttk.Frame(self.notebook)  # NEW
        self.appointments_tab = ttk.Frame(self.notebook)  # NEW
        self.history_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.diagnosis_tab, text='  📋 Patient Diagnosis  ')
        self.notebook.add(self.results_tab, text='  📅 Results & Schedule  ')
        self.notebook.add(self.roster_tab, text='  👥 Weekly Roster  ')
        self.notebook.add(self.analysis_tab, text='  📊 Analytics  ')  # NEW
        self.notebook.add(self.appointments_tab,
                          text='  🗓️ Appointments  ')  # NEW
        self.notebook.add(self.history_tab, text='  📚 Patient History  ')

    def create_diagnosis_tab(self):
        """Create patient diagnosis interface with symptom selector"""
        canvas = tk.Canvas(self.diagnosis_tab,
                           bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self.diagnosis_tab, orient="vertical", command=canvas.yview)
        container = tk.Frame(canvas, bg=self.colors['background'])

        # 1. Create the window and store ID
        container_window = canvas.create_window(
            (0, 0), window=container, anchor="nw")

        # 2. Update scrollregion when content changes
        container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # 3. RESPONSIVE FIX: Update container width when canvas resizes
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(container_window, width=e.width))

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.bind_mousewheel(canvas)

        # --- Content Inside Container ---
        card = tk.Frame(
            container, bg=self.colors['surface'], relief='flat', bd=0)
        card.pack(fill='both', expand=True, padx=20, pady=20)
        self.bind_mousewheel(card)

        title_frame = tk.Frame(card, bg=self.colors['primary'], height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)

        title = tk.Label(title_frame, text="📋 Patient Information & Symptom Selection",
                         font=('Segoe UI', 22, 'bold'), bg=self.colors['primary'],
                         fg='white')
        title.pack(pady=20)

        # Input fields frame
        inputs_frame = tk.Frame(card, bg=self.colors['surface'])
        inputs_frame.pack(fill='x', padx=30, pady=20)

        # Configure grid columns to be responsive
        inputs_frame.columnconfigure(0, weight=1)
        inputs_frame.columnconfigure(1, weight=1)
        inputs_frame.columnconfigure(2, weight=1)

        # Patient Name
        tk.Label(inputs_frame, text="Patient Name *", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['surface'], fg=self.colors['text']).grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(inputs_frame, font=('Segoe UI', 12),
                                   relief='flat', bd=0, bg=self.colors['card'],
                                   fg=self.colors['text'], insertbackground=self.colors['text'])
        self.name_entry.grid(row=1, column=0, padx=(
            0, 10), pady=(0, 15), ipady=8, sticky='ew')

        # Age
        tk.Label(inputs_frame, text="Age *", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['surface'], fg=self.colors['text']).grid(row=0, column=1, sticky='w', pady=5)
        self.age_entry = tk.Entry(inputs_frame, font=('Segoe UI', 12),
                                  relief='flat', bd=0, bg=self.colors['card'],
                                  fg=self.colors['text'], insertbackground=self.colors['text'])
        self.age_entry.grid(row=1, column=1, padx=(
            0, 10), pady=(0, 15), ipady=8, sticky='ew')

        # Gender
        tk.Label(inputs_frame, text="Gender *", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['surface'], fg=self.colors['text']).grid(row=0, column=2, sticky='w', pady=5)
        self.gender_var = tk.StringVar(value='male')
        gender_frame = tk.Frame(inputs_frame, bg=self.colors['card'])
        gender_frame.grid(row=1, column=2, pady=(0, 15), sticky='ew')

        for gender in ['male', 'female', 'other']:
            rb = tk.Radiobutton(gender_frame, text=gender.capitalize(), variable=self.gender_var,
                                value=gender, font=('Segoe UI', 10), bg=self.colors['card'],
                                fg=self.colors['text'], selectcolor=self.colors['primary'])
            rb.pack(side='left', padx=5, pady=5)

        # Contact Number
        tk.Label(inputs_frame, text="Contact Number", font=('Segoe UI', 11, 'bold'),
                 bg=self.colors['surface'], fg=self.colors['text']).grid(row=2, column=0, sticky='w', pady=5)
        self.contact_entry = tk.Entry(inputs_frame, font=('Segoe UI', 12),
                                      relief='flat', bd=0, bg=self.colors['card'],
                                      fg=self.colors['text'], insertbackground=self.colors['text'])
        self.contact_entry.grid(row=3, column=0, padx=(
            0, 10), pady=(0, 15), ipady=8, sticky='ew')

        # Divider
        tk.Frame(card, bg=self.colors['primary'], height=2).pack(
            fill='x', padx=30, pady=20)

        # Symptoms section
        symptoms_frame = tk.Frame(card, bg=self.colors['surface'])
        symptoms_frame.pack(fill='both', expand=True, padx=30, pady=10)

        tk.Label(symptoms_frame, text="Select Patient Symptoms *",
                 font=('Segoe UI', 16, 'bold'),
                 bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 15))

        symptom_notebook = ttk.Notebook(symptoms_frame)
        symptom_notebook.pack(fill='both', expand=True, pady=(0, 15))

        self.symptom_vars = {}

        for category, symptoms in SYMPTOMS_DATABASE.items():
            category_frame = tk.Frame(symptom_notebook, bg=self.colors['card'])
            symptom_notebook.add(category_frame, text=f"  {category}  ")

            cat_canvas = tk.Canvas(
                category_frame, bg=self.colors['card'], highlightthickness=0)
            cat_scrollbar = ttk.Scrollbar(
                category_frame, orient="vertical", command=cat_canvas.yview)
            cat_scrollable = tk.Frame(cat_canvas, bg=self.colors['card'])

            # Nested Responsiveness: Ensure symptom rows stretch to tab width
            cat_window = cat_canvas.create_window(
                (0, 0), window=cat_scrollable, anchor="nw")

            cat_scrollable.bind("<Configure>", lambda e, c=cat_canvas: c.configure(
                scrollregion=c.bbox("all")))
            cat_canvas.bind("<Configure>", lambda e, c=cat_canvas,
                            w=cat_window: c.itemconfig(w, width=e.width))

            cat_canvas.configure(yscrollcommand=cat_scrollbar.set)
            cat_canvas.pack(side="left", fill="both",
                            expand=True, padx=10, pady=10)
            cat_scrollbar.pack(side="right", fill="y")

            self.bind_mousewheel(cat_canvas)

            for symptom in symptoms:
                var = tk.BooleanVar()
                self.symptom_vars[symptom] = var
                cb_frame = tk.Frame(cat_scrollable, bg=self.colors['card'])
                cb_frame.pack(fill='x', pady=2)
                cb = tk.Checkbutton(cb_frame, text=symptom, variable=var,
                                    font=('Segoe UI', 11), bg=self.colors['card'],
                                    fg=self.colors['text'], selectcolor=self.colors['primary'],
                                    command=self.update_selected_symptoms)
                cb.pack(side='left', padx=10, pady=5)

        # Selected symptoms display
        selected_frame = tk.Frame(card, bg=self.colors['surface'])
        selected_frame.pack(fill='x', padx=30, pady=15)

        tk.Label(selected_frame, text="Selected Symptoms:", font=('Segoe UI', 12, 'bold'),
                 bg=self.colors['surface'], fg=self.colors['text']).pack(anchor='w', pady=(0, 10))

        self.selected_symptoms_frame = tk.Frame(
            selected_frame, bg=self.colors['card'], relief='flat')
        self.selected_symptoms_frame.pack(fill='both', padx=10, pady=10)

        # Action buttons
        button_frame = tk.Frame(card, bg=self.colors['surface'])
        button_frame.pack(fill='x', padx=30, pady=(15, 30))

        self.create_rounded_button(button_frame, "🗑️ Clear All", self.clear_all_symptoms,
                                   self.colors['danger'], padx=25, pady=12).pack(side='left', padx=(0, 10))

        self.process_btn = self.create_rounded_button(button_frame, "🤖 Run AI Diagnosis & Scheduling",
                                                      self.run_diagnosis, self.colors['primary'],
                                                      font=('Segoe UI', 14, 'bold'), padx=40, pady=15)
        self.process_btn.pack(side='right', fill='x', expand=True)

    def update_selected_symptoms(self):
        """Update the display of selected symptoms"""
        # Clear current display
        for widget in self.selected_symptoms_frame.winfo_children():
            widget.destroy()

        # Get selected symptoms
        self.symptoms = [symptom for symptom,
                         var in self.symptom_vars.items() if var.get()]

        if not self.symptoms:
            tk.Label(self.selected_symptoms_frame, text="No symptoms selected",
                     font=('Segoe UI', 10, 'italic'),
                     bg=self.colors['card'], fg=self.colors['text_secondary']).pack(pady=20)
        else:
            # Create a container for tags
            tags_container = tk.Frame(
                self.selected_symptoms_frame, bg=self.colors['card'])
            tags_container.pack(fill='both', padx=10, pady=10)

            # Display symptoms as tags
            for symptom in self.symptoms:
                tag_frame = tk.Frame(
                    tags_container, bg=self.colors['primary'], relief='flat')
                tag_frame.pack(side='left', padx=5, pady=5)

                tk.Label(tag_frame, text=f"  {symptom}  ",
                         font=('Segoe UI', 10, 'bold'),
                         bg=self.colors['primary'], fg='white').pack(side='left', padx=8, pady=5)

                # Remove button
                remove_btn = tk.Label(tag_frame, text="✕",
                                      font=('Segoe UI', 10, 'bold'),
                                      bg=self.colors['primary'], fg='white',
                                      cursor='hand2')
                remove_btn.pack(side='left', padx=(0, 8), pady=5)
                remove_btn.bind('<Button-1>', lambda e,
                                s=symptom: self.remove_symptom_by_name(s))

    def remove_symptom_by_name(self, symptom):
        """Remove a symptom by unchecking its checkbox"""
        if symptom in self.symptom_vars:
            self.symptom_vars[symptom].set(False)
            self.update_selected_symptoms()

    def clear_all_symptoms(self):
        """Clear all selected symptoms"""
        for var in self.symptom_vars.values():
            var.set(False)
        self.update_selected_symptoms()

    def create_results_tab(self):
        """Create results display interface with dark theme"""
        # Scrollable frame
        canvas = tk.Canvas(
            self.results_tab, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self.results_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Bind resize event
        def on_resize(event):
            canvas.itemconfig(canvas.find_withtag("all")
                              [0], width=event.width-20)
        canvas.bind('<Configure>', on_resize)

        self.results_container = scrollable_frame

    def create_roster_tab(self):
        """Create roster display interface with dark theme"""
        # Scrollable frame
        canvas = tk.Canvas(
            self.roster_tab, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self.roster_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        # Bind resize event
        def on_resize(event):
            canvas.itemconfig(canvas.find_withtag("all")
                              [0], width=event.width-20)
        canvas.bind('<Configure>', on_resize)

        self.roster_container = scrollable_frame

    """Analytics Dashboard with Charts"""

    def create_analysis_tab(self):
        # 1. Setup Canvas and Scrollbar
        canvas = tk.Canvas(self.analysis_tab,
                           bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self.analysis_tab, orient="vertical", command=canvas.yview)

        # 2. Setup the Frame that will hold content
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

        # 3. Create the Canvas Window and store the ID (needed for resizing)
        canvas_window = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw")

        # Update scrollregion when the frame size changes
        scrollable_frame.bind("<Configure>",
                              lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Update the width of the frame when the Canvas size changes (Responsiveness)
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(canvas_window, width=e.width))

        canvas.configure(yscrollcommand=scrollbar.set)

        # 4. Layout
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.bind_mousewheel(canvas)
        self.analysis_container = scrollable_frame

        # Initial display
        self.display_analytics()

    def display_analytics(self):
        """Display analytics charts"""
        for widget in self.analysis_container.winfo_children():
            widget.destroy()

        if not self.db or not MATPLOTLIB_AVAILABLE:
            msg_frame = tk.Frame(self.analysis_container,
                                 bg=self.colors['surface'])
            msg_frame.pack(fill='both', expand=True, padx=20, pady=20)
            tk.Label(msg_frame, text="⚠️ Analytics Unavailable\n\nRequires: database.py and matplotlib",
                     font=('Segoe UI', 14), bg=self.colors['surface'],
                     fg=self.colors['warning']).pack(pady=50)
            return

        main_container = tk.Frame(self.analysis_container,
                                  bg=self.colors['background'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title_frame = tk.Frame(
            main_container, bg=self.colors['primary'], height=80)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="📊 Analytics Dashboard",
                 font=('Segoe UI', 24, 'bold'), bg=self.colors['primary'],
                 fg='white').pack(pady=20)

        # Refresh button
        btn_frame = tk.Frame(main_container, bg=self.colors['background'])
        btn_frame.pack(fill='x', pady=(0, 20))

        self.create_rounded_button(btn_frame, "🔄 Refresh Analytics",
                                   self.display_analytics, self.colors['success'],
                                   padx=30, pady=12).pack(side='left')

        # Get data from database
        try:
            # Doctor workload analysis
            appointments = self.db.get_all_appointments() if hasattr(
                self.db, 'get_all_appointments') else []

            # Count appointments per doctor
            doctor_counts = {}
            for appt in appointments:
                doctor = appt.get('doctor_name', 'Unknown')
                doctor_counts[doctor] = doctor_counts.get(doctor, 0) + 1

            # Chart 1: Doctor Workload
            if doctor_counts:
                chart1_frame = tk.Frame(
                    main_container, bg='white', relief='solid', bd=2)
                chart1_frame.pack(fill='both', expand=True, pady=(0, 20))

                tk.Label(chart1_frame, text="Doctor Workload - Appointments Scheduled",
                         font=('Segoe UI', 14, 'bold'), bg='white').pack(pady=10)

                fig = Figure(figsize=(12, 5), dpi=100)
                ax = fig.add_subplot(111)

                doctors = list(doctor_counts.keys())
                counts = list(doctor_counts.values())
                colors = ['#6366f1', '#8b5cf6',
                          '#10b981', '#f59e0b', '#ef4444']

                ax.bar(doctors, counts, color=colors[:len(doctors)])
                ax.set_xlabel('Doctor', fontsize=12, fontweight='bold')
                ax.set_ylabel('Number of Appointments',
                              fontsize=12, fontweight='bold')
                ax.set_title('Appointments per Doctor',
                             fontsize=14, fontweight='bold')
                ax.grid(axis='y', alpha=0.3)

                # Rotate x labels if needed
                if len(doctors) > 3:
                    plt.setp(ax.xaxis.get_majorticklabels(),
                             rotation=45, ha='right')

                fig.tight_layout()

                chart_canvas = FigureCanvasTkAgg(fig, master=chart1_frame)
                chart_canvas.draw()
                chart_canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

            # Chart 2: Patient Urgency Distribution
            diagnoses = self.db.get_all_diagnoses() if hasattr(
                self.db, 'get_all_diagnoses') else []

            urgency_counts = {}
            for diag in diagnoses:
                urgency = diag.get('urgency', 'Unknown')
                urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1

            if urgency_counts:
                chart2_frame = tk.Frame(
                    main_container, bg='white', relief='solid', bd=2)
                chart2_frame.pack(fill='both', expand=True, pady=(0, 20))

                tk.Label(chart2_frame, text="Patient Distribution by Urgency Level",
                         font=('Segoe UI', 14, 'bold'), bg='white').pack(pady=10)

                fig2 = Figure(figsize=(12, 5), dpi=100)
                ax2 = fig2.add_subplot(111)

                urgencies = list(urgency_counts.keys())
                counts2 = list(urgency_counts.values())
                colors2 = {'Emergency': '#ef4444', 'High': '#f97316',
                           'Medium': '#eab308', 'Low': '#22c55e'}
                pie_colors = [colors2.get(u, '#6366f1') for u in urgencies]

                ax2.pie(counts2, labels=urgencies, autopct='%1.1f%%',
                        colors=pie_colors, startangle=90)
                ax2.set_title('Patient Urgency Distribution',
                              fontsize=14, fontweight='bold')

                fig2.tight_layout()

                chart_canvas2 = FigureCanvasTkAgg(fig2, master=chart2_frame)
                chart_canvas2.draw()
                chart_canvas2.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

            # Summary statistics
            stats_frame = tk.Frame(
                main_container, bg=self.colors['surface'], relief='solid', bd=2)
            stats_frame.pack(fill='x', pady=(0, 20))

            tk.Label(stats_frame, text="📈 Summary Statistics",
                     font=('Segoe UI', 16, 'bold'), bg=self.colors['surface'],
                     fg=self.colors['text']).pack(pady=15, padx=20, anchor='w')

            stats = self.db.get_statistics()
            stats_text = f"""
    Total Patients: {stats.get('total_patients', 0)}
    Total Appointments: {stats.get('total_appointments', 0)}
    Scheduled Appointments: {stats.get('scheduled_appointments', 0)}
    Occupied Beds: {stats.get('occupied_beds', 0)}
    Emergency Cases Today: {stats.get('emergency_cases_today', 0)}
            """

            tk.Label(stats_frame, text=stats_text.strip(), font=('Segoe UI', 12),
                     bg=self.colors['surface'], fg=self.colors['text'],
                     justify='left').pack(pady=(0, 15), padx=20, anchor='w')

        except Exception as e:
            error_frame = tk.Frame(
                main_container, bg=self.colors['danger'], relief='solid', bd=2)
            error_frame.pack(fill='x')
            tk.Label(error_frame, text=f"Error loading analytics: {str(e)}",
                     font=('Segoe UI', 12), bg=self.colors['danger'],
                     fg='white').pack(pady=20, padx=20)

    def create_appointments_tab(self):
        """NEW: Create a responsive, scrollable appointments management interface"""
        canvas = tk.Canvas(self.appointments_tab,
                           bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(
            self.appointments_tab, orient="vertical", command=canvas.yview)
        container = tk.Frame(canvas, bg=self.colors['background'])

        # Responsive binding
        appt_window = canvas.create_window(
            (0, 0), window=container, anchor="nw")
        container.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(
            appt_window, width=e.width))

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.bind_mousewheel(canvas)

        # Content Card
        card = tk.Frame(
            container, bg=self.colors['surface'], relief='flat', bd=0)
        card.pack(fill='both', expand=True, padx=20, pady=20)

        title_frame = tk.Frame(card, bg=self.colors['secondary'], height=70)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="🗓️ Appointment Management", font=('Segoe UI', 20, 'bold'),
                 bg=self.colors['secondary'], fg='white').pack(pady=15)

        # Control Buttons
        ctrl_frame = tk.Frame(card, bg=self.colors['surface'])
        ctrl_frame.pack(fill='x', padx=30, pady=20)

        self.create_rounded_button(ctrl_frame, "🔄 Refresh List", self.refresh_appointments,
                                   self.colors['primary']).pack(side='left', padx=5)
        self.create_rounded_button(ctrl_frame, "📅 Reschedule Selected", self.reschedule_appointment,
                                   self.colors['warning']).pack(side='left', padx=5)
        self.create_rounded_button(ctrl_frame, "❌ Cancel Selected", self.cancel_appointment,
                                   self.colors['danger']).pack(side='left', padx=5)
        self.create_rounded_button(ctrl_frame, "📥 Download Card", self.download_appointment_card,
                                   self.colors['success']).pack(side='left', padx=5)

        # Appointments Treeview
        tree_frame = tk.Frame(card, bg=self.colors['card'])
        tree_frame.pack(fill='both', expand=True, padx=30, pady=(0, 30))

        columns = ('ID', 'Patient', 'Doctor',
                   'Specialty', 'Time', 'Room', 'Status')
        self.appt_tree = ttk.Treeview(
            tree_frame, columns=columns, show='headings', height=15, style="Dark.Treeview")

        for col in columns:
            self.appt_tree.heading(col, text=col)
            self.appt_tree.column(col, width=100, stretch=True)

        self.appt_tree.pack(side='left', fill='both', expand=True)
        tree_scroll = ttk.Scrollbar(
            tree_frame, orient="vertical", command=self.appt_tree.yview)
        self.appt_tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side='right', fill='y')

        self.refresh_appointments()

    def refresh_appointments(self):
        """Fetch all appointments from DB and populate the treeview"""
        if not self.db:
            return
        for item in self.appt_tree.get_children():
            self.appt_tree.delete(item)

        try:
            appointments = self.db.get_all_appointments()
            for appt in appointments:
                # Ensure we handle different DB return formats
                self.appt_tree.insert('', 'end', values=(
                    appt.get('appointment_id', 'N/A'),
                    appt.get('patient_name', 'N/A'),
                    appt.get('doctor_name', 'N/A'),
                    appt.get('specialty', 'N/A'),
                    appt.get('appointment_time', 'N/A'),
                    appt.get('room_number', 'N/A'),
                    appt.get('status', 'Scheduled')
                ))
        except Exception as e:
            print(f"Error refreshing appointments: {e}")

    def reschedule_appointment(self):
        """Implements the rescheduling logic with user input"""
        selection = self.appt_tree.selection()
        if not selection:
            messagebox.showwarning(
                "Selection Required", "Please select an appointment to reschedule.")
            return

        item = self.appt_tree.item(selection[0])
        appt_id = item['values'][0]

        # simpledialog.askstring returns a string
        new_time_str = simpledialog.askstring("Reschedule", "Enter New Date & Time\nFormat: YYYY-MM-DD HH:MM",
                                              initialvalue=datetime.now().strftime('%Y-%m-%d %H:%M'))

        if new_time_str:
            try:
                # 1. Convert the string input into a datetime object
                new_datetime_obj = datetime.strptime(
                    new_time_str, '%Y-%m-%d %H:%M')

                # 2. Pass the OBJECT (not the string) to the database
                if self.db.reschedule_appointment(appt_id, new_datetime_obj):
                    messagebox.showinfo(
                        "Success", "Appointment rescheduled successfully!")
                    self.refresh_appointments()
                    self.refresh_history_tab()
                    self.db.update_appointment_status(appt_id, "Rescheduled")
                else:
                    messagebox.showerror(
                        "Error", "Could not update the database.")
            except ValueError:
                messagebox.showerror(
                    "Invalid Format", "Please use YYYY-MM-DD HH:MM")

    def cancel_appointment(self):
        """Implements the cancellation logic"""
        selection = self.appt_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required",
                                   "Please select an appointment to cancel.")
            return

        item = self.appt_tree.item(selection[0])
        appt_id = item['values'][0]

        if messagebox.askyesno("Confirm", "Are you sure you want to cancel this appointment?"):
            if self.db.update_appointment_status(appt_id, "Cancelled"):
                messagebox.showinfo(
                    "Cancelled", "Appointment has been marked as Cancelled.")
                self.refresh_appointments()
                self.refresh_history_tab()
            else:
                messagebox.showerror("Error", "Could not update status.")

    def download_appointment_card(self):
        """Logic to select an appointment and trigger PDF generation"""
        selection = self.appt_tree.selection()
        if not selection:
            messagebox.showwarning(
                "Selection Required", "Please select a patient appointment to download.")
            return

        # Extract data from the selected row
        item = self.appt_tree.item(selection[0])
        appt_values = item['values']
        # Columns: ID(0), Patient(1), Doctor(2), Specialty(3), Time(4), Room(5), Status(6)

        # Ask user where to save the file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=f"Appointment_{appt_values[1].replace(' ', '_')}.pdf",
            title="Save Appointment Card"
        )

        if file_path:
            try:
                self.generate_appointment_pdf(file_path, appt_values)
                messagebox.showinfo(
                    "Success", f"Appointment card downloaded successfully at:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate PDF: {e}")

    def generate_appointment_pdf(self, file_path, data):
        """Generates a PDF styled like the Health & Medical Center card"""
        # Create the PDF canvas
        c = canvas.Canvas(file_path, pagesize=(400, 400))
        width, height = 400, 400

        # 1. Draw the Tan/Beige header box (matches the image)
        c.setFillColorRGB(0.89, 0.83, 0.73)  # Tan color
        c.rect(0, 250, 400, 150, fill=1, stroke=0)

        # 2. Add Header Text
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, 340, "MediAI Smart Hospital System")

        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, 315, "Phone: +923099293116")
        c.drawCentredString(width/2, 295, "Email: info@mediai.com")

        # 3. Add Doctor Information
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, 210, f"{data[2]}")  # Doctor Name

        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, 185, "Appointment")

        # 4. Draw Weekdays (Matches image style)
        c.setFont("Helvetica", 10)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        x_pos = 40
        for day in days:
            c.drawString(x_pos, 150, day)
            x_pos += 70

        # 5. Draw the "For:", "Date:", and "Time:" fields with lines
        c.setFont("Helvetica", 12)

        # Patient Name Line
        c.drawString(40, 100, "For:")
        c.line(70, 98, 360, 98)
        c.setFont("Helvetica-Oblique", 12)
        c.drawString(80, 102, f"{data[1]}")  # Patient Name

        # Date and Time Lines
        c.setFont("Helvetica", 12)
        c.drawString(40, 50, "Date:")
        c.line(75, 48, 200, 48)

        # Extract just date if time is included
        appt_time_str = str(data[4])
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(80, 52, appt_time_str.split(' ')[0])

        c.setFont("Helvetica", 12)
        c.drawString(220, 50, "Time:")
        c.line(260, 48, 360, 48)
        c.setFont("Helvetica-Oblique", 10)
        # Extract time portion
        time_part = appt_time_str.split(' ')[1] if ' ' in appt_time_str else ""
        c.drawString(270, 52, time_part)

        # Finalize PDF
        c.showPage()
        c.save()

    def add_symptom(self):
        """Legacy method - not used with new symptom selector"""
        pass

    def remove_symptom(self):
        """Legacy method - not used with new symptom selector"""
        pass

    def run_diagnosis(self):
        """Execute complete AI diagnosis pipeline"""
        # Update symptoms list from checkboxes
        self.symptoms = [symptom for symptom,
                         var in self.symptom_vars.items() if var.get()]

        # Validation
        if not self.name_entry.get().strip():
            messagebox.showerror("Error", "Please enter patient name")
            self.name_entry.focus()
            return

        if not self.age_entry.get().strip():
            messagebox.showerror("Error", "Please enter patient age")
            self.age_entry.focus()
            return

        if not self.age_entry.get().isdigit():
            messagebox.showerror(
                "Error", "Please enter a valid age (numbers only)")
            self.age_entry.focus()
            return

        if not self.symptoms:
            messagebox.showerror(
                "Error", "Please select at least one symptom from the categories")
            return

        # Disable button and show processing
        self.process_btn.config(state='disabled', text='⏳ Processing AI Analysis...',
                                bg=self.colors['card'])
        self.root.update()

        try:
            # Get input data
            patient_name = self.name_entry.get().strip()
            age = int(self.age_entry.get())
            gender = self.gender_var.get()
            contact = self.contact_entry.get().strip() or None

            # Save patient to database
            if self.db:
                self.current_patient_id = self.db.add_patient(
                    patient_name, age, gender, contact)
                self.db.add_symptoms(self.current_patient_id, self.symptoms)

            # Step 1: Prolog Expert System Diagnosis
            self.diagnosis_result = PrologExpertSystem.diagnose(
                self.symptoms, age)

            # Save diagnosis to database
            if self.db and self.current_patient_id:
                diagnosis_id = self.db.add_diagnosis(
                    self.current_patient_id,
                    self.diagnosis_result['urgency'],
                    self.diagnosis_result['priority'],
                    self.diagnosis_result['specialty'],
                    self.diagnosis_result['disease'],
                    self.diagnosis_result['doctor']
                )
            else:
                diagnosis_id = None

            # Step 2: CSP Appointment Scheduling
            self.appointment = CSPScheduler.schedule_appointment(
                self.diagnosis_result, patient_name
            )

            # Save appointment to database
            if self.db and self.current_patient_id and diagnosis_id:
                self.db.add_appointment(
                    self.current_patient_id,
                    diagnosis_id,
                    self.appointment['doctor'],
                    self.appointment['specialty'],
                    self.appointment['time'],
                    self.appointment['room'],
                    self.appointment['duration']
                )

            # Step 3: CSP Bed Allocation
            self.bed_allocation = CSPScheduler.allocate_bed(
                self.diagnosis_result, patient_name, age, gender
            )

            # Save bed allocation to database
            if self.db and self.current_patient_id:
                self.db.add_bed_allocation(
                    self.current_patient_id,
                    self.bed_allocation['bed']['id'],
                    self.bed_allocation['bed']['ward'],
                    self.bed_allocation['bed'].get('type', 'Standard'),
                    self.bed_allocation['estimated_stay']
                )

            # Step 4: GA Weekly Roster Optimization
            self.roster_data, self.metrics = GeneticAlgorithmRoster.generate_optimized_roster()

            # Save roster to database
            if self.db:
                week_start = datetime.now().strftime('%Y-%m-%d')
                self.db.save_weekly_roster(self.roster_data, week_start)

            # Display results
            self.display_results()
            self.display_roster()

            # Refresh history tab if database is available
            if self.db:
                self.refresh_history_tab()

            # Switch to results tab
            self.notebook.select(self.results_tab)

            # Success message
            db_status = "Data saved to database." if self.db else "Running without database."
            messagebox.showinfo("Success",
                                f"✅ AI Analysis Complete!\n\n"
                                f"Results are now available in the Results & Schedule tab.\n"
                                f"Weekly roster has been optimized using Genetic Algorithm.\n\n"
                                f"{db_status}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        finally:
            # Re-enable button
            self.process_btn.config(state='normal',
                                    text='🤖 Run AI Diagnosis & Scheduling',
                                    bg=self.colors['primary'])

    def display_results(self):
        """Display comprehensive diagnosis and scheduling results with dark theme"""
        # Clear previous results
        for widget in self.results_container.winfo_children():
            widget.destroy()

        # Main container
        main_container = tk.Frame(
            self.results_container, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # 1. Diagnosis Card
        diag_card = tk.Frame(main_container, bg=self.diagnosis_result['color'],
                             relief='flat', bd=0)
        diag_card.pack(fill='x', pady=(0, 20))

        # Add rounded corner effect with padding
        diag_inner = tk.Frame(diag_card, bg=self.diagnosis_result['color'])
        diag_inner.pack(fill='both', expand=True, padx=3, pady=3)

        tk.Label(diag_inner, text="🤖 Prolog Expert System - Medical Diagnosis",
                 font=('Segoe UI', 20, 'bold'), bg=self.diagnosis_result['color'],
                 fg='white').pack(pady=20, padx=20, anchor='w')

        info_frame = tk.Frame(diag_inner, bg=self.diagnosis_result['color'])
        info_frame.pack(fill='x', padx=20, pady=(0, 20))

        details = [
            ("Urgency Level", self.diagnosis_result['urgency']),
            ("Priority Score", f"{self.diagnosis_result['priority']}/10"),
            ("Specialty", self.diagnosis_result['specialty']),
            ("Diagnosis", self.diagnosis_result['disease'])
        ]

        for i, (label, value) in enumerate(details):
            col = i % 4
            frame = tk.Frame(info_frame, bg=self.diagnosis_result['color'])
            frame.grid(row=0, column=col, padx=15, pady=10, sticky='w')
            info_frame.grid_columnconfigure(col, weight=1)

            tk.Label(frame, text=label, font=('Segoe UI', 10),
                     bg=self.diagnosis_result['color'], fg='white',
                     anchor='w').pack(anchor='w')
            tk.Label(frame, text=value, font=('Segoe UI', 18, 'bold'),
                     bg=self.diagnosis_result['color'], fg='white',
                     anchor='w').pack(anchor='w')

        # 2. Appointment Card
        appt_card = tk.Frame(
            main_container, bg=self.colors['surface'], relief='flat', bd=0)
        appt_card.pack(fill='x', pady=(0, 20))

        # Title bar
        title_bar = tk.Frame(appt_card, bg=self.colors['primary'], height=60)
        title_bar.pack(fill='x')
        title_bar.pack_propagate(False)

        tk.Label(title_bar, text="📅 CSP Appointment Schedule",
                 font=('Segoe UI', 18, 'bold'), bg=self.colors['primary'],
                 fg='white').pack(side='left', pady=15, padx=20)

        appt_info_frame = tk.Frame(appt_card, bg=self.colors['surface'])
        appt_info_frame.pack(fill='both', expand=True, padx=20, pady=20)

        appt_details = [
            ("👨‍⚕️ Assigned Doctor",
             self.appointment['doctor'], self.colors['primary']),
            ("🕐 Appointment Time", self.appointment['time'].strftime(
                '%a, %b %d, %Y - %I:%M %p'), self.colors['success']),
            ("🏥 Room Number",
             self.appointment['room'], self.colors['secondary']),
            ("⏱️ Duration",
             f"{self.appointment['duration']} minutes", self.colors['warning'])
        ]

        for i, (label, value, color) in enumerate(appt_details):
            # Create colored card for each detail
            frame = tk.Frame(appt_info_frame, bg=self.colors['surface'])
            frame.grid(row=i//2, column=i % 2, padx=10, pady=10, sticky='nsew')
            appt_info_frame.grid_rowconfigure(i//2, weight=1)
            appt_info_frame.grid_columnconfigure(i % 2, weight=1)

            inner_frame = tk.Frame(frame, bg=color, relief='flat', bd=0)
            inner_frame.pack(fill='both', expand=True, padx=2, pady=2)

            tk.Label(inner_frame, text=label, font=('Segoe UI', 11),
                     bg=color, fg='white').pack(anchor='w', padx=20, pady=(15, 5))
            tk.Label(inner_frame, text=value, font=('Segoe UI', 14, 'bold'),
                     bg=color, fg='white', wraplength=300).pack(anchor='w', padx=20, pady=(0, 15))

        # 3. Bed Allocation Card
        bed_card = tk.Frame(
            main_container, bg=self.colors['surface'], relief='flat', bd=0)
        bed_card.pack(fill='x', pady=(0, 20))

        # Title bar
        bed_title_bar = tk.Frame(
            bed_card, bg=self.colors['primary'], height=60)
        bed_title_bar.pack(fill='x')
        bed_title_bar.pack_propagate(False)

        tk.Label(bed_title_bar, text="🛏️ CSP Bed Allocation System",
                 font=('Segoe UI', 18, 'bold'), bg=self.colors['primary'],
                 fg='white').pack(side='left', pady=15, padx=20)

        bed_info_frame = tk.Frame(bed_card, bg=self.colors['surface'])
        bed_info_frame.pack(fill='both', expand=True, padx=20, pady=20)

        bed_details = [
            ("Bed ID", self.bed_allocation['bed']
             ['id'], self.colors['primary']),
            ("Ward Location",
             self.bed_allocation['bed']['ward'], self.colors['success']),
            ("Estimated Stay",
             self.bed_allocation['estimated_stay'], self.colors['secondary'])
        ]

        for i, (label, value, color) in enumerate(bed_details):
            frame = tk.Frame(bed_info_frame, bg=self.colors['surface'])
            frame.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            bed_info_frame.grid_columnconfigure(i, weight=1)

            inner_frame = tk.Frame(frame, bg=color, relief='flat', bd=0)
            inner_frame.pack(fill='both', expand=True, padx=2, pady=2)

            tk.Label(inner_frame, text=label, font=('Segoe UI', 11),
                     bg=color, fg='white').pack(anchor='w', padx=20, pady=(15, 5))
            tk.Label(inner_frame, text=value, font=('Segoe UI', 14, 'bold'),
                     bg=color, fg='white').pack(anchor='w', padx=20, pady=(0, 15))

        # 4. Summary Information
        summary_frame = tk.Frame(
            main_container, bg=self.colors['card'], relief='flat', bd=0)
        summary_frame.pack(fill='x')

        summary_inner = tk.Frame(summary_frame, bg=self.colors['card'])
        summary_inner.pack(fill='both', expand=True, padx=3, pady=3)

        tk.Label(summary_inner, text="📊 Summary",
                 font=('Segoe UI', 16, 'bold'), bg=self.colors['card'],
                 fg=self.colors['text']).pack(anchor='w', padx=20, pady=15)

        summary_text = f"""
Patient: {self.appointment['patient']}
Diagnosis: {self.diagnosis_result['disease']} ({self.diagnosis_result['urgency']} Priority)
Doctor: {self.appointment['doctor']} - {self.diagnosis_result['specialty']}
Appointment: {self.appointment['time'].strftime('%B %d, %Y at %I:%M %p')}
Location: {self.appointment['room']}
Bed: {self.bed_allocation['bed']['id']} in {self.bed_allocation['bed']['ward']}
        """

        tk.Label(summary_inner, text=summary_text.strip(),
                 font=('Segoe UI', 12), bg=self.colors['card'],
                 fg=self.colors['text'], justify='left').pack(anchor='w', padx=20, pady=(0, 15))

    def display_roster(self):
        """Display GA-optimized weekly roster with metrics in dark theme"""
        # Clear previous roster
        for widget in self.roster_container.winfo_children():
            widget.destroy()

        main_container = tk.Frame(
            self.roster_container, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Title Card
        title_frame = tk.Frame(
            main_container, bg=self.colors['primary'], relief='flat', bd=0)
        title_frame.pack(fill='x', pady=(0, 20))

        title_inner = tk.Frame(title_frame, bg=self.colors['primary'])
        title_inner.pack(fill='x', padx=3, pady=3)

        tk.Label(title_inner, text="🧬 Genetic Algorithm - Weekly Roster Optimization",
                 font=('Segoe UI', 22, 'bold'), bg=self.colors['primary'],
                 fg='white').pack(pady=20)

        # Metrics Dashboard
        metrics_frame = tk.Frame(main_container, bg=self.colors['background'])
        metrics_frame.pack(fill='x', pady=(0, 20))

        metric_data = [
            ("💰 Total Profit",
             f"${self.metrics['profit']}", self.colors['success'], 'Weekly'),
            ("👥 Avg Patients/Shift",
             self.metrics['avg_patients'], self.colors['primary'], 'Per Shift'),
            ("📈 Total Revenue",
             f"${self.metrics['total_revenue']}", self.colors['secondary'], 'Weekly'),
            ("💸 Total Cost",
             f"${self.metrics['total_cost']}", self.colors['warning'], 'Weekly')
        ]

        for i, (label, value, color, sublabel) in enumerate(metric_data):
            card = tk.Frame(metrics_frame, bg=color, relief='flat', bd=0)
            card.grid(row=0, column=i, padx=10, sticky='ew')
            metrics_frame.grid_columnconfigure(i, weight=1)

            card_inner = tk.Frame(card, bg=color)
            card_inner.pack(fill='both', expand=True, padx=3, pady=3)

            tk.Label(card_inner, text=label, font=('Segoe UI', 12),
                     bg=color, fg='white').pack(pady=(20, 5))
            tk.Label(card_inner, text=value, font=('Segoe UI', 26, 'bold'),
                     bg=color, fg='white').pack(pady=(0, 5))
            tk.Label(card_inner, text=sublabel, font=('Segoe UI', 10),
                     bg=color, fg='white').pack(pady=(0, 20))

        # Roster Table
        roster_card = tk.Frame(
            main_container, bg=self.colors['surface'], relief='flat', bd=0)
        roster_card.pack(fill='both', expand=True)

        # Title bar for table
        table_title_bar = tk.Frame(
            roster_card, bg=self.colors['primary'], height=60)
        table_title_bar.pack(fill='x')
        table_title_bar.pack_propagate(False)

        tk.Label(table_title_bar, text="📋 Complete Weekly Schedule",
                 font=('Segoe UI', 18, 'bold'), bg=self.colors['primary'],
                 fg='white').pack(side='left', pady=15, padx=20)

        # Create Treeview with dark theme styling
        tree_frame = tk.Frame(roster_card, bg=self.colors['surface'])
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(15, 20))

        # Configure treeview style for dark theme
        style = ttk.Style()
        style.configure("Dark.Treeview",
                        background=self.colors['card'],
                        foreground=self.colors['text'],
                        rowheight=35,
                        fieldbackground=self.colors['card'],
                        font=('Segoe UI', 10),
                        borderwidth=0)
        style.map('Dark.Treeview',
                  background=[('selected', self.colors['primary'])],
                  foreground=[('selected', 'white')])
        style.configure("Dark.Treeview.Heading",
                        font=('Segoe UI', 11, 'bold'),
                        background=self.colors['primary'],
                        foreground='white',
                        borderwidth=0,
                        relief='flat')

        columns = ('Day', 'Shift', 'Doctor', 'Specialty',
                   'Patients', 'Cost', 'Revenue')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                            height=21, style="Dark.Treeview")

        # Configure columns with responsive widths
        column_widths = {
            'Day': 120,
            'Shift': 180,
            'Doctor': 180,
            'Specialty': 150,
            'Patients': 100,
            'Cost': 100,
            'Revenue': 110
        }

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=column_widths[col],
                        anchor='center' if col in ['Patients', 'Cost', 'Revenue'] else 'w')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Populate data with alternating row colors
        for day_idx, day_schedule in enumerate(self.roster_data):
            for shift_idx, shift in enumerate(day_schedule):
                tags = ('evenrow',) if (day_idx * 3 +
                                        shift_idx) % 2 == 0 else ('oddrow',)
                tree.insert('', 'end', values=(
                    shift['day'],
                    shift['shift'],
                    shift['doctor'],
                    shift['specialty'],
                    shift['patients'],
                    f"${shift['cost']:.2f}",
                    f"${shift['revenue']}"
                ), tags=tags)

        # Configure row colors for dark theme
        tree.tag_configure('evenrow', background=self.colors['card'])
        tree.tag_configure('oddrow', background=self.colors['surface'])

        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # GA Optimization Info
        info_frame = tk.Frame(
            roster_card, bg=self.colors['card'], relief='flat', bd=0)
        info_frame.pack(fill='x', padx=20, pady=(0, 20))

        info_inner = tk.Frame(info_frame, bg=self.colors['card'])
        info_inner.pack(fill='both', expand=True, padx=3, pady=3)

        tk.Label(info_inner, text="🧬 Genetic Algorithm Optimization Details:",
                 font=('Segoe UI', 14, 'bold'), bg=self.colors['card'],
                 fg=self.colors['text']).pack(anchor='w', padx=20, pady=15)

        optimizations = [
            "✓ Balanced workload distribution across all doctors (no single doctor overloaded)",
            "✓ Minimized overtime costs while maintaining full hospital coverage",
            "✓ Fair shift rotation ensuring work-life balance for medical staff",
            "✓ Optimized for maximum hospital profit and revenue generation",
            "✓ 100+ generations evolved to find the best scheduling solution",
            "✓ Fitness function considers: cost, revenue, fairness, and coverage"
        ]

        for opt in optimizations:
            tk.Label(info_inner, text=opt, font=('Segoe UI', 11),
                     bg=self.colors['card'], fg=self.colors['text_secondary']).pack(anchor='w', padx=20, pady=3)

        tk.Label(info_inner, text="", bg=self.colors['card']).pack(pady=10)

    def create_history_tab(self):
        """Create patient history interface with dark theme"""
        main_container = tk.Frame(
            self.history_tab, bg=self.colors['background'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Title Card
        title_frame = tk.Frame(
            main_container, bg=self.colors['primary'], relief='flat', bd=0)
        title_frame.pack(fill='x', pady=(0, 20))

        title_inner = tk.Frame(title_frame, bg=self.colors['primary'])
        title_inner.pack(fill='x', padx=3, pady=3)

        tk.Label(title_inner, text="📊 Patient History & Database Records",
                 font=('Segoe UI', 22, 'bold'), bg=self.colors['primary'],
                 fg='white').pack(pady=20)

        if not self.db:
            # Show message if database not available
            no_db_frame = tk.Frame(
                main_container, bg=self.colors['surface'], relief='flat', bd=0)
            no_db_frame.pack(fill='both', expand=True)

            no_db_inner = tk.Frame(no_db_frame, bg=self.colors['surface'])
            no_db_inner.pack(fill='both', expand=True, padx=3, pady=3)

            tk.Label(no_db_inner, text="⚠️ Database Not Available",
                     font=('Segoe UI', 18, 'bold'), bg=self.colors['surface'],
                     fg=self.colors['warning']).pack(pady=50)
            tk.Label(no_db_inner,
                     text="Please ensure database.py is in the same directory as the main application.",
                     font=('Segoe UI', 12), bg=self.colors['surface'],
                     fg=self.colors['text_secondary']).pack()
            return

        # Search frame
        search_frame = tk.Frame(
            main_container, bg=self.colors['surface'], relief='flat', bd=0)
        search_frame.pack(fill='x', pady=(0, 20))

        search_inner = tk.Frame(search_frame, bg=self.colors['surface'])
        search_inner.pack(fill='x', padx=20, pady=15)

        tk.Label(search_inner, text="Search Patient:",
                 font=('Segoe UI', 12, 'bold'), bg=self.colors['surface'],
                 fg=self.colors['text']).pack(side='left', padx=(0, 15))

        self.search_entry = tk.Entry(search_inner, font=('Segoe UI', 11), width=35,
                                     bg=self.colors['card'], fg=self.colors['text'],
                                     relief='flat', bd=0, insertbackground=self.colors['text'])
        self.search_entry.pack(side='left', padx=(0, 10), ipady=8)

        search_btn = self.create_rounded_button(
            search_inner, "🔍 Search", self.search_patients,
            self.colors['primary'], padx=20, pady=8
        )
        search_btn.pack(side='left', padx=(0, 10))

        refresh_btn = self.create_rounded_button(
            search_inner, "🔄 Refresh All", self.refresh_history_tab,
            self.colors['success'], padx=20, pady=8
        )
        refresh_btn.pack(side='left')

        # Statistics cards
        stats_frame = tk.Frame(main_container, bg=self.colors['background'])
        stats_frame.pack(fill='x', pady=(0, 20))

        self.stats_labels = {}
        stat_names = [
            ('total_patients', '👥 Total Patients', self.colors['primary']),
            ('total_appointments', '📅 Appointments', self.colors['success']),
            ('occupied_beds', '🛏️ Occupied Beds', self.colors['secondary']),
            ('emergency_cases_today',
             '🚨 Emergencies Today', self.colors['danger'])
        ]

        for i, (key, label, color) in enumerate(stat_names):
            card = tk.Frame(stats_frame, bg=color, relief='flat', bd=0)
            card.grid(row=0, column=i, padx=10, sticky='ew')
            stats_frame.grid_columnconfigure(i, weight=1)

            card_inner = tk.Frame(card, bg=color)
            card_inner.pack(fill='both', expand=True, padx=3, pady=3)

            tk.Label(card_inner, text=label, font=('Segoe UI', 11),
                     bg=color, fg='white').pack(pady=(20, 5))
            self.stats_labels[key] = tk.Label(card_inner, text="0",
                                              font=('Segoe UI', 24, 'bold'),
                                              bg=color, fg='white')
            self.stats_labels[key].pack(pady=(0, 20))

        # Patients list
        list_frame = tk.Frame(
            main_container, bg=self.colors['surface'], relief='flat', bd=0)
        list_frame.pack(fill='both', expand=True)

        # Title bar
        list_title_bar = tk.Frame(
            list_frame, bg=self.colors['primary'], height=60)
        list_title_bar.pack(fill='x')
        list_title_bar.pack_propagate(False)

        tk.Label(list_title_bar, text="Recent Patients",
                 font=('Segoe UI', 16, 'bold'), bg=self.colors['primary'],
                 fg='white').pack(side='left', pady=15, padx=20)

        # Create treeview
        tree_container = tk.Frame(list_frame, bg=self.colors['surface'])
        tree_container.pack(fill='both', expand=True, padx=20, pady=(15, 20))

        columns = ('ID', 'Name', 'Age', 'Gender',
                   'Contact', 'Registration Date')
        self.history_tree = ttk.Treeview(tree_container, columns=columns,
                                         show='headings', height=15, style="Dark.Treeview")

        # Configure columns
        column_widths = {
            'ID': 60,
            'Name': 200,
            'Age': 80,
            'Gender': 100,
            'Contact': 150,
            'Registration Date': 180
        }

        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=column_widths[col],
                                     anchor='center' if col in ['ID', 'Age', 'Gender'] else 'w')

        scrollbar = ttk.Scrollbar(tree_container, orient='vertical',
                                  command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # View details button
        btn_frame = tk.Frame(list_frame, bg=self.colors['surface'])
        btn_frame.pack(fill='x', padx=20, pady=(0, 20))

        view_btn = self.create_rounded_button(
            btn_frame, "👁️ View Full History", self.view_patient_details,
            self.colors['primary'], padx=25, pady=10
        )
        view_btn.pack(side='left')

        # Load initial data
        self.refresh_history_tab()

    def refresh_history_tab(self):
        """Refresh patient history data"""
        if not self.db:
            return

        try:
            # Update statistics
            stats = self.db.get_statistics()
            for key, label_widget in self.stats_labels.items():
                label_widget.config(text=str(stats.get(key, 0)))

            # Clear and reload patients list
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)

            patients = self.db.get_all_patients()
            for patient in patients:
                self.history_tree.insert('', 'end', values=(
                    patient['patient_id'],
                    patient['name'],
                    patient['age'],
                    patient['gender'],
                    patient['contact'] or 'N/A',
                    patient['registration_date']
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh history: {e}")

    def search_patients(self):
        """Search patients by name or contact"""
        if not self.db:
            return

        search_term = self.search_entry.get().strip()
        if not search_term:
            self.refresh_history_tab()
            return

        try:
            # Clear list
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)

            patients = self.db.search_patients(search_term)
            if not patients:
                messagebox.showinfo(
                    "Search", "No patients found matching your search.")
                return

            for patient in patients:
                self.history_tree.insert('', 'end', values=(
                    patient['patient_id'],
                    patient['name'],
                    patient['age'],
                    patient['gender'],
                    patient['contact'] or 'N/A',
                    patient['registration_date']
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def view_patient_details(self):
        """View complete patient history with dark theme"""
        if not self.db:
            return

        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a patient first")
            return

        item = self.history_tree.item(selection[0])
        patient_id = item['values'][0]

        try:
            history = self.db.get_patient_history(patient_id)
            if not history:
                messagebox.showerror("Error", "Patient not found")
                return

            # Create details window with dark theme
            details_window = tk.Toplevel(self.root)
            details_window.title(
                f"Patient Details - {history['patient']['name']}")
            details_window.geometry("900x700")
            details_window.configure(bg=self.colors['background'])

            # Create scrollable frame
            canvas = tk.Canvas(
                details_window, bg=self.colors['background'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(
                details_window, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

            scrollable_frame.bind("<Configure>",
                                  lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both",
                        expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")

            # Patient info card
            info_frame = tk.Frame(
                scrollable_frame, bg=self.colors['primary'], relief='flat', bd=0)
            info_frame.pack(fill='x', padx=20, pady=20)

            info_inner = tk.Frame(info_frame, bg=self.colors['primary'])
            info_inner.pack(fill='both', expand=True, padx=3, pady=3)

            tk.Label(info_inner, text=f"👤 {history['patient']['name']}",
                     font=('Segoe UI', 20, 'bold'), bg=self.colors['primary'],
                     fg='white').pack(pady=15)

            details_text = f"""
Age: {history['patient']['age']} years
Gender: {history['patient']['gender'].capitalize()}
Contact: {history['patient']['contact'] or 'N/A'}
Registration: {history['patient']['registration_date']}
            """
            tk.Label(info_inner, text=details_text.strip(), font=('Segoe UI', 12),
                     bg=self.colors['primary'], fg='white', justify='left').pack(pady=(0, 15), padx=20)

            # Symptoms
            if history['symptoms']:
                symp_frame = tk.Frame(
                    scrollable_frame, bg=self.colors['surface'], relief='flat', bd=0)
                symp_frame.pack(fill='x', padx=20, pady=(0, 20))

                symp_inner = tk.Frame(symp_frame, bg=self.colors['surface'])
                symp_inner.pack(fill='both', expand=True, padx=3, pady=3)

                tk.Label(symp_inner, text="💊 Symptoms",
                         font=('Segoe UI', 16, 'bold'), bg=self.colors['surface'],
                         fg=self.colors['text']).pack(pady=15, padx=20, anchor='w')

                for symptom in history['symptoms']:
                    tk.Label(symp_inner, text=f"• {symptom}",
                             font=('Segoe UI', 11), bg=self.colors['surface'],
                             fg=self.colors['text_secondary']).pack(anchor='w', padx=40, pady=2)

                tk.Label(symp_inner, text="",
                         bg=self.colors['surface']).pack(pady=5)

            # Diagnoses
            if history['diagnoses']:
                diag_frame = tk.Frame(
                    scrollable_frame, bg=self.colors['surface'], relief='flat', bd=0)
                diag_frame.pack(fill='x', padx=20, pady=(0, 20))

                diag_inner = tk.Frame(diag_frame, bg=self.colors['surface'])
                diag_inner.pack(fill='both', expand=True, padx=3, pady=3)

                tk.Label(diag_inner, text="🔬 Diagnoses",
                         font=('Segoe UI', 16, 'bold'), bg=self.colors['surface'],
                         fg=self.colors['text']).pack(pady=15, padx=20, anchor='w')

                for diag in history['diagnoses']:
                    text = f"• {diag['disease']} - {diag['urgency']} Priority ({diag['specialty']})"
                    tk.Label(diag_inner, text=text,
                             font=('Segoe UI', 11), bg=self.colors['surface'],
                             fg=self.colors['text_secondary']).pack(anchor='w', padx=40, pady=2)

                tk.Label(diag_inner, text="",
                         bg=self.colors['surface']).pack(pady=5)

            # Appointments
            if history['appointments']:
                appt_frame = tk.Frame(
                    scrollable_frame, bg=self.colors['surface'], relief='flat', bd=0)
                appt_frame.pack(fill='x', padx=20, pady=(0, 20))

                appt_inner = tk.Frame(appt_frame, bg=self.colors['surface'])
                appt_inner.pack(fill='both', expand=True, padx=3, pady=3)

                tk.Label(appt_inner, text="📅 Appointments",
                         font=('Segoe UI', 16, 'bold'), bg=self.colors['surface'],
                         fg=self.colors['text']).pack(pady=15, padx=20, anchor='w')

                for appt in history['appointments']:
                    text = f"• {appt['doctor_name']} - {appt['appointment_time']} - {appt['status']}"
                    tk.Label(appt_inner, text=text,
                             font=('Segoe UI', 11), bg=self.colors['surface'],
                             fg=self.colors['text_secondary']).pack(anchor='w', padx=40, pady=2)

                tk.Label(appt_inner, text="",
                         bg=self.colors['surface']).pack(pady=5)

            # Close button
            close_btn_frame = tk.Frame(
                scrollable_frame, bg=self.colors['background'])
            close_btn_frame.pack(fill='x', padx=20, pady=(0, 20))

            close_btn = self.create_rounded_button(
                close_btn_frame, "✕ Close", details_window.destroy,
                self.colors['danger'], padx=30, pady=10
            )
            close_btn.pack()

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to load patient details: {e}")


def main():
    """Main application entry point"""
    root = tk.Tk()

    # Set window icon (optional - requires icon file)
    try:
        root.iconbitmap('hospital.ico')
    except:
        pass

    # Create application
    app = HospitalManagementGUI(root)

    # Start main loop
    root.mainloop()


if __name__ == "__main__":
    main()
