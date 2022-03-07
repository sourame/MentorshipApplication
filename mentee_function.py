

def get_mentee(mentee_id,connection):
    data = {}
    response = {} 
    try:
        sql = "SELECT * FROM Mentee WHERE id = %s"
        values = (mentee_id,)
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
        print("ERROR: No Mentee exists with the id!")
        data['errorMessage'] = 'No Mentee exists with the id!'           
        response['statusCode'] = 400
        response['body'] =  data
        return response 

    get_values = {'Mentee id': row[0], 'User id': row[1], 'Comunication Type':row[2], 
                  'Preffered Ethinicity': row[3], 'Preffered start Time': row[4],
                  'Preffered end Time': row[5]}
    data.update(get_values)
    response['statusCode'] = 200
    response['body'] =  data
    return response


def put_mentee(mentee_id,event,connection):
    data = {}
    response = {}
    # get the Mentee data from request body
    user_id = event['user_id']           
    communication_type = event['communication_type']
    pref_ethinicity = event['pref_ethinicity']
    pref_timestart = event['pref_timestart']
    pref_timeend = event['pref_timeend']
    try:
        sql = "UPDATE Mentee SET user_id = %s, communication_type = %s, pref_ethinicity = %s, pref_timestart = %s, pref_timeend = %s WHERE id = %s"
        values = (user_id,communication_type,pref_ethinicity,pref_timestart,pref_timeend,mentee_id)
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
        data['errorMessage'] = 'Mentee not updated!'           
        response['statusCode'] = 400
        response['body'] =  data
        return response

    data['message'] = 'Mentee updated successfully!'           
    response['statusCode'] = 200
    response['body'] =  data
    return response


def del_mentee(mentee_id,connection):
    data = {}
    response = {}
    try:
        sql = "DELETE FROM Mentee WHERE id = %s"
        values = (mentee_id,)
        cursor = connection.cursor()
        cursor.execute(sql,values)
        connection.commit()

    except:
        print("ERROR: DB Query Execution failed.") 
        data['errorMessage'] = 'Internal server error'           
        response['statusCode'] = 500
        response['body'] =  data
        return response

    data['message'] = 'Mentee deleted!!'
    response['statusCode'] = 200
    response['body'] =  data 
    return response


def mentee_register(event,connection):
    data = {}
    response = {} 
    # get the Mentor data from request body
    user_id = event['user_id']           
    communication_type = event['communication_type']
    pref_ethinicity = event['pref_ethinicity']
    pref_timestart = event['pref_timestart']
    pref_timeend = event['pref_timeend']

    try:     
        #print(name,ethinicity,communication_type,pref_ethinicity,pref_timeslot,max_mentees,location)        

        sql = ("INSERT INTO Mentee (`user_id`,`communication_type`,`pref_ethinicity`,`pref_timestart`,`pref_timeend`) \
                VALUES (%s,%s,%s,%s,%s)")
        values = (user_id,communication_type,pref_ethinicity,pref_timestart,pref_timeend)
        cursor = connection.cursor()
        cursor.execute(sql,values) 
        connection.commit()

    except:
        print("ERROR: DB Query Execution failed.") 
        data['errorMessage'] = 'Internal server error'           
        response['statusCode'] = 500
        response['body'] =  data
        return response
        
    data['message'] = 'Mentee successfully registered!!'
    response['statusCode'] = 200
    response['body'] =  data
    return response


def get_mentee_list(connection):
    data = {}
    response = {} 
    try:
        sql = "SELECT * FROM Mentee"
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
        print("ERROR: No Mentees Registered!")
        data['errorMessage'] = 'No Mentees Registered!'           
        response['statusCode'] = 400
        response['body'] =  data
        return response 
    
    resp_data = []
    for row in rows:
        resp_data.append({'id': row[0], 'User id':row[1], 'Communication Type':row[2], 'Preffered Ethinicity':row[3], 'Preffered Start Time':row[4], 'Preffered End Time':row[5]})            
    data['Values'] = resp_data
    response['statusCode'] = 200
    response['body'] =  data
    return response