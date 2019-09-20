from flask import Flask, render_template, url_for, request, redirect, flash
import dash
import dash_core_components as dcc
import dash_html_components as html

server = Flask(__name__)

server.secret_key = "habibi"

from sqlalchemy.orm import sessionmaker, relationship

# # this part is needed to create session to query database.  this should be JUST BELOW app.config..
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select
meta = MetaData()
engine = create_engine("postgresql://postgres:161086@localhost/test-db-02", echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# database here
# class DashGraphs(Base):
#     __tablename__ = 'dash_graphs'
#     id = Column('id', Integer, primary_key=True)
#     name = Column('name', String(20))
#     f_visit = Column('first_visit', String(3))
#     comeback = Column('visit_again', String(3))

#     def __init__(self, name, f_visit, comeback):
#         self.name = name
#         self.f_visit = f_visit
#         self.comeback = comeback

Session = sessionmaker(bind=engine)
db_session = Session()

title = "Dash Graphs"

@server.route('/')
def home():
	return render_template('home.html', title=title)

if __name__ == '__main__':
    app.run_server(debug=True)