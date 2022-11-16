import requests
import browser_cookie3 #for cookies
import json

def getCookiesFromDomain(domain,cookieName=''):

    Cookies={}
    chromeCookies = list(browser_cookie3.chrome())

    for cookie in chromeCookies:

        if (domain in cookie.domain):
            #print (cookie.name, cookie.domain,cookie.value)
            Cookies[cookie.name]=cookie.value

    if(cookieName!=''):
        try:
            return Cookies[cookieName] #return specified cookie
        except:
            return json.dumps({}) #if exception raised return an empty dictionary
    else:
        return json.dumps(Cookies) #return all cookies or nothing

#print (getCookiesFromDomain("tripadvisor"))

def split_file_by_lines(filename,num_lines):
    # Function returns a list of lists. Each list inside contains num_lines lines
    # the aim of this function is to divide long list in a way to be processed
    # in subgroup without using a lot of memory
    lines=[]

    with open(filename) as file:
        for line in file:
            lines.append(line.rstrip())

    print(f"Number of links in this file is: {len(lines)}")

    lines_splitted=[lines[i:i + num_lines] for i in range(0, len(lines), num_lines)]

    print(f"Original file will be splitted in {len(lines_splitted)} parts")

    return lines_splitted


lines=[]

# with open("hotel_links.txt") as file:
#         for line in file:
#             lines.append(line.rstrip())

# print(f"Il numero di link nel file é: {len(lines)}")

# lines=list(set(lines))

# print(f"Il numero di link nel file ora é: {len(lines)}")

# lista=[1,2,3,4,5,6,7,8,9]

# listagruppi=[lista[i:i + 2] for i in range(0, len(lista), 2)]

# print(listagruppi)