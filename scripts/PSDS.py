import json
import re
import periodictable
import requests

# PSDS stands for physical science data-science service and it allows the connection with other platforms

# The resources can be split into various types : organic, inorganic, properties and chemical availability

### Organic###
#CSD : Cambridge Structural Database
#CrystalWorks: Has access to a wide range of crystallographic structural data#

#Inorganic#
#ICSD: Inorganic crystal structure database

#Properties#
#DETHERM: Thermophysical databases
#Propersa: Property prediction (Not sure how relevant it is but worth to check it)
# ChAse: Chemcail Availbiliy Search


#PSDS = ['Cambridge Structural Database','CrystalWorks','DETHERM','Inorganic Crystal Structure Database','Chemical Avilability Search','Propersea']

#In the following codes, we will create connector that are RESTAPI based and will allow DOME to gain access to these platform. 

# One important notice to have is that these PSDS platform requires people to resgiter on their platform in order to gain access to the data. 
