import uuid,os,time

while 1 :
    os.system('echo "' +str(uuid.uuid4())+ '" > zz.py')
    time.sleep(30)

