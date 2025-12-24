% ==================== MEDICAL DIAGNOSIS EXPERT SYSTEM ====================
% Hospital Management System - Prolog Knowledge Base
% File: medical_diagnosis.pl
% Author: Hospital Management Team
% Date: December 2025

% ==================== FACTS: SYMPTOM DEFINITIONS ====================

% General Symptoms
symptom(fever).
symptom(fatigue).
symptom(weakness).
symptom(loss_of_appetite).
symptom(weight_loss).
symptom(night_sweats).
symptom(chills).
symptom(malaise).

% Respiratory Symptoms
symptom(cough).
symptom(shortness_of_breath).
symptom(wheezing).
symptom(sore_throat).
symptom(runny_nose).
symptom(nasal_congestion).
symptom(difficulty_breathing).

% Cardiovascular Symptoms
symptom(chest_pain).
symptom(heart_palpitations).
symptom(irregular_heartbeat).
symptom(high_blood_pressure).
symptom(low_blood_pressure).
symptom(rapid_heartbeat).

% Neurological Symptoms
symptom(severe_headache).
symptom(dizziness).
symptom(confusion).
symptom(seizure).
symptom(memory_loss).
symptom(numbness).
symptom(tingling).
symptom(vision_problems).
symptom(loss_of_consciousness).
symptom(difficulty_speaking).

% Gastrointestinal Symptoms
symptom(nausea).
symptom(vomiting).
symptom(diarrhea).
symptom(constipation).
symptom(abdominal_pain).
symptom(bloating).
symptom(blood_in_stool).

% Musculoskeletal Symptoms
symptom(joint_pain).
symptom(muscle_pain).
symptom(back_pain).
symptom(neck_pain).
symptom(stiffness).
symptom(swelling).
symptom(limited_mobility).

% Dermatological Symptoms
symptom(rash).
symptom(itching).
symptom(skin_discoloration).
symptom(bruising).
symptom(hives).
symptom(dry_skin).
symptom(skin_lesions).

% Pediatric Symptoms
symptom(child_fever).
symptom(infant_crying).
symptom(poor_feeding).
symptom(developmental_delay).
symptom(irritability_in_child).

% Other Symptoms
symptom(allergic_reaction).
symptom(dehydration).
symptom(insomnia).
symptom(anxiety).
symptom(depression).
symptom(bleeding).


% ==================== FACTS: SPECIALTY DEFINITIONS ====================

specialty(cardiology).
specialty(neurology).
specialty(pediatrics).
specialty(general_medicine).
specialty(orthopedics).
specialty(dermatology).
specialty(gastroenterology).
specialty(pulmonology).


% ==================== FACTS: DOCTOR ASSIGNMENTS ====================

doctor('Dr. Sarah Johnson', cardiology, 150).
doctor('Dr. Michael Chen', neurology, 140).
doctor('Dr. Emily Davis', general_medicine, 100).
doctor('Dr. Robert Lee', pediatrics, 120).
doctor('Dr. Anna Martinez', orthopedics, 130).


% ==================== RULES: URGENCY CLASSIFICATION ====================

% Emergency Level - Priority 10
urgency_level(Patient, emergency, 10) :-
    has_symptom(Patient, chest_pain).

urgency_level(Patient, emergency, 10) :-
    has_symptom(Patient, heart_palpitations).

urgency_level(Patient, emergency, 10) :-
    has_symptom(Patient, difficulty_breathing).

urgency_level(Patient, emergency, 10) :-
    has_symptom(Patient, loss_of_consciousness).

urgency_level(Patient, emergency, 10) :-
    has_symptom(Patient, severe_bleeding),
    has_symptom(Patient, bleeding).

% High Priority - Priority 8
urgency_level(Patient, high, 8) :-
    has_symptom(Patient, severe_headache).

urgency_level(Patient, high, 8) :-
    has_symptom(Patient, dizziness),
    has_symptom(Patient, confusion).

urgency_level(Patient, high, 8) :-
    has_symptom(Patient, seizure).

