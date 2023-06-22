import pandas as pd


def read_plant_csv():
    generation_data=pd.read_csv("data/powerData/Plant_1_Generation_Data.csv")
    weather_data=pd.read_csv("data/powerData/Plant_1_Weather_Sensor_Data.csv")
    generation_data['DATE'] = pd.to_datetime(generation_data['DATE_TIME']).dt.date
    generation_data['TIME'] = pd.to_datetime(generation_data['DATE_TIME']).dt.time
    weather_data['DATE'] = pd.to_datetime(weather_data['DATE_TIME']).dt.date
    weather_data['TIME'] = pd.to_datetime(weather_data['DATE_TIME']).dt.time
    del generation_data['DATE_TIME']
    del weather_data['DATE_TIME']
    weather_data['DATE_TIME'] = weather_data["DATE"].astype(str) + " " + weather_data["TIME"].astype(str)
    generation_data['DATE_TIME'] = generation_data["DATE"].astype(str) + " " + generation_data["TIME"].astype(str)
    gd1=generation_data
    del gd1['DATE']
    del gd1['TIME']
    # gd1['DATE_TIME'] =  pd.to_datetime(gd1['DATE_TIME'], format='%Y-%m-%d')
    gd1['DATE_TIME'] = pd.to_datetime(gd1['DATE_TIME'], format='%Y-%m-%d %H:%M:%S')
    wd1=weather_data
    del wd1['DATE']
    del wd1['TIME']
    # wd1['DATE_TIME'] =  pd.to_datetime(wd1['DATE_TIME'], format='%Y-%m-%d')
    wd1['DATE_TIME'] = pd.to_datetime(wd1['DATE_TIME'], format='%Y-%m-%d %H:%M:%S')
    df_solar = pd.merge(gd1.drop(columns = ['SOURCE_KEY', 'PLANT_ID']), wd1, on='DATE_TIME')
    df_solar["DATE"] = pd.to_datetime(df_solar["DATE_TIME"]).dt.date
    df_solar["TIME"] = pd.to_datetime(df_solar["DATE_TIME"]).dt.time
    df_solar['DAY'] = pd.to_datetime(df_solar['DATE_TIME']).dt.day
    df_solar['MONTH'] = pd.to_datetime(df_solar['DATE_TIME']).dt.month
    # df_solar['WEEK'] = pd.to_datetime(df_solar['DATE_TIME']).dt.week
    df_solar['WEEK'] = pd.to_datetime(df_solar['DATE_TIME']).dt.isocalendar().week

# add hours and minutes for ml models
    df_solar['HOURS'] = pd.to_datetime(df_solar['TIME'],format='%H:%M:%S').dt.hour
    df_solar['MINUTES'] = pd.to_datetime(df_solar['TIME'],format='%H:%M:%S').dt.minute
    df_solar['TOTAL MINUTES PASS'] = df_solar['MINUTES'] + df_solar['HOURS']*60
    
# add date as string column
    df_solar["DATE_STRING"] = df_solar["DATE"].astype(str) # add column with date as string
    df_solar["HOURS"] = df_solar["HOURS"].astype(str)
    df_solar["TIME"] = df_solar["TIME"].astype(str)
    print(np.unique(df_solar['SOURCE_KEY']))
    return df_solar
    
def df_solar_plant_subset(df_solar, choice):
    
    df_subset = df_solar[(df_solar["SOURCE_KEY"]== choice)]
    
    return df_subset


def Daywise_plot(data=None, row=None, col=None, title=None):
    cols = data.columns
    fig, axes = plt.subplots(nrows=row, ncols=col, figsize=(20, 40))
    fig.suptitle(title, fontsize=25, fontweight='bold', y=0.9)

    # Define gradient colors
    gradient = np.linspace(0, 1, 256)
    colors = plt.cm.PuRd(gradient)

    for i, col_name in enumerate(cols):
        ax = axes.flatten()[i]

        # Add gradient background to plot
        ax.set_facecolor(colors[i])

        data[col_name].plot(ax=ax, color='black')
        ax.set_title(col_name, fontsize=18, color='black')
        ax.set_xlabel('Time', fontsize=14, color='black')
        ax.set_ylabel('Data', fontsize=14, color='black')

    fig.tight_layout(pad=5.0)
    st.pyplot(fig)





