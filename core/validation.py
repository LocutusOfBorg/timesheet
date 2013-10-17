import cgi, yaml, random, string, hashlib, types
from core.config import schema, core_folder
from validictory import ValidationError, validate

# Dirty hack to avoid the bug 
# http://stackoverflow.com/questions/10401499/mongokit-importerror-no-module-named-objectid-error
# Old pymongo versions uses pymongo.objectid.ObjectId while new uses bson.ObjectId
try:
    from pymongo.objectid import ObjectId
except ImportError as e:
    from bson import ObjectId

def recursive_merge(container, container_override):
    """merges container_override into container and return merged result"""
    key = None
    try:
        if not isinstance(container, (types.DictType, types.ListType)):
            # border case for first run or if container is container primitive
            container = container_override
        elif isinstance(container, types.ListType):
            # lists can be only appended
            if isinstance(container_override, types.ListType):
                # merge lists
                container.extend(container_override)
            else:
                # append to list
                container.append(container_override)
        elif isinstance(container, types.DictType):
            # dicts must be merged
            if isinstance(container_override, types.DictType):
                for key in container_override:
                    if key in container:
                        container[key] = recursive_merge(container[key], container_override[key])
                    else:
                        container[key] = container_override[key]
            else:
                raise ValueError('Cannot merge non-dict "%s" into dict "%s"' % (container_override, container))
        else:
            raise ValueError('Not implemented "%s" into "%s"' % (container_override, container))
    except TypeError, e:
        raise ValueError('TypeError "%s" in key "%s" when merging "%s" into "%s"' % (e, key, container_override, container))
    return container

def recursive_replace(container, replace_function):
    t = container.__class__
    
    replaced = replace_function(container)
    
    if replaced != None:
        return replaced
    elif isinstance(container, types.DictType):
        return t((x,recursive_replace(container[x], replace_function)) for x in container)
    elif isinstance(container, types.ListType):
        # Add other non-replicable iterables here. 
        t = tuple if isinstance(t, (types.GeneratorType,)) else t
        return t(recursive_replace(x, replace_function) for x in container)
    elif isinstance(container, (int, long, float, complex)):
        return container
    else:
        raise ValueError("I don't know how to handle container type: %s" % type(container))


def _replace_function_sanitize_objectify_json(container):
    """Callback for sanitize_objectify_json"""
    
    if isinstance(container, types.DictType):
        
        # Objectify '_id' and dot-notation 'object._id' strings. Assume there is only one per dictionary.
        id_key = next((k for k in container.keys() if isinstance(container[k],basestring) and (k == '_id' or k.endswith('._id'))), None)
        if id_key:
            container[id_key] = ObjectId(container[id_key])
        
        t = container.__class__
        return t((x,recursive_replace(container[x], _replace_function_sanitize_objectify_json)) for x in container)
    elif isinstance(container, ObjectId):
        # Leave already converted ObjectId as-is
        return container
    elif isinstance(container, basestring):
        # Quote strings
        return cgi.escape(container, quote=True)

def sanitize_objectify_json(json_in):
    """Sanitize string and convert _ids to ObjectId in JSON"""
    return recursive_replace(json_in, _replace_function_sanitize_objectify_json)

def _replace_function_stringify_objectid_json(container):
    """Callback for stringify_objectid_cursor"""
    
    if isinstance(container, types.DictType) and '_id' in container and isinstance(container['_id'],ObjectId):
        # Objectify id string and continue with recursive replace
        container['_id'] = str(container['_id'])
        t = container.__class__
        return t((x,recursive_replace(container[x], _replace_function_stringify_objectid_json)) for x in container)
    elif isinstance(container, basestring):
        return container

def stringify_objectid_cursor(cursor_in):
    """Convert ObjectId to string in JSON"""
    
    stringified = []
    for json_in in cursor_in:
        stringified.append(recursive_replace(json_in, _replace_function_stringify_objectid_json))
    return stringified

def _replace_function_stringify_objectid_list(container):
    """Callback for stringify_objectid_list"""
    if isinstance(container, ObjectId):
        return str(container)

def stringify_objectid_list(list_in):
    """Convert an ObjectId list to string list"""
    return recursive_replace(list_in, _replace_function_stringify_objectid_list)

def validate_json_list(collection, list_in):
    
    for json_in in list_in:    
        # Validate json schema
        validate(json_in, schema[collection])
   
def update_password_salt_user_list(collection, list_in):
    
    if collection == 'user':
        for json_in in list_in:    
            if 'password' in json_in and json_in['password']:
                update_password_salt_user_json(json_in)
            else:
                raise ValidationError('Expected nonempty password')
        
    return list_in
        
def update_password_salt_user_json(json_in):
    json_in.update(get_password_salt(json_in['password']))

def get_password_salt(password_in):
    """Method to hash password_in and salt, if inserted"""
    
    salt = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(16))
    password_out = hashlib.sha256( salt + password_in ).hexdigest()
    
    return { 'password': password_out, 'salt' : salt }
    
    
    
    