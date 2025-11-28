from flask import Flask, render_template, request
import requests
app = Flask(__name__)
API_KEY = "1d4d70872e293cb83d98a5fb"
BASE_URL = f"https://v6.exchangerate-api.com/v6/1d4d70872e293cb83d98a5fb/latest/"
def get_currency_data(base_currency="INR"):
    try:
        url = BASE_URL + base_currency
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        currency_codes = sorted(list(data.get('conversion_rates', {}).keys()))
        return data, currency_codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None, ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"] 

@app.route("/", methods=["GET", "POST"])
def home():
    data, currencies = get_currency_data()
    result = None
    exchange_rate = None

    if request.method == "POST":
        try:
            amount = float(request.form.get("amount"))
            from_currency = request.form.get("from_currency")
            to_currency = request.form.get("to_currency")
            convert_url = BASE_URL + from_currency
            convert_response = requests.get(convert_url)
            convert_data = convert_response.json()
            rates = convert_data.get('conversion_rates')
            rate = rates.get(to_currency)
            if rate is not None and amount > 0:
                converted_amount = amount * rate
                result = f"{converted_amount:,.2f}"
                exchange_rate = rate # Pass the numerical rate
            else:
                result = "Error: Invalid currency or rate selected."
                
        except Exception as e:
            result = f"Error: Failed to connect to exchange rate service. ({e})"

    return render_template(
        "home.html", 
        currencies=currencies, 
        result=result, 
        exchange_rate=exchange_rate
    )

if __name__ == "__main__":
    app.run(debug=True)