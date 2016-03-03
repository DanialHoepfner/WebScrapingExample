import os
os.chdir('SET CURRENT DIRECTORY')
#%% Step 1 open, scrape and save to an numpy array
#%% Step 1 open, scrape and save to an numpy array
#%% Step 1 open, scrape and save to an numpy array
#%% Step 1 open, scrape and save to an numpy array
import urllib2
import re
from cookielib import CookieJar
from bs4 import BeautifulSoup
import sys
import numpy as n
numlist=list()
count=0
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
home = opener.open('http://esango.un.org/civilsociety/withOutLogin.do?method=getFieldsOfActivityCode&orgByFieldOfActivityCode=3&orgByFieldOfActivityName=Gender%20Issues%20and%20Advancement%20of%20Women&sessionCheck=false&ngoFlag=')
fhand = opener.open('http://esango.un.org/civilsociety/displayConsultativeStatusSearch.do?method=list&show=9676&from=list&col=&order=&searchType=&index=0') #Note that the show=9676, so all urls are on 1 page
soup = BeautifulSoup(fhand)
tags = soup('a')
for tag in tags:
    line=tag.get('href', None)    
    if line.startswith('showProfileDetail'):
        num=re.findall('=[0-9.]+',line) # each page has 6 digit code, pulls that code 
        numlist.append(num)
        count=count+1
# List saved as numlist has all of the codes for urls for each organization page
#Scraping the information
sys.setrecursionlimit(1000000) #Probably unnecessary for example coded, higher limited needed to scrape full datset.
j=list(range(101,9675,100)) #Information collected in blocks of 100 to keep website from signing out program and in case of issues with particular blocks
j2=list(range(200,9675,100)) # j is lower limit, j2 upper limit
for d in range(5,8): #iterates through the start and stop blocks defined above, small sample here only for example
    x=['orgnum','org', 'abr', 'add', 'web', 'orgtype', 'langs', 'area', 'scope', 'cntrys', 'mdgs', 'yrest', 'yreg', 'mems', 'aff', 'fund'] 
    data=n.array(x)    #variables above transformed in numpy array
    cj = CookieJar() #Stored seemingly empty login data, also why program cycles through fhand(two lines down) at each iteration, whereas fhand2 holds data
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    fhand = opener.open('http://esango.un.org/civilsociety/withOutLogin.do?method=getFieldsOfActivityCode&orgByFieldOfActivityCode=3&orgByFieldOfActivityName=Gender%20Issues%20and%20Advancement%20of%20Women&sessionCheck=false&ngoFlag=')
    tags = soup('a') 
    for i in range(j[d],j2[d]):
            url='http://esango.un.org/civilsociety/showProfileDetail.do?method=printProfile&tab=1&profileCode'+str(numlist[i][0])
            fhand2 = opener.open(url)
            soup = BeautifulSoup(fhand2)
            try: #each of these try/except picks out the desired information, or sets as missing and prints a note if not found.
                org=soup.find("td", text="Organization's name:").next_sibling.next_sibling.contents
            except: #Missing data does not result from errors, but organizations that did not fill in that data
                org='XZX'
                print 'MISSING: org'
            try:
                abr=soup.find("td", text="Organization's acronym:").next_sibling.next_sibling.contents
            except: 
                abr='XZX'
                print 'MISSING: abr for '+org[0]
            try: 
                add=soup.find("td", text="Address: ").next_sibling.next_sibling.contents
            except: 
               add='XZX'
               print 'MISSING: add for '+org[0]
            try:
                web=soup.find("td", text="Web site:  ").next_sibling.next_sibling.contents
            except: 
                web='XZX'
                print 'MISSING: web for '+org[0]
            try:        
                orgtype=soup.find("td", text="Organization type:").next_sibling.next_sibling.contents
            except: 
                orgtype='XZX'
                print 'MISSING: orgtype for '+org[0]
            try:        
                langs=soup.find("td", text=re.compile("Languages:*")).next_sibling.next_sibling.contents
            except: 
                langs='XZX'
                print 'MISSING: langs for '+org[0]
            try:
                area=soup.find("h3", text="Activities").find_next("td").next_sibling.next_sibling.contents
            except:
                area='XZX'
                print 'MISSING: area for '+org[0]
            try:
                scope=soup.find("td", text=re.compile("Geographic scope:")).next_sibling.next_sibling.contents
            except: 
                scope='XZX'
                print 'MISSING: scope for '+org[0]
            try:
                cntrys=soup.find("td", text=re.compile("Country / Geographical area of activity:")).next_sibling.next_sibling.contents
                cntrys[1]=unicode(str(cntrys[1]), errors='ignore')
            except: 
                cntrys='XZX'
                print 'MISSING: cntrys for '+org[0]
            try:
                mdgs=soup.find("td", text=re.compile("Millennium Development Goals:")).next_sibling.next_sibling.contents
            except: 
                mdgs='XZX'
                print 'MISSING: mdgs for '+org[0]
            try:
                yrest=soup.find("td", text=re.compile("Year established*")).next_sibling.next_sibling.contents
            except: 
                yrest='XZX'
                print 'MISSING: yrest for '+org[0]
            try:
                yreg=soup.find("td", text=re.compile("Year of registration*")).next_sibling.next_sibling.contents
            except: 
                yreg='XZX'
                print 'MISSING: yreg for '+org[0]
            try:
                mems=soup.find("td", text=re.compile("Number and type of members*")).next_sibling.next_sibling.contents
            except: 
                mems='XZX'
                print 'MISSING: mems for '+org[0]
            try:
                aff=soup.find("td", text=re.compile("Affiliation with NGO networks*")).next_sibling.next_sibling.contents
            except: 
                aff='XZX'
                print 'MISSING: aff for '+org[0]
            try:
                fund=soup.find("td", text=re.compile("Funding structure:*")).next_sibling.next_sibling.contents
            except: 
                fund='XZX'
                print 'MISSING: fund for '+org[0]
            y=[numlist[i], org, abr, add, web, orgtype, langs, area, scope, cntrys, mdgs, yrest, yreg, mems, aff, fund]
            data=n.vstack((data,y)) # appends each pages' information to the slice
    svcode=(d+1)
    print svcode ##See iteration number
    n.save('array'+str(svcode), data) # Save slice of data
