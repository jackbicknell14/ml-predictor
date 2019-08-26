from flask import request, jsonify
from app import flask_app
from app.models.persistent_models import *

# Create a model
@flask_app.route('/model', methods=['POST'])
def add_model():
	name = request.json['name']
	params = request.json['params']
	if 'upload_time' in request.json:
		upload_time = request.json['upload_time']
	else:
		upload_time = None
	in_use = request.json['in_use']
	pickle_model = request.json['pickle_model']

	new_model = PersistentModel(name, params, pickle_model, upload_time, in_use)

	db.session.add(new_model)
	db.session.commit()

	return model_schema.jsonify(new_model)


# Get all models
@flask_app.route('/model', methods=['GET'])
def get_models():
	print('hello there')

	all_models = PersistentModel.query.all()
	result = models_schema.dump(all_models)
	print(result)
	return jsonify(result)


# Get single model
@flask_app.route('/model/<id>', methods=['GET'])
def get_model(id):
	model = PersistentModel.query.get(id)
	return model_schema.jsonify(model)



# Update a model
@flask_app.route('/model/<id>', methods=['PUT'])
def update_model(id):
	model = PersistentModel.query.get(id)
	name = request.json['name']
	params = request.json['params']
	pickle_model = request.json['pickle_model']
	in_use = request.json['in_use']

	model.name = name
	model.params = params
	model.pickle_model = pickle_model
	model.in_use = in_use

	db.session.commit()

	return model_schema.jsonify(model)

# Delete a model
@flask_app.route('/model/<id>', methods=['DELETE'])
def delete_model(id):
	model = PersistentModel.query.get(id)
	db.session.delete(model)
	db.session.commit()

	return model_schema.jsonify(model)
