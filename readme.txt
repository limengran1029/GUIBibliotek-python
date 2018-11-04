 *How to use it:
1 Run lib_database.py to create a new database "library" which include three table:
2 Run try_server(connect with the database) waiting for connection request;
3 Run try_client(using GUI, provide window for user):
    -open login window for user to login or register;
    -enter the administrator window with administrator's right;
    -enter the user window with user's right;
  Call functions through buttons or menus. Establish connection with the database in the sever. Then save/get data to/from the database.
  Show result in message box or text box.


 *Knowledge has been used (Python):
1 GUI:       tkinter module (include button, entry, text, label, menu,);
2 GUI:       tkinter.message module and tkinter.simpledialog module (askstring, askinteger);
3 Socket:    socket module (communicate and exchange data between sever and client);
4 database:  mysql module (write data into database and read data from it)
