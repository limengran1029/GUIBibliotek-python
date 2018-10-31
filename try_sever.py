import socket
import mysql.connector
import json

def connect_s():
    mydb = mysql.connector.connect(host="localhost", user="root", password="root", database="library")
    mycursor = mydb.cursor()
    host,port = socket.gethostname(),9999  # 获取本地主机名
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss: # 创建 socket 对象(socket_family, socket_type)
        ss.bind((host, port))  # 绑定端口号
        ss.listen(5) # 设置最大连接数，超过后排队
        print('server listening...')
        while True:  # 建立客户端连接,无限等待连接
            cs,addr = ss.accept()
            print('Get connection from: %s\n'%addr[0])
            while True:  #通信循环，无限接受客户端信息
                msgc = cs.recv(1024).decode("utf-8")  # 接收小于 1024 字节的数据
                if msgc == 'over':
                    print('connection with : %s is break\n'%addr[0])
                    break
                else:
                    request = msgc.split('/')
                    if request[0] == 'sign in':
                        try:
                            mycursor.execute("select password from permission where name='%s'"%(request[1]))
                            pw = mycursor.fetchall()[0][0]
                            if  pw == request[2]:
                                msg = 'matched'
                                cs.send(msg.encode('utf-8'))
                            else:
                                msg = 'fail'
                                cs.send(msg.encode('utf-8'))
                                print('connection with : %s is break\n'%addr[0])
                                break
                        except IndexError:
                            msg = 'user is not exist!'
                            cs.send(msg.encode('utf-8'))
                            print('connection with : %s is break\n'%addr[0])
                            break
                    elif request[0] == 'sign in_pm':
                        mycursor.execute("select pm from permission where name='%s'"%(request[1]))
                        pm = mycursor.fetchall()[0][0]
                        msg = pm
                        cs.send(msg.encode('utf-8'))
                    elif request[0] == 'enter':
                        try:
                            mycursor.execute("select name from permission where name='%s'"%(request[1]))
                            msg = mycursor.fetchall()[0][0]
                            cs.send(msg.encode('utf-8'))
                            print('connection with : %s is break\n'%addr[0])
                            break
                        except IndexError:
                            mycursor.execute("insert into permission set name ='%s', password='%s',pm ='user'"
                                             %(request[1],request[2]))
                            mydb.commit()
                            msg = 'create the account successfully!'
                            cs.send(msg.encode('utf-8'))
                            print('connection with : %s is break\n'%addr[0])
                            break
                    elif request[0] == 'add_item':
                            mycursor.execute("select author,topic,language,location from book where title='%s'"%(request[1]))
                            myresult = mycursor.fetchall()
                            try:
                                msg = ""
                                for x in myresult:
                                    if x[0]==request[2] and x[1]==request[3] and x[2]==request[4] and x[3]==request[5]:
                                        msg = 'this item is already exist!'
                                        break
                                if msg == "":
                                    mycursor.execute('''insert into book set title='%s',author='%s',topic='%s',language='%s',
                                                        location='%s',total_number='%d',inside_number='%d' '''
                                                     %(request[1],request[2],request[3],request[4],request[5],0,0))
                                    mydb.commit()
                                    msg = 'add item successfully!'
                            except IndexError:
                               mycursor.execute('''insert into book set title='%s',author='%s',topic='%s',language='%s',
                                                   location='%s',total_number='%d',inside_number='%d' '''
                                                %(request[1],request[2],request[3],request[4],request[5],0,0))
                               mydb.commit()
                               msg = 'add item successfully!'
                            cs.send(msg.encode('utf-8'))
                    elif request[0] == 'add_book':
                        mycursor.execute('''select id,title,author,topic,language,location,total_number,inside_number from book
                                           where title='%s' '''%(request[1]))
                        myresult = mycursor.fetchall()
                        if len(myresult) == 0:
                            msg = 'item is not exist, please add the item first!'
                            cs.send(msg.encode('utf-8'))
                        else:
                            msg = json.dumps(myresult)  #convert list to string to send
                            cs.send(msg.encode('utf-8'))
                    elif request[0] == 'add_book_num':
                        mycursor.execute("update book set total_number = total_number + '%d' where id='%d'"
                                         %(int(request[3]),int(request[1])))
                        mycursor.execute("update book set inside_number = inside_number + '%d' where id='%d'"
                                         %(int(request[3]),int(request[1])))
                        mycursor.execute('''insert into event_record set book_id='%d',title='%s',debit='%d',remark='add books',
                                            operator='%s' '''%(int(request[1]),request[2],int(request[3]),request[4]))
                        mydb.commit()
                    elif request[0] == 'fb_title':
                        mycursor.execute('''select id,title,author,topic,language,location,total_number,inside_number from book
                                            where title='%s' '''%(request[1]))
                        myresult = mycursor.fetchall()
                        if len(myresult) == 0:
                            msg = 'book is not exist!'
                        else:
                            msg = ''
                            for x in myresult:
                                msg += '''bookId: {}, title: {}, author: {}, topic: {}, language: {}, location: {},
                                                            total_number: {}, inside_number: {}\n'''\
                                                 .format(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
                        cs.send(msg.encode('utf-8'))
                    elif request[0] == 'fb_author':
                        mycursor.execute('''select id,title,author,topic,language,location,total_number,inside_number from book
                                            where author='%s' '''%(request[1]))
                        myresult = mycursor.fetchall()
                        if len(myresult) == 0:
                            msg = "this author's book is not exist!"
                        else:
                            msg = ''
                            for x in myresult:
                                msg += '''bookId: {}, title: {}, author: {}, topic: {}, language: {}, location: {},
                                                            total_number: {}, inside_number: {}\n'''\
                                                 .format(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
                        cs.send(msg.encode('utf-8'))
                    elif request[0] == 'record':
                        mycursor.execute("select id,book_id,title,debit,remark,operator,time from event_record where book_id='%d' "
                                              %(int(request[1])))
                        myresult = mycursor.fetchall()
                        if len(myresult) == 0:
                            msg = 'record is not exist!'
                        else:
                            msg = ''
                            for x in myresult:
                                msg += "id: {}, book_id: {}, title: {}, debit: {}, remark: {}, operator: {}, timer: {}\n"\
                                                 .format(x[0],x[1],x[2],x[3],x[4],x[5],x[6])
                        cs.send(msg.encode('utf-8'))
                    elif request[0] == 'borrow_book':
                        mycursor.execute("select inside_number from book where id='%d' "%(int(request[1])))
                        myresult1 = mycursor.fetchall()[0][0]
                        if myresult1 > 0:
                            mycursor.execute("update book set inside_number=inside_number+'%d' where id='%d'"%(-1,int(request[1])))
                            mycursor.execute('''insert into event_record set book_id='%d',title='%s',debit='%d',
                                              remark='borrow books',operator='%s' '''%(int(request[1]),request[2],-1,request[3]))
                            mydb.commit()
                            msg = 'borrow the book successfully!'
                        else:
                            msg = 'sorry, the book is not inside!'
                        cs.send(msg.encode('utf-8'))
                    elif request[0] == 'return_book':
                        mycursor.execute("update book set inside_number=inside_number+'%d' where id='%d'"%(1,int(request[1])))
                        mycursor.execute('''insert into event_record set book_id='%d',title='%s',debit='%d',
                                          remark='return books',operator='%s' '''%(int(request[1]),request[2],1,request[3]))
                        mydb.commit()
                        msg = 'return the book successfully!'
                        cs.send(msg.encode('utf-8'))
                    elif request[0] == 'check_loans':
                        mycursor.execute('''select book_id,SUM(debit) as 'loan' from event_record
                                              where operator='%s' group by book_id'''%(request[1]))
                        myresult = mycursor.fetchall()
                        if len(myresult) == 0:
                            msg = "you have not borrowed any book!"
                        else:
                            sum = 0
                            show = ''
                            for x in myresult:
                                sum += x[1]
                                if x[1] < 0:
                                    mycursor.execute("select title from event_record  where book_id='%d' "%(x[0]))
                                    myresult1 = mycursor.fetchall()[0][0]
                                    show += "bookId: {}, title: {}, loan: {}\n".format(x[0],myresult1,x[1])
                            if sum == 0:
                                msg = "you don't have any loan!"
                            else:
                                msg = show
                        cs.send(msg.encode('utf-8'))

#-----------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    connect_s()

