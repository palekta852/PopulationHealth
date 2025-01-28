
import pandas as pd
import random
import numpy as np
from faker import Faker

fake = Faker()

# Parameters
num_patients = 1000
num_providers = 200
num_visits = 1500
num_referrals = 800
num_emergency_visits = 600
num_hospitalizations = 500
num_chronic_conditions = 700
num_sdh = 900
num_behavioral_health = 400
num_quality_metrics = 1000




# Helper function to introduce unclean data
def introduce_noise(value, prob=0.1):
    return value if random.random() > prob else None


chronic_conditions = pd.DataFrame({
    "ConditionID": range(1, num_chronic_conditions + 1),
    "PatientID": [introduce_noise(random.randint(1, num_patients)) for _ in range(num_chronic_conditions)],
    "Condition": [introduce_noise(random.choice([
        "Diabetes", "Hypertension", "Asthma", "COPD", "Arthritis", "Obesity"
    ])) for _ in range(num_chronic_conditions)],
    "DiagnosisDate": [introduce_noise(fake.date_between(start_date='-10y', end_date='today')) for _ in range(num_chronic_conditions)],
})

# Generate SDH Table (Social Determinants of Health)
sdh = pd.DataFrame({
    "SDHID": range(1, num_sdh + 1),
    "PatientID": [introduce_noise(random.randint(1, num_patients)) for _ in range(num_sdh)],
    "Factor": [introduce_noise(random.choice([
        "Housing Instability", "Food Insecurity", "Transportation Issues", 
        "Unemployment", "Low Income", "Education Barrier"
    ])) for _ in range(num_sdh)],
    "Severity": [introduce_noise(random.choice(["Low", "Medium", "High"])) for _ in range(num_sdh)],
})

# Generate Behavioral Health Table
behavioral_health = pd.DataFrame({
    "BehavioralHealthID": range(1, num_behavioral_health + 1),
    "PatientID": [introduce_noise(random.randint(1, num_patients)) for _ in range(num_behavioral_health)],
    "Diagnosis": [introduce_noise(random.choice([
        "Depression", "Anxiety", "Bipolar Disorder", "Substance Use Disorder", 
        "PTSD", "Schizophrenia"
    ])) for _ in range(num_behavioral_health)],
    "VisitDate": [introduce_noise(fake.date_between(start_date='-5y', end_date='today')) for _ in range(num_behavioral_health)],
})

# Generate Quality Metrics Table
quality_metrics = pd.DataFrame({
    "MetricID": range(1, num_quality_metrics + 1),
    "VisitID": [introduce_noise(random.randint(1, num_visits)) for _ in range(num_quality_metrics)],
    "MetricName": [introduce_noise(random.choice([
        "Medication Adherence", "Follow-Up Rate", "Preventive Screenings", 
        "Care Plan Compliance", "Vaccination Rate"
    ])) for _ in range(num_quality_metrics)],
    "Score": [introduce_noise(random.randint(0, 100)) for _ in range(num_quality_metrics)],
    "DateAssessed": [introduce_noise(fake.date_between(start_date='-2y', end_date='today')) for _ in range(num_quality_metrics)],
})

# Save Additional CSVs
additional_datasets = {
    "ChronicConditions.csv": chronic_conditions,
    "SDH.csv": sdh,
    "BehavioralHealth.csv": behavioral_health,
    "QualityMetrics.csv": quality_metrics,
}

for filename, df in additional_datasets.items():
    df.to_csv(filename, index=False)