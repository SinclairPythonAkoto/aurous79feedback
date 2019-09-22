from db_table import *
# import the database table in order to query with the functions below

Session = sessionmaker(bind=engine)
db_session = Session()

# creating ALL x axis for graphs
def x_men():
	''' finds all entries == 'men' '''
	''' X axis for graph '''
	men = db_session.query(AurousFeedback).filter(AurousFeedback.sex=='male')
	val = len([v.sex for v in men])
	return val

def x_women():
	''' finds all entries == 'female' '''
	''' X axis for graph '''
	women = db_session.query(AurousFeedback).filter(AurousFeedback.sex=='female')
	val = len([v.sex for v in women])
	return val

def x_visitors():
	''' finds all firstVisit entries == 'yes' '''
	visitors = db_session.query(AurousFeedback).filter(AurousFeedback.f_visit=='yes')
	val = len([v.f_visit for v in visitors])
	return val

def x_comeback():
	''' finds all return_v entries == 'yes' '''
	return_v = db_session.query(AurousFeedback).filter(AurousFeedback.comeback=='yes')
	val = len([v.comeback for v in return_v])
	return val

def x_shisha():
	''' finds all shisha entries == 'yes' '''
	shi = db_session.query(AurousFeedback).filter(AurousFeedback.shisha=='yes')
	val = len([v.shisha for v in shi])
	return val

def x_clean():
	''' finds all cleanliness entries '''
	''' numbers each item in list, then select the last entry '''
	tidy = db_session.query(AurousFeedback.clean).all()
	val = list(range(len([v.clean for v in tidy])))
	return val[-1]

def x_service():
	''' find all customer service entries '''
	''' numbers each item in list, then select the last entry '''
	serve = db_session.query(AurousFeedback.service).all()
	val = list(range(len([v.service for v in serve])))
	return val[-1]

def x_speed():
	''' find all speed entries '''
	''' number each item in list, then select th elast entry '''
	fast = db_session.query(AurousFeedback.speed).all()
	val = list(range(len([v.speed for v in fast])))
	return val[-1]
	
# creating ALL y axis for graphs
def y_men():
	''' sum all entries == 'men' '''
	''' the list counts from 0, 1, 2 etc '''
	men = db_session.query(AurousFeedback).filter(AurousFeedback.sex=='male')
	val = int(len([v.sex for v in men]))
	return val

def y_women():
	''' sum all entries == 'female' '''
	''' the list counts from 0, 1, 2 etc '''
	women = db_session.query(AurousFeedback).filter(AurousFeedback.sex=='female')
	val = int(len([v.sex for v in women]))
	return val

def y_visitors():
	''' sum all firstVisit entries == 'yes' '''
	''' the list counts from 0, 1, 2 etc '''
	visitors = db_session.query(AurousFeedback).filter(AurousFeedback.f_visit=='yes')
	val = int(len([v.f_visit for v in visitors]))
	return val

def y_comeback():
	''' sum all return_v entries == 'yes' '''
	''' the list counts from 0, 1, 2 etc '''
	return_v = db_session.query(AurousFeedback).filter(AurousFeedback.comeback=='yes')
	val = int(len([v.comeback for v in return_v]))
	return val

def y_shisha():
	''' sum all shisha entries == 'yes' '''
	''' the list counts from 0, 1, 2 etc '''
	shi = db_session.query(AurousFeedback).filter(AurousFeedback.shisha=='yes')
	val = int(len([v.shisha for v in shi]))
	return val

def y_clean():
	''' finds all cleanliness entries '''
	''' this finds the average '''
	''' add all entries then divide by number of enteries '''
	tidy = db_session.query(AurousFeedback.clean).all()
	total = sum([v.clean for v in tidy])
	group = len([v.clean for v in tidy])
	return int(total / group)

def y_service():
	''' finds all customer service entries '''
	''' this finds the average '''
	''' add all entries then divide by number of enteries '''
	serve = db_session.query(AurousFeedback.service).all()
	total = sum([v.service for v in serve])
	group = len([v.service for v in serve])
	return int(total / group)

def y_speed():
	''' finds all speed entries '''
	''' this finds the average '''
	''' add all entries then divide by number of enteries '''
	fast = db_session.query(AurousFeedback.speed).all()
	total = sum([v.speed for v in fast])
	group = len([v.speed for v in fast])
	return int(total / group)