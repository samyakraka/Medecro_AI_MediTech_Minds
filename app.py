from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import pickle

import requests
import google.generativeai as genai


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# MongoDB URI and connection



# Load user credentials (for login/registration)
def load_user_credentials():
    if os.path.exists('user_credentials.json'):
        with open('user_credentials.json', 'r') as f:
            return json.load(f)
    return {}

# Save user credentials
def save_user_credentials(data):
    with open('user_credentials.json', 'w') as f:
        json.dump(data, f, indent=4)

# Configure the API key from the environment variable
genai.configure(api_key= 'Your_API_Key' )
model = genai.GenerativeModel('gemini-1.5-flash')

def run_chat(prompt):
    response = model.generate_content(prompt)
    return response.text


# load databasedataset===================================
sym_des = pd.read_csv("Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning/datasets/symtoms_df.csv")
precautions = pd.read_csv("Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning/datasets/precautions_df.csv")
workout = pd.read_csv("Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning/datasets/workout_df.csv")
description = pd.read_csv("Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning/datasets/description.csv")
medications = pd.read_csv('Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning/datasets/medications.csv')
diets = pd.read_csv("Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning/datasets/diets.csv")


# load model===========================================
svc = pickle.load(open('Medicine-Recommendation-System-Personalized-Medical-Recommendation-System-with-Machine-Learning/models/svc.pkl','rb'))


#============================================================
# custome and helping functions
#==========================helper funtions================
def helper(dis):
    desc = description[description['Disease'] == dis]['Description']
    desc = " ".join([w for w in desc])

    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [col for col in pre.values]

    med = medications[medications['Disease'] == dis]['Medication']
    med = [med for med in med.values]

    die = diets[diets['Disease'] == dis]['Diet']
    die = [die for die in die.values]

    wrkout = workout[workout['disease'] == dis] ['workout']


    return desc,pre,med,die,wrkout



symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_list = {15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction', 33: 'Peptic ulcer diseae', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma', 23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)', 28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A', 19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis', 36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack', 39: 'Varicose veins', 26: 'Hypothyroidism', 24: 'Hyperthyroidism', 25: 'Hypoglycemia', 31: 'Osteoarthristis', 5: 'Arthritis', 0: '(vertigo) Paroymsal  Positional Vertigo', 2: 'Acne', 38: 'Urinary tract infection', 35: 'Psoriasis', 27: 'Impetigo'}
symptom_mapping = {
    'itching': ['itching', 'pruritus'],
    'skin_rash': ['skin rash', 'dermatitis', 'eczema', 'rash'],
    'nodal_skin_eruptions': ['nodal skin eruptions', 'lump under skin', 'bumps on skin'],
    'continuous_sneezing': ['continuous sneezing', 'persistent sneezing'],
    'shivering': ['shivering', 'chills', 'cold sweats'],
    'chills': ['chills', 'feeling cold'],
    'joint_pain': ['joint pain', 'arthralgia', 'aches and pains'],
    'stomach_pain': ['stomach pain', 'abdominal pain', 'gastralgia'],
    'acidity': ['acid reflux', 'heartburn', 'gastroesophageal reflux disease'],
    'ulcers_on_tongue': ['tongue ulcers', 'mouth ulcers', 'oral ulcers'],
    'muscle_wasting': ['muscle wasting', 'muscular atrophy'],
    'vomiting': ['vomiting', 'nausea', 'emesis'],
    'burning_micturition': ['burning urination', 'painful urination'],
    'spotting_urination': ['spotting urination', 'hematuria'],
    'fatigue': ['fatigue', 'exhaustion', 'weakness'],
    'weight_gain': ['weight gain', 'obesity', 'overweight'],
    'anxiety': ['anxiety', 'nervousness', 'unease'],
    'cold_hands_and_feets': ['cold hands and feet', 'poor circulation'],
    'mood_swings': ['mood swings', 'irritability', 'temper tantrums'],
    'weight_loss': ['weight loss', 'unintentional weight loss'],
    'restlessness': ['restlessness', 'agitation', 'fidgeting'],
    'lethargy': ['lethargy', 'lassitude', 'listlessness'],
    'patches_in_throat': ['throat patches', 'lump in throat'],
    'irregular_sugar_level': ['irregular sugar levels', 'blood sugar fluctuations'],
    'cough': ['cough', 'dry cough', 'wet cough'],
    'high_fever': ['high fever', 'pyrexia', 'fever'],
    'sunken_eyes': ['sunken eyes', 'pale eyes', 'dull eyes'],
    'breathlessness': ['breathlessness', 'shortness of breath', 'dyspnea'],
    'sweating': ['sweating', 'diaphoresis', 'perspiration'],
    'dehydration': ['dehydration', 'dry mouth', 'low fluid intake'],
    'indigestion': ['indigestion', 'dyspepsia', 'heartburn'],
    'headache': ['headache', 'cephalgia', 'migraine'],
    'yellowish_skin': ['yellowish skin', 'jaundice', 'icterus'],
    'dark_urine': ['dark urine', 'tea-colored urine'],
    'nausea': ['nausea', 'queasiness', 'morning sickness'],
    'loss_of_appetite': ['loss of appetite', 'anorexia', 'hyporexia'],
    'pain_behind_the_eyes': ['eye strain', 'ocular pain', 'orbital pain'],
    'back_pain': ['back pain', 'lower back pain', 'lumbar pain'],
    'constipation': ['constipation', 'bowel obstruction', 'intestinal blockage'],
    'abdominal_pain': ['abdominal pain', 'belly ache', 'stomach cramps'],
    'diarrhoea': ['diarrhea', 'loose stools', 'watery stools'],
    'mild_fever': ['mild fever', 'slight pyrexia', 'low-grade fever'],
    'yellow_urine': ['yellow urine', 'urine discoloration'],
    'yellowing_of_eyes': ['yellow eyes', 'xanthosis'],
    'acute_liver_failure': ['acute liver failure', 'hepatic failure'],
    'fluid_overload': ['fluid overload', 'hydrops', 'edema'],
    'swelling_of_stomach': ['stomach swelling', 'abdominal distension'],
    'swelled_lymph_nodes': ['swollen lymph nodes', 'enlarged lymph nodes'],
    'malaise': ['malaise', 'general feeling of illness', 'ill feeling'],
    'blurred_and_distorted_vision': ['blurred vision', 'double vision', 'distorted vision'],
    'phlegm': ['phlegm', 'mucus production', 'expectoration'],
    'throat_irritation': ['throat irritation', 'sore throat', 'laryngitis'],
    'redness_of_eyes': ['red eyes', 'conjunctivitis', 'pink eye'],
    'sinus_pressure': ['sinus pressure', 'sinus headache', 'nasal congestion'],
    'runny_nose': ['runny nose', 'rhinorrhea', 'nasal discharge'],
    'congestion': ['nasal congestion', 'stuffy nose', 'blocked sinuses'],
    'chest_pain': ['chest pain', 'pectorals', 'angina'],
    'weakness_in_limbs': ['limb weakness', 'paralysis', 'neuropathy'],
    'fast_heart_rate': ['tachycardia', 'rapid heartbeat', 'palpitations'],
    'pain_during_bowel_movements': ['bowel pain', 'intestinal pain', 'cramping'],
    'pain_in_anal_region': ['anal pain', 'rectal pain', 'proctalgia'],
    'bloody_stool': ['bloody stool', 'hematochezia', 'blood in feces'],
    'irritation_in_anus': ['anus irritation', 'rectal irritation', 'pruritus ani'],
    'neck_pain': ['neck pain', 'cervical pain', 'stiff neck'],
    'dizziness': ['dizziness', 'vertigo', 'lightheadedness'],
    'cramps': ['muscle cramps', 'spasm', 'tetany'],
    'bruising': ['bruising', 'ecchymosis', 'purpura'],
    'obesity': ['obesity', 'overweight', 'corpulence'],
    'swollen_legs': ['swollen legs', 'edema', 'water retention'],
    'swollen_blood_vessels': ['swollen blood vessels', 'vascular dilation'],
    'puffy_face_and_eyes': ['puffy face', 'moon face', 'facial edema'],
    'enlarged_thyroid': ['enlarged thyroid', 'goiter', 'thyromegaly'],
    'brittle_nails': ['brittle nails', 'fragile nails', 'onycholysis'],
    'swollen_extremities': ['swollen extremities', 'edema', 'lymphedema'],
    'excessive_hunger': ['excessive hunger', 'polyphagia', 'increased appetite'],
    'extra_marital_contacts': ['extramarital contacts', 'infidelity'],
    'drying_and_tingling_lips': ['dry lips', 'chapped lips', 'lip dryness'],
    'slurred_speech': ['slurred speech', 'dysarthria', 'speech difficulties'],
    'knee_pain': ['knee pain', 'patellofemoral pain syndrome', 'osteoarthritis'],
    'hip_joint_pain': ['hip joint pain', 'coxa pain', 'coxalgia'],
    'muscle_weakness': ['muscle weakness', 'myasthenia', 'muscular hypotonia'],
    'stiff_neck': ['stiff neck', 'cervical stiffness', 'right angle deformity'],
    'swelling_joints': ['swollen joints', 'arthritis', 'synovitis'],
    'movement_stiffness': ['movement stiffness', 'stiffness', 'rigor'],
    'spinning_movements': ['spinning movements', 'vertigo', 'dizziness'],
    'loss_of_balance': ['loss of balance', 'imbalance', 'ataxia'],
    'unsteadiness': ['unsteadiness', 'instability', 'lack of coordination'],
    'weakness_of_one_body_side': ['weakness of one body side', 'hemiparesis', 'monoplegia'],
    'loss_of_smell': ['loss of smell', 'anosmia', 'olfactory dysfunction'],
    'bladder_discomfort': ['bladder discomfort', 'cystitis', 'urinary tract infection'],
    'foul_smell_of_urine': ['foul odor of urine', 'ammoniacal smell'],
    'continuous_feel_of_urine': ['continuous feel of urine', 'urinary urgency'],
    'passage_of_gases': ['gas passing', 'flatulence', 'intestinal gas'],
    'internal_itching': ['internal itching', 'pruritus ani', 'rectal pruritus'],
    'toxic_look_(typhos)': ['toxic look', 'typhoid appearance', 'septic appearance'],
    'depression': ['depression', 'melancholia', 'clinical depression'],
    'irritability': ['irritability', 'testiness', 'short temper'],
    'muscle_pain': ['muscle pain', 'myalgia', 'muscular discomfort'],
    'altered_sensorium': ['altered sensorium', 'mental confusion', 'disorientation'],
    'red_spots_over_body': ['red spots over body', 'petechiae', 'purpura'],
    'belly_pain': ['belly pain', 'abdominal pain', 'stomachache'],
    'abnormal_menstruation': ['abnormal menstruation', 'menstrual irregularity'],
    'dischromic_patches': ['discolored skin patches', 'hyperpigmentation', 'hypopigmentation'],
    'watering_from_eyes': ['watering eyes', 'epiphora', 'excessive tearing'],
    'increased_appetite': ['increased appetite', 'polyphagia', 'hyperphagia'],
    'polyuria': ['polyuria', 'excessive urination'],
    'family_history': ['family history', 'genetic predisposition'],
    'mucoid_sputum': ['mucoid sputum', 'mucous expectoration'],
    'rusty_sputum': ['rusty sputum', 'bloody sputum'],
    'lack_of_concentration': ['lack of concentration', 'poor attention'],
    'visual_disturbances': ['visual disturbances', 'blurred vision'],
    'receiving_blood_transfusion': ['blood transfusion', 'transfusion history'],
    'receiving_unsterile_injections': ['unsterile injections', 'unsafe injections'],
    'coma': ['coma', 'unconsciousness'],
    'stomach_bleeding': ['stomach bleeding', 'gastrointestinal hemorrhage'],
    'distention_of_abdomen': ['abdominal distention', 'bloating'],
    'history_of_alcohol_consumption': ['alcohol consumption history', 'drinking history'],
    'blood_in_sputum': ['blood in sputum', 'hemoptysis'],
    'prominent_veins_on_calf': ['prominent veins on calf', 'varicose veins'],
    'palpitations': ['palpitations', 'rapid heartbeat'],
    'painful_walking': ['painful walking', 'claudication'],
    'pus_filled_pimples': ['pus-filled pimples', 'acne', 'pustules'],
    'blackheads': ['blackheads', 'comedones'],
    'scurring': ['scarring', 'keloid formation'],
    'skin_peeling': ['skin peeling', 'exfoliation'],
    'silver_like_dusting': ['silver-like dusting', 'psoriasis'],
    'small_dents_in_nails': ['small dents in nails', 'pitting'],
    'inflammatory_nails': ['inflammatory nails', 'paronychia'],
    'blister': ['blister', 'vesicle'],
    'red_sore_around_nose': ['red sore around nose', 'nasal ulcer'],
    'yellow_crust_ooze': ['yellow crust ooze', 'impetigo'],
}

