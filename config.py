from app import app

app.config['SQLALCHEMY_DATABASE_URL']='sqlite://'
app.config["SECRET_KEY"]= "omegasecret"