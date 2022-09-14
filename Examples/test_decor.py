
def decor_fun(fun):





def a_decorator_passing_arguments(function_to_decorate):
    def a_wrapper_accepting_arguments(arg1, arg2):
        print("Смотри, что я получил:", arg1, arg2)
        function_to_decorate(arg1, arg2)
    return a_wrapper_accepting_arguments

@a_decorator_passing_arguments
def print_full_name(first_name, last_name):
    print("Меня зовут", first_name, last_name)

print_full_name("Vasya", "Pupkin")

def pass_list_dict(fun):
    def wrapper(*listsfvSchemes):
        fun(listsfvSchemes)
    return wrapper

@pass_list_dict()
def fun(listsfvSchemes):
    for list_var in listsfvSchemes:
        for


