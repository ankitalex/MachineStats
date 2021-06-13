import re

filename=r"C:\Users\user\Downloads\access_log.txt"
with open(filename,"r") as fp:
    # declaring the regex pattern for IP addresses
    fstring=fp.readlines()
    # declaring the regex pattern for IP addresses
    pattern = re.compile('''((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)''')
    InvalidPattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    # initializing the list objects
    valid = list()
    invalid = list()

    # extracting the IP addresses
    for line in fstring:
        line = line.rstrip()
        result = pattern.search(line)
        # valid IP addresses
        try:
            if result:
                valid.append(result.group())
                #valid.add(result.group())

            # invalid IP addresses
            else:
                invalid.append(InvalidPattern.search(line).group())
                #invalid.add(InvalidPattern.search(line).group())
        except Exception:
            None

    # displaying the IP addresses
    valid.sort()
    dict1={}
    for c in valid:
        dict1[c] = valid.count(c)

    #print("Valid IPs")
    #print('*'*20)
    #print(*valid,sep='\n')
    #print('*' * 20)
    #print("Invalid IPs")
    #print('*' * 20)
    #print(*invalid,sep='\n')
    print('*' * 20)

    chargeableList=list()
    for key,value in dict1.items():
        if value>=200:
            chargeableList.append(key)
    print("Chargeable IPs")
    print('*' * 20)
    print(*chargeableList,sep='\n')
    print('*' * 20)
