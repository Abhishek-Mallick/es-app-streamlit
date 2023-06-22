import os
import io
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import streamlit as st
from src.utils.read_plot_powerdata import read_plant_csv, df_solar_plant_subset, Daywise_plot, unique_dates_df, Daywise_plot_index
import seaborn as sns
import streamlit as st
from datetime import date
from datetime import datetime

flag = 0
flag1 = 0
vegetation_growth = 29
cracking_growth = 71
dateselect = False
checkboxatt = "AMBIENT_TEMPERATURE"

st.set_page_config(page_title="Solar Energy Output Plotter", page_icon=":camera_with_flash:", layout="wide")
st.image('https://www.greenscan.io/static/media/Logo_GreenScan-05.f3b4fc90.svg', width=200)

# Sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        width: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
import streamlit as st

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #2F91A2;
    }
    [data-testid=stSidebar] {
        width: 20px;
    }
</style>
""", unsafe_allow_html=True)



st.sidebar.markdown('<img src="https://cdn-icons-png.flaticon.com/128/686/686700.png" width="20" style="vertical-align: middle;"> <span style="font-size: 24px; font-weight: light; margin-left: 10px;">Dashboard</span>', unsafe_allow_html=True)

st.markdown(
    """
    <style>
    body {
        background-color: #576D75; /* Green color */
    }
    .stApp {
        background-color: #18C3CC !important; /* Green color */
    }
    .sidebar .sidebar-content {
        background-color: #576D75 !important; /* Blue color */
    }
    .card-at {
        padding: 15px;
        background-color: #00BA38; /* Green color */
        color: #FFFFFF; /* White color */
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    .card-mt {
        padding: 15px;
        background-color: #FF9300; /* Orange color */
        color: #000000; /* Black color */
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    .card-ir {
        padding: 15px;
        background-color: #0079C2; /* Blue color */
        color: #FFFFFF; /* White color */
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    .card-dc {
        padding: 15px;
        background-color: #D90000; /* Red color */
        color: #FFFFFF; /* White color */
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    .card-ac {
        padding: 15px;
        background-color: #6200B3; /* Purple color */
        color: #FFFFFF; /* White color */
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
        unsafe_allow_html=True
    )

st.markdown("<p style='font-size: 35px; font-weight: light; font-family: Inter'>Interactive solar energy plotter</p>", unsafe_allow_html=True)


df_solar = read_plant_csv()
uarr = np.unique(df_solar.SOURCE_KEY)
options = list(uarr)
options.append('Delhi-India')
options.append('New York-US')
options.append('Colorado-US')
options.append('Canada')




def calculate_anomaly_growth(dates):

    
    start_date = date(2020, 5, 15)
    end_date = date(dates.year, dates.month, dates.day)      
    num_days = (dates - start_date).days

    if (end_date == start_date):
        return 29,71
    
    else:
        vegetation_percent = 0
        cracking_percent = 0
        # Define the input variables
        sigma = 1000.0 # or we can do int(input("enter the value"))
        T = 300.0 # or we can do int(input("enter the value"))
        R = 0.1 # or we can do int(input("enter the value"))
        environment = 13.6 # or we can do int(input("enter the value"))
        Delta_K = 126.0 # or we can do int(input("enter the value"))
        # Define the material-specific constants
        C = 0.0001
        n = 3.0
        A = 0.00001
        m = 2.5
        Q = 10000.0
        R_gas = 8.314
        p = 0.5
        C0 = 0.01
        q = 1.5

        vegetation_percent = ((5/100) * environment * (num_days +5))   # Example formula for vegetation growth
        cracking_percent = ((2/100) * Delta_K * (num_days +2))  # Example formula for cracking growth
        total = vegetation_percent + cracking_percent
        vegetation_percent = (vegetation_percent/total) * 100
        cracking_percent = (cracking_percent/total) * 100
        return vegetation_percent, cracking_percent

def total_power(Nc, It, A , N):
    E = Nc * It * A * N
    return E

Energy = total_power(49,273.15,44.67, 5)

def calculate_power_loss(vegetation_percent, cracking_percent, E):
    
    vegetation_loss = (E - (vegetation_percent * E /100))/10e3
    cracking_loss = (E - (cracking_percent * E/100))/10e3


    vegetation_loss = round(vegetation_loss, 1)
    cracking_loss = round(cracking_loss, 1)

    return vegetation_loss, cracking_loss


def calculate_anomaly_growth1(dates):

    start_date = date(2020, 5, 15)
    end_date = date(dates.year, dates.month, dates.day)
    num_days = (dates - start_date).days
    vegetation_percent = 5 + num_days  # Example formula for vegetation growth
    cracking_percent = 2 + num_days  # Example formula for cracking growth
    total = vegetation_percent + cracking_percent
    vegetation_percent = (vegetation_percent/total) * 100
    cracking_percent = (cracking_percent/total) * 100
    return vegetation_percent, cracking_percent

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot(dates, vegetation_loss, cracking_loss):
    date1 = date(dates.year, dates.month, dates.day)
    fig, ax = plt.subplots()

    # Define colors for bars
    bar_colors = ['lightblue', 'lightgreen']

    # Create the stacked bar chart
    ax.bar(['Anomalies'], [cracking_loss], color=bar_colors[0])
    ax.bar(['Anomalies'], [vegetation_loss], bottom=[cracking_loss], color=bar_colors[1])

    # Set plot labels and title
    ax.set_xlabel('Anomlaies', fontsize=12)
    ax.set_ylabel('Power Loss', fontsize=12)
    ax.set_title(f'Power Loss for {date1} in KW', fontsize=14)

    # Add grid lines
    ax.grid(axis='y', linestyle='--', linewidth=0.5)

    # Remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Customize tick labels
    ax.tick_params(axis='both', which='major', labelsize=10)

    fig.set_facecolor('#576D75')
    ax.set_facecolor('#576D75')
    plt.gca().set_facecolor('#576D75')

    ax.legend(['Cracking', 'Vegetation'])
    # Display plot using Streamlit
    st.pyplot(fig)



checkboxatt = "AMBIENT_TEMPERATURE"
dateselect = False

col1, col2 = st.columns([2,1], gap="medium")
with col1:
    st.markdown("<p style='font-size: 19px; color: white; font-weight: light; font-family: Inter;'>Parameters Selection: Choose the parameters</p>", unsafe_allow_html=True)


    col4,  col5, col6 = st.columns([1,1,1])
    with col4:
        at = st.checkbox("AMBIENT TEMPERATURE", value=False)
        mt = st.checkbox("MODULE TEMPERATURE", value=False)
        ac = st.checkbox("AC POWER", value=False)
        ir = st.checkbox("IRRADIATION", value=False)
        dc = st.checkbox("DC POWER", value=False)
        
        

    s1 = int(at)
    s2 = int(mt)
    s3 = int(ir)
    s4 = int(dc)
    s5 = int(ac)
    state = s1 + s2 + s3 + s4 + s5

    st.markdown("<p style='font-size:12px; color:White; font-weight:light; font-family: Inter;'>Selected Parameters:</p>", unsafe_allow_html=True)
    if s1:
        st.markdown("<div class='card-at'><span style='color:Black; font-family: Inter;'>AMBIENT TEMPERATURE</span></div>", unsafe_allow_html=True)
    if s2:
        st.markdown("<div class='card-mt'><span style='color:Black; font-family: Inter;'>MODULE TEMPERATURE</span></div>", unsafe_allow_html=True)
    if s3:
        st.markdown("<div class='card-ir'><span style='color:Black; font-family: Inter;'>IRRADIATION</span></div>", unsafe_allow_html=True)
    if s4:
        st.markdown("<div class='card-dc'><span style='color:Black; font-family: Inter;'>DC POWER</span></div>", unsafe_allow_html=True)
    if s5:
        st.markdown("<div class='card-ac'><span style='color:Black; font-family: Inter;'>AC</span></div>", unsafe_allow_html=True)

    with col5:
        st.markdown("<p style='font-size:19px; color:White; font-weight:light; font-family: Inter;'>Location selection</p>", unsafe_allow_html=True)
        choice = st.selectbox("Which location do you like to choose?", options, index=0)  # Update with your initial selection
        st.write('You selected:', choice)
    

    
    df_solar_subset = df_solar_plant_subset(df_solar, choice)
    solar_dc = df_solar_subset.pivot_table(values=[checkboxatt], index='TIME', columns='DATE')
    listdates = unique_dates_df(solar_dc)

    with col6:
        st.markdown("<p style='font-size:19px; color:White; font-weight:light; font-family: Inter;'>Date selection</p>", unsafe_allow_html=True)
        selected_dates = st.multiselect("Select dates", listdates)
        indices = [listdates.index(date) for date in selected_dates]
        dateselect = True   
        flag = 1
    
    if dateselect:
        placeholder = st.empty()
        with placeholder.container():

            if selected_dates:
                sd=selected_dates
                selected_dates = sorted(selected_dates)
                print(selected_dates)
                vegetation_growth, cracking_growth = calculate_anomaly_growth(selected_dates[len(selected_dates)-1])
                vg1,cg1 = calculate_anomaly_growth1(sd[len(sd)-1])
                vegetation_loss, cracking_loss = calculate_power_loss(vg1, cg1, Energy)
                flag1=1
            
                
            
            if s1 == 1:
                checkboxatt = "AMBIENT_TEMPERATURE"
                Daywise_plot_index(data=solar_dc, titles=checkboxatt, indices=indices, state=state, sd = selected_dates)

            if s2 == 1:
                checkboxatt = "MODULE_TEMPERATURE"
                Daywise_plot_index(data=solar_dc, titles=checkboxatt, indices=indices, state=state, sd = selected_dates)

            if s3 == 1:
                checkboxatt = "IRRADIATION"
                Daywise_plot_index(data=solar_dc, titles=checkboxatt, indices=indices, state=state, sd = selected_dates)

            if s4 == 1:
                checkboxatt = "DC_POWER"
                Daywise_plot_index(data=solar_dc, titles=checkboxatt, indices=indices, state=state, sd = selected_dates)

            if s5 == 1:
                checkboxatt = "AC_POWER"
                Daywise_plot_index(data=solar_dc, titles=checkboxatt, indices=indices, state=state, sd = selected_dates)

            if s1 == 0 and s2 == 0 and s3 == 0 and s4 == 0 and s5 == 0:
                Daywise_plot_index(data=solar_dc, titles=checkboxatt, indices=indices, state=state, sd = selected_dates)


    average_output = df_solar_subset.groupby('DATE')[checkboxatt].mean()
    total_output = df_solar_subset.groupby('DATE')[checkboxatt].sum()
    


    import streamlit as st

    # Define the container box CSS style
    container_style = "padding: 15px; border-radius: 5px; margin-bottom: 10px; color: #FFFFFF; font-weight: bold;"
    # Create the container boxes below the first row
    container1, container2, container3 = st.columns([1, 0.85, 0.85])


    with container1:
        st.write("Enter Price per Unit:")
        price_per_unit = st.number_input("Price", min_value=0.0, step=0.01)
        revenue_loss = price_per_unit * 34

        st.markdown(
            f'<div style="background-color: #146C94; {container_style} font-family: Inter;">'
            'Power Output in Assen<br>'
            f'<br>Anomaly loss 34KW<br>'
            f'Revenue loss ${revenue_loss}<br>',
            unsafe_allow_html=True
        )

with col2:
    # Create data for the pie chart
    labels = ['cracking growth', 'vegetation growth']
    sizes = [cracking_growth, vegetation_growth]
    colors = ['#FF9300', '#0079C2']

    # Add the pie chart
    
    st.markdown('<div style="padding: 15px; border-radius: 5px; background-color: #576D75; font-family: Inter;">', unsafe_allow_html=True)
    plt.figure(figsize=(10, 10))
    fig1, ax1 = plt.subplots()
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct=lambda pct: f'{pct:.1f}%\n({int(pct * np.sum(sizes) / 100)})', startangle=90)
    ax1.axis('equal')
    plt.title('Pie Chart showing anomaly percentage', color='black')
    fig1.set_facecolor('#576D75')
    ax1.set_facecolor('#576D75')
    plt.gca().set_facecolor('#576D75')
    
    # Customize the pie chart
    for text in texts:
        text.set_color('white')
    for autotext in autotexts:
        autotext.set_color('white')
    
    st.pyplot(fig1)
    st.markdown('</div>', unsafe_allow_html=True)

    # Add the histogram chart
    if flag1==1 :
        plot(sd[len(sd)-1], vegetation_loss, cracking_loss)
    

import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import os
# Google Sheets credentials
CREDS_FILE = 'carbon-vault-390017-c80904874e28.json'
SPREADSHEET_ID = '1aGpZWvwevazw0sQDjlHPFuE6o5j4jF_k5SM7pXph_YY'

def add_email_to_csv(email):
    file_exists = os.path.isfile("emails.csv")

    with open("emails.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Email"])
        writer.writerow([email])

def add_feedback_to_sheet(feedback):
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    sheet.append_row(feedback)


st.markdown("<p style='font-size: 24px; color: white; font-weight: light; font-family: Inter;'>Feedback</p>", unsafe_allow_html=True)
email = st.text_input("Enter your email for us to reach you out")
question1 = st.selectbox("How much will you rate the overall experience ? ", ["0 - 3", "4 - 6", "7 - 10"])
question2 = st.selectbox("How much will you rate the data visualization of the site ?", ["0 - 3", "4 - 6", "7 - 10"])
question3 = st.selectbox("Was all your needs satisfied ", ["Yes, totally.", "Could have been better.", "Not really"])

if st.button("Submit Feedback"):
    feedback = [email, question1, question2, question3]
    add_feedback_to_sheet(feedback)
    st.success("Feedback has been stored!")