def load_symptoms_data():
    # Using the provided symptoms_dict to extract the symptoms
    symptoms_dict = {
        'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 
        'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 
        'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 
        'spotting_urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 
        'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 
        'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 
        'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 
        'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 
        'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 
        'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 
        'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 
        'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 
        'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 
        'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 
        'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 
        'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 
        'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 
        'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 
        'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 
        'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 
        'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 
        'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 
        'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 
        'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 
        'bladder_discomfort': 89, 'foul_smell_of_urine': 90, 'continuous_feel_of_urine': 91, 
        'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 
        'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 
        'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 
        'dischromic_patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 
        'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 
        'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 
        'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 
        'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 
        'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 
        'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 
        'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 
        'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 
        'red_sore_around_nose': 130, 'yellow_crust_ooze': 131
    }
    
    # Return a list of symptoms
    return list(symptoms_dict.keys())


def map_user_symptoms(user_message, symptom_mapping):
    detected_symptoms = set()
    user_message_lower = user_message.lower().strip()

    # Iterate over the symptom mapping to match user input
    for symptom, synonyms in symptom_mapping.items():
        for synonym in synonyms:
            if synonym in user_message_lower:
                detected_symptoms.add(symptom)
                break  # Stop checking other synonyms if one matches
    return list(detected_symptoms)


# Model Prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return diseases_list[svc.predict([input_vector])[0]]

# Load JSON data
def load_user_data():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}


# Load responses from JSON
with open('responses.json', 'r') as f:
    responses_data = json.load(f)