import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


import seaborn as sns

def Daywise_plot_index(data=None, titles=None, indices=None, state=0, top_n=5, sd=None):
    if state == 0:
        st.markdown("<h1 style='text-align: center; color: #00BA38; font-family: Arial, sans-serif;'></h1>", unsafe_allow_html=True)
    else:
        cols = data.columns

        # Create a figure and axes for the line charts
        fig, ax = plt.subplots(figsize=(8, 2.5))

        # Set the Seaborn style and color palette
        sns.set(style='darkgrid')
        sns.set_palette("pastel")

        # Plot line charts for each date with different colors and labels
        for title, index in zip(titles, indices):
            # Replace NaN values with zeros
            data_cleaned = data[cols[index]].fillna(0)

            # Define a color for the line chart
            color = sns.color_palette()[index]

            # Plot line chart with specific color and label
            sns.lineplot(data=data_cleaned, ax=ax, color=color, label=title)

        ax.set_title('Day/Days Output', fontsize=12, fontweight='bold', color='#00BA38')
        ax.set_xlabel('Time', fontsize=12, color='white')
        if titles=="MODULE_TEMPERATURE":
            titles = "Module temperature"
        if titles=="AMBIENT_TEMPERATURE":
            titles = "Ambient temperature"
        if titles=="AC_POWER":
            titles = "AC power "
        if titles=="DC_POWER":
            titles = "DC power"
        if titles=="IRRADIATION":
            titles = "Irradiation"
            
        ax.set_ylabel(titles+"  percentage", fontsize=8, color='white')
        ax.tick_params(axis='both', labelsize=12, colors='white')
        fig.set_facecolor('#012B36')
        ax.set_facecolor('#012B36')

        # Adjust x-axis labels
        ax.xaxis.set_major_locator(plt.MaxNLocator(6))  # Set maximum number of x-axis labels to 6

        # Convert datetime objects to string format
        string_list = [dt.strftime('%Y-%m-%d %H:%M') for dt in sd]

        # Adjust grid color
        ax.grid(color='lightgray')
        print(indices)
        # Adjust legend properties
        legend_labels = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        for text, date in zip(legend_labels.get_texts(), string_list):
            date_label = date.split()[0]
            text.set_text(date_label)  # Set the legend label to the corresponding date
            text.set_fontsize(8)
            text.set_color('black')
        legend_labels.get_frame().set_facecolor('white')
    
        # Use a dark background with white grid lines
        plt.style.use('dark_background')

        # Display the plot
        st.pyplot(fig)




        


def unique_dates_df(data):
    cols = data.columns
    listdates=[]
    for i in range(1, len(cols)+1):
        listdates.append([*cols[i-1]][1])
    return listdates

# Create a pivot table of the solar energy output data
    solar_heatmap = df_solar_subset.pivot_table(values=[checkboxatt], index='DATE_TIME', columns='DATE')


    # Create a heatmap of the solar energy output
    st.subheader("Solar Energy Output Heatmap")
    plt.figure(figsize=(6, 2))
    heatmap=sns.heatmap(solar_heatmap, cmap='YlGnBu')

    fig = plt.gcf()
    fig.set_facecolor('#576D75')

    # Set the facecolor of the axes
    plt.gca().set_facecolor('#012B36')
    # Adjust font size of axis labels and tick labels
    heatmap.set_xlabel("Date", fontsize=4)
    heatmap.set_ylabel("Time", fontsize=4)
    heatmap.tick_params(axis='both', which='both', labelsize=4)

    # Display the plot
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

    