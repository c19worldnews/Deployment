from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession 
import pickle
import streamlit as st
from tensorflow import keras
# univariate bidirectional lstm example
from numpy import array 
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from datetime import timedelta, date
from geopy.geocoders import Nominatim
# Library for opening url and creating
# requests
import urllib.request
 
# pretty-print python data structures
from pprint import pprint
 
# for parsing all the tables present
# on the website
from html_table_parser.parser import HTMLTableParser
import builtins
#from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import chromedriver_binary 





chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


# open it, go to a website, and get results




import numpy as np

country_lst = ['Aruba','Afghanistan','Angola','Albania','Andorra','United Arab Emirates','Argentina','Armenia','American Samoa',
 'Antigua and Barbuda','Australia','Austria','Azerbaijan','Burundi','Belgium','Benin','Burkina Faso','Bangladesh','Bulgaria','Bahrain','Bahamas',
 'Bosnia and Herzegovina','Belarus','Belize','Bermuda','Bolivia','Brazil','Barbados','Brunei','Bhutan','Botswana','Canada','Switzerland','Chile',
 'China','Ivory Coast','Cameroon','Republic of the Congo','Cook Islands','Colombia','Comoros','Cape Verde','Costa Rica','Cuba','Curaçao','Cayman Islands',
 'Cyprus','Czech Republic','Germany','Djibouti','Dominica','Denmark','Dominican Republic','Algeria','Ecuador','Egypt','Spain','Estonia','Ethiopia','Finland',
 'Fiji','Falkland Islands','France','Faroe Islands','Gabon','United Kingdom','Guernsey','Ghana','Gibraltar','Guinea','Gambia','Guinea-Bissau',
 'Equatorial Guinea','Greece','Grenada','Guatemala','French Guiana','Guam','Guyana','Hong Kong','Honduras','Croatia','Haiti','Hungary','Indonesia',
 'Isle of Man','India','Ireland','Iran','Iraq','Iceland','Israel','Italy','Jamaica','Jersey','Jordan','Japan','Kazakhstan','Kenya','Kyrgyzstan','Cambodia',
 'Kiribati','Saint Kitts and Nevis','South Korea','Kuwait','Laos','Lebanon','Liberia','Libya','Saint Lucia','Liechtenstein','Sri Lanka','Lesotho','Lithuania',
 'Luxembourg','Latvia','Macau','Morocco','Monaco','Moldova','Madagascar','Maldives','Mexico','Marshall Islands','Mali','Malta','Myanmar','Montenegro',
 'Mongolia','Northern Mariana Islands','Mozambique','Mauritania','Montserrat','Martinique','Mauritius','Malawi','Malaysia','Mayotte','New Caledonia','Niger',
 'Nigeria','Nicaragua','Niue','Netherlands','Norway','Nepal','New Zealand','Oman','Pakistan','Panama','Peru','Philippines','Palau','Papua New Guinea','Poland',
 'Puerto Rico','North Korea','Portugal','Paraguay','French Polynesia','Qatar','Réunion','Kosovo','Romania','Russia','Rwanda','Saudi Arabia','Sudan','Senegal',
 'Singapore','Saint Helena','Solomon Islands','Sierra Leone','El Salvador','San Marino','Serbia','South Sudan','São Tomé and Príncipe','Suriname','Slovakia',
 'Slovenia','Sweden','Swaziland','Sint Maarten','Syria','Turks and Caicos Islands','Chad','Togo','Thailand','Tajikistan','Tokelau','Turkmenistan','East Timor',
 'Tonga','Trinidad and Tobago','Tunisia','Turkey','Tuvalu','Taiwan','Tanzania','Uganda','Ukraine','Uruguay','United States of America','Uzbekistan',
 'Vatican City','Saint Vincent and the Grenadines','Venezuela','British Virgin Islands','United States Virgin Islands','Vietnam','Vanuatu',
 'Wallis and Futuna','Samoa','Yemen','South Africa','Zambia','Zimbabwe']