def chatbot_response(user_message, user_id, users_data):
    response = ""
    current_chat = users_data[user_id].get('current_chat', {})
    user_message_lower = user_message.lower().strip()

    # Load doctor data
    doctors_data = load_doctor_data()
    # Start of conversation
    
    # Initialize states if not present
    if "state" not in current_chat:
        current_chat["state"] = "start"

    # if current_chat["state"] == "start":
    #     user_message_lower = user_message.lower()  # Normalize input
    #     for entry in responses_data["questions"]:
    #         if entry["question"] in user_message_lower:
    #             return entry["response"]
           
        
    all_possible_symptoms = load_symptoms_data()  # Load from a reliable source or dataset
    
    # Detect disease from symptoms
    if current_chat["state"] == "start":
        
        user_message_lower = user_message.lower()  # Normalize input

        # Load possible symptoms data
        all_possible_symptoms = load_symptoms_data()
      
        # Symptom mapping here 
        symptom_mapping = {
                'itching': ['itching', 'pruritus'],
                'skin_rash': ['skin rash', 'dermatitis', 'eczema', 'rash'],
                'nodal_skin_eruptions': ['nodal skin eruptions', 'lump under skin', 'bumps on skin'],
                'continuous_sneezing': ['continuous sneezing', 'persistent sneezing'],
                'shivering': ['shivering', 'chills', 'cold sweats'],
                'chills': ['chills', 'feeling cold'],
                'joint_pain': ['joint pain', 'arthralgia', 'aches and pains'],
                'stomach_pain': ['stomach pain', 'abdominal pain', 'gastralgia'],
                'acidity': ['acid reflux', 'heartburn', 'gastroesophageal reflux disease'],
                'ulcers_on_tongue': ['tongue ulcers', 'mouth ulcers', 'oral ulcers'],
                'muscle_wasting': ['muscle wasting', 'muscular atrophy'],
                'vomiting': ['vomiting', 'nausea', 'emesis'],
                'burning_micturition': ['burning urination', 'painful urination'],
                'spotting_urination': ['spotting urination', 'hematuria'],
                'fatigue': ['fatigue', 'exhaustion', 'weakness'],
                'weight_gain': ['weight gain', 'obesity', 'overweight'],
                'anxiety': ['anxiety', 'nervousness', 'unease'],
                'cold_hands_and_feets': ['cold hands and feet', 'poor circulation'],
                'mood_swings': ['mood swings', 'irritability', 'temper tantrums'],
                'weight_loss': ['weight loss', 'unintentional weight loss'],
                'restlessness': ['restlessness', 'agitation', 'fidgeting'],
                'lethargy': ['lethargy', 'lassitude', 'listlessness'],
                'patches_in_throat': ['throat patches', 'lump in throat'],
                'irregular_sugar_level': ['irregular sugar levels', 'blood sugar fluctuations'],
                'cough': ['cough', 'dry cough', 'wet cough'],
                'high_fever': ['high fever', 'pyrexia', 'fever'],
                'sunken_eyes': ['sunken eyes', 'pale eyes', 'dull eyes'],
                'breathlessness': ['breathlessness', 'shortness of breath', 'dyspnea'],
                'sweating': ['sweating', 'diaphoresis', 'perspiration'],
                'dehydration': ['dehydration', 'dry mouth', 'low fluid intake'],
                'indigestion': ['indigestion', 'dyspepsia', 'heartburn'],
                'headache': ['headache', 'cephalgia', 'migraine'],
                'yellowish_skin': ['yellowish skin', 'jaundice', 'icterus'],
                'dark_urine': ['dark urine', 'tea-colored urine'],
                'nausea': ['nausea', 'queasiness', 'morning sickness'],
                'loss_of_appetite': ['loss of appetite', 'anorexia', 'hyporexia'],
                'pain_behind_the_eyes': ['eye strain', 'ocular pain', 'orbital pain'],
                'back_pain': ['back pain', 'lower back pain', 'lumbar pain'],
                'constipation': ['constipation', 'bowel obstruction', 'intestinal blockage'],
                'abdominal_pain': ['abdominal pain', 'belly ache', 'stomach cramps'],
                'diarrhoea': ['diarrhea', 'loose stools', 'watery stools'],
                'mild_fever': ['mild fever', 'slight pyrexia', 'low-grade fever'],
                'yellow_urine': ['yellow urine', 'urine discoloration'],
                'yellowing_of_eyes': ['yellow eyes', 'xanthosis'],
                'acute_liver_failure': ['acute liver failure', 'hepatic failure'],
                'fluid_overload': ['fluid overload', 'hydrops', 'edema'],
                'swelling_of_stomach': ['stomach swelling', 'abdominal distension'],
                'swelled_lymph_nodes': ['swollen lymph nodes', 'enlarged lymph nodes'],
                'malaise': ['malaise', 'general feeling of illness', 'ill feeling'],
                'blurred_and_distorted_vision': ['blurred vision', 'double vision', 'distorted vision'],
                'phlegm': ['phlegm', 'mucus production', 'expectoration'],
                'throat_irritation': ['throat irritation', 'sore throat', 'laryngitis'],
                'redness_of_eyes': ['red eyes', 'conjunctivitis', 'pink eye'],
                'sinus_pressure': ['sinus pressure', 'sinus headache', 'nasal congestion'],
                'runny_nose': ['runny nose', 'rhinorrhea', 'nasal discharge'],
                'congestion': ['nasal congestion', 'stuffy nose', 'blocked sinuses'],
                'chest_pain': ['chest pain', 'pectorals', 'angina'],
                'weakness_in_limbs': ['limb weakness', 'paralysis', 'neuropathy'],
                'fast_heart_rate': ['tachycardia', 'rapid heartbeat', 'palpitations'],
                'pain_during_bowel_movements': ['bowel pain', 'intestinal pain', 'cramping'],
                'pain_in_anal_region': ['anal pain', 'rectal pain', 'proctalgia'],
                'bloody_stool': ['bloody stool', 'hematochezia', 'blood in feces'],
                'irritation_in_anus': ['anus irritation', 'rectal irritation', 'pruritus ani'],
                'neck_pain': ['neck pain', 'cervical pain', 'stiff neck'],
                'dizziness': ['dizziness', 'vertigo', 'lightheadedness'],
                'cramps': ['muscle cramps', 'spasm', 'tetany'],
                'bruising': ['bruising', 'ecchymosis', 'purpura'],
                'obesity': ['obesity', 'overweight', 'corpulence'],
                'swollen_legs': ['swollen legs', 'edema', 'water retention'],
                'swollen_blood_vessels': ['swollen blood vessels', 'vascular dilation'],
                'puffy_face_and_eyes': ['puffy face', 'moon face', 'facial edema'],
                'enlarged_thyroid': ['enlarged thyroid', 'goiter', 'thyromegaly'],
                'brittle_nails': ['brittle nails', 'fragile nails', 'onycholysis'],
                'swollen_extremities': ['swollen extremities', 'edema', 'lymphedema'],
                'excessive_hunger': ['excessive hunger', 'polyphagia', 'increased appetite'],
                'extra_marital_contacts': ['extramarital contacts', 'infidelity'],
                'drying_and_tingling_lips': ['dry lips', 'chapped lips', 'lip dryness'],
                'slurred_speech': ['slurred speech', 'dysarthria', 'speech difficulties'],
                'knee_pain': ['knee pain', 'patellofemoral pain syndrome', 'osteoarthritis'],
                'hip_joint_pain': ['hip joint pain', 'coxa pain', 'coxalgia'],
                'muscle_weakness': ['muscle weakness', 'myasthenia', 'muscular hypotonia'],
                'stiff_neck': ['stiff neck', 'cervical stiffness', 'right angle deformity'],
                'swelling_joints': ['swollen joints', 'arthritis', 'synovitis'],
                'movement_stiffness': ['movement stiffness', 'stiffness', 'rigor'],
                'spinning_movements': ['spinning movements', 'vertigo', 'dizziness'],
                'loss_of_balance': ['loss of balance', 'imbalance', 'ataxia'],
                'unsteadiness': ['unsteadiness', 'instability', 'lack of coordination'],
                'weakness_of_one_body_side': ['weakness of one body side', 'hemiparesis', 'monoplegia'],
                'loss_of_smell': ['loss of smell', 'anosmia', 'olfactory dysfunction'],
                'bladder_discomfort': ['bladder discomfort', 'cystitis', 'urinary tract infection'],
                'foul_smell_of_urine': ['foul odor of urine', 'ammoniacal smell'],
                'continuous_feel_of_urine': ['continuous feel of urine', 'urinary urgency'],
                'passage_of_gases': ['gas passing', 'flatulence', 'intestinal gas'],
                'internal_itching': ['internal itching', 'pruritus ani', 'rectal pruritus'],
                'toxic_look_(typhos)': ['toxic look', 'typhoid appearance', 'septic appearance'],
                'depression': ['depression', 'melancholia', 'clinical depression'],
                'irritability': ['irritability', 'testiness', 'short temper'],
                'muscle_pain': ['muscle pain', 'myalgia', 'muscular discomfort'],
                'altered_sensorium': ['altered sensorium', 'mental confusion', 'disorientation'],
                'red_spots_over_body': ['red spots over body', 'petechiae', 'purpura'],
                'belly_pain': ['belly pain', 'abdominal pain', 'stomachache'],
                'abnormal_menstruation': ['abnormal menstruation', 'menstrual irregularity'],
                'dischromic_patches': ['discolored skin patches', 'hyperpigmentation', 'hypopigmentation'],
                'watering_from_eyes': ['watering eyes', 'epiphora', 'excessive tearing'],
                'increased_appetite': ['increased appetite', 'polyphagia', 'hyperphagia'],
                'polyuria': ['polyuria', 'excessive urination'],
                'family_history': ['family history', 'genetic predisposition'],
                'mucoid_sputum': ['mucoid sputum', 'mucous expectoration'],
                'rusty_sputum': ['rusty sputum', 'bloody sputum'],
                'lack_of_concentration': ['lack of concentration', 'poor attention'],
                'visual_disturbances': ['visual disturbances', 'blurred vision'],
                'receiving_blood_transfusion': ['blood transfusion', 'transfusion history'],
                'receiving_unsterile_injections': ['unsterile injections', 'unsafe injections'],
                'coma': ['coma', 'unconsciousness'],
                'stomach_bleeding': ['stomach bleeding', 'gastrointestinal hemorrhage'],
                'distention_of_abdomen': ['abdominal distention', 'bloating'],
                'history_of_alcohol_consumption': ['alcohol consumption history', 'drinking history'],
                'blood_in_sputum': ['blood in sputum', 'hemoptysis'],
                'prominent_veins_on_calf': ['prominent veins on calf', 'varicose veins'],
                'palpitations': ['palpitations', 'rapid heartbeat'],
                'painful_walking': ['painful walking', 'claudication'],
                'pus_filled_pimples': ['pus-filled pimples', 'acne', 'pustules'],
                'blackheads': ['blackheads', 'comedones'],
                'scurring': ['scarring', 'keloid formation'],
                'skin_peeling': ['skin peeling', 'exfoliation'],
                'silver_like_dusting': ['silver-like dusting', 'psoriasis'],
                'small_dents_in_nails': ['small dents in nails', 'pitting'],
                'inflammatory_nails': ['inflammatory nails', 'paronychia'],
                'blister': ['blister', 'vesicle'],
                'red_sore_around_nose': ['red sore around nose', 'nasal ulcer'],
                'yellow_crust_ooze': ['yellow crust ooze', 'impetigo'],
            }

        # # Detect disease from symptoms
        # detected_symptoms = [sym for sym in all_possible_symptoms if sym in user_message_lower]


        # detected_symptoms = [sym for sym in all_possible_symptoms if sym in user_message_lower]
        # response = "It seems like you haven't mentioned enough symptoms. Can you please specify more symptoms?"
        detected_symptoms = map_user_symptoms(user_message_lower, symptom_mapping)


        if detected_symptoms:
            # Call the prediction function with detected symptoms
            predicted_disease = get_predicted_value(detected_symptoms)
            dis_des, precautions, medications, rec_diet, workout = helper(predicted_disease)

            # Format the response with detailed information
            response = (
                    "<div style='font-family: Arial, sans-serif; line-height: 1.5;'>"
                    "<h2 style='color: #2C3E50;'>Predicted Disease</h2>"
                    f"<p style='font-size: 18px; color: #2980B9;'><strong>{predicted_disease}</strong></p>"
                    
                    "<h3 style='color: #8E44AD;'>Description</h3>"
                    f"<p>{dis_des}</p>"
                    
                    "<h3 style='color: #8E44AD;'>Precautions</h3>"
                   f"<p>{', '.join(map(str, precautions[0]))}</p>"

                    
                    "<h3 style='color: #8E44AD;'>Medications</h3>"
                    f"<p>{', '.join(medications)}</p>"
                    
                    "<h3 style='color: #8E44AD;'>Workout</h3>"
                    f"<p>{', '.join(workout)}</p>"
                    
                    "<h3 style='color: #8E44AD;'>Diet</h3>"
                    f"<p>{', '.join(rec_diet)}</p>"
                    "</div>"
                )


            # Continue to doctor selection based on the predicted disease
            doctors = [doc for doc in doctors_data if predicted_disease.lower() in doc["specialty"].lower()]
            current_chat["doctors"] = doctors
            if doctors:
                doctor_names = "\n".join([f"{i + 1}) {doc['name']}" for i, doc in enumerate(doctors)])
                response += f"\nHere are the doctors available for {predicted_disease}:\n{doctor_names}\nPlease select a doctor by number."
                current_chat["state"] = "select_doctor"
            else:
                response += "Sorry, there are no doctors available for this disease currently ."
                current_chat.clear()

        else:
            # response = "It seems like you haven't mentioned enough symptoms. Can you please specify more symptoms?"
            # current_chat["state"] = "start"
            return run_chat(user_message)

    elif current_chat["state"] == "select_doctor":
        try:
            doctor_choice = int(user_message_lower) - 1
            selected_doctor = current_chat["doctors"][doctor_choice]
            current_chat["selected_doctor"] = selected_doctor["name"]  # Store doctor's name

            response = "You have selected Dr. {}.\nPlease choose a day for your appointment from today to the next 7 days (Monday to Friday):".format(selected_doctor["name"])
            
            weekdays = get_weekdays()
            response += " " + ", ".join([day.split()[0] for day in weekdays])
            current_chat["state"] = "select_day"
        except (ValueError, IndexError):
            response = "Invalid choice. Please select a valid doctor by number you are currently in the middle of taking an appointment."
    # # Handle doctor selection
    # elif current_chat["state"] == "select_doctor":
    #     try:
    #         doctor_choice = int(user_message_lower) - 1
    #         selected_doctor = current_chat["doctors"][doctor_choice]
    # #         response = f"You have selected Dr. {selected_doctor['name']}.\nPlease select a day and time for your appointment."
    # #         current_chat["selected_doctor"] = selected_doctor
    # #         current_chat["state"] = "appointment_booking"
    # #     except (ValueError, IndexError):
    # #         response = "Invalid choice. Please select a valid doctor by number."
    # # # Selecting a doctor
    # # elif current_chat["state"] == "select_doctor" and user_message.isdigit():
    # #     doctor_index = int(user_message) - 1
        
    # #     if 0 <= doctor_index < len(current_chat["doctors"]):
    # #         current_chat["selected_doctor"] = current_chat["doctors"][doctor_index]["name"]
    #         response = "Please choose a day for your appointment from today to the next 7 days (Monday to Friday):"
    #         weekdays = get_weekdays()
    #         response += " " + ", ".join([day.split()[0] for day in weekdays])
    #         current_chat["state"] = "select_day"
    #     except (ValueError, IndexError):
    #         response = "Invalid choice. Please select a valid doctor by number."

    # Selecting a day
    elif current_chat["state"] == "select_day":
        weekdays = get_weekdays()  # Initialize weekdays here
        valid_days = [day.split()[0].lower() for day in get_weekdays()]
        if user_message_lower in valid_days:
            selected_day = next(day for day in weekdays if day.lower().startswith(user_message_lower))
            current_chat["selected_day"] = selected_day
            response = "Please choose a time slot: 9-12, 1-3, 4-6."
            current_chat["state"] = "select_time_slot"
        else:
            response = "Please select a valid weekday."

    # Selecting a time slot
    elif current_chat["state"] == "select_time_slot":
        valid_time_slots = ["9-12", "1-3", "4-6"]
        if user_message in valid_time_slots:
            selected_doctor = next(doc for doc in doctors_data if doc["name"] == current_chat["selected_doctor"])

            # Check if the selected time slot is already booked for the selected day
            existing_appointment = any(
                appt["day"] == current_chat["selected_day"] and appt["time_slot"] == user_message
                for appt in selected_doctor["appointments"]
            )

            if existing_appointment:
                response = f"Sorry, {current_chat['selected_doctor']} already has an appointment on {current_chat['selected_day']} during the {user_message} time slot. Please choose another time slot."
            else:
                # If no conflict, book the appointment
                appointment = {
                    "doctor": current_chat["selected_doctor"],
                    "day": current_chat["selected_day"],
                    "time_slot": user_message
                }
                users_data[user_id]['appointments'].append(appointment)

                # Add the appointment to the doctor's JSON data as well
                selected_doctor["appointments"].append({
                    "patient_id": user_id,
                    "day": current_chat["selected_day"],
                    "time_slot": user_message
                })

                response = f"Your appointment has been booked with {current_chat['selected_doctor']} on {current_chat['selected_day']} during the time slot {user_message}."
                current_chat["state"] = "completed"
                save_user_data(users_data)
                save_doctor_data(doctors_data)  # Save the updated doctor data
                current_chat.clear()
        else:
            response = "Please choose a valid time slot you are currently in the middle of booking appointment ."

    else:
        # If no matching question is found, get a response from the Gemini API
        return run_chat(user_message)

    users_data[user_id]['current_chat'] = current_chat
    save_user_data(users_data)
    return response






