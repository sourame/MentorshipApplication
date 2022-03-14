def get_error_msg(data,stat_code):
    print(f'ERROR: {data}')
    response = {}
    response['statusCode'] = stat_code
    response['body'] =  data
    return response