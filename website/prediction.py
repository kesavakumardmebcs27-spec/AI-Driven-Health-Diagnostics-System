from flask import Blueprint, render_template, request, session
from .app_functions import ValuePredictor

prediction = Blueprint('prediction', __name__)

@prediction.route('/')
def index():
    return render_template('index.html')

@prediction.route('/predict', methods=['POST'])
def predict(): 
    try:
        disease_inputs = {
            'heart': ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                      'restecg', 'thalach', 'exang', 'oldpeak', 'slope',
                      'ca', 'thal'],
            'liver': ['age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin',
                      'Alkaline_Phosphotase', 'Alamine_Aminotransferase',
                      'Aspartate_Aminotransferase', 'Total_Protiens',
                      'Albumin', 'Albumin_and_Globulin_Ratio'],
            'kidney': ['age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'bgr', 'bu', 'sc',
                       'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc', 'htn', 'dm', 'cad', 'appet', 'pe', 'ane'],
            'stroke': ['Gender','age','hypertension','heart_disease',
                       'ever_married','work_type','Residence_type',
                       'avg_glucose_level','bmi','smoking_status'],
            'diabetes': ['pregnancies','Glucose','blood_pressure','BSkinThickness',
                         'Insulin','BMI','DiabetesPedigreeFunction','Age']
        }

        matched_disease = None
        for disease, fields in disease_inputs.items():
            if all(field in request.form for field in fields):
                matched_disease = disease
                expected_order = fields
                break

        if not matched_disease:
            raise ValueError("Input list length does not match any supported disease model.")

        input_data = {key: request.form[key] for key in expected_order}
        to_predict_list = [float(input_data[key]) for key in expected_order]

        prediction_value, page = ValuePredictor(to_predict_list)
        session['last_prediction_data'] = input_data

        css_class = "alert-danger" if prediction_value == 1 else "alert-success"
        message = "⚠️ High risk detected" if prediction_value == 1 else "✅ No significant risk detected"

        return render_template(f"{page}_report.html",
                               input_data=input_data,
                               prediction_text=message,
                               prediction_class=css_class,
                               prediction_value=prediction_value)

    except ValueError as ve:
        return f"Invalid input: {ve}", 400
    except FileNotFoundError as fe:
        return f"Model file not found: {fe}", 500
    except Exception as e:
        return f"An unexpected error occurred: {e}", 500
