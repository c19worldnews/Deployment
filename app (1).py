from bs4 import BeautifulSoup
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


country_lst = ['Alberta', 'British Columbia','Manitoba','New Brunswick','Newfoundland and Labrador','Northwest Territories','Nova Scotia', 'Nunavut',
               'Ontario','Prince Edward Island','Quebec','Saskatchewan','Yukon']

isos=['CAN']

# loading the trained model
model = keras.models.load_model('/content/drive/MyDrive/Weather/Deployment/finalmodel.h5')
#model = keras.models.load_model('path/to/location')
#regression = pickle.load(model)

@st.cache()



# Define a dictionary containing  data 
#country_lst = ['Canada','United States of America','France','United Kingdom']

#country_label_lst = [35,207,65,205]


def prediction(country_name):   

        session = HTMLSession()
        base_link = "https://www.google.com/search?q=weather+"
        country = country_name
        search_link = base_link+country
        response = session.get(search_link)
        soup = BeautifulSoup(response.content, 'html.parser')
        temp =  soup.find("span", attrs={"id": "wob_tm"}).text
        # store all results on this dictionary
        next_days = []
        days = soup.find("div", attrs={"id": "wob_dp"})
        for day in days.findAll("div", attrs={"class": "wob_df"}):
            # extract the name of the day
            day_name = day.findAll("div")[0].attrs['aria-label']
            # get weather status for that day
            weather = day.find("img").attrs["alt"]
            region = day.findAll("span", {"class": "wob_loc"})
            ttemp = day.findAll("span", {"class": "wob_t"})
            # maximum temparature in Celsius, use temp[1].text if you want fahrenheit
            max_temp = ttemp[1].text
            # minimum temparature in Celsius, use temp[3].text if you want fahrenheit
            min_temp = ttemp[3].text
            next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp,"region": region})
            # extract region
            #weatherdata['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
            # extract temperature now
            #weatherdata['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
            # get the day and hour now
            #weatherdata['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
            # get the actual weather
            #weatherdata['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
        
       

       #covid data
        df_covid = pd.read_csv('https://raw.githubusercontent.com/ccodwg/Covid19Canada/master/timeseries_prov/active_timeseries_prov.csv')
        #iso_name = df_covid[df_covid['location']==country]['iso_code'].values[0]
        iso_code = 35 
        new_cases = df_covid[df_covid['province']==country]['active_cases'].values[0]
        final_prediction = []
        lengthnewcases = len(str(int(new_cases)))
        n_steps = 1
        n_features = 3
        x_input = array([iso_code, int(new_cases), float(temp)])
        x_input = x_input.reshape((1, n_steps, n_features))
          # Making predictions 
        prediction = model.predict(x_input)
        #formatting the prediction values
        for i in prediction:
          for j in i:
            out = f'{j:.10f}'
            out = out.split('.')[1]
            # Strip the zeros from the left side of your split decimal
            out = out.lstrip('0')
            final_no = out[:lengthnewcases]
            #print(final_no)
            final_prediction.append(final_no)
            #print(f"{int(final_no):,}")
       
        return final_prediction,next_days




# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    
    html_temp = """ 
    <div style ="background-color:MidnightBlue;padding:8px"> 
    <h1 style ="color:white;text-align:center;font-size:20px">Covid 19 New Cases Prediction App</h1> 
    </div> 
    <br>
    <h3 style ="color:maroon;text-align:left;font-size:16px">5 Days Forescasting of New Covid 19 New Cases Based on Weather</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    country_name = st.selectbox('Choose Location',('Alberta', 'British Columbia','Manitoba','New Brunswick','Newfoundland and Labrador','Northwest Territories','Nova Scotia', 'Nunavut',
               'Ontario','Prince Edward Island','Quebec','Saskatchewan','Yukon'))
    result =""
    
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = prediction(country_name)
        forecast_weather = result[1]
        forecast_weather = forecast_weather[1:6]
        max_temp = [d['max_temp'] for d in forecast_weather if 'max_temp' in d]
        min_temp = [d['min_temp'] for d in forecast_weather if 'min_temp' in d]
        weather = [d['weather'] for d in forecast_weather if 'weather' in d]
        #st.success(forecast_weather)
        forecast_newcases = result[0]
        for i in range(len(forecast_newcases)):
            tomorrow_dt = date.today() + timedelta(1)
            Date_req = tomorrow_dt + timedelta(days=i)
            st.success("Date : " + "  "+"  "+ Date_req.strftime("%d %b, %Y") + "  " + " , " + "New Cases :" + " " + f"{int(forecast_newcases[i]):,}" + " , "
             +  "Max_Temp: " + " " + max_temp[i] + "," +  "Min_Temp: " + " " + min_temp[i] + "," + "Desc: " + " " + weather[i] )
            
       
     
if __name__=='__main__': 
    main()
     