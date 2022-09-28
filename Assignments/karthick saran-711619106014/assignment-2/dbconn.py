import ibm_db
try:
    con = ibm_db.connect("DATABASE=bludb;HOSTNAME=6667d8e9-9d4d-4ccb-ba32-21da3bb5aafc.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30376;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cbz80734;PWD=cz0m6kftvJbqAQfP;", '', '')
    print("db connection successfully")
except:
    print("db connection failed")