isos=['ABW','AFG','AGO','AIA','ALB','AND','ARE','ARG','ARM','ASM','ATG','AUS','AUT','AZE','BDI','BEL','BEN','BFA','BGD','BGR','BHR','BHS','BIH',
'BLR','BLZ','BMU','BOL','BRA','BRB','BRN','BTN','BWA','CAN','CHE','CHL','CHN','CIV','CMR','COG','COK','COL','COM','CPV','CRI','CUB','CUW',
'CYM','CYP','CZE','DEU','DJI','DMA','DNK','DOM','DZA','ECU','EGY','ESP','EST','ETH','FIN','FJI','FLK','FRA','FRO','GAB','GBR','GGY','GHA',
'GIB','GIN','GMB','GNB','GNQ','GRC','GRD','GTM','GUF','GUM','GUY','HKG','HND','HRV','HTI','HUN','IDN','IMN','IND','IRL','IRN','IRQ','ISL',
'ISR','ITA','JAM','JEY','JOR','JPN','KAZ','KEN','KGZ','KHM','KIR','KNA','KOR','KWT','LAO','LBN','LBR','LBY','LCA','LIE','LKA','LSO','LTU',
'LUX','LVA','MAC','MAR','MCO','MDA','MDG','MDV','MEX','MHL','MLI','MLT','MMR','MNE','MNG','MNP','MOZ','MRT','MSR','MTQ','MUS','MWI','MYS',
'MYT','NCL','NER','NGA','NIC','NIU','NLD','NOR','NPL','NZL','OMN','PAK','PAN','PER','PHL','PLW','PNG','POL','PRI','PRK','PRT','PRY','PYF',
'QAT','REU','RKS','ROU','RUS','RWA','SAU','SDN','SEN','SGP','SHN','SLB','SLE','SLV','SMR','SRB','SSD','STP','SUR','SVK','SVN','SWE','SWZ',
'SXM','SYR','TCA','TCD','TGO','THA','TJK','TKL','TKM','TLS','TON','TTO','TUN','TUR','TUV','TWN','TZA','UGA','UKR','URY','USA','UZB','VAT',
'VCT','VEN','VGB','VIR','VNM','VUT','WLF','WSM','YEM','ZAF','ZMB','ZWE']

# loading the trained model
model = keras.models.load_model('finalmodel.h5')
#regression = pickle.load(model)

@st.cache()


# session = requests.Session()
def getWeather(city_name,country_name):
  
  
  session = HTMLSession()
  headers = {'Accept-Language': 'en-US,en;q=0.8'}
  base_link = "https://www.google.com/search?q=weather/"+ city_name + "+" +country_name
  
  response = session.get(base_link)
  soup = bs(response.content, 'html.parser')

  #return base_link
  
  temp =  soup.find("span", attrs={"id": "wob_tm"}).text
 
  region = soup.find("div", attrs={"id": "wob_loc"}).text
          
          # store all results on this dictionary
  next_days = []
  days = soup.find("div", attrs={"id": "wob_dp"})
  for day in days.findAll("div", attrs={"class": "wob_df"}):
    day_name = day.findAll("div")[0].attrs['aria-label']
              # get weather status for that day
    weather_img = day.find("img").attrs["src"]
    weather_desc = day.find("img").attrs["alt"]
    maxtemp = day.findAll("div", {"class": "gNCp2e"})
    max_temp = maxtemp[0].text
    mintemp = day.findAll("div", {"class": "QrNVmd ZXCv8e"})
    min_temp = mintemp[0].text
    next_days.append({"name": day_name, "weather_desc": weather_desc, "weather_img":weather_img , "max_temp": max_temp[2:], "min_temp": min_temp[2:]})
  return next_days,temp,region,base_link




