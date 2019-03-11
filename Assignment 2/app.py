## Import the Packages##
## render_template is used to render html files
## request is to handle GET and POST request from HTML Forms
## os library will allow to access the file paths in our system
from flask import Flask, render_template, request, session, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker
from sql import *
from sql1 import *

import os
import datetime
engine = create_engine('sqlite:///tutorial.db', echo = True)

##Intialize the Flask Application
app = Flask(__name__)

## Routes to the home function
@app.route("/", methods = ["GET","POST"])
def home():
    return render_template('login.html')


## Checks username and password if yes then renders to home page else returns back to login page
@app.route("/login", methods = ["GET","POST"])
def login():
    if request.form['username'] == 'admin' and request.form['password'] == 'admin' :
        return render_template('home.html')
    else:
        return render_template('login.html')

@app.route('/createVm', methods = ['GET','POST'])
def create():
    return render_template('createVm.html')


## Choose the plan
@app.route('/chooseplan', methods = ['GET','POST'])
def plan():
    if request.form:
        PLAN = str(request.form['plan'])
        Session = sessionmaker(bind = engine)
        s = Session()
        
        ## Value is inserted in database
        virtual_machine = CreateVirtualMachine(plan = PLAN)
        
        s.add(virtual_machine)
        s.commit()
        flash(" You have choosen " + virtual_machine.plan )
        
    return render_template('home.html')

## List Virtual Machine Instances
@app.route('/listVm', methods = ['GET','POST'])
def list():
    Session = sessionmaker(bind = engine)
    s = Session()
    virtual_machines = s.query(CreateVirtualMachine).all()
    return render_template('listVm.html', virtual_machines = virtual_machines)


## Delete the Virtual Machine
@app.route('/deleteVm/<int:id>', methods = ['GET','POST'])
def deleteVm(id):
    Session = sessionmaker(bind = engine)
    s = Session()
    virtual_machines = s.query(CreateVirtualMachine).filter_by(id = id ).first()
    s.delete(virtual_machines)
    s.commit()
    flash("Virtual Machine Deleted")
    return redirect('/listVm')



## Upgrade the Plan of Virtual Machine
@app.route('/upgradeVm/<int:id>', methods = ['GET','POST'])
def upgradeVm(id):
    startnow = datetime.datetime.now()
    usage = 0
    charges = 0
    Session = sessionmaker(bind = engine)
    s = Session()
    virtual_machines = s.query(CreateVirtualMachine).filter_by(id = id ).first()
    current_plan = virtual_machines.plan
    virtual_machines_usage = s.query(VirtualMachineUsage).filter_by(instanceid = id).first()
    if current_plan == 'planA':
        current_plan = 'planB'
        
    elif current_plan == 'planB':
        current_plan = 'planC'
        
    elif current_plan == 'planC':
        flash('Your plan is already upgraded')
        return redirect('/listVm')
        
    virtual_machines.plan = current_plan
    if virtual_machines_usage:
        if virtual_machines_usage.plan != virtual_machines.plan:
            virtual_machines_usage = VirtualMachineUsage(instanceid = id, plan = current_plan, starttime = startnow, stoptime = startnow, usage = usage, charges = charges)
            s.add(virtual_machines_usage)
    

    s.commit()
    flash('Your plan is upgraded to ' + virtual_machines.plan )
    return redirect('/listVm')

##Downgrade the plan in Virtual Machine
@app.route('/downgradeVm/<int:id>', methods = ['GET','POST'])
def downgradeVm(id):
    
    startnow = datetime.datetime.now()
    usage = 0
    charges = 0
    Session = sessionmaker(bind = engine)
    s = Session()
    virtual_machines = s.query(CreateVirtualMachine).filter_by(id = id ).first()
    current_plan = virtual_machines.plan

    virtual_machines_usage = s.query(VirtualMachineUsage).filter_by(instanceid = id).first()
    

    if current_plan == 'planC':
        current_plan = 'planB'
        
    elif current_plan == 'planB':
        current_plan = 'planA'
        
    elif current_plan == 'planA':
        flash('You are using Basic plan')
        return redirect('/listVm')
        
    virtual_machines.plan = current_plan
    if virtual_machines_usage.plan == current_plan:
        virtual_machines_usage = s.query(VirtualMachineUsage).filter_by(plan = current_plan).first()
        virtual_machines_usage.stoptime = startnow
    s.commit()
    flash('Your plan is demoted to ' + virtual_machines.plan )
    return redirect('/listVm')