# Combining stacks into full dataset
data=n.load('array6.npy')
for i in range(7,9):
    array= 'array'+str(i)+'.npy'
    toappend=n.load(array)
    toappend=toappend[1:] # Removes first row, which is variable names, in all but first slice
    data=n.vstack((data,toappend))
n.save('fullset', data)
#%%Step 2 Cleaning the data
#%%Step 2 Cleaning the data
#%%Step 2 Cleaning the data
#%%Step 2 Cleaning the data
import numpy as n
import re

data=n.load('fullset.npy')
# Column 1 Removing from list and converting to interger(Org Number)
for i in range(1,298):
    data[i,0]=data[i,0][0][1:]
    data[i,0]=int(data[i,0])
print "Example: "+str(data[30,00])+" Type: "+str(type(data[30,0]))

# Column 2: Removing from orgname list
for i in range(1,298):
    if type(data[i,1])==list:
        data[i,1]=unicode(data[i,1][0])
    else: #In case some cells were not a list, though most were
        print i        
        print str(data[i,1])+' Not a list'
        print type(data[i,1])
print "Example: "+str(data[30,1])+" Type: "+str(type(data[30,1]))
# Column 3: Removing string and unicode from lists(Org Abbrevation)
for i in range(1,298):
    if type(data[i,2])==list:
        data[i,2]=unicode(data[i,2][0])
    else:
        print unicode(data[i,1])+' Not a list'
        print type(data[i,1])
        print i       
# Looks good, only unicode and strings and missing code intact.
for i in range(0,298):
    if type(data[i,2])!=str and type(data[i,2])!=unicode: # Confirms all items are unicode or strings
        print unicode(data[i,1])
        print type(data[i,1])
        print i 
