import ldap, sys
from core.config import conf_auth_ldap
from core.validation import validate_json_list, sanitize_objectify_json, update_password_salt_user_json
from core.db import db


def check_credentials(username, password, migrate=True):
    """User authentication based on LDAP"""
    
    bind_search_string = conf_auth_ldap['bind_search_string'].format(username=username)
    ldap_connection = ldap.open(conf_auth_ldap['hostname'])
    ldap_connection.protocol_version = ldap.VERSION3
    ldap_connection.simple_bind_s(bind_search_string, password)

    search_scope = ldap.SCOPE_SUBTREE
    attributes = None 
    search_filter = conf_auth_ldap['search_filter'].format(username=username)

    ldap_results = ldap_connection.search_s(bind_search_string, search_scope, search_filter, attributes)
    
    # If ldap give a result, and user is not already in db, migrate the user into database
    if ldap_results and ldap_results[0] and ldap_results[0][0] == bind_search_string:
        ldap_result_dict = ldap_results[0][1]
        if migrate and not _user_exists_in_db(username):
            id = _migrate_user_to_db(ldap_result_dict, password)
            if not id:
                print 'Some error occurred migrating user from LDAP to database, please check.'
        
        return None
    else:
        return u"Incorrect username or password."
    
def _user_exists_in_db(username):
    """Check if username already exists in db"""
    cursor = db['user'].find({"username": username}).limit(1)
    return cursor.count() > 0

def _migrate_user_to_db(ldap_result_dict, password):
    """Migrate LDAP user informations to database"""
    
    user_dict = {
                 'name' : ldap_result_dict.get('givenName', [''])[0], 
                 'surname' : ldap_result_dict.get('sn', [''])[0],
                 'username' : ldap_result_dict.get('uid', [''])[0],
                 'email' : ldap_result_dict.get('mail',[''])[0],
                 'phone' : ldap_result_dict.get('phone',[''])[0],
                 'mobile' : ldap_result_dict.get('mobile',[''])[0],
                 'city' : ldap_result_dict.get('city',[''])[0],
                 'group' : "employee",
                 'password' : password,
                 'salt' : ''
                 }
    
    validate_json_list('user', [ user_dict ])
    
    sanified_documents_list = sanitize_objectify_json(user_dict)
    update_password_salt_user_json(user_dict)
    
    return db['user'].insert(sanified_documents_list)
    


        
