from app import app


@app.cli.command('check')
def check():
    print("fine")