#Working on Column 4(Address)
# Addresses come in lists of length 3 5 or 7
numlist=list() 
for i in range(1,298):
    if type(data[i,3])==list:
        length=str(len(data[i,3]))        
        if length in numlist: continue
        else:
            numlist.append(length)
print numlist
# Elements 1, 3 and 5 are always just a line break and can be deleted.
for i in range(1,298):
    if type(data[i,3])==list:
        if len(data[i,3])==3:
            if str(data[i,3][1])!='<br/>': #Removes item 1 if length 3, items 1 and 3 if length is 5 and 1, 3 and 5 if lenth is 7
                print i 
                print data[i,3][1]
        elif len(data[i,3])==5:
            if str(data[i,3][1])!='<br/>' or str(data[i,3][3])!='<br/>':
                print i 
                print data[i,3][1]
                print data[i,3][3]
        elif len(data[i,3])==7:
            if str(data[i,3][1])!='<br/>' or str(data[i,3][3])!='<br/>'or str(data[i,3][5])!='<br/>':
                print i 
                print data[i,3][1]
                print data[i,3][3]
                print data[i,3][5]
#Remove nonsystematic brs                
for i in range(1,298):
    if type(data[i,3])==list:
        brc=0
        for j in range(len(data[i,3])-1):
            data[i,3][j]=unicode(data[i,3][j])
            if data[i,3][j]==('<br/>'):
                brc=brc+1
        for k in xrange(brc):
            data[i,3].remove('<br/>')
for i in range(1,298):
    if type(data[i,3])!=list and data[i,3]!='XZX':
        print i
        print data[i,3]                
#No non-missing or proper type observations

#Removes other formatting 
for i in range(1,298):
    if type(data[i,3])==list:
        for j in range(len(data[i,3])): 
            data[i,3][j]=re.sub(u'\\n', u'', data[i,3][j])
            data[i,3][j]=re.sub(u'\\t', u'', data[i,3][j])
            

#Creating new variable, country the organization is headquartered in
headq=n.array('headq',ndmin=2, dtype='object_')
for i in range(1,298):
    if type(data[i,3])==list:
        headq=n.append(headq, data[i,3][len(data[i,3])-1])
    else:
        headq=n.append(headq, 'XZX')
#Only 1 missing case for this. 

#Confirms the countries were properly coded        
for i in range(1,298):
    print "CASE NUMBER"+str(i)    
    if type(data[i,3])==list:
        print data[i,3][len(data[i,3])-1]
    else:
        print data[i,3]
    print headq[i]
#New variable appended to data
headq=n.expand_dims(headq,axis=1)
data=n.hstack((data,headq))

#Condensing address to unicode from list
for i in range(1,298):
    if type(data[i,3])==list:
            if len(data[i,3])==2:
                data[i,3]=unicode(data[i,3][0])+unicode(data[i,3][1])
            if len(data[i,3])==3:
                data[i,3]=unicode(data[i,3][0])+unicode(data[i,3][1])+unicode(data[i,3][2])
            if len(data[i,3])==4:
                data[i,3]=unicode(data[i,3][0])+unicode(data[i,3][1])+unicode(data[i,3][2])+unicode(data[i,3][3])
    else:
        data[i,3]=unicode('XZX')

#Addressses successsfully condensed
# Column 5 recoding lists to unicode(Website)
print data[1,4]
numlist=list() 
for i in range(1,298):
    if type(data[i,4])==list:
        length=str(len(data[i,4]))        
        if length in numlist: continue
        else:
            numlist.append(length)
print numlist
#All lists are single item
#Recoding to unicode
for i in range(1,298):
    if type(data[i,4])==list:
            data[i,4]=unicode(data[i,4][0])
    else:
        print data[i,4] #Only missing values not unicode      
#Column 6 Organizational type
print data[1,5]    
numlist=list() 
for i in range(1,298):
    if type(data[i,5])==list:
        length=str(len(data[i,5]))        
        if length in numlist: continue
        else:
            numlist.append(length)
