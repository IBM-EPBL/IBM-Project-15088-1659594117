from flask import Flask, render_template, request,redirect
import ibm_db
import dbconn

app = Flask(__name__)


@app.route('/')
def register():
    return render_template("register.html")


@app.route('/login')
def login():
     return render_template("login.html")

#welcome page code

@app.route('/welcome')
def welcome():
   
      if dbconn.con:
          sql="SELECT * FROM userdetails"
          smt= ibm_db.exec_immediate(dbconn.con,sql)
          res = ibm_db.fetch_both(smt)
          result=[]
          while res != False:
            result.append(res)
            row=len(result) 
            res = ibm_db.fetch_both(smt)
          return render_template("welcome.html",r=result,rows=row)
                           
    

#registration page code


@app.route("/signup", methods=['POST'])
def signup():
       if request.method == 'POST':
         name = request.form.get('name')
         email = request.form.get('email')
         pwd = request.form.get('pwd')
         roll = request.form.get('roll')
         sql = "INSERT INTO  userdetails (username,email,password,rollnumber) VALUES ('{0}','{1}','{2}','{3}')"
         res = ibm_db.exec_immediate(dbconn.con, sql.format(name, email, pwd, roll))
         if sql:
            return redirect("/login")
         else:
            return redirect("/")
       else:
        print("Could'nt store anything...")


#login page code      


@app.route("/signin", methods=['POST'])
def signin():
       if request.method == 'POST':
            email = request.form.get('email')
            pwd = request.form.get('pwd')
            sql = "SELECT * FROM  userdetails WHERE EMAIL='{0}' AND PASSWORD='{1}'"
            smt = ibm_db.prepare(dbconn.con, sql.format(email,pwd))
            ibm_db.execute(smt)
            res=ibm_db.fetch_assoc(smt)
            if res:
                 return redirect("/welcome")
            else:
                 return redirect("/login")
       else:
         print("Could'nt store anything...")

        
#update page code

@app.route("/update/<string:id>", methods=['POST','GET'])
def update(id):
            if request.method =='POST':
               name = request.form.get('name')
               email = request.form.get('email')
               pwd = request.form.get('pwd')
               roll = request.form.get('roll')
               sql="UPDATE  userdetails SET username='{0}',email='{1}',password='{2}',rollnumber='{3}' WHERE id='{4}'"
               res = ibm_db.exec_immediate(dbconn.con, sql.format(name,email,pwd,roll,id))
               if sql:
                 return redirect("/welcome")
               else:
                 return redirect("/")
            else:
                print("Could'nt store anything...") 

            sql="SELECT * FROM  userdetails WHERE id='{0}'"
            smt=ibm_db.exec_immediate(dbconn.con,sql.format(id))
            res = ibm_db.fetch_both(smt)
            return render_template("update.html",update=res)



#delete page code

@app.route("/delete/<string:id>",methods=['POST','GET'])
def delete(id):
         sql="DELETE FROM  userdetails WHERE id='{0}'"
         smt=ibm_db.exec_immediate(dbconn.con,sql.format(id))
         return redirect("/welcome")



if __name__ == '__main__':
    app.run(debug=True)