def prediction(city_name,country_name,iso_code,label_alpha_2,select_location):
  session = HTMLSession()
  headers = {'Accept-Language': 'en-US,en;q=0.8'}

  location = select_location.replace(" ", "-")
  country = location.lower()
 
  usa_prov = country_name.lower()
  #scraping the button show all click data
  #return select_location
  wd = webdriver.Chrome('/usr/bin/chromedriver',options=chrome_options)
  #wd.get("https://share.streamlit.io/")
  wd = webdriver.Chrome()
  #wd = webdriver.Chrome('chromedriver',options=options)
  #wd = webdriver.Chrome(executable_path ='/usr/bin/chromedriver')
  

  if select_location == 'USA':
      wd.get("https://www.nytimes.com/interactive/2021/us/"+usa_prov+"-covid-cases.html")
      #baseurl = "https://www.nytimes.com/interactive/2021/us/"+usa_prov+"-covid-cases.html"
      #return baseurl
  else:
      wd.get("https://www.nytimes.com/interactive/2021/world/"+country+"-covid-cases.html")
      #baseurl ="https://www.nytimes.com/interactive/2021/world/"+country+"-covid-cases.html"
      #print(baseurl)
   


  #element = wd.find_element(By.XPATH,"//button[contains(@class,'showall')]")
  #element = wd.find_element(By.XPATH,"//*[@id='world-france-covid-cases']/div/div/main/div[3]/div[4]/section[2]/div[2]/table/tbody/tr")
  #wd.execute_script("arguments[0].click();", element)

  elements=wd.find_elements_by_xpath("//button[contains(@class,'showall')]")
  for element in elements:
    wd.execute_script("arguments[0].click();", element);
    #return element.text
  # Get 'HTML'

  html_data = wd.page_source
  #return html_data
  soup = bs(html_data, 'html.parser')
  table = soup.findAll('table', {"class": "g-table super-table withchildren"})
  #return table
  if len(table) == 2:

      df = pd.read_html(str(table[0]))[0]
      df = df[df.columns[:2]]
      df = df.rename(columns={ df.columns[0]: "location", df.columns[1]: "new_cases" })
      #if country=='italy':
       # df.drop(columns=['Per 100,000',	'14-day change'], inplace=True)
       # df.rename(columns={'Unnamed: 0': 'location', 'Cases Daily Avg.':'new_cases'}, inplace=True)
      #else:
       # df.drop(columns=['Per 100,000',	'14-day change',	'Deaths Daily Avg.',	'Per 100,000.1'], inplace=True)
       # df.rename(columns={'Unnamed: 0': 'location', 'New Hospitalizations Daily Avg.':'new_cases'}, inplace=True)
      
      df2 = pd.read_html(str(table[1]))[0]


      df2 = df2[df2.columns[:2]]
      df2 = df2.rename(columns={ df2.columns[0]: "location", df2.columns[1]: "new_cases" })
      #if country=='italy':
       # df2.drop(columns=['Per 100,000',	'14-day change'], inplace=True)
       # df2.rename(columns={'Unnamed: 0': 'location', 'Cases Daily Avg.':'new_cases'}, inplace=True)
      #else:
       # df2.drop(columns=['Per 100,000',	'14-day change',	'Deaths Daily Avg.',	'Per 100,000.1'], inplace=True)
       # df2.rename(columns={'Unnamed: 0': 'location', 'New Hospitalizations Daily Avg.':'new_cases'}, inplace=True)

      df = df.append(df2)
    

  else:

      df = pd.read_html(str(table[0]))[0]
      df = df[df.columns[:2]]
      df = df.rename(columns={ df.columns[0]: "location", df.columns[1]: "new_cases" })
      #df.drop(columns=['Per 100,000',	'14-day change',	'Deaths Daily Avg.',	'Per 100,000.1'], inplace=True)
      #df.rename(columns={'Unnamed: 0': 'location', 'Cases Daily Avg.':'new_cases'}, inplace=True)

  #return df  
  if select_location == 'USA':  
      df['location'] = df['location'].replace('[^a-zA-Z0-9 ]', '', regex=True)
      #city =  df[df['location'] == city_name]  
      new_cases = df[df['location'] == city_name]['new_cases'].values[0]
     
  else:
      #city =  df[df['location'] == city_name]   
      new_cases = df[df['location'] == city_name]['new_cases'].values[0]
     

      
  if str(new_cases).startswith('<'): 
      new_cases = int(new_cases[1:])
  else :
      int(new_cases)

  #return new_cases 
  #call the weather function
  
  weatherData = getWeather(city_name,country_name)
 # return weatherData
  #prepare temp to pass into model
  temp = int(weatherData[1])  
           
  lengthnewcases = len(str(new_cases))

        #preparation of model data
  final_prediction = []  
  n_steps = 1
  n_features = 3
  #max_temp = 45
  #min_temp = 29
  x_input = array([int(iso_code), int(new_cases), float(temp)])
  x_input = x_input.reshape((1, n_steps, n_features))   
      # Making predictions 
  prediction = model.predict(x_input)
              #formatting the prediction values
  #return prediction
            
  for i in prediction: 
      
      for j in i:
        out = f'{j:.10f}'
        out = out.split('.')[1]
                  # Strip the zeros from the left side of your split decimal
        out = out.lstrip('0')
        final_no = out[:lengthnewcases]           
        final_prediction.append(final_no)

        #print(f"{int(final_no):,}")

            
  return final_prediction,select_location,weatherData,new_cases,label_alpha_2,city_name
       

