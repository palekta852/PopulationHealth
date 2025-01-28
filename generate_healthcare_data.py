import pandas as pd
import random
from faker import Faker
from datetime import datetime

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

# Helper function to generate dates after a given date
def random_date_after(start_date):
    return fake.date_between_dates(date_start=start_date, date_end=datetime.now().date())

# Generate Patients Table
patients = pd.DataFrame({
    "PatientID": range(1, num_patients + 1),
    "FirstName": [introduce_noise(fake.first_name()) for _ in range(num_patients)],
    "LastName": [introduce_noise(fake.last_name()) for _ in range(num_patients)],
    "DateOfBirth": [introduce_noise(fake.date_of_birth(minimum_age=0, maximum_age=90)) for _ in range(num_patients)],
    "Gender": [introduce_noise(random.choice(["Male", "Female", "Other"])) for _ in range(num_patients)],
    "RaceEthnicity": [introduce_noise(fake.random_element(elements=("White", "Black", "Asian", "Hispanic", "Other"))) for _ in range(num_patients)],
    "Address": [introduce_noise(fake.address().replace("\n", ", ")) for _ in range(num_patients)],
    "City": [introduce_noise(fake.city()) for _ in range(num_patients)],
    "State": [introduce_noise(fake.state()) for _ in range(num_patients)],
    "ZIPCode": [introduce_noise(fake.zipcode()) for _ in range(num_patients)],
    "InsuranceType": [introduce_noise(random.choice(["Private", "Medicaid", "Medicare", "Uninsured"])) for _ in range(num_patients)],
})

# Generate Providers Table
providers = pd.DataFrame({
    "ProviderID": range(1, num_providers + 1),
    "ProviderName": [introduce_noise(fake.name()) for _ in range(num_providers)],
    "Specialty": [introduce_noise(random.choice(["Primary Care", "Cardiology", "Oncology", "Pediatrics", "Emergency Medicine"])) for _ in range(num_providers)],
    "ClinicName": [introduce_noise(fake.company()) for _ in range(num_providers)],
    "City": [introduce_noise(fake.city()) for _ in range(num_providers)],
    "State": [introduce_noise(fake.state()) for _ in range(num_providers)],
    "ZIPCode": [introduce_noise(fake.zipcode()) for _ in range(num_providers)],
})

# Generate PrimaryCareVisits Table
primary_care_visits = pd.DataFrame({
    "VisitID": range(1, num_visits + 1),
    "PatientID": [introduce_noise(random.randint(1, num_patients)) for _ in range(num_visits)],
    "VisitDate": [introduce_noise(fake.date_this_decade()) for _ in range(num_visits)],
    "ReasonForVisit": [introduce_noise(fake.lexify("?????")) for _ in range(num_visits)],  # Simulating ICD-10
    "LabTestsOrdered": [introduce_noise(", ".join(fake.words(nb=random.randint(0, 3)))) for _ in range(num_visits)],
    "MedicationsPrescribed": [introduce_noise(", ".join(fake.words(nb=random.randint(0, 3)))) for _ in range(num_visits)],
    "ProviderID": [introduce_noise(random.randint(1, num_providers)) for _ in range(num_visits)],
})

# Generate EmergencyVisits Table
emergency_visits = pd.DataFrame({
    "EmergencyVisitID": range(1, num_emergency_visits + 1),
    "PatientID": [introduce_noise(random.randint(1, num_patients)) for _ in range(num_emergency_visits)],
    "VisitDate": [introduce_noise(fake.date_this_year()) for _ in range(num_emergency_visits)],
    "ReasonForVisit": [introduce_noise(fake.lexify("?????")) for _ in range(num_emergency_visits)],
    "ProviderID": [introduce_noise(random.randint(1, num_providers)) for _ in range(num_emergency_visits)],
    "Disposition": [introduce_noise(random.choice(["Admitted", "Discharged", "Transferred"])) for _ in range(num_emergency_visits)],
})

# Generate Hospitalizations Table
hospitalizations = pd.DataFrame({
    "HospitalizationID": range(1, num_hospitalizations + 1),
    "PatientID": [introduce_noise(random.randint(1, num_patients)) for _ in range(num_hospitalizations)],
    "AdmissionDate": [introduce_noise(fake.date_this_year()) for _ in range(num_hospitalizations)],
    "DischargeDate": [introduce_noise(random_date_after(fake.date_this_year())) for _ in range(num_hospitalizations)],
    "ReasonForAdmission": [introduce_noise(fake.lexify("?????")) for _ in range(num_hospitalizations)],
    "ProviderID": [introduce_noise(random.randint(1, num_providers)) for _ in range(num_hospitalizations)],
})

# Generate Referrals Table
referrals = pd.DataFrame({
    "ReferralID": range(1, num_referrals + 1),
    "PatientID": [introduce_noise(random.randint(1, num_patients)) for _ in range(num_referrals)],
    "ReferringProviderID": [introduce_noise(random.randint(1, num_providers)) for _ in range(num_referrals)],
    "SpecialistProviderID": [introduce_noise(random.randint(1, num_providers)) for _ in range(num_referrals)],
    "ReferralDate": [introduce_noise(fake.date_this_year()) for _ in range(num_referrals)],
    "ReasonForReferral": [introduce_noise(fake.lexify("?????")) for _ in range(num_referrals)],
    "FollowUpCompleted": [introduce_noise(random.choice(["Yes", "No"])) for _ in range(num_referrals)],
})

# Quality Reporting Function
def generate_quality_report(dfs):
    report = []
    for name, df in dfs.items():
        report.append({
            "TableName": name,
            "TotalRows": len(df),
            "NullValues": df.isnull().sum().to_dict(),
            "PercentageNull": (df.isnull().mean() * 100).to_dict(),
        })
    return pd.DataFrame(report)

# Save CSVs
datasets = {
    "Patients.csv": patients,
    "Providers.csv": providers,
    "PrimaryCareVisits.csv": primary_care_visits,
    "EmergencyVisits.csv": emergency_visits,
    "Hospitalizations.csv": hospitalizations,
    "Referrals.csv": referrals,
}

for filename, df in datasets.items():
    df.to_csv(filename, index=False)

# Generate and save quality report
quality_report = generate_quality_report(datasets)
quality_report.to_csv("QualityReport.csv", index=False)

print("Data generation complete. Quality report saved as 'QualityReport.csv'.")
