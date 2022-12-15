from drip import app
from drip.models import db
from drip.routes import *  # Import all routes from the routes module

"""checks if the file is being run directly or imported"""

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    #app.run(debug=True, host='0.0.0.0', port=5000)
    
db.create_all()
