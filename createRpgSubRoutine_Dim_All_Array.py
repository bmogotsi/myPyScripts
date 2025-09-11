3# Get a text file bbbb.txt
# Extraxt java logs
# change to RPG eval statements
# use regEx to extract and change

""" Flow
    1. open a chosen java logs text file
    2. read the text file line by line
        a. check if line is Stand Alone field or List field
            field_and_value_separator = ["=", "]  Value [", " : "]
            a01. skip if field value is blank, zero or empty
            a02. if field is NOT Stand Alone or List
                - get Request Handler name
                - get Program name
                - get Copybook name
             a03. extract field name and field value
        C. change to RPG eval statements
"""

import re, pathlib
from datetime import datetime, timedelta, date
import traceback
# from traceback import TracebackException

# inputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/erp_LOADEPCCC_FIEPCRH_Raw.txt'
inputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/Member_Install_Error_Raw.txt'
outputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/'
outputfile = 'RPG_Eval_Statements_'
field_value_Bracket_open = "["
field_value_Bracket_close = "]"
field_and_value_separator = ["=", "]  Value [", " : "]
field_value_is_blank = ["", " ", "0", "null", "",  "0.0","\n"]
equal_Sign="="
end_of_line=';'

try:

    def findAll(inPattern, inStr):
        return re.findall(inPattern, inStr)

    def fieldNameAndValue(inStr, inSeperator):
        """ Extract field name and field value from text
                Strip the square brackets "[]"
            Return 2 variables Before (fierd name) and After (field value)
        """
        s= inStr
        c= inSeperator
        i=s.index(c)

        i=0
        for idx, value in enumerate(c):
            if value in s:
                i=s.index(value)
                break
        if i == 0:
           return '', ''


            #print(f"Error: invalid inSeperator, must be: {inSeperator} ")
            #raise ValueError(f"Error: invalid inSeperator, must be: {inSeperator}")

        bef = s[:i]
        aft = s[i+1:]
        aft = aft.strip().strip(field_value_Bracket_open).strip(field_value_Bracket_close).strip(field_value_Bracket_close)
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



    def returnRpgStatement(inStr, fieldName):
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

    def get_Occurance(inStr):
        pattern = re.compile(r"occurs(\s+)?=(\s+)?\[\d+\]")

        # Using re.search() -
        #     returns first match STRING
        #     Returns None if no match found

        search_returnValue = re.search(pattern, inStr.lower()) # Case-sensitive by default

        if search_returnValue != None:
            # get value
            returnStr = search_returnValue.group()
            return_Occurs = returnStr.split("=")[1].strip(field_value_Bracket_open).strip(field_value_Bracket_close)
            # print(f"The decimal value of the 'occurs' is: {return_Occurs}")
        else:
            returnStr = 0

        return return_Occurs

    def get_Dimensions(inStr):
        changeStr =inStr
        return_string = "%list( "
        new_change_string = re.sub(r"(\d+\))", r"|", changeStr)
        new_change_string = new_change_string.strip("|")
        all_dim = new_change_string.split("|")
        for index,dim in enumerate(all_dim):
            if index > input_Occurs-1:
                break
            dim_String = returnRpgStatement(dim.strip(), bef) #change field value to Filed TYPE string

            return_string = return_string + dim_String.strip()  + " :"

        return_string = return_string.strip(":") +  " )"

        return return_string

    def get_CopybookName_or_ProgramName(inProgram, inCopybook):
        copybook = inCopybook
        program = inProgram

        if program == '' and copybook != '' :
            program = copybook.strip('CB') + 'RH'
            print(f"program name from copybook {copybook} ---> : {program}")

        if program != '' and copybook == '' :
            copybook = program.strip('RH') + 'CB'
            print(f"copybook name from program {program} ---> : {copybook}")

        return program, copybook

    def getCopybookName(inStr):
        copybook = ""
        pattern_cb_1 = re.compile(r"(file\[\w+\])") # PCML File[FINENCB]
        if re.search(pattern_cb_1, inStr.lower()):
            copybook = re.search(pattern_cb_1, inStr.lower()).group()
            #    requestHandler = requestHandler.split("[")
            #    requestHandler = requestHandler[1]
            #    requestHandler = requestHandler.strip(field_value_Bracket_close)
            #    requestHandler = requestHandler.strip("}")
            #    requestHandler = requestHandler.strip()
            copybook = copybook.split("[")[1].strip(field_value_Bracket_close).strip("}").strip()

        return copybook.upper()

    def getProgramName(inStr):
        programName = ""
        pattern_pgm_1 = re.compile(r"program\[\w+\.\w+\]") #program[fiepcrh.LOADEPCCC]

        if re.search(pattern_pgm_1, inStr.lower()): # program[fiepcrh.LOADEPCCC]
            programName = re.search(pattern_pgm_1, inStr.lower()).group()
            programName = programName.split(".")[0].strip("program").strip(field_value_Bracket_open).strip()

        return programName.upper()

    def getRequestHandler(inStr):
        requestHandler = ""
        pattern_rh_1 = re.compile(r"(request\[\w+\])|(requestname\[\w+\])")
        pattern_rh_2 = re.compile(r"updater\.requestname\:(\s+)?\w+")
        pattern_rh_3 = re.compile(r"program\[\w+\.\w+\]") #program[fiepcrh.LOADEPCCC]
        if re.search(pattern_rh_1, inStr.lower()):
            requestHandler = re.search(pattern_rh_1, inStr.lower()).group()
            #    requestHandler = requestHandler.split("[")
            #    requestHandler = requestHandler[1]
            #    requestHandler = requestHandler.strip(field_value_Bracket_close)
            #    requestHandler = requestHandler.strip("}")
            #    requestHandler = requestHandler.strip()
            requestHandler = requestHandler.split("[")[1].strip(field_value_Bracket_close).strip("}").strip()

        elif re.search(pattern_rh_2, inStr.lower()):
            requestHandler = re.search(pattern_rh_2, inStr.lower()).group()
            requestHandler = requestHandler.split(" ")[1].strip(field_value_Bracket_close).strip("\n").strip()

        elif re.search(pattern_rh_3, inStr.lower()): # program[fiepcrh.LOADEPCCC]
            requestHandler = re.search(pattern_rh_3, inStr.lower()).group()
            requestHandler = requestHandler.split(".")[1].strip(field_value_Bracket_close).strip("}").strip()


        return requestHandler.upper()

    def getRpgProgramCallStatement(copyBook, requestHandler, programName):
        ret_begSr = ''
        ret_Call = ''
        ret_endSr = ''
        # indentRpg = "    "

        process_3Letter =  copyBook[2:-2].strip("").lower()
        ret_begSr = indentRpg + "//----------------------------------------------------------------  " + "\n"\
                + indentRpg + "BegSr  Get" + process_3Letter.title() + "Values" + "Sr;" + "\n" \
                + indentRpg + "//----------------------------------------------------------------  " + "\n" \
                + indentRpg + "clear  " + process_3Letter + "InDs" +"; " + "\n" \
                + indentRpg + "clear  " + process_3Letter + "OtDs" +"; " + "\n" \
                + indentRpg + "\n\n"\
                + indentRpg + "     " + "if AllocRequest(" + process_3Letter + "PtrIn" +": " + process_3Letter + "PtrOt" + ": "\
                + indentRpg + process_3Letter + "SizeIn" +": " + process_3Letter + "SizeOt"  +"); " + "\n"

        ret_Call = indentRpg + "fiRqstNmO = " + "'" + requestHandler.strip() + "'" +";" + "\n" \
                + indentRpg + "ApiPgm(" + "'" + programName.strip() + "'" + ": " + "fiRqstNmO" + ": "\
                + indentRpg + process_3Letter + "PtrIn" +": " \
                + indentRpg + process_3Letter + "PtrOt" +"); " + "\n"\
                + indentRpg + "\n" + indentRpg +"if fiRtnCodO = '0';" + "\n"\
                + indentRpg + "    " + "//" + process_3Letter + "OtDs;" + "\n" \
                + indentRpg + "endIf; "  \
                + indentRpg + "\n"

        ret_endSr = indentRpg + "     " + "endIf;" + "\n"\
                + indentRpg + "\n\n"\
                + indentRpg + "//----------------------------------------------------------------  " + "\n" \
                + indentRpg + "EndSr;"+"\n"\
                + indentRpg + "//----------------------------------------------------------------  " + "\n" \


        return ret_begSr, ret_Call, ret_endSr

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

    """ it all starts here
        1. find a specific text files in the directory
          2. read the text file
          3. extract the java logs
          4. change to RPG eval statements
          5. use regEx to extract and change
          6. append RPG Statements to a text file
    """

    startStr ='updater.inParameters.'
    with open(inputpath) as f:
        lines = f.readlines()
        #append text file
        rpgfile=open(datefilename, mode='w', encoding='utf-8')
        rpgfile=open(datefilename, mode='a', encoding='utf-8')

        input_Occurs = 0
        request_name = ''
        program_name = ''
        copybook_name = ''

        for index,l in enumerate(lines):
            if l.strip().endswith('=[]]')\
                or '\n' == l.strip() \
                or re.search(re.compile(r"(?<!\w)\d+:\n"), l.lower())\
                    : # skip blank/zeros fields STAND Alone
                    continue

            patternStandalone = re.compile(r"(\s+)?=(\s+)?\[(\w+)\]")
            patternStandalone2 = re.compile(r"\](\s+)?Value(\s+)?\[\w+\]") # occurs=[10]
            patternList = re.compile(r"(\w+)(\s+)?=(\s+)?0\)")
            patternList2 = re.compile(r"\](\s+)?value(\s+)?\[\[\w+\]\]")
            patternOccurs = re.compile(r"occurs(\s+)?=(\s+)?")
            field_is_Standalone = False
            field_is_List = False

            if re.search(patternStandalone, l.lower()): # Case-sensitive by default
                field_is_Standalone = True
            elif re.search(patternList, l.lower()):
                field_is_List = True
            else:
                field_is_Standalone = False
                field_is_List = False

                # get RH, CB and Request Name
                if l.strip() == '\n':
                    continue
                if re.search(re.compile(r"(?<!\w)\d+:\n"), l.lower()):
                    continue

                if request_name == '':
                    request_name = getRequestHandler(l.lower())
                    if request_name != '':
                        print(f"request name: {request_name}")

                if program_name == '':
                    program_name = getProgramName(l.lower())
                    if program_name != '':
                        print(f"program name: {program_name}")

                if copybook_name == '':
                    copybook_name = getCopybookName(l.lower())
                    if copybook_name != '':
                        print(f"copybook name: {copybook_name}")

                continue

            bef, aft = fieldNameAndValue(l.strip(), field_and_value_separator)
            if bef in field_value_is_blank or aft in field_value_is_blank:
                continue

            if re.search(patternOccurs, l.lower()):
                input_Occurs = int(get_Occurance(l.strip()))

            elif aft.strip() in ("", "0", "0.0"," ","\n")\
                :
                continue

            if field_is_Standalone == True:
                ret_aft = str(returnRpgStatement(aft,bef)) #mask the field value based on Field Type (date/TimeStamp/Int...)
            if field_is_List == True:
                ret_aft = get_Dimensions(aft)

            # rpg_1_fmt = '{:>12}   {:4}   {:>12}  {:>12}'.format(rpg_1_idx[0],rpg_1_idx[1],rpg_1_idx[2],rpg_1_idx[3])
            sublist = [bef,equal_Sign,ret_aft,end_of_line]
            mainList.append(sublist)

        ## Do this bit dynamically when you get a moment....Get copyBook and Reqhest Handler
        if (program_name == '' and copybook_name != '') or (program_name != '' and copybook_name == '')  :
            program_name, copybook_name = get_CopybookName_or_ProgramName(program_name, copybook_name)
        print(f"program name: {program_name}")
        print(f"copybook name: {copybook_name}")
        apiPgmNm = "ApiPgm('FINENRH': " + "fiRqstNmO: " +  "nenPtrIn: nenPtrOt);"
        copyBook = copybook_name
        requestHandler = request_name
        indentRpg = "         "

        # program_callStatement = getRpgProgramCallStatement(copybook_name, request_name, program_name)
        begSr, call, endSr = getRpgProgramCallStatement(copybook_name, request_name, program_name)
        # print(f"\\\ begSr: \n {begSr}")
        # print(f"\\\ call:  \n {call}")
        # print(f"\\\ endSr: \n {endSr}")

        rpgfile.write('\n')
        rpgfile.write(begSr)
        rpgfile.write('\n\n')

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
                rpgfile.write(indentRpg + str(rpg_new).strip())
                rpgfile.write('\n')

        rpgfile.write('\n')
        rpgfile.write(call)
        rpgfile.write('\n')

        rpgfile.write('\n')
        rpgfile.write(endSr)
        rpgfile.write('\n')

        rpgfile.close()

    print(f"Completed Successfully...Horray!!!!!!")

except Exception as e:
    print("Something went Wrong!!!! Exception.......:  " + str(e))
    # print(str(TracebackException.from_exception(e).stack.format()))
    traceback.print_exc()

quit()