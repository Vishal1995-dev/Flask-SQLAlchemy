from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Employee


engine = create_engine('sqlite:///employees.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) 

# Create the appropriate app.route functions, 
#test and see if they work


#Make an app.route() decorator here
@app.route("/")
@app.route("/employees", methods = ['GET', 'POST'])
def employeesFunction():
  if request.method == 'GET':
    #Call the method to Get all of the employees
    return getAllemployees()
  elif request.method == 'POST':
    #Call the method to make a new employee
    print ("Making a New employee")
    
    name = request.args.get('name', '')
    description = request.args.get('description', '')
    print (name)
    print (description)
    return (makeANewemployee(name, description))
 
  
 
#Make another app.route() decorator here that takes in an integer id in the URI
@app.route("/employees/<int:id>", methods = ['GET', 'PUT', 'DELETE'])
#Call the method to view a specific employee
def employeesFunctionId(id):
  if request.method == 'GET':
    return getemployee(id)
    
#Call the method to edit a specific employee  
  elif request.method == 'PUT':
    name = request.args.get('name', '')
    description = request.args.get('description', '')
    return updateemployee(id,name, description)
    
 #Call the method to remove a employee 
  elif request.method == 'DELETE':
    return deleteemployee(id)

def getAllemployees():
  employees = session.query(Employee).all()
  return jsonify(employees=[i.serialize for i in employees])

def getemployee(id):
  employee = session.query(Employee).filter_by(id = id).one()
  return jsonify(employee=employee.serialize) 
  
def makeANewemployee(name,description):
  employee = Employee(name = name, description = description)
  session.add(employee)
  session.commit()
  return jsonify(employee=employee.serialize)

def updateemployee(id,name, description):
  employee = session.query(Employee).filter_by(id = id).one()
  
  employee.name = name
  employee.description = description
  session.add(employee)
  session.commit()
  return "Updated a employee with id %s" % id

def deleteemployee(id):
  employee = session.query(Employee).filter_by(id = id).one()
  session.delete(employee)
  session.commit()
  return "Removed employee with id %s" % id


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)	
