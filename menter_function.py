
def get_mentor(mentor_id,connection):
    data = {}
    response = {}  
    try:
        sql = "SELECT * FROM Mentor WHERE id = %s"
        values = (mentor_id,)
        cursor = connection.cursor()
        row_cnt = cursor.execute(sql,values)
        row = cursor.fetchone()

    except:
        print("ERROR: DB Query Execution failed.") 
        data['errorMessage'] = 'Internal server error'           
        response['statusCode'] = 500
        response['body'] =  data
        return response

    if row_cnt <= 0 :
        print("ERROR: No Mentor exists with the id!")
        data['errorMessage'] = 'No Mentor exists with the id!'           
        response['statusCode'] = 400
        response['body'] =  data
        return response 

    get_values = {'Mentor id': row[0], 'User id': row[1], 'Comunication Type': row[2],
                    'Preffered Ethinicity': row[3], 'Preffered start Time': row[4], 
                    'Preffered end Time': row[5], 'Max Mentees': row[6], 'Active Mentees': row[7]}
    data.update(get_values)
    response['statusCode'] = 200
    response['body'] =  data
    return response    


def put_mentor(mentor_id,event,connection):
    data = {}
    response = {} 
    # get the Mentor data from request body 
    user_id = event['user_id']           
    communication_type = event['communication_type']
    pref_ethinicity = event['pref_ethinicity']
    pref_timestart = event['pref_timestart']
    pref_timeend = event['pref_timeend']
    max_mentees = event['max_mentees']
    active_mentees = event['active_mentees']
    try:
        sql = "UPDATE Mentor SET user_id = %s, communication_type = %s, pref_ethinicity = %s, pref_timestart = %s, pref_timeend = %s, max_mentees = %s, active_mentees = %s WHERE id = %s"
        values = (user_id,communication_type,pref_ethinicity,pref_timestart,pref_timeend,max_mentees,active_mentees,mentor_id)
        cursor = connection.cursor()
        row_cnt = cursor.execute(sql,values)
        connection.commit()        

    except:
        print("ERROR: DB Query Execution failed.") 
        data['errorMessage'] = 'Internal server error'           
        response['statusCode'] = 500
        response['body'] =  data
        return response

    if row_cnt <= 0 :        
        data['errorMessage'] = 'Mentor not updated!'           
        response['statusCode'] = 400
        response['body'] =  data
        return response

    data['message'] = 'Mentor updated successfully!'           
    response['statusCode'] = 200
    response['body'] =  data
    return response
  

def del_mentor(mentor_id,connection):
    data = {}
    response = {}   
    try:
        sql = "DELETE FROM Mentor WHERE id = %s"
        values = (mentor_id,)
        cursor = connection.cursor()
        cursor.execute(sql,values)
        connection.commit()

    except:
        print("ERROR: DB Query Execution failed.") 
        data['errorMessage'] = 'Internal server error'           
        response['statusCode'] = 500
        response['body'] =  data
        return response

    data['message'] = 'Mentor deleted!!'
    response['statusCode'] = 200
    response['body'] =  data
    return response


def mentor_register(event,connection):
    data = {}
    response = {}
    # get the Mentor data from request body
    user_id = event['user_id']           
    communication_type = event['communication_type']
    pref_ethinicity = event['pref_ethinicity']
    pref_timestart = event['pref_timestart']
    pref_timeend = event['pref_timeend']
    max_mentees = event['max_mentees']
    active_mentees = event['active_mentees']

    try:     
        #print(name,ethinicity,communication_type,pref_ethinicity,pref_timeslot,max_mentees,location)        

        sql = ("INSERT INTO Mentor (`user_id`,`communication_type`,`pref_ethinicity`,`pref_timestart`,`pref_timeend`,`max_mentees`,`active_mentees`) \
                VALUES (%s,%s,%s,%s,%s,%s,%s)")
        values = (user_id,communication_type,pref_ethinicity,pref_timestart,pref_timeend,max_mentees,active_mentees)
        cursor = connection.cursor()
        cursor.execute(sql,values) 
        connection.commit()
    except:
        print("ERROR: DB Query Execution failed.") 
        data['errorMessage'] = 'Internal server error'           
        response['statusCode'] = 500
        response['body'] =  data
        return response
        
    data['message'] = 'Mentor successfully registered!!'
    response['statusCode'] = 200
    response['body'] =  data
    return response


def get_mentor_list(connection):
    data = {}
    response = {}
    try:
        sql = "SELECT * FROM Mentor"
        cursor = connection.cursor()
        row_cnt = cursor.execute(sql)
        rows = cursor.fetchall()
    except:
        print("ERROR: DB Query Execution failed.") 
        data['errorMessage'] = 'Internal server error'           
        response['statusCode'] = 500
        response['body'] =  data
        return response

    if row_cnt <= 0 :
        print("ERROR: No Mentors Registered!")
        data['errorMessage'] = 'No Mentors Registered!'           
        response['statusCode'] = 400
        response['body'] =  data
        return response 
        
    resp_data = []
    for row in rows:
        resp_data.append({'id': row[0], 'User id':row[1], 'Communication Type':row[2], 'Preffered Ethinicity':row[3], 'Preffered Time Start':row[4], 'Preffered Time End':row[5], 'Max Mentees Allowed':row[6], 'Active Mentees':row[7]})            
    data['Values'] = resp_data
    response['statusCode'] = 200
    response['body'] =  data
    return response
