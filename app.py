from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = 'BU5JLY8XNDIWVEK7'
# 

#example from the website docs
#use it to understand how I did it
@app.route('/docs', methods=['GET'])
def docs():
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=demo'
    r = requests.get(url)
    data = r.json()
    print(data)
    return data


@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		try:
			amount = request.form['amount']
			amount = float(amount)#inorder to display in decimals
			convert_from = request.form['convert_from']
			convert_to = request.form['convert_to']
			url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={convert_from}&to_currency={convert_to}&apikey={API_KEY}'
			response = requests.get(url).json()
			Exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
			Exchange_rate = float(Exchange_rate) #inorder to display in decimals
			result = Exchange_rate * amount
			convert_from_code = response['Realtime Currency Exchange Rate']['1. From_Currency Code']
			convert_from_name = response['Realtime Currency Exchange Rate']['2. From_Currency Name']
			convert_to_code = response['Realtime Currency Exchange Rate']['3. To_Currency Code']
			convert_to_name = response['Realtime Currency Exchange Rate']['4. To_Currency Name']
			updated_time = response['Realtime Currency Exchange Rate']['6. Last Refreshed']
			return render_template('home.html', result=round(result, 2), amount=amount,
								convert_from_code=convert_from_code, convert_from_name=convert_from_name,
								convert_to_code=convert_to_code, convert_to_name=convert_to_name, updated_time=updated_time)
		except Exception as e:
			return f'<h1> Bad Request : {e} </h1>'
            
        
	else:
		return render_template('home.html')


if __name__ == "__main__":
	app.run(debug=True)
