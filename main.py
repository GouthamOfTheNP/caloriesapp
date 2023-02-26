from wtforms.validators import DataRequired
from flask.views import MethodView
from flask import Flask, render_template, request
from wtforms import Form, StringField, SubmitField
from backend.calorie import Calorie
from backend.temperature import Temperature

app = Flask(__name__)


class MainPage(MethodView):
	def get(self):
		return render_template('index.html')


class CalculatePage(MethodView):
	def get(self):
		calc_form = CalculateForm()
		return render_template('calculate.html', calc_form=calc_form)

	def post(self):
		calc_form = CalculateForm(request.form)
		if calc_form.validate():
			weight = float(calc_form.weight.data)
			height = float(calc_form.height.data)
			age = float(calc_form.age.data)
			city = calc_form.city.data
			country = calc_form.country.data
			try:
				temperature = Temperature(city, country).get()
				result = Calorie(weight, height, age, temperature).calculate_calories()
				calories = f"You need {result} calories (kcal) today!"
				return render_template('calculate.html', calc_form=calc_form, calories=calories)
			except Exception:
				calories = f"You need to enter a valid city and country!"
				return render_template('calculate.html', calc_form=calc_form, calories=calories)


class CalculateForm(Form):
	weight = StringField('Weight:', validators=[DataRequired()])
	height = StringField('Height:', validators=[DataRequired()])
	age = StringField('Age:', validators=[DataRequired()])
	city = StringField('City:', validators=[DataRequired()])
	country = StringField('Country:', validators=[DataRequired()])
	submit = SubmitField('Calculate')


if __name__ == '__main__':
	app.add_url_rule('/', view_func=MainPage.as_view('index'))
	app.add_url_rule('/calories-form/', view_func=CalculatePage.as_view('calculate'))
	app.run(debug=True)
