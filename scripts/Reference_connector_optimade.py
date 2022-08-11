import ABC_connector.abc_reference_conector
import json
import re
import periodictable
import requests



class dome_search(abc_reference_conector):

    def search_string (self, String):
        elements = []
        for term in [a for a in re.split(",|\s+", String.strip()) if a]:
            try:
                elements.append(periodictable.elements.name(term.lower()))
            except ValueError:
                pass
            
            pass
        return elements

    def platform_name(self, platform_string):
        if platform_string == "":
            return print("No platform has been entered! Please enter a valid platform")
        
        if platform_string != "":
            return platform_string.lower()

        #You should create a script to check the version based URLs, this helps the later querying.
        #The version endpoint in Optimade could help with that.

    def searching(self, search_string, platform_name,data_type):


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

        Optimade_platform_front ={'Materials Project':'materialsproject.org', '2dmatpedia.org':'2dmatpedia','Open Database Xtals':'openmaterialsdb.se'}


        Optimade_platform_end={'Crystallography':'crystallography.net/cod','Novel Materials Discovery':'nomad-lab.eu/prod/rae','AFLOW':'aflow.org/API',
        'Theoretical Crystallography Open Database':'crystallography.net/tcod',
        'The Open Quantum Materials':'oqmd.org'}     

        List_of_data_types = ['structures','references','info','Links']

        if platform_name in Optimade_platform_front:
            platform_string = Optimade_platform_front.get(platform_name)
            print(platform_string)
            optimade_platform_URL = f("https:optimade.{platform_string}/v1/") 

        elif platform_name in Optimade_platform_end:
            platform_string = Optimade_platform_end.get(platform_name)
            optimade_platform_URL = f("https:optimade.{platform_string}/v1/") 

        elif platform_name == 'JARVIS-DFT':
            optimade_platform_URL = "https://jarvis.nist.gov/optimade/jarvisdft/v1/"


        if data_type == "structures":
            optimade_platform_URL_structures= optimade_platform_URL+"structures"

        searched_results=[]

        elements_str = ", ".join([f'"{el}"' for el in elements])
        filters = f"(elements HAS ALL {elements_str})"

        res = requests.get(optimade_platform_URL_structures, params=dict(filter=filters, page_limit=10)).json()
        
        #if res ==[]:
        #     NameError: "Wrong query parameters have been entered"

        try:
            for entry in res["data"]:
                attrs = entry["attributes"]
                item = {
                    "keyword": attrs["chemical_formula_descriptive"],
                    "dataCreator": platform_name,
                    "URL": optimade_platform_URL+entry["id"],
                    "data": json.dumps(entry, sort_keys=True, indent=4),
                }
                searched_results.append(item)
        except:
            return []
        
        return(searched_results)

