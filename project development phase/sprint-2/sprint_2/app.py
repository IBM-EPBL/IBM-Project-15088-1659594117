from flask import Flask, render_template, request,redirect,g,session
import math
import ibm_db
import uuid
import os
import dbconn
import api

app = Flask(__name__)

app.secret_key=os.urandom(24)

@app.route('/')
def index():
    if "UID" in session:
       return redirect("/home/api/headlines")
    else:
        return render_template("index.html")
@app.route('/signup')
def register():
    return render_template("signup.html")

@app.route('/signin')
def login():
    return render_template("signin.html")



#registration page code


@app.route("/registration", methods=['POST'])
def signup():
       if request.method == 'POST':
         name = request.form.get('name')
         email = request.form.get('email')
         pwd = request.form.get('pwd')
         emailcheck="SELECT * FROM authentication WHERE EMAIL='{0}' "
         smt = ibm_db.prepare(dbconn.con, emailcheck.format(email))
         ibm_db.execute(smt)
         mailres=ibm_db.fetch_assoc(smt)
         if mailres:
              return render_template("signup.html",msg="Email Is Already Taken")
         else:
           sql = "INSERT INTO authentication (id,username,email,password) VALUES ('{0}','{1}','{2}','{3}')"
           res = ibm_db.exec_immediate(dbconn.con, sql.format(uuid.uuid4(),name, email, pwd,))
           if sql:
              return redirect("/signin")
           else:
              return redirect("/")
       else:
        print("Could'nt store anything...")



#login page code      


@app.route("/login", methods=['POST'])
def signin():
       if request.method == 'POST':
            email = request.form.get('email')
            pwd = request.form.get('pwd')
            sql = "SELECT * FROM authentication WHERE EMAIL='{0}' AND PASSWORD='{1}'"
            smt = ibm_db.prepare(dbconn.con, sql.format(email,pwd))
            ibm_db.execute(smt)
            res=ibm_db.fetch_assoc(smt)
            
            if res: 
                 session["UID"]=res['ID']
                 return redirect("/home/api/headlines?page=1")
            else:
                  return render_template("signin.html",msg="Invalid Email Or Password")
       else:
         print("Could'nt store anything...")

#home page

@app.route('/home/api/headlines')
def home():
      if "UID" in session:
         sql = "SELECT * FROM authentication WHERE ID='{0}' "
         smt = ibm_db.prepare(dbconn.con, sql.format(session["UID"]))
         ibm_db.execute(smt)
         res=ibm_db.fetch_assoc(smt)
         if res:
            h=api.headlines()
            tore=h['totalResults']
            to=math.ceil(tore/int(9))
            u=request.base_url
            pn=request.args.get('page')
            pn=1
            if pn:
               e_p=int(pn)*int(9)
               s_p=int(e_p)-int(9)
            return render_template("home.html",data=res,news=h,url_head=u,s=s_p,e=e_p,total=to,title="headlines")
         else:
            return redirect("/signin")
      else:
        return redirect("/signin")

 #search module

@app.route('/home/api/query',methods=['GET'])
def query():
        if "UID" in session:
            sql = "SELECT * FROM authentication WHERE ID='{0}' "
            smt = ibm_db.prepare(dbconn.con, sql.format(session["UID"]))
            ibm_db.execute(smt)
            res=ibm_db.fetch_assoc(smt)
            if res:
                  q=request.args.get('search')
                  s=api.search(q)
                  tore=s['totalResults']
                  to=math.floor(tore/int(9))
                  if to>=10:
                     to=10
                  u=request.base_url
                  pn=request.args.get('page')
                  pn=1
                  if pn:
                    e_p=int(pn)*int(9)
                    s_p=int(e_p)-int(8)
                  return render_template("home.html",data=res,news=s,url_query=u,q=q,s=s_p,e=e_p,total=to,title=q)
            else:
              return redirect("/signin")
        else:
           return redirect("/signin")

#category module

@app.route('/home/api/cat-list',methods=['GET'])
def category():
        if "UID" in session:
            sql = "SELECT * FROM authentication WHERE ID='{0}' "
            smt = ibm_db.prepare(dbconn.con, sql.format(session["UID"]))
            ibm_db.execute(smt)
            res=ibm_db.fetch_assoc(smt)
            if res:
                  q=request.args.get('category')
                  s=api.category(q)
                  tore=s['totalResults']
                  to=math.floor(int(tore)/int(9))
                  print(to)
                  u=request.base_url
                  pn=request.args.get('page')
                  if pn:
                    e_p=int(pn)*int(9)
                    s_p=int(e_p)-int(9)
                  return render_template("home.html",data=res,news=s,url_cat=u,s=s_p,e=e_p,qu=q,total=to,title=q)
            else:
              return redirect("/signin")
        else:
           return redirect("/signin")

#logout module

@app.route('/logout')
def logout():
        session.pop("UID",None)
        return redirect("/signin")

if __name__ == '__main__':
    app.run(debug=True)