## Start time
@app.route('/startVm/<int:id>', methods = ['GET','POST'])
def starttime(id):
    
    startnow = datetime.datetime.now()
    usage = 0
    charges = 0
    Session = sessionmaker(bind = engine)
    s = Session()
    virtual_machines = s.query(CreateVirtualMachine).filter_by(id = id ).first()
    plan = virtual_machines.plan
    virtual_machines_usage = s.query(VirtualMachineUsage).filter_by(instanceid = id).first()   
    if virtual_machines_usage:
        if(virtual_machines_usage.plan == plan):
            virtual_machines_usage.stoptime = startnow
            s.commit()
    else:
        virtual_machines_usage = VirtualMachineUsage(instanceid = id, plan = plan, starttime = startnow, stoptime = startnow, usage = usage, charges = charges)
        s.add(virtual_machines_usage)
        s.commit()
    flash("Virtual Machine started at : " + str(startnow.hour) + ":" + str(startnow.minute))    
    
    return redirect('/listVm')

## Stop Time
@app.route('/startVm/stopVm/<int:id>', methods = ['GET','POST'])
def stoptime(id):
    stopnow = datetime.datetime.now()
    Session = sessionmaker(bind = engine)
    s = Session()
    
    virtual_machines = s.query(CreateVirtualMachine).filter_by(id = id ).first()
    
    plan = virtual_machines.plan
    virtual_machines_usage = s.query(VirtualMachineUsage).filter_by(instanceid = id, plan=plan).first()
    
    if virtual_machines_usage:
        if virtual_machines_usage.plan == plan:
            virtual_machines_usage.stoptime = stopnow
            hours = virtual_machines_usage.stoptime.hour - virtual_machines_usage.starttime.hour
            minutes = virtual_machines_usage.stoptime.minute -virtual_machines_usage.starttime.minute
            hr_to_min = hours * 60
            virtual_machines_usage.usage = minutes + hr_to_min
            if virtual_machines_usage.plan == 'planA':
                virtual_machines_usage.charges = 0.05 * virtual_machines_usage.usage
            elif virtual_machines_usage.plan == 'planB':
                virtual_machines_usage.charges = 0.10 * virtual_machines_usage.usage
            elif virtual_machines_usage.plan == 'planC':
                virtual_machines_usage.charges = 0.15 * virtual_machines_usage.usage
        else:
            flash(virtual_machines_usage.plan, "is not a plan")
    s.commit()

    flash("Details of Cloud Usage")

    flash(" Instance ID " + str(virtual_machines_usage.instanceid))
    flash(" Plan choosen is " + virtual_machines_usage.plan)
    flash(" Start Time is  " + str(virtual_machines_usage.starttime.hour) + " : " + str(virtual_machines_usage.starttime.minute) + " : " + str(virtual_machines_usage.starttime.second))
    flash(" Stop Time is  " + str(virtual_machines_usage.stoptime.hour) + ":" + str(virtual_machines_usage.stoptime.minute) + " : " + str(virtual_machines_usage.stoptime.second))
    flash(" Usage is " + str(virtual_machines_usage.usage) + " minutes")
    flash(" Charge is "+ str(virtual_machines_usage.charges) + " CAD")
    return redirect('/listusageVm/' + str(id))

#list Usage of Virtual Machines
@app.route('/listusageVm/<int:id>', methods = ['GET','POST'])
def list_usage(id):
    Session = sessionmaker(bind = engine)
    s = Session()
    virtual_machines_usage = s.query(VirtualMachineUsage).all()
    virtual_machines_usage = s.query(VirtualMachineUsage).filter(VirtualMachineUsage.instanceid.in_(str(id)))
    return render_template('listUsageVm.html', virtual_machines_usage = virtual_machines_usage)

##Delete Usage
@app.route('/listusageVm/deleteUsage/<int:id>', methods = ['GET','POST'])
def deleteUsageVm(id):
    Session = sessionmaker(bind = engine)
    s = Session()
    virtual_machines_usage = s.query(VirtualMachineUsage).filter_by(id = id ).first()
    s.delete(virtual_machines_usage)
    s.commit()
    return redirect('/listVm')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host = os.getenv('IP', '0.0.0.0'), port = int(os.getenv('PORT', 8080)),debug = True)
