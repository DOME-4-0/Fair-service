"""Connector service"""
import json
import re
from typing import List
from operator import itemgetter
import periodictable  # type: ignore
import requests  # type: ignore
from fastapi import APIRouter

router = APIRouter()


# pylint:disable=line-too-long
# pylint: disable=too-many-locals


def search_string_split(search_string: str) -> List:
    """Split the search string"""
    elements = []
    for term in [a for a in re.split(",|\s+", search_string.strip()) if a]:  # pylint: disable=W1401
        try:
            elements.append(periodictable.elements.name(term.lower()))
        except ValueError:
            print(" ")

        print(" ")
    return elements


def search_api(platform_name):
    """Generate the API automatically"""
    # Optimade query URLs:
    # (Not Worked) Materials Platform for Data Science: https://api.mpds.io
    # (Not worked) Open Materials Database: http://optimade.openmaterialsdb.se

    # Common Endpoints : Links, references, structures, info

    # (Worked) MaterialsProject : https://optimade.materialsproject.org
    # (Worked) 2DMatpedia: http://optimade.2dmatpedia.org
    # (Worked) Open Database Xtals: https://optimade.odbx.science
    # (Worked) Crystallography: http://crystallography.net/cod/optimade
    # (Worked) Novel Materials Discovery (NOWAD): https://nomad-lab.eu/prod/rae/optimade
    # (Worked) AFLOW: http://aflow.org/API/optimade
    # (Worked) Theoretical Crystallography Open Database: https://www.crystallography.net/tcod/optimade
    # (Worked) The Open Quantum Materials: http://oqmd.org/optimade
    # (Worked) JARVIS_DFT: https://jarvis.nist.gov/optimade/jarvisdft
    # In total, four types of results can be returned from the queries, links, references, structures, info.
    optimade_platform_front = {'MATERIALSPROJECT': 'materialsproject.org',
                               'OPEN_DATABASE_XTALS': 'odbx.science'}
    optimade_platform_end = {'NOWAD': 'nomad-lab.eu/prod/rae', 'AFLOW': 'aflow.org/API',
                             'THE_OPEN_QUANTUM_MATERIALS': 'oqmd.org'}
    new_optimade_cod_api = {'THEORETICAL_CRYSTALLOGRAPHY_OPEN_DATABASE': 'crystallography.net/tcod',
                            'CRYSTALLOGRAPHY': 'crystallography.net/cod'}
    # optimade_results_types = ['structures', 'references', 'info', 'Links']
    if platform_name in optimade_platform_front:
        platform_string = optimade_platform_front.get(platform_name)
        query_base_url = f"https://optimade.{platform_string}/v1/structures"
        print(query_base_url)

    elif platform_name in optimade_platform_end:
        platform_string = optimade_platform_end.get(platform_name)
        query_base_url = f"https://{platform_string}/optimade/v1/structures"

    elif platform_name in new_optimade_cod_api:
        platform_string = new_optimade_cod_api.get(platform_name)
        query_base_url = f"https://www.{platform_string}/optimade/v1.1.0/structures"
    # if results_type == "references":
    #    query_base_url_references = query_base_url+"references"
    #
    # if results_type == "info":
    #    query_base_url_info = query_base_url+"info"
    #
    # if results_type == "Links":
    #    query_base_url_links = query_base_url+"links"

    elif platform_name == 'JARVIS_DFT':
        query_base_url = "https://jarvis.nist.gov/optimade/jarvisdft/v1/structures"

    # elif platform_name == '2DMatpedia':
    #   query_base_url = "https://www.optimade.2dmatpedia.org/v1/structures"
    elif platform_name == "PUBCHEM":
        query_base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"

    elif platform_name == "CHEMEO":
        query_base_url = "https://www.chemeo.com/api/v1/search"

    else:
        query_base_url = " "

    return query_base_url


@router.get("/fair")
async def return_raw_results(
        search_string: str,
        platform_name: str):
    """helps to connect to data platforms"""
    search_url_base = search_api(platform_name)
    if platform_name == "PUBCHEM":
        base_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{search_string}/record/JSON?callback=pubchem_callback"
        res_base = requests.get(base_url, params=dict(page_limit=10)).json()
        chemical_pubchem_results = res_base["PC_Compounds"][0]
        cid_id = chemical_pubchem_results.get(
            'id', {}).get('id', {}).get('cid')
        pubchem_chem_hazard_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid_id}/JSON/?response_type=display&heading=GHS%20Classification"
        print(pubchem_chem_hazard_url)
        res = requests.get(
            pubchem_chem_hazard_url, params=dict(page_limit=10)).json()
    elif platform_name == "CHEMEO":
        try:
            search_url_chemeo = f"{search_url_base}?q={search_string}"
            res = requests.get(search_url_chemeo,
                               headers={"Authorization": "Bearer 6d767996_1922_4328_967e_82104b1ae6c9"}).json()
        except KeyError:
            pass
    else:
        elements = search_string_split(search_string)
        elements_str = ", ".join([f'"{el}"' for el in elements])
        filters = f"(elements HAS ALL {elements_str})"
        res = requests.get(search_url_base, params=dict(
            filter=filters, page_limit=10)).json()

    return res