urgency_level(Patient, high, 8) :-
    has_symptom(Patient, vision_problems),
    has_symptom(Patient, severe_headache).

urgency_level(Patient, high, 8) :-
    has_symptom(Patient, irregular_heartbeat).

% Medium Priority - Priority 5-6
urgency_level(Patient, medium, 6) :-
    patient_age(Patient, Age),
    Age < 18.

urgency_level(Patient, medium, 6) :-
    has_symptom(Patient, child_fever).

urgency_level(Patient, medium, 5) :-
    has_symptom(Patient, fever),
    has_symptom(Patient, cough).

urgency_level(Patient, medium, 5) :-
    has_symptom(Patient, fever),
    has_symptom(Patient, shortness_of_breath).

urgency_level(Patient, medium, 5) :-
    has_symptom(Patient, vomiting),
    has_symptom(Patient, diarrhea).

% Low Priority - Priority 3
urgency_level(Patient, low, 3) :-
    has_symptom(Patient, fatigue).

urgency_level(Patient, low, 3) :-
    has_symptom(Patient, joint_pain).

urgency_level(Patient, low, 3) :-
    has_symptom(Patient, back_pain).

urgency_level(Patient, low, 3) :-
    has_symptom(Patient, rash).

% Default case if no specific urgency found
urgency_level(Patient, low, 3) :-
    has_symptom(Patient, _).


% ==================== RULES: SPECIALTY ROUTING ====================

% Cardiology
recommend_specialty(Patient, cardiology) :-
    has_symptom(Patient, chest_pain).

recommend_specialty(Patient, cardiology) :-
    has_symptom(Patient, heart_palpitations).

recommend_specialty(Patient, cardiology) :-
    has_symptom(Patient, irregular_heartbeat).

recommend_specialty(Patient, cardiology) :-
    has_symptom(Patient, high_blood_pressure).

% Neurology
recommend_specialty(Patient, neurology) :-
    has_symptom(Patient, severe_headache).

recommend_specialty(Patient, neurology) :-
    has_symptom(Patient, dizziness),
    has_symptom(Patient, confusion).

recommend_specialty(Patient, neurology) :-
    has_symptom(Patient, seizure).

recommend_specialty(Patient, neurology) :-
    has_symptom(Patient, memory_loss).

recommend_specialty(Patient, neurology) :-
    has_symptom(Patient, numbness).

recommend_specialty(Patient, neurology) :-
    has_symptom(Patient, vision_problems).

% Pediatrics
recommend_specialty(Patient, pediatrics) :-
    patient_age(Patient, Age),
    Age < 18.

recommend_specialty(Patient, pediatrics) :-
    has_symptom(Patient, child_fever).

recommend_specialty(Patient, pediatrics) :-
    has_symptom(Patient, infant_crying).

recommend_specialty(Patient, pediatrics) :-
    has_symptom(Patient, poor_feeding).

% Orthopedics
recommend_specialty(Patient, orthopedics) :-
    has_symptom(Patient, joint_pain).

recommend_specialty(Patient, orthopedics) :-
    has_symptom(Patient, back_pain).

recommend_specialty(Patient, orthopedics) :-
    has_symptom(Patient, neck_pain).

recommend_specialty(Patient, orthopedics) :-
    has_symptom(Patient, limited_mobility).

% Dermatology
recommend_specialty(Patient, dermatology) :-
    has_symptom(Patient, rash).

recommend_specialty(Patient, dermatology) :-
    has_symptom(Patient, skin_lesions).

recommend_specialty(Patient, dermatology) :-
    has_symptom(Patient, hives).

% Gastroenterology
recommend_specialty(Patient, gastroenterology) :-
    has_symptom(Patient, abdominal_pain),
    has_symptom(Patient, vomiting).

recommend_specialty(Patient, gastroenterology) :-
    has_symptom(Patient, blood_in_stool).

recommend_specialty(Patient, gastroenterology) :-
    has_symptom(Patient, diarrhea),
    has_symptom(Patient, nausea).

