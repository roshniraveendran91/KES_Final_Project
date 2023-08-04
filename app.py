from flask import Flask, render_template, request

app = Flask(__name__)

# List of rules for respiratory illness prediction
rules = [
    {
        "disease": "acuteBronchitis",
        "ageGroup": ["children", "elderly"],
        "gender": ["female", "male"],
        "familyHistory": "N",
        "smokingHistory": "N",
        "duration": ">1 week, <4 weeks",
        "chestPain": "Y",
        "cough": "productive",
        "coughingUpBlood": "N",
        "fever": ["N", "Y"],
        "rapidBreathing": "N",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "Y",
        "wheezing": "Y"
    },
    {
        "disease": "asthma",
        "ageGroup": "children",
        "gender": ["female", "male"],
        "familyHistory": "Y",
        "smokingHistory": "N",
        "duration": "years",
        "chestPain": "N",
        "cough": ["dry", "productive"],
        "coughingUpBlood": "N",
        "fever": "N",
        "rapidBreathing": "Y",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "Y",
        "wheezing": "Y"
    },
    {
        "disease": "bronchiectasis",
        "ageGroup": "elderly",
        "gender": "female",
        "familyHistory": "N",
        "smokingHistory": "N",
        "duration": ["months", "years"],
        "chestPain": "Y",
        "cough": "productive",
        "coughingUpBlood": "Y",
        "fever": "N",
        "rapidBreathing": "N",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "Y",
        "wheezing": "Y"
    },
    {
        "disease": "bronchiolitis",
        "ageGroup": "infants",
        "gender": "male",
        "familyHistory": "N",
        "smokingHistory": "Y",
        "duration": ">1 week, <4 weeks",
        "chestPain": "N",
        "cough": "dry",
        "coughingUpBlood": "N",
        "fever": ["N", "Y"],
        "rapidBreathing": "Y",
        "rapidHeartbeat": ["N", "Y"],
        "shortnessOfBreath": "Y",
        "wheezing": "Y"
    },
    {
        "disease": "copd",
        "ageGroup": "elderly",
        "gender": ["female", "male"],
        "familyHistory": "N",
        "smokingHistory": "Y",
        "duration": "months",
        "chestPain": "N",
        "cough": "productive",
        "coughingUpBlood": "N",
        "fever": "N",
        "rapidBreathing": "Y",
        "rapidHeartbeat": "Y",
        "shortnessOfBreath": "Y",
        "wheezing": "Y"
    },
    {
        "disease": "commonCold",
        "ageGroup": ["infants", "children", "youngAdults", "middleAged", "elderly"],
        "gender": ["female", "male"],
        "familyHistory": "N",
        "smokingHistory": "N",
        "duration": "<1 week",
        "chestPain": "N",
        "cough": "productive",
        "coughingUpBlood": "N",
        "fever": "N",
        "rapidBreathing": "N",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "N",
        "wheezing": "Y"
    },
    {
        "disease": "covid-19",
        "ageGroup": ["middleAged", "elderly"],
        "gender": "male",
        "familyHistory": "N",
        "smokingHistory": "N",
        "duration": ">1 week, <4 weeks",
        "chestPain": ["N", "Y"],
        "cough": "dry",
        "coughingUpBlood": "Y",
        "fever": "Y",
        "rapidBreathing": "Y",
        "rapidHeartbeat": "Y",
        "shortnessOfBreath": "Y",
        "wheezing": "N"
    },
    {
        "disease": "croup",
        "ageGroup": "infants",
        "gender": "male",
        "familyHistory": "Y",
        "smokingHistory": "N",
        "duration": "<1 week",
        "chestPain": "N",
        "cough": "productive",
        "coughingUpBlood": "N",
        "fever": "Y",
        "rapidBreathing": "Y",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "Y",
        "wheezing": "N"
    },
    {
        "disease": "cysticFibrosis",
        "ageGroup": "infants",
        "gender": ["female", "male"],
        "familyHistory": "Y",
        "smokingHistory": "N",
        "duration": ["<1 week", ">1 week, <4 weeks", "months", "years"],
        "chestPain": "N",
        "cough": "productive",
        "coughingUpBlood": "N",
        "fever": ["N", "Y"],
        "rapidBreathing": "Y",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "Y",
        "wheezing": "Y"
    },
    {
        "disease": "influenza",
        "ageGroup": ["infants", "elderly"],
        "gender": ["female", "male"],
        "familyHistory": "N",
        "smokingHistory": "N",
        "duration": ">1 week, <4 weeks",
        "chestPain": ["N", "Y"],
        "cough": "dry",
        "coughingUpBlood": "N",
        "fever": "Y",
        "rapidBreathing": ["N", "Y"],
        "rapidHeartbeat": ["N", "Y"],
        "shortnessOfBreath": "Y",
        "wheezing": "N"
    },
    {
        "disease": "lungCancer",
        "ageGroup": ["middleAged", "elderly"],
        "gender": "male",
        "familyHistory": "Y",
        "smokingHistory": "Y",
        "duration": "years",
        "chestPain": "Y",
        "cough": "productive",
        "coughingUpBlood": "Y",
        "fever": ["N", "Y"],
        "rapidBreathing": "Y",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "Y",
        "wheezing": "Y"
    },
    {
        "disease": "occupationalLungDiseases",
        "ageGroup": ["infants", "children", "youngAdults", "middleAged", "elderly"],
        "gender": "male",
        "familyHistory": "N",
        "smokingHistory": "Y",
        "duration": "years",
        "chestPain": "Y",
        "cough": "dry",
        "coughingUpBlood": "N",
        "fever": "N",
        "rapidBreathing": "Y",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "Y",
        "wheezing": "Y"
    },
    {
        "disease": "pertussis",
        "ageGroup": ["infants", "children", "youngAdults", "middleAged", "elderly"],
        "gender": ["female", "male"],
        "familyHistory": "N",
        "smokingHistory": "N",
        "duration": ">1 week, <4 weeks",
        "chestPain": "N",
        "cough": "dry",
        "coughingUpBlood": "N",
        "fever": "Y",
        "rapidBreathing": "N",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "Y",
        "wheezing": "N"
    },
    {
        "disease": "pneumonia",
        "ageGroup": ["children", "elderly"],
        "gender": ["female", "male"],
        "familyHistory": "N",
        "smokingHistory": "Y",
        "duration": ["<1 week", ">1 week, <4 weeks", "months", "years"],
        "chestPain": "Y",
        "cough": "productive",
        "coughingUpBlood": "N",
        "fever": "Y",
        "rapidBreathing": "Y",
        "rapidHeartbeat": "Y",
        "shortnessOfBreath": "Y",
        "wheezing": "Y"
    },
    {
        "disease": "rhinosinusitis",
        "ageGroup": ["youngAdults", "middleAged"],
        "gender": ["female", "male"],
        "familyHistory": "N",
        "smokingHistory": "Y",
        "duration": ">1 week, <4 weeks",
        "chestPain": "N",
        "cough": "productive",
        "coughingUpBlood": "N",
        "fever": "Y",
        "rapidBreathing": "N",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "Y",
        "wheezing": "N"
    },
    {
        "disease": "tuberculosis",
        "ageGroup": ["infants", "children", "youngAdults", "middleAged", "elderly"],
        "gender": ["female", "male"],
        "familyHistory": "N",
        "smokingHistory": "N",
        "duration": ">1 week, <4 weeks",
        "chestPain": "Y",
        "cough": "productive",
        "coughingUpBlood": "Y",
        "fever": "Y",
        "rapidBreathing": "N",
        "rapidHeartbeat": "N",
        "shortnessOfBreath": "Y",
        "wheezing": "N"
    }
]

def respiratory_illness_prediction(inputs):
    for rule in rules:
        # Check if all conditions of the rule are met
        if all(inputs[key] in rule[key] for key in inputs):
            return rule["disease"]
    return "Inconclusive, further tests required"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user inputs from the form
        inputs = {
            "ageGroup": request.form.get("age_group"),
            "gender": request.form.get("gender"),
            "familyHistory": request.form.get("family_history"),
            "smokingHistory": request.form.get("smoking_history"),
            "duration": request.form.get("duration"),
            "chestPain": request.form.get("chest_pain"),
            "cough": request.form.get("cough"),
            "coughingUpBlood": request.form.get("coughing_up_blood"),
            "fever": request.form.get("fever"),
            "rapidBreathing": request.form.get("rapid_breathing"),
            "rapidHeartbeat": request.form.get("rapid_heartbeat"),
            "shortnessOfBreath": request.form.get("shortness_of_breath"),
            "wheezing": request.form.get("wheezing")
        }

        # Get the respiratory illness prediction
        result = respiratory_illness_prediction(inputs)
        return render_template('result.html', result=result)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
