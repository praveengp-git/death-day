import streamlit as st
import datetime
from datetime import timedelta

# ------------------------------------------------------------------------------
# A simple dictionary mapping countries to base average life expectancies.
# Adjust or expand as needed. (Values here are illustrative.)
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
# A dictionary for average ABV (alcohol by volume) of different drinks.
# These are rough, fictional examples; real ABVs vary widely.
# ------------------------------------------------------------------------------
alcohol_abv = {
    "Beer": 5.0,
    "Wine": 12.0,
    "Whiskey": 40.0,
    "Tequila": 40.0,
    "Other": 10.0  # fallback for any category not listed
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
    st.title("Hypothetical Death Day Predictor")
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
    weekly_alcohol_volume_ml = 0
    alcohol_type = "Beer"
    if alcohol_status == "Yes":
        alcohol_type = st.selectbox("What type of alcohol do you mostly consume?", list(alcohol_abv.keys()))
        weekly_alcohol_volume_ml = st.slider("How many ml of this alcohol per week on average?", 0, 5000, 500)
    
    # 6. Height
    height_cm = st.slider("Height (cm)", 100, 220, 170)
    
    # 7. Weight
    weight_kg = st.slider("Weight (kg)", 30, 200, 70)
    
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
    # Only calculate and display results after clicking "Calculate"
    # ------------------------------------------------------------------------------
    if st.button("Calculate"):
        
        # --------------------------------------------------------------------------
        #  Base Life Expectancy Calculation
        # --------------------------------------------------------------------------
        base_life_expectancy = country_life_expectancy.get(country, 75)
        
        # Gender-based adjustment (example logic)
        if gender == "Male":
            base_life_expectancy -= 2
        elif gender == "Female":
            base_life_expectancy += 2
        
        # --------------------------------------------------------------------------
        # Adjusting Life Expectancy by user inputs (purely illustrative!)
        # --------------------------------------------------------------------------
        
        # 1) Smoking impact
        if smoke_status == "Yes":
            if cigs_per_day > 5:
                base_life_expectancy -= 1 + (cigs_per_day - 5) * 0.2
            else:
                base_life_expectancy -= 1
        
        # 2) Alcohol impact: using ABV to estimate pure alcohol consumption
        if alcohol_status == "Yes":
            abv_percent = alcohol_abv.get(alcohol_type, 10.0)  # default to 10 if not found
            # pure alcohol in ml/week = total volume * (ABV / 100)
            pure_alcohol_ml_per_week = weekly_alcohol_volume_ml * (abv_percent / 100.0)
            
            # Example logic:
            # If user consumes <= 100 ml of pure alcohol/week => -0.5 year
            # Above 100 ml => subtract additional 0.5 year per each 100 ml over 100
            if pure_alcohol_ml_per_week > 100:
                base_life_expectancy -= 0.5 + ((pure_alcohol_ml_per_week - 100) / 100) * 0.5
            else:
                base_life_expectancy -= 0.5
        
        # 3) Family history
        if family_heart_disease == "Yes":
            base_life_expectancy -= 2
        if family_cancer == "Yes":
            base_life_expectancy -= 2
        
        # 4) Sleep
        if sleep_hours < 6:
            base_life_expectancy -= (6 - sleep_hours) * 0.5
        elif sleep_hours > 9:
            base_life_expectancy -= (sleep_hours - 9) * 0.5
        
        # 5) BMI impact
        #    BMI = kg / (m^2)
        bmi = 0
        if height_cm > 0:
            bmi = weight_kg / ((height_cm / 100) ** 2)
        
        # Example: 
        # - Underweight (<18.5): -1 year
        # - Overweight (25 <= BMI < 30): -1 year
        # - Obese (>=30): -2 years
        if bmi < 18.5:
            base_life_expectancy -= 1
        elif 25 <= bmi < 30:
            base_life_expectancy -= 1
        elif bmi >= 30:
            base_life_expectancy -= 2
        
        # 6) Work hours (Stress factor)
        #    e.g. For each hour above 40, subtract 0.05 years
        if work_hours_per_week > 40:
            over_40 = work_hours_per_week - 40
            base_life_expectancy -= over_40 * 0.05
        
        # 7) Exercise
        if exercise_hours_per_week <= 5:
            base_life_expectancy += exercise_hours_per_week * 0.2
        else:
            base_life_expectancy += 5 * 0.2
        
        # 8) Diet Quality
        diet_impact = {
            "Poor": -2,
            "Moderate": -1,
            "Good": 0,
            "Excellent": 1
        }
        base_life_expectancy += diet_impact.get(diet_quality, 0)
        
        # Ensure life expectancy doesn't drop below 1
        if base_life_expectancy < 1:
            base_life_expectancy = 1
        
        # --------------------------------------------------------------------------
        # Calculate Date of Death
        # --------------------------------------------------------------------------
        total_days = int(base_life_expectancy * 365.25)
        predicted_death_date = dob + timedelta(days=total_days)
        death_day_of_week = get_day_of_week(predicted_death_date)
        
        # --------------------------------------------------------------------------
        # Calculate how many hours left (awake and not working)
        # --------------------------------------------------------------------------
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
            free_hours_from_leftover_days = leftover_days * (
                awake_hours_per_day - (work_hours_per_week / 7.0)
            )
            
            free_hours_left = free_hours_from_full_weeks + free_hours_from_leftover_days
        
        # Convert free_hours_left into days and years (24 hrs = 1 day, 365 days = 1 year)
        free_days_left = free_hours_left / 24.0
        free_years_left = free_days_left / 365.0
        
        # --------------------------------------------------------------------------
        # Display the results
        # --------------------------------------------------------------------------
        st.subheader("Let's put things into Perspective!")
        st.write(f"**Calculated Life Expectancy**: ~{base_life_expectancy:.1f} years from birth")
        st.write(f"**Predicted Date of Death**: {predicted_death_date.strftime('%Y-%m-%d')}")
        st.write(f"**Day of the Week**: {death_day_of_week}")
        
        # We intentionally do NOT show BMI here as per your instructions.
        
        st.write(
            f"**Free Hours Left (awake & not working)**: ~{int(free_hours_left)} hours "
            f"(~{free_days_left:.2f} days, ~{free_years_left:.2f} years)"
        )

if __name__ == "__main__":
    main()
