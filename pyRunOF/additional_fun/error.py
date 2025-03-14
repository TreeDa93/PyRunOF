import sys
import traceback

def raise_error(*vargs, type_error=0):
    if type_error == 'var_1':
        error_message = f''' 
                        ------------------------------------------
                        You did not specify either in the object or 
                        in the method.
                        Above information can help you find where is it.
                        ------------------------------------------
                        '''
    elif type_error == 'var_2':
        error_message = f''' 
                        ------------------------------------------
                        You did not specify either in the object or 
                        in the method.
                        Above information can help you find where is it.
                        ------------------------------------------
                        '''
    elif type_error == 'path_error':
        error_message = f''' 
                        ------------------------------------------
                        You did not specify path_dict either in the object or 
                        in the method.
                        Above information can help you find where is it.
                        ------------------------------------------
                        '''
    elif type_error == 'name_error':
        error_message = f''' 
                        ------------------------------------------
                        You did not specify name either in the object or 
                        in the method.
                        Above information can help you find where is it.
                        ------------------------------------------
                        '''
    elif type_error == 'check_key_error':
        error_message = f''' 
                        ------------------------------------------
                        You write wrong key {vargs[0]}. Please check it.
                        Above information can help you find where is it.
                        ------------------------------------------
                        '''
    elif type_error == 'check_name_error':
        error_message = f''' 
                        ------------------------------------------
                        You write wrong name {vargs[0]}. Please check it.
                        Above information can help you find where is it.
                        ------------------------------------------
                        '''
    elif type_error == 'check_key_path':
        error_message = f''' 
                        ------------------------------------------
                        You have set neither the name nor the key to the name. 
                        Above information can help you find where is it.
                        ------------------------------------------
                        '''

    elif type_error == 'check_path_existence_error_1':
        error_message = f''' 
                            ------------------------------------------
                            Your name {vargs[0]} and is not exist! But directory 
                            {vargs[1]} is exist! You can create folder {vargs[2]} 
                            yourself or set flag make_new as True to make the Folder
                            by the script with name {vargs[2]}! 
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
    elif type_error == 'check_path_existence_error_2':
        error_message = f''' 
                        ------------------------------------------
                        The given name is not exist and directory {vargs[0]}
                        of the folder {vargs[1]} is not exist as well.  
                        Above information can help you find where is it.
                        ------------------------------------------
                        '''
    elif type_error == 'check_key_name_error':
        error_message = f''' 
                        ------------------------------------------
                        You have set neither the name nor the key to the name. 
                        Above information can help you find where is it.
                        ------------------------------------------
                        '''
    else:
        error_message = f''' 
                        ------------------------------------------
                        I do not know the error! The developer should it check!
                        ------------------------------------------
                        '''
    for message in traceback.format_stack():
        print(message)
    #print(repr(traceback.format_stack()))
    raise SystemExit(error_message)


def error_create_folder():
    error_message = f''' 
        ------------------------------------------
        The folder is already exist and your moder 
        of writing is available to make copy.
        Above information can help you find where is it.
        ------------------------------------------
        '''
    for message in traceback.format_stack():
        print(message)
    #print(repr(traceback.format_stack()))
    raise SystemExit(error_message)


def raise_error_run():
    sys.exit('You have to set numbers of cores for OpenFOAM')


def _raise_error_no_correct_mode_run(self):
    sys.exit('''you write not correct mode
                Please chose from following modes:
                common - general mode only for OpenFOAM;
                parallel is the mode to run your case in parallel calculations
                EOF is the mode to run your case with Elmer_old together''')


def raise_error(*vargs, type_error=0):
    match type_error:
        case 'var_1':
            error_message = f''' 
                            ------------------------------------------
                            You did not specify either in the object or 
                            in the method.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        case 'var_2':
            error_message = f''' 
                            ------------------------------------------
                            You did not specify either in the object or 
                            in the method.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        case 'path_error':
            error_message = f''' 
                            ------------------------------------------
                            You did not specify path_dict either in the object or 
                            in the method.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        case 'name_error':
            error_message = f''' 
                            ------------------------------------------
                            You did not specify name either in the object or 
                            in the method.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        case 'check_key_error':
            error_message = f''' 
                            ------------------------------------------
                            You write wrong key {vargs[0]}. Please check it.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        case 'check_name_error':
            error_message = f''' 
                            ------------------------------------------
                            You write wrong name {vargs[0]}. Please check it.
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        case 'check_key_path':
            error_message = f''' 
                            ------------------------------------------
                            You have set neither the name nor the key to the name. 
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''

        case 'check_path_existence_error_1':
            error_message = f''' 
                                ------------------------------------------
                                Your name {vargs[0]} and is not exist! But directory 
                                {vargs[1]} is exist! You can create folder {vargs[2]} 
                                yourself or set flag make_new as True to make the Folder
                                by the script with name {vargs[2]}! 
                                Above information can help you find where is it.
                                ------------------------------------------
                                '''
        case 'check_path_existence_error_2':
            error_message = f''' 
                            ------------------------------------------
                            The given name is not exist and directory {vargs[0]}
                            of the folder {vargs[1]} is not exist as well.  
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        case 'check_key_name_error':
            error_message = f''' 
                            ------------------------------------------
                            You have set neither the name nor the key to the name. 
                            Above information can help you find where is it.
                            ------------------------------------------
                            '''
        case _:
            error_message = f''' 
                            ------------------------------------------
                            I do not know the error! The developer should it check!
                            ------------------------------------------
                            '''
    for message in traceback.format_stack():
        print(message)
    #print(repr(traceback.format_stack()))
    raise SystemExit(error_message)

    
            

