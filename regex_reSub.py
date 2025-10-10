
import re
import unicodedata
try:
    inputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/erp_LOADEPCCC_FIEPCRH_Raw.txt'
    outputpath = 'C:/Users/Ben.Mogotsi/Downloads/delete_/srcmbr/'
    outputfile = 'RPG_Eval_Statements_FIEPCRH'

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

    test = 'hello, hallo, \tworld! \n'
    #test = 'Go.	Va !'
    text_ret = normalize(test)
    quit()

    if 1 ==2:
        text_file = "fra.txt"
        with open(text_file) as fp:
            text_pairs = [normalize(line) for line in fp]

except Exception as e:
    print("Something went Wrong!!!! Exception.......:  " + str(e))

quit()