# Get a text file bbbb.txt
# Extraxt java logs
# change to RPG eval statements
# use regEx to extract and change

import re, pathlib
from datetime import datetime, timedelta, date
try:
    def findAll(inPattern, inStr):
        return re.findall(inPattern, inStr)

    def fieldNameAndValue(inStr, inSeperator):
        s= inStr
        c= inSeperator
        i=s.index(c)
        bef = s[:i]
        aft = s[i+1:]
        return bef,aft

    def checkForType(inStr, fieldName):
        #date
        pattern      = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
        input_str    = inStr.strip()
        matcher = pattern.fullmatch(input_str.strip())
        if matcher:
            return 'D'

        #Time Stamp
        pattern = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.[0-9]{6}")
        input_str    = inStr.strip()
        matcher = pattern.fullmatch(input_str.strip())
        if matcher:
            return 'Z'

        ## pattern      = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}")
        ## input_str    = inStr.strip()
        ## matcher = pattern.findall(input_str.strip())
        ## if matcher:
        ##     return 'Z'

        # Float
        pattern = re.compile(r"^-?\d+\.\d+$")   # works ['45.60'/'817600.0'] treated as float
        matcher = pattern.fullmatch(input_str.strip())
        if matcher:  # works ['45.60'/'817600.0'] treated as float
            return 'F'

        #numeric
        pattern      = re.compile(r"^[0-9]+")
        input_str    = inStr.strip()
        matcher = pattern.findall(input_str.strip())
        if matcher:
            if fieldName.strip()[-4:] == 'CODE':
                return 'S'
            else:
                if str(input_str).strip().isdecimal() == True: # works ['17602550'] treated as interger
                    return 'I'
                if str(input_str).strip().isdecimal() == False: # works ['45.60'/'817600.0'] treated as float
                    return 'F'

                return None # Error


        #String
        pattern      = re.compile(r"^[a-z]|^[A-Z]")
        input_str    = inStr.strip()
        matcher = pattern.findall(input_str.strip())
        if matcher:
            return 'S'



    def returnLines(inStr, fieldName):
        def typeString(varString):
                return "'"  + varString.strip() + "'"

        def typeDecimal(varString):
                return varString.strip()

        def typeDate(varString):
                return "d'" + varString.strip() + "'"

        def typeTimeStamp(varString):
                return "%timeStamp('"  + varString.strip() + "')"

        returnType = checkForType(inStr, fieldName)
        #date
        if returnType == 'D':
            return typeDate(inStr.strip())

        #Time Stamp
        if returnType == 'Z':
            return typeTimeStamp(inStr.strip())

        #numeric
        if returnType in ('I', 'F') :
            return typeDecimal(inStr.strip())


        #string
        if returnType == 'S':
            return typeString(inStr.strip())


        #could not determine type
        return "ERROR"

    inputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/Member_Install_Error_Raw.txt'
    outputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/'
    outputfile = 'RPG_Eval_Statements'

    datenow = datetime.now()
    datestrftime= datenow.strftime('%Y%m%d%h%m')
    datefileext = datestrftime + '.txt'
    print(datenow)
    print(datestrftime)
    print(datefileext)

    # masking
    ## first 2 rows is for masking
    mainList = [["abcdefghkl","=","abcdefghklmnopqrstuvwxyzabcdefghklmnopqrstuvwxyz",";"]]
    sublist = ["12345890","=","1234567890mnopqrstuvwxyz1234567890z",";"]

    mainList.append(sublist)
    print(mainList)

    datefilename = outputpath + outputfile + datefileext
    print(datefilename)

    fiRqstNm = ''
    apiPgmNm = ''

    startStr ='updater.inParameters.'
    with open(inputpath) as f:
        lines = f.readlines()
        #append text file
        rpgfile=open(datefilename, mode='w', encoding='utf-8')
        rpgfile=open(datefilename, mode='a', encoding='utf-8')
        for index,l in enumerate(lines):
            if l.strip().startswith(startStr):
                rpg_l = l.replace(startStr, '').strip()
                # .replace(startStr, 'updater.inParameters.')
                bef, aft = fieldNameAndValue(rpg_l, ':')
                if aft.strip() in ("", "0", "0.0"," "):
                    continue

                rpg_l_str = bef + " = "  + str(returnLines(aft,bef)) + " ; "
                ret_aft = str(returnLines(aft,bef))
                rpg_1_idx = rpg_l_str.split(' ')
                eq="="
                endline=';'
                # maxField =
                if 1 > 2: # index%2 == 0:   *** the below works but I like the dynamic space allocation (esle:)
                    #rpg_1_fmt =f"{rpg_1_idx[0].ljust(12)}{rpg_1_idx[1].ljust(3)}{rpg_1_idx[2].ljust(40)}{rpg_1_idx[3].ljust(15)}"
                    rpg_1_fmt =f"{bef.ljust(12)}{eq.ljust(3)}{ret_aft.ljust(40)}{endline.ljust(15)}"
                    rpgfile.write(str(rpg_1_fmt).strip())
                    rpgfile.write('\n')
                else:
                    # rpg_1_fmt = '{:>12}   {:4}   {:>12}  {:>12}'.format(rpg_1_idx[0],rpg_1_idx[1],rpg_1_idx[2],rpg_1_idx[3])
                    sublist = [bef,"=",ret_aft,";"]
                    mainList.append(sublist)

            if l.strip().startswith('updater.requestName:'):
                fiRqstNm = "fiRqstNmO = " + l.strip().replace('updater.requestName:', '').strip() + ' ; '


        if mainList[2] != []:
            # print(mainList)
            #rpgfile.write(str(rpg_1_fmt).strip())
            items=mainList
            length = [max([len(item[i]) for item in items]) for i in range(len(items[0]))] # maximum length of each field
            max_length = sum(length)
            for rowIdx,item in enumerate(items): # rows

                if rowIdx < 2: # ignore first two rows (masking)
                    continue

                rpg_new =''
                for i in range(len(length)): # maximum length of each field
                    item_length = len(item[i])

                    if i != 0: # if it is not the first item in the list (first field) add a SPACE before
                        rpg_new += " "

                    if length[i] > len(item[i]): # maximum length is greater than the item, then align item to the maximum length
                        #print(item[i] + " " * (length[i] - item_length), end="|")
                        rpg_new += item[i] + " " * (length[i] - item_length)
                    else: # same as maximum length
                        #print(item[i], end="|")
                        rpg_new += item[i]
                #print()
                #print(rpg_new)
                rpgfile.write(str(rpg_new).strip())
                rpgfile.write('\n')

        rpgfile.write('\n')
        rpgfile.write(str(fiRqstNm).strip())
        rpgfile.write('\n')

        ## Do this bit dynamically when you get a moment....Get copyBook and Reqhest Handler
        apiPgmNm = "ApiPgm('FINENRH': " + "fiRqstNmO: " +  "nenPtrIn: nenPtrOt);"

        rpgfile.write('\n')
        rpgfile.write(str(apiPgmNm).strip())
        rpgfile.write('\n')

        input_Ds = "Clear  NenInDs;"
        rpgfile.write('\n')
        rpgfile.write(str(input_Ds).strip())
        rpgfile.write('\n')

        rpgfile.close()

    print(f"Completed Successfully...Horay!!!!!!")

except Exception as e:
    print("Something went Wrong!!!! Exception.......:  " + str(e))

quit()