from django.shortcuts import render
import requests

FASTAPI_URL = "https://carpricefastapi.onrender.com/predict"  # replace with your actual Render URL


def predict_view(request):
    continuous_inputs = [
        "milage",
        "HP",
        "L",
        "Cylinders",
        "transmission_speeds",
        "Age",
        "brand_encoded",
        "model_encoded",
        "ext_col_encoded",
        "int_col_encoded",
    ]

    binary_inputs = [
        "clean_title_yes",
        "accident_not_reported",
        "CVT",
        "Manual",
        "other",
        "Electric",
        "Flex",
        "Gasoline",
        "Hybrid",
        "Plug_In_Hybrid",
        "dash",
    ]
    continuous_ranges = {
        "milage": "100 - 400000",
        "HP": "70 - 1000",
        "L": "1 - 8",
        "Cylinders": "3 - 12",
        "transmission_speeds": "1 - 10",
        "Age": "1 - 50",
        "brand_encoded": "30000 - 50000",
        "model_encoded": "30000 - 50000",
        "ext_col_encoded": "30000 - 50000",
        "int_col_encoded": "30000 - 50000",
    }

    # Create a list of tuples: (feature_name, range)
    continuous_ranges_list = [(f, continuous_ranges[f]) for f in continuous_inputs]

    prediction = None

    if request.method == "POST":
        # Collect data from the form
        data = {}
        for feature in continuous_inputs:
            value = request.POST.get(feature)
            if value:
                data[feature] = float(value)
        for feature in binary_inputs:
            data[feature] = 1 if request.POST.get(feature) else 0

        # Call FastAPI
        try:
            response = requests.post(FASTAPI_URL, json=data)
            prediction = response.json().get("prediction")

            # ✅ Clean & format prediction
            if isinstance(prediction, list) and len(prediction) > 0:
                prediction = float(prediction[0])
            elif isinstance(prediction, (int, float)):
                prediction = float(prediction)
            else:
                prediction = None

        except Exception as e:
            prediction = f"Error: {e}"

    return render(
        request,
        "dashboard/form.html",
        {
            "continuous_inputs": continuous_inputs,
            "binary_inputs": binary_inputs,
            "prediction": prediction,
            "continuous_ranges_list": continuous_ranges_list,
        },
    )
