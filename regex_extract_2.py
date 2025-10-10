import re
from datetime import datetime, timedelta, date
import traceback

# inputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/erp_LOADEPCCC_FIEPCRH_Raw.txt'
inputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/'
# inputfile = 'Member_Install_Error_Raw.txt'
inputfile = 'erp_LOADEPCCC_FIEPCRH_Raw.txt'
outputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/'
outputfile = 'RPG_Eval_Statements_'
field_value_Bracket_open = "["
field_value_Bracket_close = "]"
field_and_value_separator = "="
equal_Sign="="
end_of_line=';'

"""
    extracting data from a string, using regex pattern
         Extract  using start position and end position

"""
try:
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

    datefilename = outputpath + outputfile + '_' + inputfile[:-4] + '_' + datefileext
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
    with open(inputpath+inputfile) as f:
        lines = f.readlines()
        #append text file
        rpgfile=open(datefilename, mode='w', encoding='utf-8')
        rpgfile=open(datefilename, mode='a', encoding='utf-8')

        input_Occurs = 0

    request_name = ''
    program_name = ''
    copybook_name = ''

    for index,l in enumerate(lines):
        if l == '\n':
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

    if (program_name == '' and copybook_name != '') or (program_name != '' and copybook_name == '')  :
        program_name, copybook_name = get_CopybookName_or_ProgramName(program_name, copybook_name)
        print(f"program name: {program_name}")
        print(f"copybook name: {copybook_name}")

    indentRpg = "    "
    begSr, call, endSr = getRpgProgramCallStatement(copybook_name, request_name, program_name)
    print(f"\\\ begSr: \n {begSr}")
    print(f"\\\ call:  \n {call}")
    print(f"\\\ endSr: \n {endSr}")

except Exception as e:
    print("Error in getRequestHandler: ", str(e))
    traceback.print_exc()

quit()
