from ment_error_handling import get_error_msg

def get_mentee(user_id,connection):
    data = {}
    response = {} 
    try:
        sql = "SELECT id,user_id,communication_type,pref_ethinicity,pref_timestart,pref_timeend FROM Mentee WHERE user_id = %s"
        values = (user_id,)
        cursor = connection.cursor()
        row_cnt = cursor.execute(sql,values)
        row = cursor.fetchone()

    except:         
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
        return response

    if row_cnt <= 0 :        
        data['errorMessage'] = 'No Mentee exists with the id!'           
        response = get_error_msg(data,400)
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
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
        return response 

    if row_cnt <= 0 :        
        data['errorMessage'] = 'Mentee not updated!'           
        response = get_error_msg(data,400)
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
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
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

    sql = ("INSERT INTO Mentee (`user_id`,`communication_type`,`pref_ethinicity`,`pref_timestart`,`pref_timeend`) \
                VALUES (%s,%s,%s,%s,%s)")
    values = (user_id,communication_type,pref_ethinicity,pref_timestart,pref_timeend)
    cursor = connection.cursor()
    cursor.execute(sql,values)

    skills = event['skills']
    print(skills)
    for skill in skills:
        user_id = event['user_id']        
        skill_id = skill 
        interest = 'A'        
    
        sql = ("INSERT INTO SkillSet (`user_id`,`skill_id`,`interest`) \
                    VALUES (%s,%s,%s,%s)")
        values = (user_id,skill_id,interest)
        cursor = connection.cursor()
        cursor.execute(sql,values) 

    try:          
        connection.commit()

    except:         
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
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
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
        return response

    if row_cnt <= 0 :
        data['errorMessage'] = 'No Mentees Registered!'           
        response = get_error_msg(data,400)
        return response 
    
    resp_data = []
    for row in rows:
        resp_data.append({'id': row[0], 'User id':row[1], 'Communication Type':row[2], 'Preffered Ethinicity':row[3], 'Preffered Start Time':row[4], 'Preffered End Time':row[5]})            
    data['Mentees'] = resp_data
    response['statusCode'] = 200
    response['body'] =  data
    return response

def get_mentor_matches(mentee_id,connection):
    data = {}
    response = {}
    # Call the Stored Procedure to get the matching mentors list
    try:
        cursor = connection.cursor() 
        args = [mentee_id,]        
        cursor.callproc('get_mentor_match',args)
        rows = cursor.fetchall()
    except: 
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
        return response

    resp_data = []
    st_time = []
    end_time = []
    i=0
    for row in rows:
        st_time.append(str(row[7].total_seconds()/3600) + ':00')
        end_time.append(str(row[8].total_seconds()/3600) + ':00')               
        resp_data.append({'User id':row[0], 'Name':row[1] + ' ' + row[2], 'Email':row[3],
        'Ethinicity':row[4], 'Communication Mode': row[5], 
        'Preffered Ethinicity':row[6], 'Preffered Start Time':st_time[i], 
        'Preffered End Time':end_time[i],'Street':row[9],'City':row[10],'State':row[11]}) 
        i+=1
                  
    data['Mentors'] = resp_data
    response['statusCode'] = 200
    response['body'] =  data
    return response

def send_req_to_mentor(event,connection):
    data = {}
    response = {} 
    # get the Mentor data from request body
    skills = event['skills']
    print(skills)
    for skill in skills:
        mentor_id = event['mentor_id']  
        mentee_id = event['mentee_id']
        skill_id = skill 
        m_status = 'N'        
    
        sql = ("INSERT INTO Mentorship (`mentor_id`,`mentee_id`,`skill_id`,`m_status`) \
                    VALUES (%s,%s,%s,%s)")
        values = (mentor_id,mentee_id,skill_id,m_status)
        cursor = connection.cursor()
        cursor.execute(sql,values) 

    try:
        connection.commit()
    except: 
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
        return response

    data['message'] = 'New request sent to Mentor!!'
    response['statusCode'] = 200
    response['body'] =  data
    return response