print numlist
#Also all lists of length 1, Converting to unicode
for i in range(1,298):
    if type(data[i,5])==list:
            data[i,5]=unicode(data[i,5][0])
    else:
        if data[1,5]!='XZX':
            print i        
            print data[i,5]
        data[i,5]=unicode('XZX')    
#Column 7 Too many languages to create indicator for each preserving column and adding a langauge count 
numlist=list() 
for i in range(1,298):
    if type(data[i,6])==list:
        length=str(len(data[i,6]))        
        if length in numlist: continue
        else:
            numlist.append(length)
print numlist
# all three long list, probably all w/ center item as only needed one. 
#Removing Formatting                
for i in range(1,298):
    if type(data[i,6])==list:
        brc=0
        for j in range(len(data[i,6])):
            data[i,6][j]=unicode(data[i,6][j])
            if data[i,6][j]==('\n'):
                brc=brc+1
        for k in xrange(brc):
            data[i,6].remove('\n')
    
#Formatting removed
for i in range(1,298):
    if type(data[i,6])==list:
            data[i,6]=unicode(data[i,6][0])
    else:
        if data[1,6]!='XZX':
            print i        
            print data[i,6]
        data[i,6]=unicode('XZX')    
#Creating count of number of languages used in each organization
langct=n.array('langct',ndmin=2, dtype='object_')
wlist=[]
for i in range(1,298):
    delimter='<br/>'
    count=0
    data[i,6]=re.sub(u'<li>', u'', data[i,6])
    data[i,6]=re.sub(u'</li>', u'', data[i,6])
    data[i,6]=re.sub(u'<ul>', u'', data[i,6])
    data[i,6]=re.sub(u'</ul>', u'', data[i,6])    
    ls=data[i,6].split(delimter)
    for words in ls:
        count=count+1
        if words in wlist:continue
        else:
            wlist.append(words)
    if count>0:
        langct=n.append(langct, (count-1))
    else:
        langct=n.append(langct, 'XZX')        
print wlist


#Adding to data
langct=n.expand_dims(langct,axis=1)
data=n.hstack((data,langct))
# Cleaning up preserved list of languanges 
for i in range(1,298):
    data[i,6]=re.sub(u'<br/>', u',', data[i,6])
    print data[i,6]
#Column 8  lists of activities
# Removing all of the \n list items
for i in range(1,298):
    if type(data[i,7])==list:
        brc=0
        for j in range(len(data[i,7])):
            data[i,7][j]=unicode(data[i,7][j])
            if data[i,7][j]==('\n'):
                brc=brc+1
        for k in xrange(brc):
            data[i,7].remove('\n')

# Removing all of the \n\t\tetc list items
for i in range(1,298):
    if type(data[i,7])==list:
        brc=0
        for j in range(len(data[i,7])):
            data[i,7][j]=unicode(data[i,7][j])
            if data[i,7][j]==(':\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t'):
                brc=brc+1
        for k in xrange(brc):
            data[i,7].remove(':\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')            
            
# Removing all of the <br/> list items
for i in range(1,298):
    if type(data[i,7])==list:
        brc=0
        for j in range(len(data[i,7])):
            data[i,7][j]=unicode(data[i,7][j])
            if data[i,7][j]==('<br/>'):
                brc=brc+1
        for k in xrange(brc):
            data[i,7].remove('<br/>')

#Condenses list into major and minor areas of activity, saved as unicode, and a count of each 
genactct=n.array('genactct',ndmin=2, dtype='object_')
specactct=n.array('specactct',ndmin=2, dtype='object_')
garea=n.array('garea',ndmin=2, dtype='object_')
sarea=n.array('sarea',ndmin=2, dtype='object_')
glist=[]
slist=[]
for i in range(1,298):
    if type(data[i,7])==list: 
        gcount=0
        scount=0
        gar=unicode('')
        sar=unicode('')
        #print 'Interation Number: '+str(i)
        for li in range(len(data[i,7])):
            #print 'Interation Number: '+str(i)+'List Item: '+str(li)
            if data[i,7][li].startswith('<b>'): #Counts major areas of activity and stores 
                gcount=gcount+1
                gar=gar+', '+data[i,7][li][3:-4]
                if data[i,7][li][3:-4] in glist: continue
                else:
                    glist.append(data[i,7][li][3:-4])
            if data[i,7][li].startswith('<li>'): #Counts minor areas of activity and stores
                scount=scount+1
                sar=sar+', '+data[i,7][li][4:-6]
                if data[i,7][li][4:-6] in slist: continue
                else:
                    slist.append(data[i,7][li][4:-6])
        genactct=n.append(genactct, gcount)
        specactct=n.append(specactct, scount)
        garea=n.append(garea, gar)
        sarea=n.append(sarea, sar)
    else:     
        genactct=n.append(genactct, 'XZX')
        specactct=n.append(specactct, 'XZX')
        garea=n.append(garea, 'XZX')
        sarea=n.append(sarea, 'XZX')

