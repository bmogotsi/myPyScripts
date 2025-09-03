
import re
import unicodedata

inputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/erp_LOADEPCCC_FIEPCRH_Raw.txt'
outputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/'
outputfile = 'RPG_Eval_Statements_FIEPCRH'

try:

    def findOccurence(inStr):
        #date
        pattern      = re.compile(r"Occurs(\s+)?=(\s+)?\[\d+\]", re.IGNORECASE )

        input_str    = inStr.strip()
        if  pattern.findall(input_str) == True:
            return 0 # match found
        else:
            return 1 # match not found
        
    def normalize(line): # 'hello, \tworld! \n'
        """Normalize a line of text and split into two at the tab character"""
        line = unicodedata.normalize("NFKC", line.strip().lower()) # 'hello, \tworld!'
        """Insert a space before or after punctuation (PM) if it is not preceded or followed by a space(\s)"""
        line = re.sub(r"^([^ \w])(?!\s)", r"\1 ", line)    # 'hello, \tworld!' -- START(^) position is a PM and not followed by space (\s) == ins space AFT PM
        line = re.sub(r"(\s[^ \w])(?!\s)", r"\1 ", line)   # 'hello, \t world!'-- ANYWHERE space+PM+"Not space (\s) == ins space aft PM
        line = re.sub(r"(?!\s)([^ \w])$", r" \1", line)    # 'hello, \t world !' -- END($) position is a PM and not preceded by space (\s)== ins space BEF PM
        line = re.sub(r"(?!\s)([^ \w]\s)", r" \1", line)   # 'hello , \t world !'-- ANYWHERE position is a PM and not preceded by space (\s) == ins space BEF PM
        eng, fra = line.split("\t")
        fra = "[start] " + fra + " [end]"
        return eng, fra
        
    def fieldNameAndValue(inStr, inSeperator):
        s= inStr
        c= inSeperator
        i=s.index(c)
        bef = s[:i]
        aft = s[i+1:]
        return bef,aft
    
    seperator = '='
    with open(inputpath, 'r') as fp:
        lines = fp.readlines()
        field_Occur = findOccurence(str(lines).lower())
        for line in lines:
            field_Name, field_Value = fieldNameAndValue(line, seperator)
            if field_Value.endswith("]"):
                field_is_Standalone = True
            elif field_Value.startswith("0)"):
                field_is_List = True
            else: 
                print(f"not a list or standalone: {field_Name} with value: {field_Value}")
                continue
            

            if field_Value.strip("[").strip("]") in ("", "0", "0.0"," "):
                continue
            
            print(line)
            continue
        

    quit()

    #  test = 'hello, hallo, \tworld! \n'
    #  #test = 'Go.	Va !'
    #  text_ret = normalize(test)
    #  quit()


except Exception as e:
    print("Something went Wrong!!!! Exception.......:  " + str(e))

quit()