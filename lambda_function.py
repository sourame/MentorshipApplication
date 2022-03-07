
import pymysql
from config import endpoint,username,password,database_name
#from api_event import event
from menter_function import get_mentor,put_mentor,del_mentor,get_mentor_list, mentor_register
from mentee_function import get_mentee,get_mentee_list,mentee_register,put_mentee,del_mentee

#Connection
connection = pymysql.connect(host=endpoint,user=username,password=password,database=database_name)

def lambda_handler(event,context):

    path = event['path']
    http_method = event['httpMethod']
    
    response = {}

    split_path = path.split('/')

    if (split_path[-1] == 'mentors' or split_path[-1] == 'mentees') :

        if (split_path[-1] == 'mentors' and http_method == 'GET') :
            response = get_mentor_list(connection)

        elif (split_path[-1] == 'mentors' and http_method == 'POST') :
            response = mentor_register(event['body'],connection)

        elif (split_path[-1] == 'mentees' and http_method == 'GET'):
            response = get_mentee_list(connection)

        elif (split_path[-1] == 'mentees' and http_method == 'POST'):
            response = mentee_register(event['body'],connection)

    elif split_path[-2] == 'mentors' :
        print(f"path = {path}, method = {http_method}")        
        mentor_id = split_path[-1]
        
        if http_method == 'GET':
            response = get_mentor(mentor_id,connection)
        
        elif http_method == 'PUT':
            response = put_mentor(mentor_id,event['body'],connection)
        
        elif http_method == 'DELETE':  
            response = del_mentor(mentor_id,connection)
        
        else: 
            print("Error in Http Method") 

    elif split_path[-2] == 'mentees' :
        print(path,http_method)
        mentee_id = split_path[-1]

        if http_method == 'GET':
            response = get_mentee(mentee_id,connection)
        
        elif http_method == 'PUT':
            response = put_mentee(mentee_id,event['body'],connection)
        
        elif http_method == 'DELETE':  
            response = del_mentee(mentee_id,connection)
        
        else: 
            print("Error in Http Method")
    else:
        print('Error in path')
    
    return response



