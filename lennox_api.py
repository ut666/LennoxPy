import requests
import json

class Lennox_iComfort_API():
    """Representation of the Lennox iComfort thermostat sensors."""
    
    def __init__(self, username, password, system, zone):
        """Initialize the sensor."""
        self._name = 'lennox'
        self._username = username
        self._password = password

        self._system = system
        self._zone = zone

        self._serialNumber = "Unknown"

        self._temperature = "Unknown"
        self._humidity = "Unknown"
        self._heatto = "Unknown"
        self._coolto = "Unknown"
        self._awaymode = "Unknown"
        self._programmode = "Unknown"
        self._tempunit = "1" #0 = F, 1 = C

        self._state = "Unknown"
        self._state_list = ['Idle', 'Heating', 'Cooling'];
        self._program = "Unknown"
        self._program_list = []
        self._opmode = "Unknown"
        self._opmode_list = ['Off', 'Heat only', 'Cool only', 'Heat & Cool']
        self._fanmode = "Unknown"
        self._fanmode_list = ['Auto', 'On', 'Circulate']
        self.get()
    
    def set(self):
        #Perform our json query
        validateUser = "ValidateUser";
        getSystemsInfo = "GetSystemsInfo";
        gatewaySN  = "?gatewaysn="
        getTStatInfoList = "GetTStatInfoList";
        setTStatInfo = "SetTStatInfo";
        userID = "?UserId=";
        serviceURL = "https://" + self._username + ":" + self._password + "@services.myicomfort.com/DBAcessService.svc/";
        session_url = serviceURL + validateUser + "?UserName=" + self._username + "&TempUnit=+ " + self._tempunit;
        s = requests.session();
        cookies = s.get(session_url)

        #form our string
        data = {
            'Cool_Set_Point':self._coolto, 
            'Heat_Set_Point':self._heatto, 
            'Fan_Mode':self._fanmode, 
            'Operation_Mode':self._opmode, 
            'Pref_Temp_Units':self._tempunit, 
            'Zone_Number':self._zone, 
            'GatewaySN':self._serialNumber}
        
        #now do a setTStatInfo request
        url = serviceURL + setTStatInfo;
        headers = {'contentType': 'application/x-www-form-urlencoded', 'requestContentType': 'application/json; charset=utf-8'}

        #do our http PUT call
        resp2 = s.put(url, json=data, headers=headers);
        #print resp2
        
    def get(self):
        #Perform our json query
       
        getSystemsInfo = "GetSystemsInfo";
        getTStatInfoList = "GetTStatInfoList";
        getTStatScheduleInfo = "GetTStatScheduleInfo";
        getProgramInfo = "GetProgramInfo";
               
        validateUser = "ValidateUser";
        gatewaySN  = "?gatewaysn="
        userID = "?UserId=";
        serviceURL = "https://" + self._username + ":" + self._password + "@services.myicomfort.com/DBAcessService.svc/";
        session_url = serviceURL + validateUser + "?UserName=" + self._username + "&TempUnit=" + self._tempunit;
        s = requests.session();
        cookies = s.get(session_url)
        url = serviceURL + getSystemsInfo + userID + self._username;
        r = s.get(url)

        #fetch the requested system
        system = r.json()["Systems"][self._system]

        #fetch our system serial number
        self._serialNumber = system["Gateway_SN"];

        #now do a getTStatInfoList request
        url = serviceURL + getTStatInfoList + gatewaySN + self._serialNumber + "&TempUnit=" + self._tempunit;
        resp = s.get(url);

        #fetch the stats for the requested zone
        statInfo = resp.json()['tStatInfo'][self._zone];

        #get our status
        self._state = int(statInfo['System_Status']);

        #get our operation mode
        self._opmode = int(statInfo['Operation_Mode']);
        #print "_opmode: " + str(self._opmode)
        
        #get our fan mode
        self._fanmode = int(statInfo['Fan_Mode']);
                
        #get our away mode
        self._awaymode = int(statInfo['Away_Mode']);
        
        #get our indoor temperature
        self._temperature = float(statInfo['Indoor_Temp']);

        #get our indoor humidity
        self._humidity = float(statInfo['Indoor_Humidity']);

        #get our heat to temperature
        self._heatto = float(statInfo['Heat_Set_Point']);
        
        #get our cool to temperature
        self._coolto = float(statInfo['Cool_Set_Point']);
        
        #get our program mode
        self._programmode = int(statInfo['Program_Schedule_Mode'])
        #print "Program Mode: " + str(self._programmode)
        
        #get our selected program
        self._programselection = statInfo['Program_Schedule_Selection']
        #print "Program Selection: " + str(self._programselection)

        #get the available programs
        self._program_list = []
        url = serviceURL + getTStatScheduleInfo + gatewaySN + self._serialNumber;
        resp = s.get(url);

        for program in resp.json()['tStatScheduleInfo']:   
            #print str(program['Schedule_Number']) + ": " + str(program['Schedule_Name'])
            self._program_list.insert(int(program['Schedule_Number']), program['Schedule_Name'])

        if self._programmode == 1:
            #print "Program Mode is ON"
            url = serviceURL + getProgramInfo + gatewaySN + self._serialNumber + "?ScheduleNum=" + str(self._programselection) + "&TempUnit=" + self._tempunit;
            resp = s.get(url);
            #print resp
            #print resp.json()
        