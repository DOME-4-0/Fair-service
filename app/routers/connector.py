import json
import re
import periodictable
import requests

import json
from typing import List, Optional

import requests  # type: ignore
from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/test")
async def test():
    """
    test endpoint
    """
    return {"msg": "Hello from the connector service!"}



@router.get("/platforms")
async def platform_name(platform_string:str):
    Available_platform = ['Crystallography','Novel Materials Discovery','AFLOW',
    'Theoretical Crystallography Open Database',
    'The Open Quantum Materials', 'Materials Project','2DMatpedia','Open Database Xtals',"Pubchem"]

    if platform_string == "":
        return {"msg":"No platform has been entered! Please enter a valid platform"}

    elif platform_string not in Available_platform:
        return {"msg":"The entered platform is either not valid or not available for search on DOME yet"}

    elif platform_string in Available_platform:
        return platform_string.lower()
    #You should create a script to check the version based URLs, this helps the later querying.
    #The version endpoint in Optimade could help with that.


@router.get("/results")

async def searched_platform(self, platform):
        if platform == "":
            return print("No platform has been entered! Please enter a valid platform")
        
        if platform != "":
            return platform.lower()

def search_string_split(String:str) -> List:
    elements = []
    for term in [a for a in re.split(",|\s+", String.strip()) if a]:
        try:
            elements.append(periodictable.elements.name(term.lower()))
        except ValueError:
            pass
        
        pass
    return elements


def Search_API (platform_name, results_type):
    #Optimade query URLs:
    #(Not Worked) Materials Platform for Data Science: https://api.mpds.io
    #(Not worked) Open Materials Database: http://optimade.openmaterialsdb.se
    
    #Common Endpoints : Links, references, structures, info

    #(Worked) MaterialsProject : https://optimade.materialsproject.org
    #(Worked) 2DMatpedia: http://optimade.2dmatpedia.org
    #(Worked) Open Database Xtals: http://optimade.openmaterialsdb.se
    #(Worked) Crystallography: http://crystallography.net/cod/optimade
    #(Worked) Novel Materials Discovery (NOWAD): https://nomad-lab.eu/prod/rae/optimade
    #(Worked) AFLOW: http://aflow.org/API/optimade
    #(Worked) Theoretical Crystallography Open Database: https://www.crystallography.net/tcod/optimade
    #(Worked) The Open Quantum Materials: http://oqmd.org/optimade
    #(Worked) JARVIS-DFT: https://jarvis.nist.gov/optimade/jarvisdft
    # In total, four types of results can be returned from the queries, links, references, structures, info. 
    # On the other hand, ALFOW can return calculations as an addition of properties return

    Optimade_platform_front ={'Materials Project':'materialsproject.org', '2DMatpedia':'2dmatpedia.org','Open Database Xtals':'openmaterialsdb.se'}
    Optimade_platform_end={'Crystallography':'crystallography.net/cod','Novel Materials Discovery':'nomad-lab.eu/prod/rae','AFLOW':'aflow.org/API',
    'Theoretical Crystallography Open Database':'crystallography.net/tcod',
    'The Open Quantum Materials':'oqmd.org'}

    Optimade_results_types = ['structures','references','info','Links']
    if platform_name in Optimade_platform_front:
        platform_string = Optimade_platform_front.get(platform_name)
        query_base_url = f"https://optimade.{platform_string}/v1/" 
        print(query_base_url)

    elif platform_name in Optimade_platform_end:
        platform_string = Optimade_platform_end.get(platform_name)
        query_base_url = f"https://{platform_string}/optimade/v1/"

    elif platform_name == 'JARVIS-DFT':
        query_base_url = "https://jarvis.nist.gov/optimade/jarvisdft/v1/"

    
    elif platform_name == "Pubchem":
        query_base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"

    if results_type == "structures":
        query_base_url_structures= query_base_url+"structures"

    if results_type == "references":
        query_base_url_references= query_base_url+"references"
    
    if results_type == "info":
        query_base_url_info= query_base_url+"info"
    
    if results_type == "Links":
        query_base_url_Links= query_base_url+"links"

    return query_base_url_structures


def searching(search_string, platform_name,results_type):

    Search_URL_base = Search_API(platform_name, results_type)
    print(Search_URL_base)
    searched_results=[]

    if platform_name =="Pubchem":
        res = requests.get(Search_URL_base, params=dict(page_limit=10)).json()

    else: 
        elements =search_string_split(search_string)
        elements_str = ", ".join([f'"{el}"' for el in elements])
        filters = f"(elements HAS ALL {elements_str})"
        res = requests.get(Search_URL_base, params=dict(filter=filters, page_limit=10)).json()
    
    #if res ==[]:
    #     NameError: "Wrong query parameters have been entered"
    try:
        for entry in res["data"]:
            attrs = entry["attributes"]
            item = {
                "keyword": attrs["chemical_formula_descriptive"],
                "dataCreator": platform_name,
                "URL": Search_URL_base+entry["id"],
                "data": json.dumps(entry, sort_keys=True, indent=4),
            }
            searched_results.append(item)
    except:
        return []
    
    return(searched_results)


#print(Search_API(platform_name='Materials Project',results_type='structures'))
#print(searching(search_string ='carbon',platform_name='JARVIS-DFT',results_type='structures'))