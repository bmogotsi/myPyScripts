import re

try:
    text = "Hello world, hello Python."
    a,b = 0,2
    if a <= b:
        pattern = re.compile(r"occurs(\s+)?=(\s+)?\[\d+\]")

        text = """  lEpcPty =[]]
              lEpcDepNo =[]]
              lEpcCancelNo =[]]
              kEpcOccurs =[12345987]
              kEpcGrpNo =[FTD]
              kEpcPerNo =[3320503]
              """

        # text = "abc kEpcOccurs =[1] xyz"

        # Using re.match()
        match_hello_start = re.match(pattern, text.lower())
        print(f"re.match({pattern}, text): {match_hello_start.group() if match_hello_start else None}")

        # Using re.search() -
        #     returns first match
        #     Returns None if no match found

        search_hello = re.search(pattern, text.lower()) # Case-sensitive by default
        search = search_hello.group()
        search1= search_hello.group(1)
        search2= search_hello.group(2)
        print(f"re.search({pattern}, text): {search_hello.group() if search_hello else None}")

        if search_hello != None:
            # get value
            returnStr = search_hello.group()
            return_Occurs = returnStr.split("=")[1].strip("[").strip("]")
            print(f"The decimal value of the 'occurs' is: {return_Occurs}")
        else:
            returnStr = "No match found"

    else:

        # Using re.match()
        match_hello_start = re.match(r"Hello", text)
        print(f"re.match('Hello', text): {match_hello_start.group() if match_hello_start else None}")

        match_python_start = re.match(r"Python", text)
        print(f"re.match('Python', text): {match_python_start.group() if match_python_start else None}")

        # Using re.search()
        search_hello = re.search(r"hello", text) # Case-sensitive by default
        print(f"re.search('hello', text): {search_hello.group() if search_hello else None}")

        search_python = re.search(r"Python", text)
        print(f"re.search('Python', text): {search_python.group() if search_python else None}")

except Exception as e:
    print(f"Something went wrong...:   {str(e)}")

quit()