#sorting lists
glist.sort()
slist.sort()
# Appending new variables to data
garea=n.expand_dims(garea,axis=1)
data=n.hstack((data,garea))
genactct=n.expand_dims(genactct,axis=1)
data=n.hstack((data,genactct))
sarea=n.expand_dims(sarea,axis=1)
data=n.hstack((data,sarea))
specactct=n.expand_dims(specactct,axis=1)
data=n.hstack((data,specactct))
#Column 9 Scope of operation 

#Removing \ns
for i in range(1,298):
    if type(data[i,8])==list:
        brc=0
        for j in range(len(data[i,8])):
            data[i,8][j]=unicode(data[i,8][j])
            if data[i,8][j]==('\n'):
                brc=brc+1
        for k in xrange(brc):
            data[i,8].remove('\n')
#Removing brs
for i in range(1,298):
    if type(data[i,8])==list:
        brc=0
        for j in range(len(data[i,8])):
            data[i,8][j]=unicode(data[i,8][j])
            if data[i,8][j]==('<br/>'):
                brc=brc+1
        for k in xrange(brc):
            data[i,8].remove('<br/>')
#Removing other formatting
for i in range(1,298):
    if type(data[i,8])==list:
        for j in range(len(data[i,8])):
            data[i,8][j]=re.sub(u'<li>', u'', data[i,8][j])
            data[i,8][j]=re.sub(u'</li>', u'', data[i,8][j])
            data[i,8][j]=re.sub(u'<ul>', u'', data[i,8][j])
            data[i,8][j]=re.sub(u'</ul>', u'', data[i,8][j])
            data[i,8][j]=re.sub(u'\n', u'', data[i,8][j])
            data[i,8][j]=re.sub(u'\t', u'', data[i,8][j])

# Organizations with Regional scope list the regions, otherwise left blank
#Captures the listed regions in a separate variable and appends it to the data
region=n.array('region',ndmin=2, dtype='object_')            
for i in range(1,298):
    if type(data[i,8])==list:
        if len(data[i,8])==2:
            region=n.append(region, data[i,8][1])
        else:
            region=n.append(region, u'NA')
    else: 
        region=n.append(region, u'XZX')
region=n.expand_dims(region,axis=1)
data=n.hstack((data,region))

# Removes the list of regions from original column leaving only a nominal scope
for i in range(1,298):
    if type(data[i,8])==list:
        data[i,8]=data[i,8][0]
    print data[i,8]
# Column 10 list of countries organization is active in
#Removing Formatting
for i in range(1,298):
    if type(data[i,9])==list:
        brc=0
        for j in range(len(data[i,9])):
            data[i,9][j]=unicode(data[i,9][j])
            if data[i,9][j]==('\n'):
                brc=brc+1
        for k in xrange(brc):
            data[i,9].remove('\n')
#Delistifying column
for i in range(1,298):
    if type(data[i,9])==list:
        data[i,9]=unicode(data[i,9][0])            
#
for i in range(1,298):
    print i
    data[i,9]=re.sub(u'<li>', u'', data[i,9])
    data[i,9]=re.sub(u'<ul>', u'', data[i,9])
    data[i,9]=re.sub(u'</ul>', u'', data[i,9])
    data[i,9]=re.sub(u'</li>', u',', data[i,9])
