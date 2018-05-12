
# coding: utf-8

# In[ ]:


from urllib.request import urlopen as uo
from urllib.parse import urlencode
from xml.etree import ElementTree as et

parliaments = et.parse(uo("https://www.abgeordnetenwatch.de/api/parliaments.xml"))

#traverse parliaments
for parliament in parliaments.findall("parliament"):
    
    #restrict to Bundestag, maybe add more alter
    if (parliament.findall("name")[0].text == "Bundestag"):
        parliamentName=parliament.findall("name")[0].text
        print(parliamentName)
        
        parliamentCandidatesUrl=parliamentName=parliament.findall("datasets/deputies/by-name")[0].text
        
        print(parliamentCandidatesUrl)
        #sample document: https://www.abgeordnetenwatch.de/api/parliament/bundestag/deputies.xml
        candidates = et.parse(uo(parliamentCandidatesUrl))


        #traverse canditades
        for candidate in candidates.findall("profile"):
            firstName= candidate.findall("personal/first_name")[0].text
            lastName= candidate.findall("personal/last_name")[0].text
            
            
            print(firstName+" "+lastName)
            
            #build the query string for the wiki api
            payload = {"action":"query","titles":"{firstName} {lastName}".format(firstName=firstName, lastName=lastName),"prop":"revisions","rvprop":"content","format":"xml"}
            encodedPayload = urlencode(payload)
            
            #we take the german wikipedia api
            wikiUrl="https://de.wikipedia.org/w/api.php?{encodedPayload}".format(encodedPayload=encodedPayload)
            
            print(wikiUrl)
            
            #parse the wiki api page
            #example document with a page: https://en.wikipedia.org/w/api.php?action=query&titles=Angela%20Merkel&prop=revisions&rvprop=content&format=xml&formatversion=2
            #example document with NO page: https://en.wikipedia.org/w/api.php?action=query&titles=Angela%20Musterman&prop=revisions&rvprop=content&format=xml&formatversion=2
            wiki = et.parse(uo(wikiUrl))

            page= wiki.findall("query/pages/page")[0]
            pageId=page.attrib["_idx"]
            #if _idx attribute is -1 than there is no page
            print(pageId)

