
#Pubchem: https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest

import json
import re
import periodictable
import requests



def Pubchem_search(chemical_name):
    """Search using names"""

    base_url= f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{chemical_name}/record/JSON?callback=pubchem_callback"
    print(base_url)
    searched_results=[]
    res = requests.get(base_url, params=dict(page_limit=10)).json()
    
    print(res)
    if res ==[]:
         NameError: "Wrong query parameters have been entered"
    try:
        for entry in res["data"]:
            attrs = entry["attributes"]
            item = {
                "keyword": attrs["Properties"],
                "dataCreator": "PubChem",
                "URL": base_url+entry[["id"]],
                "data": json.dumps(entry, sort_keys=True, indent=4),
            }
            searched_results.append(item)
    except:
        return []
    
    return(searched_results)    


print(Pubchem_search('potassium chloride'))


    

