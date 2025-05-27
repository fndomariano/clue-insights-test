from src import create_app, debug
	
if __name__ == "__main__":
	app = create_app()
	app.run(debug=debug, host='0.0.0.0')