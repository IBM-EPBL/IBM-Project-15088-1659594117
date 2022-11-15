import ibm_db
try:
    con = ibm_db.connect("DATABASE=bludb;HOSTNAME=b1bc1829-6f45-4cd4-bef4-10cf081900bf.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32304;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=gbl11433;PWD=r1iyI6KcILvCmHw1;", '', '')
    print("db connection successfully")
except:
    print("db connection failed")