% Pulmonology (Respiratory)
recommend_specialty(Patient, pulmonology) :-
    has_symptom(Patient, shortness_of_breath),
    has_symptom(Patient, cough).

recommend_specialty(Patient, pulmonology) :-
    has_symptom(Patient, wheezing).

recommend_specialty(Patient, pulmonology) :-
    has_symptom(Patient, difficulty_breathing).

% General Medicine (default)
recommend_specialty(Patient, general_medicine) :-
    has_symptom(Patient, fever).

recommend_specialty(Patient, general_medicine) :-
    has_symptom(Patient, fatigue).

recommend_specialty(Patient, general_medicine) :-
    has_symptom(Patient, cough).


% ==================== RULES: DISEASE DIAGNOSIS ====================

% Cardiac Conditions
diagnose_disease(Patient, 'Possible Cardiac Event') :-
    has_symptom(Patient, chest_pain).

diagnose_disease(Patient, 'Cardiac Arrhythmia') :-
    has_symptom(Patient, heart_palpitations),
    has_symptom(Patient, irregular_heartbeat).

diagnose_disease(Patient, 'Hypertension') :-
    has_symptom(Patient, high_blood_pressure),
    has_symptom(Patient, severe_headache).

% Neurological Conditions
diagnose_disease(Patient, 'Neurological Concern') :-
    has_symptom(Patient, severe_headache),
    has_symptom(Patient, dizziness).

diagnose_disease(Patient, 'Migraine') :-
    has_symptom(Patient, severe_headache),
    has_symptom(Patient, vision_problems).

diagnose_disease(Patient, 'Stroke Risk') :-
    has_symptom(Patient, confusion),
    has_symptom(Patient, difficulty_speaking).

diagnose_disease(Patient, 'Epilepsy') :-
    has_symptom(Patient, seizure).

% Respiratory Conditions
diagnose_disease(Patient, 'Respiratory Infection') :-
    has_symptom(Patient, fever),
    has_symptom(Patient, cough).

diagnose_disease(Patient, 'Pneumonia') :-
    has_symptom(Patient, fever),
    has_symptom(Patient, cough),
    has_symptom(Patient, shortness_of_breath).

diagnose_disease(Patient, 'Asthma') :-
    has_symptom(Patient, wheezing),
    has_symptom(Patient, shortness_of_breath).

diagnose_disease(Patient, 'Bronchitis') :-
    has_symptom(Patient, cough),
    has_symptom(Patient, chest_pain).

% Gastrointestinal Conditions
diagnose_disease(Patient, 'Gastroenteritis') :-
    has_symptom(Patient, vomiting),
    has_symptom(Patient, diarrhea).

diagnose_disease(Patient, 'Food Poisoning') :-
    has_symptom(Patient, nausea),
    has_symptom(Patient, vomiting),
    has_symptom(Patient, abdominal_pain).

diagnose_disease(Patient, 'Appendicitis') :-
    has_symptom(Patient, abdominal_pain),
    has_symptom(Patient, fever).

% Musculoskeletal Conditions
diagnose_disease(Patient, 'Arthritis') :-
    has_symptom(Patient, joint_pain),
    has_symptom(Patient, stiffness).

diagnose_disease(Patient, 'Muscle Strain') :-
    has_symptom(Patient, muscle_pain).

diagnose_disease(Patient, 'Spinal Disorder') :-
    has_symptom(Patient, back_pain),
    has_symptom(Patient, limited_mobility).

% Pediatric Conditions
diagnose_disease(Patient, 'Pediatric Consultation') :-
    patient_age(Patient, Age),
    Age < 18.

diagnose_disease(Patient, 'Infant Colic') :-
    has_symptom(Patient, infant_crying),
    has_symptom(Patient, irritability_in_child).

% Dermatological Conditions
diagnose_disease(Patient, 'Skin Infection') :-
    has_symptom(Patient, rash),
    has_symptom(Patient, fever).

diagnose_disease(Patient, 'Allergic Reaction') :-
    has_symptom(Patient, hives),
    has_symptom(Patient, itching).

