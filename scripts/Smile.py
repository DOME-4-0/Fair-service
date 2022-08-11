
# These lines of codes allow us to convert the chemical names into the SMILE format chemicals. These can then be passed as a query to detox database for querying. 
from urllib.request import urlopen
from urllib.parse import quote

def SMILEconvert(chemical_name):
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + quote(chemical_name) + '/smiles'
        smile_name = urlopen(url).read().decode('utf8')
        return smile_name
    except:
        return 'The entered chemical name is either wrong or the database could not find any suitable SMILE names'



print(SMILEconvert('benzene'))