def get_weekdays():
    from datetime import datetime, timedelta

    weekdays = []
    today = datetime.now()
    for i in range(7):
        day = today + timedelta(days=i)
        if day.weekday() < 5:  # Monday to Friday
            weekdays.append(day.strftime("%A %d %b %Y"))
    return weekdays

def load_doctor_data():
    import json
    with open("doctors.json", "r") as file:
        return json.load(file)

def save_doctor_data(doctors_data):
    import json
    with open("doctors.json", "w") as file:
        json.dump(doctors_data, file, indent=4)

def save_user_data(users_data):
    import json
    with open("users.json", "w") as file:
        json.dump(users_data, file, indent=4)





@app.route('/')
def home():
    username = None  # Initialize the username variable
    
    if 'user_email' in session:
        username = session['user_email']  # Retrieve the email from the session and assign it to username

        # Check if the email belongs to a doctor
        doctors = load_doctor_data()
        for doctor in doctors:
            if 'email' in doctor and doctor['email'] == username:
                return redirect(url_for('doctor_index'))  # Redirect to doctor index page
        
        # If the email does not match any doctor, treat it as a patient
        return render_template('patient_index.html', username=username)  # Pass username to the template

    return render_template('index.html')


@app.route('/profile')
def profile():
    username = session['user_email']  # Get the logged-in user's email
    users_data = load_user_data()  # Load user data from your storage mechanism
    users_credentials = load_user_credentials()  # Load user credentials
    doctors_data = load_doctor_data()  # Load doctors data

    user_data = users_data.get(username, {})
    user_credentials = users_credentials.get(username, {})

    # Get personal information
    first_name = user_credentials.get('first_name', '')
    last_name = user_credentials.get('last_name', '')
    phone_number = user_credentials.get('phone', '')
    email = username  # Use the email as the username

    # Get appointments
    user_appointments = user_data.get('appointments', [])

    # Extract appointment details
    appointments = []
    for appointment in user_appointments:
        doctor_name = appointment.get('doctor')  # Assuming doctor name is used in appointments
        doctor_info = next((doc for doc in doctors_data if doc["name"] == doctor_name), {})

        appointment_info = {
            'doctor': doctor_name,
            'specialization': doctor_info.get('specialty', 'Unknown'),
            'day': appointment.get('day', ''),
            'time_slot': appointment.get('time_slot', ''),
            'status': 'Pending'  # Default status if not provided
        }
        appointments.append(appointment_info)

    return render_template('profile.html', username=username, user_appointments=appointments,
                           first_name=first_name, last_name=last_name, phone_number=phone_number,
                           email=email)



# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return 'Passwords do not match!'

        user_credentials = load_user_credentials()

        if email in user_credentials:
            return 'Email already registered!'

        # Add user data
        user_credentials[email] = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'password': password
        }

        save_user_credentials(user_credentials)
        return redirect(url_for('login'))

    return render_template('register.html')



# Doctor registration page
@app.route('/register_doctor', methods=['GET', 'POST'])
def register_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialty = request.form['specialty']
        phone = request.form['phone']
        email = request.form['email']
        
        # Prepend "Dr." to the doctor's name
        name = f"Dr. {name}"
        
        # Create a new doctor record
        new_doctor = {
            "name": name,
            "specialty": specialty,
            "phone": phone,
            "email": email,
            "appointments": []
        }

        # Read existing doctors and append the new doctor
        doctors = load_doctor_data()
        doctors.append(new_doctor)
        
        # Save the updated doctors list
        save_doctor_data(doctors)
        
        return redirect(url_for('login'))
    
    return render_template('doctor_registration.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # Use get() to avoid KeyError
        password = request.form.get('password')  # Use get() to avoid KeyError

        # Check if the email belongs to a doctor
        doctors = load_doctor_data()
        for doctor in doctors:
            if 'email' in doctor and doctor['email'] == email:
                # For doctors, no password check (as per your structure)
                session['user_email'] = email  # Create session for the doctor
                session['user_type'] = 'doctor'  # Mark session type as doctor
                return redirect(url_for('doctor_index'))  # Redirect to doctor dashboard

        # Check if the email belongs to a regular user (user with password)
        user_credentials = load_user_credentials()
        if email not in user_credentials or user_credentials[email]['password'] != password:
            return render_template('login.html', error='Invalid email or password!')  # Render error in the template

        # If user credentials are correct
        session['user_email'] = email  # Create session for the user
        session['user_type'] = 'user'  # Mark session type as regular user
        return redirect(url_for('home'))  # Redirect to home page

    # Render the login page if it's a GET request
    return render_template('login.html')

@app.route('/doctor_index')
def doctor_index():
    # Check if user is logged in
    if 'user_email' in session:
        doctor_email = session.get('user_email')
        user_type = session.get('user_type')  # Use 'user_type' for consistency
        
        # Check if the user is a doctor
        if user_type == 'doctor':
            return render_template('doctor_index.html', doctor_email=doctor_email)
        else:
            # If not a doctor, redirect to login or error page
            return redirect(url_for('login'))  # Optionally redirect to an error page for non-doctors
    else:
        # If no user is logged in, redirect to login
        return redirect(url_for('login'))


@app.route('/doctor_index_timetable')
def doctor_index_timetable():
    if 'user_email' in session:
        doctor_email = session.get('user_email')
        user_type = session.get('user_type')
        doctors_data = load_doctor_data()

        if user_type == 'doctor':
            # Find the doctor by email
            doctor = next((doc for doc in doctors_data if doc.get('email') == doctor_email), None)

            if doctor:
                appointments = doctor.get('appointments', [])

                # Organize appointments by actual date
                timetable = {}
                for appointment in appointments:
                    day_info = appointment['day'].split()  # Handles cases like "Wednesday 25 Sep"
                    if len(day_info) > 1:
                        # Handle cases where full date is provided
                        date = ' '.join(day_info[1:])
                    else:
                        # If no date, fallback to just weekday
                        date = day_info[0].capitalize()

                    time_slot = appointment['time_slot']
                    patient_id = appointment.get('patient_id', appointment.get('patient_email', 'Unknown'))

                    # Use date as key to organize appointments
                    if date not in timetable:
                        timetable[date] = []

                    timetable[date].append({
                        'time_slot': time_slot,
                        'patient_id': patient_id
                    })

                return render_template('doctor_index_timetable.html', doctor_email=doctor_email, timetable=timetable)
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    user_id = session['user_email']
    users_data = load_user_data()

    # If user data doesn't exist, create it
    if user_id not in users_data:
        users_data[user_id] = {"chat_history": [], "appointments": [], "current_chat": {}}
        save_user_data(users_data)

    # Chat handling
    if request.method == 'POST':
        user_message = request.form.get('message')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Store the user's chat
        users_data[user_id]['chat_history'].append({
            'sender': 'user',
            'message': user_message,
            'timestamp': timestamp
        })
        
        # Generate chatbot response
        bot_message = chatbot_response(user_message, user_id, users_data)
        bot_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Store the chatbot's chat
        users_data[user_id]['chat_history'].append({
            'sender': 'bot',
            'message': bot_message,
            'timestamp': bot_timestamp
        })

        save_user_data(users_data)

    chat_history = users_data[user_id]['chat_history']
    appointments = users_data[user_id]['appointments']

    return render_template('chat.html', chat_history=chat_history, appointments=appointments)

@app.route('/appointments')
def view_appointments():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    users_data = load_user_data()
    appointments = users_data[user_id]['appointments']
    return render_template('appointments.html', appointments=appointments)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'user_email' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    username = session['user_email']
    
    # Load user and doctor data
    users_data = load_user_data()
    doctors_data = load_doctor_data()

    current_appointments = users_data.get(username, {}).get('appointments', [])
    # current_appointment = current_appointments[0] if current_appointments else None

    if request.method == 'POST':
        selected_day = request.form.get('selected_day')
        selected_time_slot = request.form.get('selected_time_slot')
        selected_doctor = request.form.get('selected_doctor')
        
        # Find the selected doctor
        doctor = next((doc for doc in doctors_data if f"{doc['specialty']} ({doc['name']})" == selected_doctor), None)
        if not doctor:
            return "Doctor not found."

        # Check if the user already has an appointment
        existing_user_appointment = next((appt for appt in current_appointments if appt['day'].lower() == selected_day.lower()), None)
        if existing_user_appointment:
            return render_template('book_appointment.html', 
                                   weekdays=get_weekdays(), 
                                   specialties_with_doctors=specialties_with_doctors, 
                                   doctors=doctors, 
                                   current_appointment=existing_user_appointment)

        # Check if the selected time slot is available
        existing_appointment = any(
            appt["day"].lower() == selected_day.lower() and appt["time_slot"] == selected_time_slot
            for appt in doctor["appointments"]
        )
        
        if existing_appointment:
            return f"Sorry, {doctor['name']} is already booked on {selected_day} during the {selected_time_slot} time slot. Please choose another time slot."
        
        # If available, book the appointment
        appointment = {
            "patient_id": username,
            "day": selected_day,
            "time_slot": selected_time_slot,
        }

        # Store in doctor.json
        doctor["appointments"].append(appointment)

        # Store in users.json
        users_data[username]['appointments'].append({
            "doctor": doctor['name'],
            "day": selected_day,
            "time_slot": selected_time_slot,
        })

        # Save updated user and doctor data
        save_user_data(users_data)
        save_doctor_data(doctors_data)

        return f"Your appointment has been booked with {doctor['name']} on {selected_day} during the {selected_time_slot}."

    # If GET request, render the booking form
    weekdays = get_weekdays()
    doctors = load_doctor_data()  # Load doctors to display in the form
    
    # Create a list of doctor specialties for the dropdown
    specialties_with_doctors = [
        f"{doctor['specialty']} ({doctor['name']})" for doctor in doctors if doctor.get('specialty') and doctor.get('name')
    ]
    
    return render_template('book_appointment.html', 
                           weekdays=weekdays, 
                           specialties_with_doctors=specialties_with_doctors, 
                           doctors=doctors, 
                           current_appointment=current_appointments if current_appointments else None)


def get_weekdays():
    weekdays = []
    tomorrow = datetime.now() + timedelta(days=1)  # Start from tomorrow
    for i in range(8):  # Extend to 8 to include tomorrow and next 7 days
        day = tomorrow + timedelta(days=i)
        if day.weekday() < 5:  # Monday to Friday
            weekdays.append(day.strftime("%A %d %b %Y"))
    return weekdays




@app.route('/doctor_dashboard')
def doctor_dashboard():
    doctors_data = load_doctor_data()
    return render_template('doctor_dashboard.html', doctors=doctors_data)


