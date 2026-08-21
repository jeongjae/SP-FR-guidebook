import csv

def fix_csv(filename, replacements):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    for old, new in replacements.items():
        content = content.replace(old, new)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Fixed {filename}")

reps = {
    "marche-liberation": "marche-de-la-liberation",
    "restaurant-salon-de-the-beatrice": "restaurant-beatrice"
}

fix_csv("FCR_66_MEAL_SLOT_MATRIX.csv", reps)
fix_csv("FCR06_WISH_VENUE_CLOSURE.csv", reps)
