from flask import request, jsonify
from app import flask_app
from app.models.predictions import *

# Create a prediction
@flask_app.route('/prediction', methods=['POST'])
def add_prediction():

	model_id = request.json['model_id']
	customer_id = request.json['customer_id']
	if 'prediction_time' in request.json:
		prediction_time = request.json['prediction_time']
	else:
		prediction_time = None
	prediction = request.json['prediction']

	new_prediction = Prediction(model_id, customer_id, prediction, prediction_time)

	db.session.add(new_prediction)
	db.session.commit()

	return prediction_schema.jsonify(new_prediction)


# Get all predictions
@flask_app.route('/prediction', methods=['GET'])
def get_predictions():
	print('hello there')

	all_predictions = Prediction.query.all()
	result = predictions_schema.dump(all_predictions)
	print(result)
	return jsonify(result)


# Get single prediction
@flask_app.route('/prediction/<id>', methods=['GET'])
def get_prediction(id):
	prediction = Prediction.query.get(id)
	return prediction_schema.jsonify(prediction)



# Update a prediction
@flask_app.route('/prediction/<id>', methods=['PUT'])
def update_prediction(id):
	prediction = Prediction.query.get(id)
	model_id = request.json['model_id']
	customer_id = request.json['customer_id']
	prediction_data = request.json['prediction']

	prediction.model_id = model_id
	prediction.customer_id = customer_id
	prediction.prediction = prediction_data

	db.session.commit()

	return prediction_schema.jsonify(prediction)

# Delete a prediction
@flask_app.route('/prediction/<id>', methods=['DELETE'])
def delete_prediction(id):
	prediction = Prediction.query.get(id)
	db.session.delete(prediction)
	db.session.commit()

	return prediction_schema.jsonify(prediction)
