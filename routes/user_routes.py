from routes.core import *
from sanic.response import redirect
from model.objects.user import User

def add_routes(app):
	# create account page
	@app.route("/user/create_account")
	async def create_account(request):
		return html(template('user/create_account.html').render())

	# create user post request
	@app.route("/user", methods=['POST'])
	def post(request):
		print(request.body)

		user_name, email, password = [request.form.get(p) for p in ('user_name', 'email', 'password')]
		try:
			User.create(user_name, email, password)
			return redirect('/decks')
		except Exception as e:
			return html(template('user/create_account.html').render(error_msg=e.message))

