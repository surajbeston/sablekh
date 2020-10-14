import psycopg2

def migrate_data(records):
    formatted_tags, formatted_downloadlot, formatted_file, formatted_implicitdata, formatted_library, formatted_like, formatted_pwresettoken, formatted_visitor, formatted_user, formatted_token = [], [], [], [], [], [], [], [], [], []
    for record in records["tags"]:
        formatted_tags.append({"id": record[0], "tag": record[1], "datetime": record[2]})
    
    for record in records["downloadlot"]:
        formatted_downloadlot.append({"id": record[0],"zipname": record[1],"datetime": record[2], "files": record[3], "downloads": record[4], "library_id": record[5], "visitor_id": record[6]})
    
    for record in records["file"]:
        formatted_file.append({"hid": record[0], "title":record[1], "_file": record[2], "size": record[3], "library":record[4]})

    for record in records["library"]:
        formatted_library.append({"hid": record[0],"title": record[1],"description": record[2], "thumbnail":record[3], "link_str": record[4],"tags": record[5],"finished": record[6], "searchable": record[7],"datetime": record[8],"no_files": record[9],"user_id":record[10], "_order": 1})

    for record in records["like"]:
        formatted_like.append({"id": record[0],"datetime": record[1],"library_id": record[2],"user_id": record[3]})

    for record in records["visitor"]:
        formatted_visitor.append({"id": record[0],"hid": record[1], "email_verified": False})

    for record in records["user"]:
        formatted_user.append({"id": record[0],"password": record[1],"last_login": record[2], "is_superuser": record[3],"username":record[4],"first_name": record[5], "last_name": record[6],"email":record[7],"is_staff": record[8],"is_active": record[9],"date_joined": record[10]})
    
    for record in records["token"]:
        formatted_token.append({"key": record[0],"created": record[1],"user_id": record[2]})
    try:
        connection = psycopg2.connect(user="postgres",
                                    password="rugby",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="sablekh")    

        cursor = connection.cursor()
        print ( connection.get_dsn_parameters(),"\n")
        cursor.executemany("""INSERT INTO api_tag VALUES (%(id)s, %(tag)s, %(datetime)s)""", formatted_tags)
        cursor.executemany(""" INSERT INTO api_downloadlot VALUES (%(id)s, %(zipname)s, %(datetime)s, %(files)s, %(downloads)s, %(library_id)s, %(visitor_id)s) """, formatted_downloadlot)
        cursor.executemany(""" INSERT INTO api_file VALUES (%(hid)s, %(title)s, %(_file)s, %(size)s, %(library)s)""", formatted_file)
        cursor.executemany(""" INSERT INTO api_library VALUES (%(hid)s, %(title)s,%(description)s, %(thumbnail)s, %(link_str)s, %(tags)s, %(finished)s,%(searchable)s, %(datetime)s,%(no_files)s,%(user_id)s, %(_order)s)""", formatted_library)
        cursor.executemany(""" INSERT INTO api_like VALUES (%(id)s, %(datetime)s, %(library_id)s,%(user_id)s)""", formatted_like)
        cursor.executemany(""" INSERT INTO api_visitor VALUES (%(id)s,%(hid)s,%(email_verified)s)""", formatted_visitor)
        cursor.executemany(""" INSERT INTO auth_user VALUES (%(id)s, %(password)s, %(last_login)s, %(is_superuser)s, %(username)s, %(first_name)s, %(last_name)s, %(email)s, %(is_staff)s, %(is_active)s, %(date_joined)s)""", formatted_user)
        cursor.executemany(""" INSERT INTO authtoken_token VALUES (%(key)s, %(created)s,%(user_id)s)""", formatted_token)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.commit()
            connection.close()
            print("Data pushed")

try:
    connection = psycopg2.connect(user="postgres",
                                  password="rugby",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="sablekhbackup")
    cursor = connection.cursor()
    table_arr = [("api_tag","tags"),("api_downloadlot","downloadlot"),("api_file","file"),("api_library","library"), ("api_like","like"),("api_visitor","visitor"),("auth_user","user"),("authtoken_token", "token")]
    records = {}
    for table in table_arr:
        query = "SELECT * from "+table[0]
        cursor.execute(query)
        records[table[1]] = cursor.fetchall()



finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("Data collected now, pushing data now..")
        
        migrate_data(records)
        # except:
        #     print ("Unknown error abrupted the transfer.")

