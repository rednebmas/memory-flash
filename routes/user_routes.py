from routes.core import *
from sanic.response import redirect
from model.objects.user import User

def add_routes(app):
	# create account page
	@app.route("/user/create_account")
	async def create_account(request):
		return jinja_response('user/create_account.html')

	# login to account page
	@app.route("/user/login", methods=['GET'])
	async def login(request):
		return jinja_response('user/login.html')

	@app.route("/user/login", methods=['POST'])
	async def login(request):
		form = request.form

		try:
			user = User.authenticate(form.get('login'), form.get('password'))
			request['session']['user_name'] = user.user_name
			return redirect('/decks')
		except Exception as e:
			return html(jinja_render('user/login.html', error_msg=e.message), status=401)

		return redirect('/decks')

	# create user post request
	@app.route("/user", methods=['POST'])
	def post(request):
		form = request.form
		user_name, email, password = [form.get(p) for p in ('user_name', 'email', 'password')]
		try:
			User.create(user_name, email, password)
			request['session']['user_name'] = form.get('user_name')
			return redirect('/decks')
		except Exception as e:
			return jinja_response('user/create_account.html', error_msg=e.message)