#
type(data[2,9])    
# Generating number of countries and country list population
nctry=n.array('nctry',ndmin=2, dtype='object_')
wlist=[]
for i in range(1,298):
    delimter=','
    count=0
    ls=data[i,9].split(delimter)
    for words in ls:
        count=count+1
        if words[1:] in wlist: continue
        else:
            wlist.append(words[1:])
    if count>0:
        nctry=n.append(nctry, (count-1))
    else:
        nctry=n.append(nctry, 'XZX')        
wlist.sort()
wlist.remove('ZX') # Missing variable notation caught in wordlist for countries, removed
wlist.remove('')
#Appending number of countries organization is operating in
nctry=n.expand_dims(nctry,axis=1)
data=n.hstack((data,nctry))
#Creates wlist2 which is list of arrays with indicator variables for each country
wlist2=list(wlist)
for c in range(0,len(wlist)):
    wlist2[c]=n.array(str(wlist[c]),ndmin=2, dtype='object_')
for i in range(1,298):
    for c in range(0,len(wlist)):
         if re.search(str(wlist[c]), data[i,9]):
             wlist2[c]=n.append(wlist2[c], 1)
         else:
             wlist2[c]=n.append(wlist2[c], 0)
#Appends that list of arrays to data
for c in range(0,len(wlist)):
    wlist2[c]=n.expand_dims(wlist2[c],axis=1)
    data=n.hstack((data,wlist2[c]))

#Column 11 Millenium Development Goals
#Removing formatting
for i in range(1,298):
    if type(data[i,10]) is list: 
        data[i,10].remove('\n')
        data[i,10].remove('\n')
    else: continue    
# Converting from list to string
for i in range(1,298): 
    if type(data[i,10]) is list:
        data[i,10]=str(data[i,10])
#Removing more formatting
for i in range(1,298):
    data[i,10]=re.sub('<li>', '', data[i,10])
    data[i,10]=re.sub('<ul>', '', data[i,10])
    data[i,10]=re.sub('</ul>', '', data[i,10])
    data[i,10]=re.sub('</li>', ',', data[i,10])
#List of goals
delimiter=','
wlist=list()    
for i in range(1,298): 
    ls=data[i,10].split(delimter)
    for words in ls:
        count=count+1
        if words[1:] in wlist: continue
        else:
            wlist.append(words[1:])
#print wlist
wlist.remove('ZX')
wlist.remove('n]')
#Removing more formatting
for i in range(len(wlist)):
    wlist[i]=re.sub('^n', '', wlist[i]) 
    wlist[i]=re.sub('\\\\n', '', wlist[i])
#Creating a list of arrays for millenium development goals to append indicator variables for each

wlist2=list(wlist)
for c in range(0,len(wlist)):
    wlist2[c]=n.array(str(wlist[c]),ndmin=2, dtype='object_')
for i in range(1,298):
    for c in range(0,len(wlist)):
         if re.search(str(wlist[c]), data[i,10]):
             wlist2[c]=n.append(wlist2[c], 1)
         else:
             wlist2[c]=n.append(wlist2[c], 0)

#Appending to data
for c in range(0,15):
    wlist2[c]=n.expand_dims(wlist2[c],axis=1)
    data=n.hstack((data,wlist2[c]))


#Column 12 year organization was established
#converting to interger
for i in range(1,298):
    if type(data[i,11]) is list: 
        data[i,11]=int(data[i,11][0])
    else: continue

# Column 13 number of years organization has been on register
#converting to interger
for i in range(1,298):
    if type(data[i,12]) is list: 
        data[i,12]=int(data[i,12][0])
    else: continue  

# Column 14 members, too many types of information to do much with except make a string
for i in range(1,298):
    if type(data[i,13]) is list: 
        data[i,13]=unicode(data[i,13][0])
    else: continue
# Column 15 Affiliation, once again a wide variety of responses in the column
for i in range(1,298):
    if type(data[i,14]) is list: 
        data[i,14]=unicode(data[i,14][0])
    else: continue