diagnose_disease(Patient, 'Eczema') :-
    has_symptom(Patient, rash),
    has_symptom(Patient, dry_skin).

% General Conditions
diagnose_disease(Patient, 'Viral Infection') :-
    has_symptom(Patient, fever),
    has_symptom(Patient, fatigue).

diagnose_disease(Patient, 'Dehydration') :-
    has_symptom(Patient, dehydration),
    has_symptom(Patient, dizziness).

diagnose_disease(Patient, 'General Checkup') :-
    has_symptom(Patient, fatigue).


% ==================== RULES: DOCTOR ASSIGNMENT ====================

assign_doctor(Patient, DoctorName) :-
    recommend_specialty(Patient, Specialty),
    doctor(DoctorName, Specialty, _).

% Default doctor if no specialty match
assign_doctor(_, 'Dr. Emily Davis') :-
    !.


% ==================== RULES: COMPLETE DIAGNOSIS ====================

% Main diagnosis rule that combines all components
complete_diagnosis(Patient, Diagnosis) :-
    urgency_level(Patient, Urgency, Priority),
    recommend_specialty(Patient, Specialty),
    diagnose_disease(Patient, Disease),
    assign_doctor(Patient, Doctor),
    Diagnosis = diagnosis(
        urgency(Urgency),
        priority(Priority),
        specialty(Specialty),
        disease(Disease),
        doctor(Doctor)
    ).


% ==================== HELPER PREDICATES ====================

% Check if patient has a specific symptom
has_symptom(Patient, Symptom) :-
    patient_symptom(Patient, Symptom).

% Age-based rules
is_child(Patient) :-
    patient_age(Patient, Age),
    Age < 18.

is_elderly(Patient) :-
    patient_age(Patient, Age),
    Age >= 65.

% Risk assessment
high_risk_patient(Patient) :-
    is_elderly(Patient),
    has_symptom(Patient, chest_pain).

high_risk_patient(Patient) :-
    has_symptom(Patient, difficulty_breathing).


% ==================== QUERIES & TESTING ====================

% Example queries:

% Query 1: Diagnose patient with chest pain
% ?- assert(patient_symptom(patient1, chest_pain)), 
%    complete_diagnosis(patient1, D).

% Query 2: Check urgency for headache patient
% ?- assert(patient_symptom(patient2, severe_headache)),
%    assert(patient_symptom(patient2, dizziness)),
%    urgency_level(patient2, Urgency, Priority).

% Query 3: Find recommended specialty
% ?- assert(patient_symptom(patient3, fever)),
%    assert(patient_symptom(patient3, cough)),
%    recommend_specialty(patient3, Specialty).

% Query 4: Pediatric patient
% ?- assert(patient_age(patient4, 8)),
%    assert(patient_symptom(patient4, fever)),
%    recommend_specialty(patient4, Specialty).

% Query 5: Multiple symptoms diagnosis
% ?- assert(patient_symptom(patient5, joint_pain)),
%    assert(patient_symptom(patient5, stiffness)),
%    diagnose_disease(patient5, Disease).


% ==================== DYNAMIC FACTS (For Runtime) ====================

:- dynamic patient_symptom/2.
:- dynamic patient_age/2.
:- dynamic patient_gender/2.


% ==================== UTILITY PREDICATES ====================

% Clear patient data
clear_patient(Patient) :-
    retractall(patient_symptom(Patient, _)),
    retractall(patient_age(Patient, _)),
    retractall(patient_gender(Patient, _)).

% Add multiple symptoms at once
add_symptoms(Patient, []).
add_symptoms(Patient, [Symptom|Rest]) :-
    assertz(patient_symptom(Patient, Symptom)),
    add_symptoms(Patient, Rest).

% Get all symptoms for a patient
get_all_symptoms(Patient, Symptoms) :-
    findall(S, patient_symptom(Patient, S), Symptoms).

% Count symptoms
count_symptoms(Patient, Count) :-
    get_all_symptoms(Patient, Symptoms),
    length(Symptoms, Count).


% ==================== END OF KNOWLEDGE BASE ====================