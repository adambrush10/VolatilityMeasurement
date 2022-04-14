from volFuncs import *




st.set_page_config(layout="wide")


projectlist = ["Ethereum", "Bitcoin","Cardano","DogeCoin","PolkaDot","Avalanche","Solana","Litecoin","Zcash"]

st.title("Volatility in Crypto")


st.text("Analyze Volatility and Log Returns for Crypto protocols.")
st.text("Select a Protocol and a Time range to view various Statistics illustrating the volatility of the selected protocol during a specific time range. ")
#st.text("Select a Protocol and a Time range to view various Statistics illustrating the volatility of the selected protocol during a specific time range. ")

col1, col2 = st.columns([1,5,])

with col1:
    st.write("Input Search Criteria Below")
    slct = st.selectbox(
    'Select Protocol', projectlist)
    option = get_key(slct)

    date1 = st.date_input('start date', datetime(2022,1,1))
    st.write(date1)

    date2 = st.date_input('end date', datetime(2022,4,9))
    st.write(date2)

    st.metric(label="Average Daily Volatility", value= DAILYavgVol(json_to_df(cryptowatchAPIcall(option, to_timestamp(date1), to_timestamp(date2)))))
    st.write(f'Over a period of {daycount(cryptowatchAPIcall(option, to_timestamp(date1), to_timestamp(date2)))} days')

    st.metric(label="Volatility Score", value=VolScore(json_to_df(cryptowatchAPIcall(option, to_timestamp(date1), to_timestamp(date2)))), delta=123,
     delta_color="off")

with col2:
    
    st.plotly_chart(RollingVolCrypto_MONTH(json_to_df_WEEK(cryptowatchAPIcallWEEK(option, to_timestamp(date1), to_timestamp(date2)))), use_container_width=True)

    st.plotly_chart(lineChart(json_to_df_WEEK(cryptowatchAPIcallWEEK(option, to_timestamp(date1), to_timestamp(date2)))), use_container_width=True, use_container_height=False)

    st.plotly_chart(logLinechart(json_to_df(cryptowatchAPIcall(option, to_timestamp(date1), to_timestamp(date2)))), use_container_width=True)
    
    st.plotly_chart(histologs(json_to_df_WEEK(cryptowatchAPIcallWEEK(option, to_timestamp(date1), to_timestamp(date2)))), use_container_width=True)

    