#Column 16 Funding
for i in range(1,298):
    if type(data[i,15]) is list and len(data[i,15])>1:
        print data[i,15]
#Removing \n list items
for i in range(1,298):
    if type(data[i,15])==list:
        brc=0
        for j in range(len(data[i,15])):
            data[i,15][j]=unicode(data[i,15][j])
            if data[i,15][j]==(u'\n'):
                brc=brc+1
        for k in xrange(brc):
            data[i,15].remove(u'\n')
# Converting from list to string
for i in range(1,298): 
    if type(data[i,15]) is list:
        data[i,15]=str(data[i,15])#%%#Removing more formatting
for i in range(1,298):
    data[i,15]=re.sub('<li>', '', data[i,15])
    data[i,15]=re.sub('<ul>', '', data[i,15])
    data[i,15]=re.sub('</ul>', '', data[i,15])
    data[i,15]=re.sub('</li>', ',', data[i,15])
    data[i,15]=re.sub('<br/>', ',', data[i,15])
    data[i,15]=re.sub('\\n', ',', data[i,15])
    

#List of goals
delimiter=','
wlist=list()    
for i in range(1,298): 
    ls=data[i,15].split(delimter)
    for words in ls:
        count=count+1
        if words[1:] in wlist: continue
        else:
            wlist.append(words[1:])
wlist.remove('ZX')
wlist.remove('n\']')
#Removing more formatting
for i in range(len(wlist)):
    wlist[i]=re.sub('^n', '', wlist[i]) 
    wlist[i]=re.sub('\\\\n', '', wlist[i])
    wlist[i]=re.sub(']', '', wlist[i])
#Creating indicator variables    
wlist2=list(wlist)
for c in range(0,len(wlist)):
    wlist2[c]=n.array(str(wlist[c]),ndmin=2, dtype='object_')
for i in range(1,298):
    for c in range(0,len(wlist)):
         if re.search(str(wlist[c]), data[i,10]):
             wlist2[c]=n.append(wlist2[c], 1)
         else:
             wlist2[c]=n.append(wlist2[c], 0)

#Appending to data
for c in range(0,24):
    wlist2[c]=n.expand_dims(wlist2[c],axis=1)
    data=n.hstack((data,wlist2[c]))    
n.save('fullsetclean', data)    
#%%Some simple descriptives from the data
#%%Some simple descriptives from the data
#%%Some simple descriptives from the data
#%%Some simple descriptives from the data    
data=n.load('fullsetclean.npy')
#Percentage of groups that work on participation
import re
import numpy as n
delimiter=','
count=0
partc=0
for i in range(1,298): 
    if re.search('Gender Issues and Advancement of Women', data[i,18]):
                    count+=1                    
                    if re.search('participation', data[i,20]):
                        partc+=1
aver=float(partc)/float(count)
print "Count: "+str(partc)
print "Proportion: "+str(aver) 
print "It Looks like about 15 percent of groups working on the advancement of women encourage participation as an activity"
#Percentage of groups that work on outreach
delimiter=','
count=0
partc=0
for i in range(1,298): 
    if re.search('Gender Issues and Advancement of Women', data[i,18]):
                    count+=1                    
                    if re.search('outreach', data[i,20]):
                        partc+=1
aver=float(partc)/float(count)
print "Count: "+str(partc)
print "Proportion: "+str(aver) 
print "A considerable 56 percent of groups working on the advancement of women work on outreach as an activity"

#Percentage of groups in Nigeria that work on outreach
delimiter=','
count=0
partc=0
for i in range(1,298): 
    if re.search('Gender Issues and Advancement of Women', data[i,18]):
        if  re.search('Nigeria', data[i,16]) or re.search('Chile', data[i,16]) or re.search('Uganda', data[i,16]): 
            count+=1                    
            if re.search('outreach', data[i,20]):
                partc+=1
aver=float(partc)/float(count)
print "Count: "+str(partc)
print "Proportion: "+str(aver) 
print "86 percent of groups working on the advancement of women in Nigeria Chile and Uganda(for example) work on outreach as an activity"


