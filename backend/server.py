import numpy as np
from flask import Flask, request
import pickle

app = Flask(__name__)

thyroid_model = pickle.load(open('./model.sav', 'rb'))


@app.route('/thyroidpredict', methods=['POST'])
def thyroidpredict():
    try:
        print(request.json)
        data = request.json  # Access JSON data instead of form data

        Age = int(data.get('age', 0))  # Use get to handle missing keys
        Thyroid_Stimulating_Hormone_Level = float(data.get('TSH', 0))
        Pregnant = int(data.get('pregnant', 0))
        Triiodothyronine_T3 = float(data.get('T3', 0))
        Total_Thyroxine_TT4 = float(data.get('TT4', 0))
        On_thyroxine_Medication = int(data.get('on_thyroxine', 0))
        T4U_Measure = float(data.get('T4U', 0))
        FTI_Measured = int(data.get('FTI_measured', 0))
        Tumor = int(data.get('tumor', 0))
        Free_Thyroxine_Index_FTI = float(data.get('FTI', 0))

        # Create a dictionary for easier access
        values = {
            "age": Age,
            "TSH": Thyroid_Stimulating_Hormone_Level,
            "pregnant": Pregnant,
            "T3": Triiodothyronine_T3,
            "TT4": Total_Thyroxine_TT4,
            "on_thyroxine": On_thyroxine_Medication,
            "T4U": T4U_Measure,
            "FTI_measured": FTI_Measured,
            "tumor": Tumor,
            "FTI": Free_Thyroxine_Index_FTI
        }

        # Create a NumPy array for prediction
        arr = np.array([[Age, Thyroid_Stimulating_Hormone_Level, Pregnant, Triiodothyronine_T3, Total_Thyroxine_TT4,
                         On_thyroxine_Medication, T4U_Measure, FTI_Measured, Tumor, Free_Thyroxine_Index_FTI]])

        # Make the prediction using your model
        pred = thyroid_model.predict(arr)

        # Map the prediction to a result string
        if pred == 0:
            res_Val = "Compensated hypothyroid"
        elif pred == 1:
            res_Val = "No thyroid"
        elif pred == 2:
            res_Val = 'Primary hypothyroid'
        elif pred == 3:
            res_Val = 'Secondary hypothyroid'

        return res_Val  

    except ValueError as e:
        print('Error:', e) 
        return str(e), 400


if __name__ == '__main__':
    app.run(debug=True)
