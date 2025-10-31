# Get a Stored Procedure bbb.Sql
# Extraxt To Db2 SQL Claims Formatted File

""" Flow
    1. open a chosen Stored Procedure file
    2. read the Stored Procedure file line by line
        a. beginning of SQL statement section
            --(begining of line)
            Set @sqltext = '
        b.  get sql statement - convert @sqltext
            -
            -
            -
        c. END of SQL statement section
            -- (begining of line)
            Set @sqltext = '
"""

import re, pathlib
from datetime import datetime, timedelta, date
import traceback
# from traceback import TracebackException

# inputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/erp_LOADEPCCC_FIEPCRH_Raw.txt'
inputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/sql_claims/in_Store_Grp.txt'
outputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/sql_claims/'
outputfile = 'out_Store_Grp'
field_value_Bracket_open = "["
field_value_Bracket_close = "]"
field_and_value_separator = ["=", "]  Value [", " : "]
field_value_is_blank = ["", " ", "0", "null", "",  "0.0","\n"]
equal_Sign="="
end_of_line=';'

keywords_sql = ["SELECT", "FROM", "WHERE", "JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN",
                "ON", "GROUP BY", "ORDER BY", "HAVING", "INSERT INTO", "VALUES",
                "UPDATE", "SET", "DELETE", "CREATE TABLE", "ALTER TABLE",
                "DROP TABLE", "UNION", "UNION ALL", "EXCEPT", "INTERSECT",
                "DISTINCT", "AS", "IN", "IS NULL", "IS NOT NULL", "LIKE",
                "BETWEEN", "AND", "OR", "NOT", "CASE", "WHEN", "THEN", "ELSE",
                "END", "LIMIT", "OFFSET", "DECLARE", "CURSOR", "FOR", "OPEN",
                "FETCH", "CLOSE", "SET", "ELSEIF", "ELSE"
            ]

try:
    def get_where_secureGroups(inputString):
        """ change SecureGroups WHERE
            clause
        """
        secGrp = """
            WHERE (v_grpno = '*' OR grpgrpno = v_grpno)
               AND (p_secure_groups_only = 'n' OR grpgrpno IN (
              SELECT sengrpno FROM FAWDATA.FSGRPSENPF
              ));
            """
        new_change_string = re.sub(r"(grpgrpno)", inputString.strip(), secGrp)
        return new_change_string

    def get_section_middle(midStr):
        """ Check sqlText"""
        if re.findall(r"(Set @sqltext)(\s+)?(=)(\s+)?(')",midStr,re.IGNORECASE):
            return "bengin select..:0" + midStr.strip()

        elif re.findall(r"(Set @sqltext)(\s+)?(=)(\s+)?(Rtrim)",midStr,re.IGNORECASE):
            return "End select..:1" + midStr.strip()

        elif re.findall(r"(Set @sqltext)(\s+)?(=)(\s+)?(Rtrim)",midStr,re.IGNORECASE):
            return "bengin select..:2" + midStr.strip()

        elif re.findall(r"(Set @sqltext)(\s+)?(=)(\s+)?(Rtrim)",midStr,re.IGNORECASE):
            return "bengin select..:3" + midStr.strip()

        elif re.findall(r"(Set @sqltext)(\s+)?(=)(\s+)?(Rtrim)",midStr,re.IGNORECASE):
            return "bengin select..:4" + midStr.strip()

        else:
            return "dont know!!!!!!!!!!!!!!"+ midStr.strip()


    def get_Section_start(line):
        """ get begining of SQL section
            --(begining of line)
            Set @sqltext = '
        """
        global Section_start
        global Section_end
        global Section_mid
        #line=line.strip('\n')
        pattern = re.compile(r"^--\S+") # cannot use '^--\S+$' because there is blanks
        matcher = pattern.findall(line)
        if matcher:
            if Section_start == False:
                Section_start, Section_end, Section_mid = True, False, True
            else:
                Section_start, Section_end, Section_mid = False, True, False

            return  line.strip(), True
        else:
            if Section_start == True:
                line_mid=get_section_middle(line)
                return line_mid, True

        return line.strip(), False

    """
        ################################----------------------------------#################################
        ################################----------------------------------#################################
                                            Main Program
        ################################----------------------------------#################################
        ################################----------------------------------#################################
    """
    # main program starts here
    datenow = datetime.now()
    datestrftime= datenow.strftime('%Y%m%d%h%m')
    datefileext = datestrftime + '.txt'


    # masking
    ## first 2 rows is for masking
    mainList = [["abcdefghkl","=","abcdefghklmnopqrstuvwxyzabcdefghklmnopqrstuvwxyz",";"]]
    sublist = ["12345890","=","1234567890mnopqrstuvwxyz1234567890z",";"]

    mainList.append(sublist)
    print(mainList)


    datefilename = outputpath + outputfile + datefileext
    print(datefilename)

    Section_start = False
    Section_end = False
    Section_mid = False

    """ it all starts here
        1. read stored procedure
        2. loop through text file
        3. extract sql statements
        4. use regEx to extract and change
        5. change to DB2 SQL statements
        6. append DB2 SQL Statements to a text file
    """

    indentSQL = "     "
    stripStr =['updater.inParameters.', '[', ']' ]
    with open(inputpath) as f:
        lines = f.readlines()
        #append text file
        db2File=open(datefilename, mode='w', encoding='utf-8')
        db2File=open(datefilename, mode='a', encoding='utf-8')

        input_Occurs = 0
        request_name = ''
        program_name = ''
        copybook_name = ''

        for index,l in enumerate(lines):
            if l.strip().endswith('=[]]')\
                or '\n' == l.strip() \
                or re.search(re.compile(r"(?<!\w)\d+:\n"), l.lower())\
                or re.search(re.compile(r"(?<!\w)\w+:\s"), l.lower()) :  # skip blank/zeros or empty field values
                    continue

            if l.strip() == '\n':
                continue
            if l.strip() == '':
                continue

            newComment, tfFound = get_Section_start(l)
            ## add to list
            if tfFound == True:
                sublist = [newComment]
                mainList.append(sublist)
                db2File.write('\n')
                if Section_mid:
                   continue
                if Section_start:
                    sublist = ['-- S T A R T S   H E R E']
                    mainList.append(sublist)
                if Section_end:
                    sublist = ['-- E N D S   H E R E']
                    mainList.append(sublist)


    db2File.write('\n')
    db2File.write("-- ================================== S T A R T S   H E R E ============================")
    db2File.write('\n\n')

    ## do all
    if mainList[2] != []:

        items=mainList
        for rowIdx,item in enumerate(items): # rows
            if rowIdx < 2: # ignore first two rows (masking)
                continue

            db2File.write(indentSQL + str(item).strip().strip("[").strip("]").strip("'"))
            db2File.write('\n')

    print(f"Completed Successfully...Horray!!!!!!")
    db2File.write('\n')
    db2File.write("-- ================================== E N D S    H E R E ============================")
    db2File.close()

except Exception as e:
    print("Something went Wrong!!!! Exception.......:  " + str(e))
    # print(str(TracebackException.from_exception(e).stack.format()))
    traceback.print_exc()

quit()
