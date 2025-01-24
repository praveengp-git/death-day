import streamlit as st
import datetime
from datetime import timedelta
import math

# ------------------------------------------------------------------------------
# A simple dictionary mapping countries to base average life expectancies.
# Adjust or expand as needed.
# (Values here are illustrative and not necessarily accurate.)
# ------------------------------------------------------------------------------
country_life_expectancy = {
    "United States": 77,
    "Canada": 80,
    "India": 70,
    "United Kingdom": 79,
    "Australia": 82,
    "Other": 75  # Fallback
}

# ------------------------------------------------------------------------------
# A helper function to get day of the week from a date
# ------------------------------------------------------------------------------
def get_day_of_week(date_obj):
    return date_obj.strftime("%A")

# ------------------------------------------------------------------------------
# Main streamlit code
# ------------------------------------------------------------------------------
def main():
    st.title("Hypothetical Death Day Predictor by Praveen GP")
    st.write("**Disclaimer**: This is purely a fun, illustrative app and does **not** provide any real medical or actuarial advice. All numbers are fictional.")
    
    # 1. Date of Birth (date picker)
    dob = st.date_input("Date of Birth", datetime.date(1990,1,1))
    
    # 2. Residing Country (drop down)
    country = st.selectbox("Country of Residence", list(country_life_expectancy.keys()))
    
    # 3. Gender
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    # 4. Smoking
    smoke_status = st.selectbox("Do you smoke?", ["No", "Yes"])
    cigs_per_day = 0
    if smoke_status == "Yes":
        cigs_per_day = st.slider("How many cigarettes per day on average?", 1, 60, 10)
    
    # 5. Alcohol
    alcohol_status = st.selectbox("Do you consume alcohol?", ["No", "Yes"])
    weekly_alcohol_ml = 0
    alcohol_type = ""
    if alcohol_status == "Yes":
        weekly_alcohol_ml = st.slider("How many ml of alcohol per week on average?", 0, 5000, 500)
        alcohol_type = st.text_input("What type of alcohol do you mostly consume? (e.g., beer, wine, whiskey...)")
    
    # 6. Height
    height = st.slider("Height (cm)", 100, 220, 170)
    
    # 7. Weight
    weight = st.slider("Weight (kg)", 30, 200, 70)
    
    # 8. Family History
    family_heart_disease = st.selectbox("Family history of heart disease?", ["No", "Yes"])
    family_cancer = st.selectbox("Family history of cancers?", ["No", "Yes"])
    
    # 9. Hours of sleep
    sleep_hours = st.slider("Hours of sleep per day (average)", 0, 12, 7)
    
    # 10. Hours of work
    work_hours_per_week = st.slider("Hours of work per week (average)", 0, 100, 40)
    
    # 11. Hours of exercise
    exercise_hours_per_week = st.slider("Hours of exercise per week (average)", 0, 20, 2)
    
    # 12. Additional relevant questions (optional)
    diet_quality = st.selectbox("Diet Quality?", ["Poor", "Moderate", "Good", "Excellent"])
    
    # ------------------------------------------------------------------------------
    #  Base Life Expectancy Calculation
    # ------------------------------------------------------------------------------
    
    # Get base life expectancy from user's chosen country
    base_life_expectancy = country_life_expectancy.get(country, 75)
    
    # Adjust for gender (rough, fictional assumptions)
    # Male: -2, Female: +2, Other: no change
    if gender == "Male":
        base_life_expectancy -= 2
    elif gender == "Female":
        base_life_expectancy += 2
    
    # ------------------------------------------------------------------------------
    # Adjusting Life Expectancy by user inputs (purely illustrative!)
    # ------------------------------------------------------------------------------
    
    # Smoking impact
    if smoke_status == "Yes":
        if cigs_per_day > 5:
            base_life_expectancy -= 1 + (cigs_per_day - 5) * 0.2
        else:
            base_life_expectancy -= 1
    
    # Alcohol impact
    if alcohol_status == "Yes":
        base_life_expectancy -= (weekly_alcohol_ml / 500) * 1
    
    # Family history
    if family_heart_disease == "Yes":
        base_life_expectancy -= 2
    if family_cancer == "Yes":
        base_life_expectancy -= 2
    
    # Sleep
    if sleep_hours < 6:
        base_life_expectancy -= (6 - sleep_hours) * 0.5
    elif sleep_hours > 9:
        base_life_expectancy -= (sleep_hours - 9) * 0.5
    
    # Work hours
    if work_hours_per_week > 60:
        base_life_expectancy -= (work_hours_per_week - 60) * 0.1
    
    # Exercise
    if exercise_hours_per_week <= 5:
        base_life_expectancy += exercise_hours_per_week * 0.2
    else:
        base_life_expectancy += 5 * 0.2
    
    # Diet Quality
    diet_impact = {
        "Poor": -2,
        "Moderate": -1,
        "Good": 0,
        "Excellent": 1
    }
    base_life_expectancy += diet_impact.get(diet_quality, 0)
    
    # Ensure life expectancy doesn't go below 0
    if base_life_expectancy < 0:
        base_life_expectancy = 1  # minimal fallback
    
    # ------------------------------------------------------------------------------
    # Calculate Date of Death
    # ------------------------------------------------------------------------------
    total_days = int(base_life_expectancy * 365.25)
    predicted_death_date = dob + timedelta(days=total_days)
    death_day_of_week = get_day_of_week(predicted_death_date)
    
    # ------------------------------------------------------------------------------
    # Calculate how many hours left (awake and not working)
    # ------------------------------------------------------------------------------
    today = datetime.date.today()
    
    if predicted_death_date <= today:
        free_hours_left = 0
    else:
        days_remaining = (predicted_death_date - today).days
        
        awake_hours_per_day = 24 - sleep_hours
        awake_hours_per_week = 7 * awake_hours_per_day
        free_hours_per_week = awake_hours_per_week - work_hours_per_week
        
        full_weeks = days_remaining // 7
        leftover_days = days_remaining % 7
        
        free_hours_from_full_weeks = full_weeks * free_hours_per_week
        free_hours_from_leftover_days = leftover_days * (awake_hours_per_day - (work_hours_per_week / 7.0))
        
        free_hours_left = free_hours_from_full_weeks + free_hours_from_leftover_days
    
    # Convert free_hours_left into days and years (24 hrs = 1 day, 365 days = 1 year)
    free_days_left = free_hours_left / 24.0
    free_years_left = free_days_left / 365.0
    
    # ------------------------------------------------------------------------------
    # Display the results
    # ------------------------------------------------------------------------------
    st.subheader("Results")
    st.write(f"**Calculated Life Expectancy**: ~{base_life_expectancy:.1f} years from birth")
    st.write(f"**Predicted Date of Death**: {predicted_death_date.strftime('%Y-%m-%d')}")
    st.write(f"**Day of the Week**: {death_day_of_week}")
    
    st.write(f"**Free Hours Left (awake & not working)**: ~{int(free_hours_left)} hours "
             f"(~{free_days_left:.2f} days, ~{free_years_left:.2f} years)")

if __name__ == "__main__":
    main()
