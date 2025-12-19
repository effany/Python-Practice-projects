from scrapper import Scrapper
from data_filler import DATAFILLER

scrapper = Scrapper()

properties_info = scrapper.get_property_listings()

data_filler = DATAFILLER()

# for i in range(len(properties_info)):
#     data_filler.fill_form([properties_info[i]])

data_filler.fill_form(properties_info)