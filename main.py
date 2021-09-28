from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
import matplotlib.pyplot as plt

#prompts for zipcode to scrap from
zip = input("enter zipcode ")
print("This takes a few seconds...")
# gets coordinates from address
app = Nominatim(user_agent="scraper")

# the set up for scraping Realtor.com
page_url ="https://www.realtor.com/realestateandhomes-search/"+ zip +"/type-single-family-home/lot-sqft-2000-7500"
hdr = {'User-Agent': 'Mozilla/5.0'}
req =Request(page_url, headers=hdr)
page = urlopen(req)
soup1 = soup(page, "html.parser")
page.close()
house_cont = soup1.find_all('div', {'class':'jsx-4015109390 property-wrap'})

#saving scraped informationt to csv file
data_file = "house_data_" + zip + ".csv"
headers = "Address , prices ,house_size(sqft) , lot_size(sqft), Longitude, Latitude \n"

f = open(data_file , "w")
f.write(headers)

#arrays used for scatter plot
x = []
y = []
z = []

for houses in house_cont:
    # scrapes the prices of the houses
    prices = houses.select("div")[0].select("span")[0].text.strip().replace("$","").replace(",","")

    # scrapes the lot size of the house
    lot_size = houses.select("div")[1].select("div")[0].select("ul")[0].select("li")[3].text.strip().replace(" Sq. Ft.","")\
        .replace(",","").replace("sqft lot","").replace("acre lot","")

    #scrapes the size of the house
    sqft = houses.select("div")[1].select("div")[0].select("ul")[0].select("li")[2].text.strip().replace(" Sq. Ft.","")\
        .replace(",","").replace("sqft","").replace("acre lot","")

    #scrapes the address of the house
    address = houses.select("div")[3].text.strip().replace(",","")

    #finds the longitute and latitude of the house using the address
    location = app.geocode(address)
    if location:
        long = str(location.longitude)
        lat = str(location.latitude)
    else:
        long = "-----not found-----"
        lat = "-----not found-----"

    # writes the information to the csv file created above
    f.write(address + "," + prices + ", " + sqft + "," + lot_size + "," + long + "," + lat + "\n")

    # prepares the information to be plotted on the graph
    x.append(float(lot_size))
    y.append(float(prices)/1000)
    z.append(float(sqft))

f.close()


#setting up and showing the graph
plt.figure(figsize=(7,5))
plt.title("Zipcode: " + zip)
plt.xlabel("Size in Square Feet")
plt.ylabel("price $ (K)")
plt.scatter(x, y, color = 'r')
plt.scatter(z, y, color = 'b')
plt.legend(["lot size","house size"], loc = "upper center", bbox_to_anchor =(.88, 1.15))
plt.show()