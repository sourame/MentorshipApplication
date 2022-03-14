
import pymysql
from config import endpoint,username,password,database_name
from api_event import event
from menter_function import get_mentor,put_mentor,del_mentor,get_mentor_list, mentor_register,get_active_mentees_list,get_new_mentees_list,accept_mentee_req
from mentee_function import get_mentee,get_mentee_list,mentee_register,put_mentee,del_mentee,get_mentor_matches,send_req_to_mentor
from ment_error_handling import get_error_msg

#Connection
connection = pymysql.connect(host=endpoint,user=username,password=password,database=database_name)


def lambda_handler(event,context):

    path = event['path']
    http_method = event['httpMethod']
    
    response = {}

    split_path = path.split('/')

    print(split_path)

    if split_path[-1] == 'mentors':
        if http_method == 'GET':
            response = get_mentor_list(connection)
        elif http_method == 'POST':
            response = mentor_register(event['body'],connection)
        else:            
            response = get_error_msg('Error in Http Method',400)        
    
    elif split_path[-1] == 'mentees':
        if http_method == 'GET':
            response = get_mentee_list(connection)            
        elif http_method == 'POST':
            response = mentee_register(event['body'],connection)
        else:            
            response = get_error_msg('Error in Http Method',400)

    elif split_path[-2] == 'mentors' :
        print(f"path = {path}, method = {http_method}")        
        user_id = split_path[-1]        
        if http_method == 'GET':
            response = get_mentor(user_id,connection)        
        elif http_method == 'PUT':
            response = put_mentor(user_id,event['body'],connection)        
        elif http_method == 'DELETE':  
            response = del_mentor(user_id,connection)        
        else:            
            response = get_error_msg('Error in Http Method',400) 

    elif split_path[-2] == 'mentees' :
        print(path,http_method)
        user_id = split_path[-1]
        if http_method == 'GET':
            response = get_mentee(user_id,connection)        
        elif http_method == 'PUT':
            response = put_mentee(user_id,event['body'],connection)        
        elif http_method == 'DELETE':  
            response = del_mentee(user_id,connection)        
        else:            
            response = get_error_msg('Error in Http Method',400)
    
    elif split_path[-3] == 'mentees' and split_path[-1] == 'search':
        mentee_id = split_path[-2] 
        if http_method == 'GET':       
            response = get_mentor_matches(mentee_id,connection)
        else:            
            response = get_error_msg('Error in Http Method',400)

    elif split_path[-3] == 'mentees' and split_path[-1] == 'sendRequest':                
        if http_method == 'POST':       
            response = send_req_to_mentor(event['body'],connection)
        else:            
            response = get_error_msg('Error in Http Method',400)
    
    elif split_path[-3] == 'mentors' and split_path[-1] == 'active':
        mentor_id = split_path[-2]        
        if http_method == 'GET':       
            response = get_active_mentees_list(mentor_id,connection)
        else:            
            response = get_error_msg('Error in Http Method',400)

    elif split_path[-3] == 'mentors' and split_path[-1] == 'new':
        mentor_id = split_path[-2]        
        if http_method == 'GET':       
            response = get_new_mentees_list(mentor_id,connection)
        else:            
            response = get_error_msg('Error in Http Method',400)

    elif split_path[-3] == 'mentors' and split_path[-1] == 'accept':                
        if http_method == 'PUT':       
            response = accept_mentee_req(event['body'],connection)
        else:            
            response = get_error_msg('Error in Http Method',400)

    else:    
        response = get_error_msg('Error in path',400)
    
    return response

""" def call_proc():
    cursor = connection.cursor()    
    cursor.callproc('get_mentor_match',[1,])
    result = cursor.fetchall()
    print(result) """
     # print out the result
"""     for result in cursor.stored_results():
        print(result.fetchall()) """

context = 2
resp = lambda_handler(event,context)
print (resp)

""" func1 = call_proc() """
