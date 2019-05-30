from flask_restplus import Api

# flask_restplus API porvides living swagger document
api = Api(version='0.1',
          title='LEFT API',
          description='listen everything from tweets',
          doc='/doc')
