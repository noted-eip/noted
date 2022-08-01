import inspect

def object_must_be_valid(func):
    def wrapper_object_must_be_valid(obj, *args, **kwargs):
        is_valid_attr = getattr(obj, "is_valid", None)
        if not callable(is_valid_attr): 
            print("The method's object on which this decorator has been put does not have a 'is_valid' function")    
        elif obj.is_valid() == True:
            return func(obj, *args, **kwargs)
        else:
            missing_elements = ', '.join(class_var_symbols.keys() - obj.__dict__.keys())
            print(f"The object of type {obj.__class__.__name__} does not have those values filled in: {missing_elements}")
        return None
    return wrapper_object_must_be_valid
