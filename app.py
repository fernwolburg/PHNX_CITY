from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify 
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Create a path to the database
engine = create_engine("sqlite:////Users/fernandawolburg/Downloads/PHXproject.db")

#reflect database and tables
Base = automap_base()
Base.prepare(engine, reflect = True)

#Setup flask
app = Flask(__name__)

# Save table reference
data = Base.classes.PHXdata

def item_amount():
    """This function will showcase how much was spent on each item listed"""

    # Create a dataframe for the dates, the commitment item, and the invoice item
    commitment_results = session.query(data.CheckPaymentDate, data.CommitmtItemName, data.InvoiceNetAmt).all()

    # loop throuh the results in the query and assign them to a variable each
    Date = [commitment_results[0] for result in commitment_results[0:]]
    Item = [commitment_results[1] for result in commitment_results[0:]]
    Amount = [commitment_results[2] for result in commitment_results[0:]]

    return Date, Item, Amount

def spending_date():
     """This function will showcase how much was spent on each day
        total, without listing the items"""

    # obtain the total amount spent on on a given day
    qry = session.query(func.sum(data.InvoiceNetAmt).label("total_amount"))
    qry = qry.group_by(data.CheckPaymentDate)
    
    # pass the values to a list
    total_amount = [list(i) for i in qry]

    # remove the square brackets from the list above
    total_amount = [x[0] for x in total_amount]
    
    # find the unique values for the dates and add them to a list
    qry2 = session.query(data.CheckPaymentDate).distinct()
    unique_dates = [list(i) for i in qry2]

    return total_amount, unique_dates

def department_spending():
    """This function will show how much was spent by on each department description"""
    # find how much was spent by each department and arrange it from highest to lowest spending
    qry3 = session.query(data.DeptDescrptn).group_by(data.DeptDescrptn).order_by(func.sum(data.InvoiceNetAmt).desc())
    qry4 = session.query(func.sum(data.InvoiceNetAmt)).group_by(data.DeptDescrptn).order_by(func.sum(data.InvoiceNetAmt).desc())

    # add both to a list for flask app
    dept_spending = [list(i) for i in qry3]
    dept_amount = [list(i) for i in qry4]

    # remove the square brackets
    dept_spending = [x[0] for x in dept_spending]
    dept_amount = [x[0] for x in dept_amount]

    return dept_spending, dept_amount

if __name__ == '__main__':
    app.run(debug=True)


