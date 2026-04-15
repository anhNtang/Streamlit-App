import streamlit as st
import pandas as pd
from PIL import Image 
from streamlit_option_menu import option_menu # additional library 
import plotly.express as px
import plotly.graph_objects as go 
import gdown 

def load_data():
    url = "https://drive.google.com/uc?id=1MUXTLZzmqlbVdLy_Nn2tjgzEVeCXdxCCGySoVmgL_V8"
    output = "data.csv" 
    gdown.download(url, output, quiet=False)
    return pd.read_csv(output, on_bad_lines="skip") 


def get_medal_counts(df, group_by_column):
    return df.groupby([group_by_column])['Medal'].value_counts().unstack(fill_value=0)

# Part 4: Create an option menu 
with st.sidebar:
    selected = option_menu(
        menu_title="Main menu", 
        options=["Home", "Data", "Graph"], 
        icons=["house", "database", "bar-chart"]
    )
    
if selected == "Home":
    # Part 1: Title, header and subheader, text and text input 
    st.title("Olympics Guide App")

    st.header("Welcome!👋")
    name = st.text_input("What's your name?")  # Create a text input box for user to enter their name 

    st.subheader("Introduction")
    st.text("The Olympic Games are an international competition where individual athletes and teams compete for their home country.")

    # Part 2: Add images 
    img = Image.open("olympics_logo.png")
    st.image(img)

    # Part 3: Use columns to organize layout 
    col1, col2 = st.columns(2) 

    with col1:
        if st.button("Show Greeting"):
            st.success(f"Hello there {name.title()}!")
    with col2: 
        if st.button("Click me for no reason!"):
            st.balloons()
if selected == "Data":
    st.header("Data")

    # Load data 
    df = load_data()

    # Part 5: Create a selection box 
    sport_list = sorted(df["Sport"].unique().tolist())
    options = ["All sports"] + sport_list # This includes the all sports option 
    selected_sport = st.selectbox("What is your favorite sport?", options, help="Pick one sport at a time or explore all by selecting All sports.") # Add tooltip 

    # Filter data based on sport filter selection 
    if selected_sport == "All sports":
        df_filtered = df
    else:
        df_filtered = df[df["Sport"] == selected_sport]

    st.write(df_filtered)
    st.link_button("Data Source", "https://www.kaggle.com/datasets/harshvgh/olympics")  # Add a link 
if selected == "Graph":

    # Create an interactive bar graph with Plotly 
    data = load_data()

    st.subheader("Global Medal Counts By Year Range (Choose Range)")

    year_filter = st.slider(
        "Year Range",
        int(data['Year'].min()),
        int(data['Year'].max()),
        (int(data['Year'].min()), int(data['Year'].max()))
    )

    filtered_data = data[
        (data['Year'] >= year_filter[0]) &
        (data['Year'] <= year_filter[1])
    ]

    # Aggregate medal counts 
    medal_counts = get_medal_counts(filtered_data, 'Team').reset_index()

    # Handle missing values 
    for col in ['Gold', 'Silver', 'Bronze']:
        if col not in medal_counts.columns:
            medal_counts[col] = 0

    medal_counts['Total'] = medal_counts[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    # Top 20 countries with the highest medal count 
    top_countries = medal_counts.sort_values(by='Total', ascending=False).head(20)
    st.subheader("Top 20 Countries by Total Medals")

    fig = px.bar(
        top_countries,
        x='Total',
        y='Team',
        orientation='h',
        title="Top 20 Countries by Total Medals",
        color='Team',
        color_discrete_sequence=px.colors.qualitative.Prism
    )

    fig.update_layout(showlegend=False, height=600)

    st.plotly_chart(fig)


# Add additional elements to sidebar
st.sidebar.subheader("Olympics", divider="rainbow")
with st.sidebar:
    img2 = Image.open("logo.png")
    st.image(img2, use_container_width=True)




