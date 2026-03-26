# ========================================
# Threat Detection and Safety Analyzer
# ========================================

import random


threat_objects = ['Missile', 'Drone', 'Rocket', 'Balloon', 'Firework', 'UAV', 'Grenade', 'Debris', 'Satellite']
veg_levels = ['Low', 'Medium', 'High']


def get_input(prompt, valid=None, cast=str):
    while True:
        user_val = input(prompt)
        if user_val.lower() == 'exit':
            return 'exit'
        if valid and user_val not in valid:
            print("Invalid input. Try again.")
            continue
        if cast != str:
            try:
                return cast(user_val)
            except ValueError:
                print("Please enter a valid value.")
                continue
        return user_val

def classify(score, thresholds):
    for level, limit in thresholds:
        if score >= limit:
            return level
    return 'Unknown'

def give_advice(level, advice_dict):
    return random.choice(advice_dict[level])

def show_result(title, level, value=None, unit=None, advice=None):
    print("\n" + "-"*45)
    print(f"{title} RESULT")
    print("-"*45)
    if value is not None:
        print(f"Level: {level}")
        print(f"Score: {round(value,1)}{unit if unit else ''}")
    else:
        print(f"Level: {level}")
    print(f"Advice: {advice}")
    print("-"*45 + "\n")

# ---------- Detection Functions ----------
def threat_detection():
    print("\n--- Threat Detection ---")
    obj = get_input(f"Enter object {threat_objects}: ", threat_objects)
    if obj == 'exit': return
    distance = get_input("Distance (m): ", cast=int)
    if distance == 'exit': return
    speed = get_input("Speed (km/h): ", cast=int)
    if speed == 'exit': return
    size = get_input("Size (Small/Medium/Large): ", ['Small','Medium','Large'])
    if size == 'exit': return

    score = threat_objects.index(obj) + 1
    score += {'Small':1,'Medium':2,'Large':3}[size]
    score += max(0, 1000 - distance)/100
    score += speed/50

    level = classify(score, [('High',15),('Medium',8),('Low',0)])
    impact = min(10, score/2)

    advice_dict = {
        'High': ["Take cover immediately.", "Call authorities!"],
        'Medium': ["Stay indoors.", "Be cautious."],
        'Low': ["Minor threat.", "Just watch surroundings."]
    }

    show_result("Threat", level, impact, "/10", give_advice(level, advice_dict))

def forest_fire_detection():
    print("\n--- Forest Fire Detection ---")
    temp = get_input("Temperature (°C): ", cast=int)
    if temp == 'exit': return
    humidity = get_input("Humidity (%): ", cast=int)
    if humidity == 'exit': return
    wind = get_input("Wind speed (km/h): ", cast=int)
    if wind == 'exit': return
    veg = get_input("Vegetation (Low/Medium/High): ", veg_levels)
    if veg == 'exit': return

    score = temp/5 + wind/10
    score += {'Low':1,'Medium':2,'High':3}[veg]
    score -= humidity/10

    level = classify(score, [('High',15),('Medium',8),('Low',0)])
    severity = min(10, score/1.5)

    advice_dict = {
        'High': ["Evacuate area!", "Fire danger high."],
        'Medium': ["Stay alert.", "Possible fire risk."],
        'Low': ["Looks safe.", "Still keep watch."]
    }

    show_result("Forest Fire", level, severity, "/10", give_advice(level, advice_dict))

def air_quality_detection():
    print("\n--- Air Quality ---")
    pm25 = get_input("PM2.5 (µg/m³): ", cast=float)
    if pm25 == 'exit': return
    pm10 = get_input("PM10 (µg/m³): ", cast=float)
    if pm10 == 'exit': return
    co = get_input("CO (ppm): ", cast=float)
    if co == 'exit': return

    score = pm25/12 + pm10/50 + co/9
    level = classify(score, [('Poor',10),('Moderate',5),('Good',0)])

    advice_dict = {
        'Poor': ["Avoid going outside.", "Use masks."],
        'Moderate': ["Limit exposure.", "Be cautious."],
        'Good': ["Air is clean.", "Enjoy outside."]
    }

    show_result("Air Quality", level, None, None, give_advice(level, advice_dict))

def water_detection():
    print("\n--- Water Check ---")
    ph = get_input("pH value: ", cast=float)
    if ph == 'exit': return
    turbidity = get_input("Turbidity (NTU): ", cast=float)
    if turbidity == 'exit': return
    bacteria = get_input("Bacteria count (CFU/mL): ", cast=int)
    if bacteria == 'exit': return

    score = abs(7 - ph) + turbidity/5 + bacteria/100
    level = classify(score, [('High',10),('Medium',5),('Low',0)])

    advice_dict = {
        'High': ["Unsafe to drink.", "Boil or filter before use."],
        'Medium': ["Be cautious.", "Boil water if possible."],
        'Low': ["Safe to drink.", "Good quality."]
    }

    show_result("Water", level, None, None, give_advice(level, advice_dict))

# ---------- Main Menu ----------
def main():
    print("=== SAFETY DETECTION CLI ===")

    while True:
        print("\nSelect hazard to detect:")
        print("1 - Threat")
        print("2 - Forest Fire")
        print("3 - Air Quality")
        print("4 - Water")
        print("5 - Exit")

        choice = input("Enter choice (1-5): ").strip()

        if choice == '1':
            threat_detection()
        elif choice == '2':
            forest_fire_detection()
        elif choice == '3':
            air_quality_detection()
        elif choice == '4':
            water_detection()
        elif choice == '5' or choice.lower() == 'exit':
            print("Exiting program. Stay safe!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
