
import re
import unicodedata
import traceback

try:
    inputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/sample_regex_extract.txt'
    outputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/'
    outputfile = 'RPG_Eval_Statements_FIEPCRH'

    field_value_Bracket_open = "["
    field_value_Bracket_close = "]"
    field_and_value_separator = ["=", "]  Value [", " : "]
    field_value_is_blank = ["", " ", "0", "null", "",  "0.0","\n"]
    equal_Sign="="
    end_of_line=';'


    def get_is_Standalone(inStr):
        patternStandalone = re.compile(r"(\s+)?=(\s+)?\[(\w+)\]")
        patternStandalone2 = re.compile(r"\](\s+)?Value(\s+)?\[\w+\]")
        if re.search(patternStandalone, inStr, re.IGNORECASE): # Case-sensitive by default
            field_is_Standalone = True # occurs=[10]
            return field_is_Standalone
        elif re.search(patternStandalone2, inStr, re.IGNORECASE):
            return field_is_Standalone
        else:
            field_is_Standalone = False
            return field_is_Standalone

    def get_is_List(inStr):
        patternList = re.compile(r"(\w+)(\s+)?=(\s+)?0\)")
        patternList2 = re.compile(r"\](\s+)?value(\s+)?\[\[\w+\]\]")
        if re.search(patternList, inStr, re.IGNORECASE): # Case-sensitive by default
            field_is_List = True
            return field_is_List
        elif re.search(patternList2, inStr, re.IGNORECASE):
            field_is_List = True
            return field_is_List
        else:
            field_is_List = False
            return field_is_List

    def get_Field_Value(inStr):
        before, after = '', ''

        for i,sep in enumerate(field_and_value_separator):
            if sep in inStr:
                before = inStr.split(sep)[0].strip() # field name
                after = inStr.split(sep)[1].strip() # field value
                break

        return before, after

    def get_Dimensions(inStringline):
        before, after = '', ''

        for i,sep in enumerate(field_and_value_separator):
            if sep in inStringline:
                before = inStringline.split(sep)[0].strip() # field name
                after = inStringline.split(sep)[1].strip() # field value
                break

        return before, after

    def get_field_is_Standalone_is_List(inStringline):
        alone, list =False, False
        before, after = '', ''

        alone = get_is_Standalone(inStringline)
        if alone == True:
            before, after = get_Field_Value(inStringline)

        list = get_is_List(inStringline)
        if list == True:
            before, after = get_Field_Value(inStringline)

        return alone, list, after, before

    def returnRpgStatement(inStr, fieldName):
        return "'"  + inStr.strip() + "'"

    """
    do all lines
    """
    if 1 ==1:
        text_file = inputpath
        with open(text_file) as fp:
            lines = fp.readlines()


            for index,l in enumerate(lines):
                field_is_Standalone = False
                field_is_List = False
                field_is_Standalone, field_is_List, aft, bef = get_field_is_Standalone_is_List(l)

                if field_is_Standalone == True:
                    ret_aft = str(returnRpgStatement(aft,bef)) #mask the field value based on Field Type (date/TimeStamp/Int...)
                if field_is_List == True:
                    ret_aft = get_Dimensions(aft)

except Exception as e:
    print("Something went Wrong!!!! Exception.......:  " + str(e))
    traceback.print_exc

quit()