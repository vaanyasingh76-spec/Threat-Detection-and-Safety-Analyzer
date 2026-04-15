# ========================================
# Threat Detection and Safety Analyzer
# ========================================

import random
import math

history = []


def distance(p1, p2):
    total = 0
    for i in range(len(p1)):
        total += (p1[i] - p2[i]) ** 2
    return math.sqrt(total)


def knn_predict(train_X, train_y, new_point, k=5):
    distances = []

    for i in range(len(train_X)):
        d = distance(train_X[i], new_point)
        distances.append((d, train_y[i]))

    
    distances.sort(key=lambda x: x[0])
    neighbors = distances[:k]


    votes = {}
    for _, label in neighbors:
        votes[label] = votes.get(label, 0) + 1

    # return label with max votes
    return max(votes, key=votes.get)



def make_threat_data():
    X, y = [], []

    for _ in range(200):
        obj = random.randint(1, 9)
        size = random.randint(1, 3)
        distance_val = random.randint(50, 1000)
        speed = random.randint(10, 800)

        score = obj + size + max(0, 1000 - distance_val)/100 + speed/50

        if score >= 15:
            label = 2
        elif score >= 8:
            label = 1
        else:
            label = 0

        X.append([obj, size, distance_val, speed])
        y.append(label)

    return X, y


def make_fire_data():
    X, y = [], []

    for _ in range(200):
        temp = random.randint(10, 50)
        humidity = random.randint(10, 100)
        wind = random.randint(0, 100)
        veg = random.randint(1, 3)

        score = temp/5 + wind/10 + veg - humidity/10

        if score >= 15:
            label = 2
        elif score >= 8:
            label = 1
        else:
            label = 0

        X.append([temp, humidity, wind, veg])
        y.append(label)

    return X, y



print("Preparing data...")

threat_X, threat_y = make_threat_data()
fire_X, fire_y = make_fire_data()

print("System ready ✔")


def show_result(title, level, confidence, advice):
    print("\n" + "-"*40)
    print(f"{title} RESULT")
    print("-"*40)
    print(f"Risk Level : {level}")
    print(f"Confidence : {round(confidence*100, 2)}%")
    print(f"Advice     : {advice}")
    print("-"*40 + "\n")

def get_confidence(train_X, train_y, new_point, k=5):
    distances = []

    for i in range(len(train_X)):
        d = distance(train_X[i], new_point)
        distances.append((d, train_y[i]))

    distances.sort(key=lambda x: x[0])
    neighbors = distances[:k]

    votes = {}
    for _, label in neighbors:
        votes[label] = votes.get(label, 0) + 1

    max_votes = max(votes.values())
    return max_votes / k


def detect_threat():
    print("\n--- Threat Detection ---")

    obj = int(input("Object type (1-9): "))
    size = int(input("Size (1=Small, 2=Medium, 3=Large): "))
    distance_val = int(input("Distance (m): "))
    speed = int(input("Speed (km/h): "))

    new_point = [obj, size, distance_val, speed]

    pred = knn_predict(threat_X, threat_y, new_point)
    confidence = get_confidence(threat_X, threat_y, new_point)

    levels = ["Low", "Medium", "High"]
    advice = [
        "Nothing serious, just stay aware.",
        "Stay alert, something seems unusual.",
        "Danger detected! Take cover immediately."
    ]

    level = levels[pred]

    history.append(("Threat", level))
    show_result("Threat", level, confidence, advice[pred])



def detect_fire():
    print("\n--- Forest Fire Check ---")

    temp = int(input("Temperature (°C): "))
    humidity = int(input("Humidity (%): "))
    wind = int(input("Wind speed (km/h): "))
    veg = int(input("Vegetation (1-3): "))

    new_point = [temp, humidity, wind, veg]

    pred = knn_predict(fire_X, fire_y, new_point)
    confidence = get_confidence(fire_X, fire_y, new_point)

    levels = ["Low", "Medium", "High"]
    advice = [
        "Looks safe for now.",
        "Be cautious, risk is increasing.",
        "High fire risk! Consider evacuation."
    ]

    level = levels[pred]

    history.append(("Fire", level))
    show_result("Forest Fire", level, confidence, advice[pred])


def show_history():
    print("\n--- Past Results ---")

    if not history:
        print("No previous checks yet.")
        return

    for i, (system, level) in enumerate(history, 1):
        print(f"{i}. {system} → {level}")


def main():
    print("\n=====  Safety Analyzer  =====")

    while True:
        print("\nWhat do you want to check?")
        print("1. Threat Detection")
        print("2. Forest Fire Risk")
        print("3. Show History")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            detect_threat()
        elif choice == '2':
            detect_fire()
        elif choice == '3':
            show_history()
        elif choice == '4':
            print("Exiting... stay safe 👍")
            break
        else:
            print("Invalid input, try again.")


if __name__ == "__main__":
    main()