import base64
   

# this is the main function in which we define our webpage  
def main():  
    # front end elements of the web page 
    st.set_page_config(layout="wide")
    main_bg = "giphy.gif"
    main_bg_ext = "gif"
    padding_left = "50px"
    #background-color: #1c294b
    #background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
    #background-size: cover;
    #background-position: center;
    #backdrop-filter: blur(5px);
    st.sidebar.markdown(
      f"""
      <style>
      
      .reportview-container .main {{

          background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
          
          background-size: 150px 100px;
          background-repeat: repeat-y;
          background-color: #031444;
          

          }}

     
      </style>
      """,
      unsafe_allow_html=True
    )
     
  
   
    st.sidebar.image("tlogo.png")
    Date_today = date.today()  
       
    html_date = str("<p style='color: white; text-align:center; font-size:20px'>") + str(Date_today.strftime("%d %b, %y"))+ str("</p>")
    st.sidebar.markdown(html_date, unsafe_allow_html=True)
   
    st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {{
         
          background-color:#031444;
          width:230px;
          
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
    
    
    new_title = '<p style="font-style: oblique; text-align:center;color:#ffe168; font-size:25px">5  Days Forecasting of Covid 19 New Cases Based on Weather</p>'
    st.markdown(new_title,unsafe_allow_html=True)
   
  

    #adding sidebar

    #-- Set by location
    sel_location = '<p style="font-style: oblique; text-align:left;color:white; font-size:16px">Select Location</p>'
    st.sidebar.markdown(sel_location,unsafe_allow_html=True)
    st.markdown(
    """
    <style>
    [data-baseweb="select"] {
        margin-top: -50px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    select_location = st.sidebar.selectbox('Select Location',
                                    ['Australia', 'Brazil','Canada','France','Germany','Italy','India','Japan','Mexico','Spain','United Kingdom','USA'])
    
                             

    if select_location == 'USA':
            usa_dataset = pd.read_csv('https://raw.githubusercontent.com/neerja198/Deployment/main/USA_referance.csv') 
           
            sel_prov = '<p style="font-style: oblique; text-align:left;color:white; font-size:16px">Select Province</p>'
            st.sidebar.markdown(sel_prov,unsafe_allow_html=True)
            us_state = st.sidebar.selectbox("Select Province", sorted(usa_dataset.State.unique()), index=0)
            sel_city = '<p style="font-style: oblique; text-align:left;color:white; font-size:16px">Select City</p>'
            st.sidebar.markdown(sel_city,unsafe_allow_html=True)
            city_name = st.sidebar.selectbox("Select City", sorted(usa_dataset.loc[usa_dataset.State == us_state].City.unique()))
           
            city_name = city_name.replace("'", "")
            
            # 0: city   1: country   2: ISO   3: Label
            us_reference =usa_dataset.loc[usa_dataset.City== city_name].values[0]
          
            country_name = us_state
            iso_code = us_reference[4]
            alpha_2 = us_reference[2] 
            label_alpha_2 = alpha_2[:2].lower()


            result =""

    else: 
          reference_file = pd.read_csv('https://raw.githubusercontent.com/neerja198/Deployment/main/location_list.csv')
          

          #country = st.sidebar.selectbox("Select Country", sorted(reference_file.Country.unique()), index=0)
          country = select_location
          sel_prov_city = '<p style="font-style: oblique; text-align:left;color:white; font-size:16px">Select Province/City</p>'
          st.sidebar.markdown(sel_prov_city,unsafe_allow_html=True)
          city_name = st.sidebar.selectbox("Select Province/City", sorted(reference_file.loc[reference_file.Country == country].City.unique()))    
          city_name = city_name.replace("'", "")
          
          # 0: city   1: country   2: ISO   3: Label
          city_reference =reference_file.loc[reference_file.City== city_name].values[0]
        
          country_name = city_reference[1]
          country_name = country_name.lower()
          iso_code = city_reference[3]
          alpha_2 = city_reference[2] 
          label_alpha_2 = alpha_2[:2].lower()


          result =""

    # when 'Predict' is clicked, make the prediction and store it 
    if st.sidebar.button("Predict"): 
        result = prediction(city_name,country_name,iso_code,label_alpha_2,select_location)
        #st.success(result)
        if len(result) == 6:
            forecast_weather = result[2]
            forecast_weather = forecast_weather[:2]
           
            max_temp = [d['max_temp'] for d in forecast_weather[0] if 'max_temp' in d]
            min_temp = [d['min_temp'] for d in forecast_weather[0] if 'min_temp' in d]
            weather_desc = [d['weather_desc'] for d in forecast_weather[0] if 'weather_desc' in d]
            weather_img = [d['weather_img'] for d in forecast_weather[0] if 'weather_img' in d]

           
            col1,col2= st.columns(2)
            Date_today = date.today()  
            
            html_location = str("<p style='text-align: left; color: white; font-size:20px'>") + str( result[5] + " , "  +result[1])+ str("</p>")
            col1.markdown(html_location, unsafe_allow_html=True)
            if result[4] == 'fl':
                st.image("https://flagcdn.com/256x192/"+ "us-" +result[4]+".png" , width=40)
            else:
                st.image("https://flagcdn.com/256x192/"+result[4]+".png" , width=40)
            html_newcases = str("<p style='text-align: right; color: white; font-size:20px'>") + str( "New Cases: " + f"{int(result[3]):,}")+ str("</p>")
            col2.markdown(html_newcases, unsafe_allow_html=True)
            
            
            #st.metric("New Cases", f"{int(result[3]):,}") 
            #st.metric("Location", result[1].title())
        

            forecast_newcases = result[0]
            #print(forecast_newcases)
            forecast_newcases.insert(0,result[3])
            
            
            association_msg = []
            for i in builtins.range(0,5):
               if int(forecast_newcases[i]) < int(forecast_newcases[i+1]):
                  association_msg.append("Today the weather is " + weather_desc[i] + " and temp is between " + min_temp[i] + "/ " + max_temp[i] + " , So the number of new cases of covid-19 cases may increase.")

               elif int(forecast_newcases[i]) > int(forecast_newcases[i+1]):
                  association_msg.append("Today the weather is " + weather_desc[i] + " and temp is between " + min_temp[i] + "/ " + max_temp[i] + " , So the number of new cases of covid-19 cases may decrease.")

               else:
                  association_msg.append("Today the weather is " + weather_desc[i] + " and temp is between " + min_temp[i] + "/ " + max_temp[i] + ", So the number of new cases of covid-19 cases may not be affected.")
           
           
            format_nc = []
            for x in forecast_newcases:
              x = int(x)
              if x < 4:
                minimum_cases = 0
                maximum_cases = x
                new_cases = str(minimum_cases)+" - "+str(maximum_cases)
                format_nc.append(new_cases)
              else:
                range = x/4
                range = int(range)
                minimum_cases = x-range
                maximum_cases = x + range
                cases_range = "between " + str(minimum_cases)+" and "+str(maximum_cases)
                new_cases = str(minimum_cases)+" - "+str(maximum_cases)
                format_nc.append(new_cases)
            #st.success(format_nc)
            
            #date list
            date_lst = []
           

            for i in builtins.range(0,5):
                Date_req = Date_today+ timedelta(days=i+1)
                date_lst.append(Date_req.strftime("%d %b %y"))


            
                
            
            #index_value = ['Date','New Cases','Icon','Desc','Max_Temp','Min_Temp']
            #tble for date

            html_code1 = str("<h4 style='text-align: center; color: white;'>") + str(date_lst[0])+ str("</h4>")
            html_code2 = str("<h4 style='text-align: center; color: white;'>") + str(date_lst[1])+ str("</h4>")
            html_code3 = str("<h4 style='text-align: center; color: white;'>") + str(date_lst[2])+ str("</h4>")
            html_code4 = str("<h4 style='text-align: center; color: white;'>") + str(date_lst[3])+ str("</h4>")
            html_code5 = str("<h4 style='text-align: center; color: white;'>") + str(date_lst[4])+ str("</h4>")

           
            col9,col10,col11,col12,col13 = st.columns(5)
            col9.markdown(html_code1, unsafe_allow_html=True)
            col10.markdown(html_code2, unsafe_allow_html=True)
            col11.markdown(html_code3, unsafe_allow_html=True)
            col12.markdown(html_code4, unsafe_allow_html=True)
            col13.markdown(html_code5, unsafe_allow_html=True)

            #table for new cases
            html_code6 = str("<h3 style='text-align: center; color: #ffe168;'>") +str(format_nc[1] )+ str("</h3>")
            html_code7 = str("<h3 style='text-align: center; color: #ffe168;'>") + str(format_nc[2])+ str("</h3>")
            html_code8 = str("<h3 style='text-align: center; color: #ffe168;'>") + str(format_nc[3])+ str("</h3>")
            html_code9 = str("<h3 style='text-align: center; color: #ffe168;'>") + str(format_nc[4])+ str("</h3>")
            html_code10 = str("<h3 style='text-align: center; color: #ffe168;'>") + str(format_nc[5])+ str("</h3>")

           
            col14,col15,col16,col17,col18 = st.columns(5)
            col14.markdown(html_code6,unsafe_allow_html=True)
            
            col15.markdown(html_code7,unsafe_allow_html=True)
            col16.markdown(html_code8,unsafe_allow_html=True)
            col17.markdown(html_code9,unsafe_allow_html=True)
            col18.markdown(html_code10,unsafe_allow_html=True)

            html_ass1 = str("<p style='text-align: center; color: white;'>") +str(association_msg[0])+ str("</p>")
            html_ass2= str("<p style='text-align: center; color: white;'>") +str(association_msg[1] )+ str("</p>")
            html_ass3= str("<p style='text-align: center; color: white;'>") +str(association_msg[2] )+ str("</p>")
            html_ass4= str("<p style='text-align: center; color: white;'>") +str(association_msg[3] )+ str("</p>")
            html_ass5= str("<p style='text-align: center; color: white;'>") +str(association_msg[4] )+ str("</p>")

            col_ass1,col_ass2,col_ass3,col_ass4,col_ass5 = st.columns(5)
            col_ass1.markdown(html_ass1,unsafe_allow_html=True)
            col_ass2.markdown(html_ass2,unsafe_allow_html=True)
            col_ass3.markdown(html_ass3,unsafe_allow_html=True)
            col_ass4.markdown(html_ass4,unsafe_allow_html=True)
            col_ass5.markdown(html_ass5,unsafe_allow_html=True)

            #table for Desc
            html_code11 = str("<p style='text-align: center; font-style: oblique; color: white; font-size:20px'>") + str(weather_desc[0])+ str("</p>")
            html_code12 = str("<p style='text-align: center; font-style: oblique; color: white; font-size:20px'>") + str(weather_desc[1])+ str("</p>")
            html_code13 = str("<p style='text-align: center; font-style: oblique; color: white; font-size:20px'>") + str(weather_desc[2])+ str("</p>")
            html_code14 = str("<p style='text-align: center; font-style: oblique; color: white; font-size:20px'>") + str(weather_desc[3])+ str("</p>")
            html_code15 = str("<p style='text-align: center; font-style: oblique; color: white; font-size:20px'>") + str(weather_desc[4])+ str("</p>")

           
            col19,col20,col21,col22,col23 = st.columns(5)
            col19.markdown(html_code11, unsafe_allow_html=True)
            col20.markdown(html_code12, unsafe_allow_html=True)
            col21.markdown(html_code13, unsafe_allow_html=True)
            col22.markdown(html_code14, unsafe_allow_html=True)
            col23.markdown(html_code15, unsafe_allow_html=True)
            
            

            #table for icon

            col24,col25,col26,col27,col28,col24_1,col24_2,col24_3,col24_4,col24_5 = st.columns([1,2,1,2,1,2,1,2,1,2])
           
           
        
            with col25:
                st.image("https:"+weather_img[0])
            with col27:
                st.image("https:"+weather_img[1])
            with col24_1:
                st.image("https:"+weather_img[2])
            with col24_3:
                st.image("https:"+weather_img[3])
            with col24_5:
                st.image("https:"+weather_img[4])
            
            
            
            #col26.image("https:"+weather_img[1])
            #col27.image("https:"+weather_img[2])
            #col28.image("https:"+weather_img[3])
            #col34.image("https:"+weather_img[4])

            #table for mintemp/maxtemp
            html_code21 = str("<p style='text-align: center; color: white; font-size:20px'>") + str(min_temp[0] + "C"+ "/"+max_temp[0]+ "C")+ str("</p>")
            html_code22 = str("<p style='text-align: center; color: white; font-size:20px'>") + str(min_temp[1] + "C" + " / "+max_temp[1]+ "C")+ str("</p>")
            html_code23 = str("<p style='text-align: center; color: white; font-size:20px'>") + str(min_temp[2] + "C" + " / "+max_temp[2]+ "C")+ str("</p>")
            html_code24 = str("<p style='text-align: center; color: white; font-size:20px'>") + str(min_temp[3] + "C" + " / "+max_temp[3]+ "C")+ str("</p>")
            html_code25 = str("<p style='text-align: center; color: white; font-size:20px'>") + str(min_temp[4] + "C" + " / "+max_temp[4]+ "C")+ str("</p>")

           
            col29,col30,col31,col32,col33 = st.columns(5)
            col29.markdown(html_code21,unsafe_allow_html=True)
            col30.markdown(html_code22,unsafe_allow_html=True)
            col31.markdown(html_code23,unsafe_allow_html=True)
            col32.markdown(html_code24,unsafe_allow_html=True)
            col33.markdown(html_code25,unsafe_allow_html=True)
        else:
            st.success(result)  

            
            
            #st.success("Date : " + "  "+"  "+ Date_req.strftime("%d %b, %Y") + "  " + " , " + "New Cases :" + " " + f"{int(forecast_newcases[i]):,}" + " , "
             #+  "Max_Temp: " + " " + max_temp[i] + "°C"+"," +  "Min_Temp: " + " " + min_temp[i] + "°C"+"," + "Desc: " + " " + weather[i] )
     
     
if __name__=='__main__': 
    main()
     
