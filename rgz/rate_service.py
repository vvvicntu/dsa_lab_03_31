from flask import Flask, request, jsonify

app = Flask(__name__)

rates = {
    'USD': 70.00,
    'EUR': 102.30
}

@app.route('/rate')
def get_rate():

    currency = request.args.get('currency')

    try:
        # Проверяем, есть ли валюта в нашем словаре
        if currency not in rates:

            return jsonify({
                "message": "UNKNOWN CURRENCY"
            }), 400

        return jsonify({
            "rate": rates[currency]
        })
    
    except:

        return jsonify({
            "message": "UNEXPECTED ERROR"
        }), 500


if __name__ == '__main__':
    app.run(port=5001)