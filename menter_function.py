
from ment_error_handling import get_error_msg


def get_mentor(user_id,connection):
    data = {}
    response = {}  
    try:
        sql = "SELECT id,user_id,communication_type,pref_ethinicity,pref_timestart,pref_timeend,max_mentees,active_mentees FROM Mentor WHERE id = %s"
        values = (user_id,)
        cursor = connection.cursor()
        row_cnt = cursor.execute(sql,values)
        row = cursor.fetchone()

    except:
        data['errorMessage'] = 'Internal server error'
        response = get_error_msg(data,500)
        return response
        
    if row_cnt <= 0 :        
        data['errorMessage'] = 'No Mentor exists with the id!'           
        response = get_error_msg(data,400)
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
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
        return response

    if row_cnt <= 0 :        
        data['errorMessage'] = 'Mentor not updated!'           
        response = get_error_msg(data,400)
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
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
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

    sql = ("INSERT INTO Mentor (`user_id`,`communication_type`,`pref_ethinicity`,`pref_timestart`,`pref_timeend`,`max_mentees`,`active_mentees`) \
                VALUES (%s,%s,%s,%s,%s,%s,%s)")
    values = (user_id,communication_type,pref_ethinicity,pref_timestart,pref_timeend,max_mentees,active_mentees)
    cursor = connection.cursor()
    cursor.execute(sql,values)

    skills = event['skills']
    print(skills)
    for skill in skills:
        user_id = event['user_id']        
        skill_id = skill 
        interest = 'E'        
    
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
        
    data['message'] = 'Mentor successfully registered!!'
    response['statusCode'] = 200
    response['body'] =  data
    return response


def get_mentor_list(connection):
    data = {}
    response = {}
    try:
        sql = "SELECT id,user_id,communication_type,pref_ethinicity,pref_timestart,pref_timeend,max_mentees,active_mentees FROM Mentor"
        cursor = connection.cursor()
        row_cnt = cursor.execute(sql)
        rows = cursor.fetchall()
    except:         
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
        return response

    if row_cnt <= 0 :        
        data['errorMessage'] = 'No Mentors Registered!'           
        response = get_error_msg(data,400)
        return response 
        
    resp_data = []
    for row in rows:
        resp_data.append({'id': row[0], 'User id':row[1], 'Communication Type':row[2], 'Preffered Ethinicity':row[3], 'Preffered Time Start':row[4], 'Preffered Time End':row[5], 'Max Mentees Allowed':row[6], 'Active Mentees':row[7]})            
    data['Mentors'] = resp_data
    response['statusCode'] = 200
    response['body'] =  data
    return response


def get_active_mentees_list(mentor_id,connection):
    data = {}
    response = {}  
    try:
        sql = "SELECT m.mentee_id,u.first_name,u.last_name,m.skill_id,m.start_time \
                FROM Mentorship m \
                INNER JOIN User u ON m.mentor_id = u.id \
                WHERE m.mentor_id = %s and m.m_status = %s"
        values = (mentor_id,'A') # A for Active Mentees
        cursor = connection.cursor()
        row_cnt = cursor.execute(sql,values)
        rows = cursor.fetchall()

    except:         
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
        return response

    if row_cnt <= 0 :        
        data['errorMessage'] = 'No active mentees currently!'           
        response = get_error_msg(data,400)
        return response     
        
    resp_data = []
    for row in rows:        
        resp_data.append({'Mentee id': row[0], 'Name':row[1] + ' ' + row[2], 'Skill':row[3], 'Start time':row[4]})            
    data['Active Mentees'] = resp_data
    response['statusCode'] = 200
    response['body'] =  data
    return response 

def get_new_mentees_list(mentor_id,connection):
    data = {}
    response = {}  
    try:
        sql = "SELECT m.mentee_id,u.first_name,u.last_name,m.skill_id \
                FROM Mentorship m \
                INNER JOIN User u ON m.mentor_id = u.id \
                WHERE m.mentor_id = %s and m.m_status = %s"
        values = (mentor_id,'N') # N for New Mentee Requests
        cursor = connection.cursor()
        row_cnt = cursor.execute(sql,values)
        rows = cursor.fetchall()

    except:         
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
        return response

    if row_cnt <= 0 :        
        data['errorMessage'] = 'No new mentee requests currently!'           
        response = get_error_msg(data,400)
        return response     
        
    resp_data = []
    for row in rows:        
        resp_data.append({'Mentee id': row[0], 'Name':row[1] + ' ' + row[2], 'Skill':row[3]})            
    data['New Mentee Requests'] = resp_data
    response['statusCode'] = 200
    response['body'] =  data
    return response 


def accept_mentee_req(event,connection):
    data = {}
    response = {}
    mentor_id = event['mentor_id']           
    mentee_id = event['mentee_id']
    
    try:
        sql = "UPDATE Mentorship SET  m_status = %s WHERE mentor_id = %s and mentee_id = %s and m_status = %s"
        values = ('A',mentor_id,mentee_id,'N')
        cursor = connection.cursor()
        row_cnt = cursor.execute(sql,values)
        connection.commit()
    
    except:         
        data['errorMessage'] = 'Internal server error'           
        response = get_error_msg(data,500)
        return response

    if row_cnt <= 0 :        
        data['errorMessage'] = 'Mentee request not accepted!'           
        response = get_error_msg(data,400)
        return response

    data['message'] = 'Mentee request accepted!'           
    response['statusCode'] = 200
    response['body'] =  data
    return response



"""         print("ERROR: DB Query Execution failed.") 
        data['errorMessage'] = 'Internal server error'           
        response['statusCode'] = 500
        response['body'] =  data
        return response """