import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime
 
# storing the current time in the variable
m = datetime.now().month
datemap = {1: 'styczeń',
           2:	'luty',
           3:'marzec',
           4:'kwiecień',
           5:'maj',
           6:'czerwiec',
           7:'lipiec',
           8:'sierpień',
           9:'wrzesień'
}
month_now = [v for k, v in datemap.items() if m == k]
custom_colors = ['#FF9999', '#FFCC99', '#FFFF99', '#99FF99']

st.set_page_config(page_title='Sales Dashboard',
                   page_icon=':bar_char:',
                   layout='wide')

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io = 'dash_budget.xlsx',
        engine='openpyxl',
        sheet_name='total_analise',
        skiprows=0,
        usecols='A:K',
        nrows=13
    )
    savings = pd.read_excel(
        io = 'dash_budget.xlsx',
        engine='openpyxl',
        sheet_name='savings',
        skiprows=0,
        usecols='J:L',
        nrows=2
    )

    return df, savings

df = get_data_from_excel()[0].dropna()
savings = get_data_from_excel()[1]

# ---- SIDEBAR ---- 

st.sidebar.header('Please Filter Here:')
month = st.sidebar.multiselect(
    'Select the Month:',
    options=df['month'].unique(),
    default=month_now
)

df_selection = df.query(
    'month == @month '
)



# ----- MAIN PAGE ------
st.title(' :bar_chart: Financial Dashboard')
st.markdown('##')



# TOP KPI's
month_income = int(df_selection['income'].sum())
#total_spendings = int(df_selection['spendings'].sum())
save = savings['save']
come_soon = savings['come_soon']
total_savings = save + come_soon
to_pay = savings['to_pay']
now_month_balance = df.loc[df['month'] == month_now[0], 'balance'].values[0]
now_month_income = df.loc[df['month'] == month_now[0], 'income'].values[0]
now_month_spendings = df.loc[df['month'] == month_now[0], 'spendings'].values[0]

# income by category in current month


st.markdown('<h1 style="background-color:#363062; color:#F5E8C7;"> Current month stats: </h1>', unsafe_allow_html=True)
st.markdown('---')
l_column, m_column, r_column = st.columns(3)
with l_column:
    st.subheader(f'{month_now[0].title()} Income:')
    st.subheader(f'{now_month_income} ZŁ')
with m_column:
    st.subheader(f'{month_now[0].title()} Spendings:')
    st.subheader(f' {now_month_spendings} ZŁ')
with r_column:
    st.subheader(f'Left from {month_now[0].title()}:🤑')
    st.subheader(f' {now_month_balance} ZŁ')
st.markdown('---')

st.markdown('<h1 style="background-color:#363062; color:#F5E8C7;"> Other stats: </h1>', unsafe_allow_html=True)

st.markdown('---')

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader('Total :green[Savings]:🤑')
    st.subheader(f' {total_savings[0]} ZŁ')
with middle_column:
    st.subheader('To Pay:💸')
    st.subheader(f' {to_pay[0]} ZŁ ')
with right_column:
    st.subheader('Selected Month Income:')
    st.subheader(f' {month_income} ZŁ') # do poprawy

st.markdown('---')

# Income BY MONTH [BAR CHART]
inc_by_mth = df['income']
fig_inc_by_mth = px.bar(
    inc_by_mth,
    x=df['month'],
    y='income',
    title='<b>Income By Month</b>',
    color_discrete_sequence=custom_colors * len(inc_by_mth),
    template='plotly_white',
)
fig_inc_by_mth.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=False)),
    xaxis_title="month"
)

# Spending BY Month[BAR CHART]
fig_product_sales = px.bar(
    df['spendings'],
    x=df['month'],
    y='spendings',
    title='<b>Spending by month</b>',
    color_discrete_sequence=['#0083B8'] * len(df['spendings']),
    template='plotly_white'
)
fig_product_sales.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=(dict(showgrid=False)),
    xaxis_title="month"
)

# preparing df to use Pie chart
df_melted = df_selection.melt(id_vars=['month', 'income'], 
                    value_vars=['total_K','total_D','total_passive'],
                    var_name='category', 
                    value_name='income_by_cat')
df_melted_spend = df_selection.melt(id_vars=['month', 'spendings'], 
                    value_vars=['spend_other', 'spend_bils', 'spend_food', 'spend_fuel'],
                    var_name='category', 
                    value_name='spendings_by_cat')


#------INCOME BY CATEGORY {PIE CHART}------
fig_inc_by_cat = px.pie(
    df_melted, names='category', values='income_by_cat', title=f' Income by category in selected Month', color_discrete_sequence=custom_colors
)
fig_sp_by_cat = px.pie(
    df_melted_spend, names='category', values='spendings_by_cat', title=f' Spend by category in selected Month'
)


left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_inc_by_mth)
right_column.plotly_chart(fig_product_sales)
#Pie charts display
st.markdown('---')
left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_inc_by_cat)
right_column.plotly_chart(fig_sp_by_cat)

#HIDE STREAMLIT STYLE
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Example of setting custom colors in Markdown
st.markdown('<p style="color:#FF5733;">This is a paragraph with custom color.</p>', unsafe_allow_html=True)
st.markdown('<h1 style="color:#33FF57;">This is a heading with custom color.</h1>', unsafe_allow_html=True)
st.markdown('<p style="background-color:#3357FF; color:#FFFFFF;">This is a paragraph with a custom background color.</p>', unsafe_allow_html=True)

# Display styled DataFrame in Streamlit
st.dataframe(df_selection)