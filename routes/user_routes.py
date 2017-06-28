from routes.core import *
from sanic.response import redirect
from model.objects.user import User
from viewmodel.user_view_model import my_dashboard_data

def add_routes(app):
	# create account page
	@app.route("/user/create_account")
	async def create_account(request):
		return jinja_response('user/create_account.html')

	# login to account page
	@app.route("/user/login", methods=['GET'])
	async def login(request):
		return jinja_response('user/login.html')

	# login post api method
	@app.route("/user/login", methods=['POST'])
	async def login(request):
		form = request.form

		try:
			user = User.authenticate(form.get('login'), form.get('password'))
			request['session']['user_name'] = user.user_name
			request['session']['user_id'] = user.user_id
			print(user.user_name)
			print(request['session']['user_name'])
			return redirect('/decks')
		except Exception as e:
			return html(jinja_render('user/login.html', error_msg=e.message), status=401)

		return redirect('/decks')

	# logout
	@app.route("/user/logout", methods=['GET'])
	async def logout(request):
		if 'user_name' in request['session']:
			del request['session']['user_name'] 
		if 'user_id' in request['session']:
			del request['session']['user_id']
		return redirect('/user/login')

	# user homepage
	@app.route("/user/me", methods=['GET'])
	async def logout(request):
		user = User.from_db_id(request['session'].get('user_id'))
		# print(my_dash_board_data(user))

		return jinja_response('user/me.html')

	# create user post request
	@app.route("/user", methods=['POST'])
	def post(request):
		form = request.form
		user_name, email, password = [form.get(p) for p in ('user_name', 'email', 'password')]
		try:
			User.create(user_name, email, password)
			return redirect('/user/login')
		except Exception as e:
			return jinja_response('user/create_account.html', error_msg=e.message)

