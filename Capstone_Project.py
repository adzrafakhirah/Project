import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import geopandas as gpd
import json
import altair as alt

dataset = pd.read_csv('dataset.csv')
alldataset = pd.read_csv('all dataset.csv')
all_listings = pd.read_csv('all listings.csv')
reviews_18 = pd.read_csv('reviews 2018 - 2023.csv')

# Convert 'date' column to datetime type
dataset['date'] = pd.to_datetime(dataset['date'])


dataset = dataset.assign(roomtype_neighbourhood= dataset['room_type'] + ' // ' + dataset['neighbourhood'], 
                         host_roomtype=dataset['host_name'] + ' // ' + dataset['room_type'],
                         host_neighbourhood=dataset['host_name'] + ' // ' + dataset['neighbourhood'])

dataset = dataset.assign(property_neighbourhood= dataset['neighbourhood'] + ' // ' + dataset['name'])

st.set_page_config(
    page_title="Airbnb Bangkok, Thailand: Exploratory Dashboard",
    layout='wide'
)

st.markdown("<h6 style='text-align: center;'>Adzra Fakhirah's Capstone Project</h6>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Analisis Penyewaan Properti Airbnb di Bangkok, Thailand</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>(2018 - 2023)</h2>", unsafe_allow_html=True)
st.header("")

#column 1
a1,a2 = st.columns(2)
with a1:
    st.image('airbnb.jpg')
with a2:
    st.markdown("**:red[Airbnb merupakan marketplace online penyedia jasa sewa penginapan]** yang memungkinkan pengguna mendaftarkan atau menyewa propertinya yang dapat berupa private room, apartemen, rumah, hotel, sharing room, dan properti pribadi lainnya.")
    st.markdown("Saat perjalanan terus pulih **:red[pasca-pandemi, property yang dipesan di Thailand melalui Airbnb naik lebih dari dua kali lipat]** tahun lalu sejak tahun 2020, dengan perjalanan internasional memimpin dan **:red[Bangkok muncul sebagai destinasi pilihan teratas bagi traveler global di Airbnb.]** Ibu kota yang populer ini muncul sebagai tujuan paling populer secara global untuk tamu Airbnb pada Q3 tahun 2022 dan kelima dalam daftar tempat perjalanan global paling populer di Airbnb pada tahun 2023.")
    st.markdown("Banyaknya jumlah property yang disewakan pada Airbnb tentunya dapat membingungkan penyewa dalam memilih tempat penyewaan yang tepat. **:red[Tempat penyewaan yang tepat berpengaruh terhadap tingginya kegiatan penyewaan]**, maka dari itu analisis ini dilakukan untuk **:red[membantu penyewa agar bisa mendapatkan keuntungan maksimal]** dari hasil kegiatan penyewaan properti di Airbnb yang akan dilakukan.")

   
#Trend 1
# Membuat data rata-rata review per tahun
reviews_ay = dataset.groupby('reviews_year').agg(avg_review=('date', lambda x: int(len(x) / len(x.dt.month.unique())))).reset_index()

# Chart trend rata-rata review per tahun
fig_ay = alt.Chart(reviews_ay).mark_line(point=alt.MarkConfig(color="#ff5a5f"), strokeWidth=3,color="#ff5a5f").encode(
    x=alt.X('reviews_year:O',title='Tahun'), # type: ignore
    y=alt.Y('avg_review', title='Rata-rata Jumlah Review'), # type: ignore
    tooltip=['reviews_year', 'avg_review']
).properties(
    title='Trend Rata-rata Jumlah Penyewaan per Tahun (2018 - 2023)',
    width=600,
    height=400
).configure_title(
    fontSize=20,
    font='century gothic'
).configure_axis(
    labelFontSize=13,
    titleFontSize=13,
    labelFont='century gothic',
    titleFont='century gothic'
).configure_axisX(
    labelAngle=0
)


#Trend 2
# Membuat data rata-rata review per bulan
reviews_m = dataset.groupby('reviews_month').agg(jumlah_review=('date', 'count')).reset_index()
reviews_m = reviews_m.sort_values('reviews_month')
reviews_m.head()
# Chart trend rata-rata review per bulan
fig_m = alt.Chart(reviews_m).mark_line(point=alt.MarkConfig(color="#ff5a5f"), strokeWidth=3,color="#ff5a5f").encode(
    x=alt.X('reviews_month:O', title='Bulan-Tahun'),
    y=alt.Y('jumlah_review', title='Jumlah Review'),
    tooltip=['reviews_month', 'jumlah_review']
).properties(
    title='Trend Penyewaan per Bulan (2018-01 s/d 2023-03)',
    width=600,
    height=400
).configure_title(
    fontSize=20,
    font='century gothic'
).configure_axis(
    labelFontSize=13,
    titleFontSize=13,
    labelFont='century gothic',
    titleFont='century gothic'
).configure_axisX(
    labelAngle=0
)

fig_m.configure_line(
    color='#ff5a5f',
    size=3
).configure_point(
    color='#ff5a5f',
    size=8
)



# Select box 1
st.header("Trend Jumlah Penyewaan Airbnb Bangkok, Thailand")
options = ['Trend Rata-rata Penyewaan per Tahun','Trend Penyewaan per Bulan']
factor_group = st.selectbox("", options, key="factor_group")
if factor_group == 'Trend Rata-rata Penyewaan per Tahun':
   st.altair_chart(fig_ay,use_container_width=True)
   st.markdown("Pada **:red[tahun 2020 hingga 2021]** Airbnb Bangkok, Thailand **:red[mengalami penurunan jumlah penyewaan yang sangat tajam]**. Hal ini dikarenakan **:red[terjadinya pandemi Covid-19]** yang melanda seluruh dunia **:red[pada awal tahun 2020 dan diberlakukannya lockdown]** sehingga hal ini berdampak pula pada sektor bisnis yang ada di Bangkok, Thailand. Akan tetapi dapat dilihat bahwa **:red[pasca pandemi rata-rata jumlah penyewaan per tahunnya mengalami peningkatan yang sangat signifikan]** dan **:red[puncaknya berada di tahun 2023]**, jumlah ini bahkan melebihi jumlah penyewa sebelum pandemi. Jumlah penyewa yang meningkat ini ternyata sejalan dengan meningkatnya jumlah wisatawan yang datang ke Thailand di kuartal pertama tahun 2023.")
elif factor_group == 'Trend Penyewaan per Bulan':
   st.altair_chart(fig_m,use_container_width=True)
   st.markdown("Berdasarkan trend penyewaan per bulan, **:red[pada saat sebelum dan sesudah pandemi dapat dilihat bahwa setiap tahunnya terdapat pola fluktuatif yang terus terjadi]** dan hampir selalu sama setiap tahunnya. Pada bulan **:red[Juni - Agustus dan November - Januari selalu mengalami peningkatan]** jumlah penyewaan dikarenakan bertepatan dengan musim panas dan musim dingin dimana banyak negara yang memiliki liburan sekolah di kedua musim tersebut, serta musim liburan akhir tahun, dan diskon promosi akhir tahun. Sedangkan pada bulan **:red[Januari - Mei dan September - Oktober hampir selalu mengalami penurunan]** mungkin dikarenakan sudah masuk masa pasca-liburan sehingga orang-orang sudah mulai sibuk sekolah dan bekerja, serta merupakan musim peralihan dengan cuaca yang tidak menentu.")




# Map 1
# Membuat dataset Lokasi properti beserta Jumlah Review dan Properti
maps_listing = all_listings.groupby('neighbourhood').agg(
latitude=('latitude', 'first'),
longitude=('longitude', 'first'),
total_listing=('id', 'nunique')
).reset_index().sort_values('total_listing', ascending=False)
# Maps Geojson
with open('neighbourhoods.geojson') as f:
    geojson_data = json.load(f)
df_geojson = pd.json_normalize(geojson_data['features'])
merged_df = df_geojson.merge(maps_listing, left_on='properties.neighbourhood', right_on='neighbourhood', how='inner')
fig_maplisting = px.choropleth_mapbox(merged_df, geojson=geojson_data, color='total_listing', labels={'total_listing':'Jumlah Properti'},
                           locations='neighbourhood', featureidkey='properties.neighbourhood',
                           mapbox_style='carto-positron', zoom=8.9,
                           center={'lat': merged_df['latitude'].mean(), 'lon': merged_df['longitude'].mean()},
                           opacity=0.7,
                           color_continuous_scale= ["#fff3e6","#fdbdc4","#fa87a1","#f8517f","#f51b5c"])
fig_maplisting.update_layout(margin={'r': 0, 't': 40, 'l': 0, 'b': 0})

#MAP 2
# Membuat dataset Lokasi Distrik beserta Jumlah Review
maps = dataset.groupby(['neighbourhood', 'latitude', 'longitude']).agg(
Jumlah_Review=('date', 'count')
).reset_index().sort_values('Jumlah_Review', ascending=False)
# Membuat visualisasi peta jumlah review per distrik dengan heatmap menggunakan plotly.graph_objects
fig_hmr = go.Figure(go.Densitymapbox(
lat=maps['latitude'],
lon=maps['longitude'],
z=maps['Jumlah_Review'],
radius=10,
colorscale='Plasma',
hovertemplate='<b>Latitude:</b> %{lat}<br><b>Longitude:</b> %{lon}<br><b>Jumlah Review:</b> %{z}<extra></extra>'
))

fig_hmr.update_layout(
mapbox_style='open-street-map',
mapbox_zoom=9,
mapbox_center={'lat': maps['latitude'].mean(), 'lon': maps['longitude'].mean()},
margin={'r': 0, 't': 40, 'l': 0, 'b': 0},
height=500
)



# Tab 1
a3,a4 = st.columns(2)
with a3:
   st.header("Peta Jumlah Properti per Distrik")
   st.plotly_chart(fig_maplisting)

with a4:
   st.header("Peta Jumlah Review per Distrik")
   st.plotly_chart(fig_hmr)
st.markdown("Berdasarkan kedua peta di atas terkait **:red[jumlah property dan jumlah penyewaan]** yang dipetakan berdasarkan distrik, didapatkan bahwa keduanya **:red[terkonsentrasi di sekitar pusat kota Bangkok]**. Adapun **:red[top 6 besar distriknya]**  yaitu **:red[Vadhana, Khlong Toei, Huai Khwang, Ratchadewi, Sathon, dan Bang Rak]***. Berdasarkan hal tersebut dapat kita simpulkan bahwa **:red[penyewa lebih berminat untuk menyewa property di sekitaran pusat kota]** dan property yang disewakan pun banyak juga tersebar di sana. Hal ini dikarenakan penyewa akan lebih efisien dan tidak banyak menghabiskan waktu di jalan apabila menginap di sekitar pusat kota, karena **:red[pada pusat kota terdapat banyak tempat yang wajib dikunjungi oleh para wisatawan]** seperti Siam Square, Benjakitti Forest Park, Samyan Mitrtown, Mahanakhon Skywalk dan masih banyak lagi destinasi wisata lainnya di pusat kota Bangkok. ")
st.markdown("_:orange[* = Urutan berdasarkan jumlah property, pada jumlah penyewaan top 6 nya juga sama hanya berbeda urutan]_")


# Distrik 1
# Membuat dataset Distrik beserta Jumlah Review dan Properti
jrd = dataset.groupby('neighbourhood').agg(jumlah_review=('date', 'count'), total_listing=('id', 'nunique')).reset_index().rename(columns={'neighbourhood': 'Distrik'}).sort_values('jumlah_review', ascending=False)
# Membuat Chart Jumlah Review per Distrik
fig_jrd = px.bar(jrd, y='Distrik', x='jumlah_review', color='Distrik', orientation='h',
                template='plotly_white', color_discrete_sequence=px.colors.qualitative.Pastel)
fig_jrd.update_layout(
    title='<b>Distribusi Jumlah Review per Distrik</b>',
    title_font=dict(size=20, family='Century Gothic', color="#FF6969"),
    xaxis=dict(title="<b>Jumlah Review</b>", title_font=dict(size=13, family='Century Gothic')),
    yaxis=dict(title="<b>Distrik</b>", title_font=dict(size=13, family='Century Gothic')),
    xaxis_side="top",
    margin=dict(t=130, l=150),
    font_family="Century Gothic"
)

# Distrik 2
# Top 5 Neighbourhood
rent_trend_N = dataset.groupby('neighbourhood')['date'].count().reset_index() 
rent_trend_N.rename(columns= {'date':'jumlah_review'}, inplace=True)
rent_trend_N = rent_trend_N.sort_values(by='jumlah_review', ascending=False).reset_index(drop=True)
top5n = rent_trend_N.head(5)
others_count = rent_trend_N['jumlah_review'].iloc[5:].sum()
others = pd.DataFrame({'neighbourhood': ['Others'], 'jumlah_review': [others_count]})
top5nOthers = pd.concat([top5n, others])
# Membuat chart Top 5 Neighbourhood
fig_pie_RTN = px.pie(top5nOthers,values="jumlah_review",color="neighbourhood", names="neighbourhood",color_discrete_sequence=["#89375F","#D14D72","#E98EAD","#FEA1BF","#FFC6D3","lightgrey"], hole=0.5)
fig_pie_RTN.update_layout(title="<b>Presentase Jumlah Review per Distrik</b>", title_font=dict(size=20,family='century gothic',color="#FF6969"), paper_bgcolor="white", legend=dict(orientation="v", xanchor="right", x=1.8), legend_font=dict(family='century gothic'))
fig_pie_RTN.update_traces(textposition="outside", textfont=dict(color="black", size=13,family='century gothic'),textinfo="label+percent", pull=[0.1,0,0,0,0,0,0,0,0,0,0.1])

#Roomtype 1
# Membuat data Room Type yang paling banyak di sewa selama 2018-2023
mostlistings_RT = dataset.groupby('room_type')['date'].count().reset_index() 
mostlistings_RT.rename(columns= {'date':'jumlah_review'}, inplace=True)
mostlistings_RT = mostlistings_RT.sort_values(by='jumlah_review', ascending=False).reset_index(drop=True)
# Membuat Chart Roomtype Most Rent 2018-2023
fig_pie_mr = px.pie(mostlistings_RT,values="jumlah_review",color="room_type", names="room_type",color_discrete_sequence=["#89375F","#D14D72","#E98EAD","#FEA1BF","#FFC6D3","lightgrey"], hole=0.5)
fig_pie_mr.update_layout(title="<b>Presentase Jumlah Review per Room Type</b>", title_font=dict(size=20,family='century gothic',color="#FF6969"), paper_bgcolor="white", legend=dict(orientation="v", xanchor="right", x=1.5), legend_font=dict(family='century gothic'))
fig_pie_mr.update_traces(textposition="outside", textfont=dict(color="black", size=13,family='century gothic'),textinfo="label+percent", pull=[0.1,0,0,0],rotation=480)

#Roomtype 2
# Membuat data trend review average roomtype per year
room_type_year_avg = dataset.groupby(['reviews_year', 'room_type']).agg(avg_review=('date', lambda x: x.count() / x.dt.month.nunique())).reset_index()
room_type_year_avg = room_type_year_avg.sort_values(['reviews_year', 'avg_review'], ascending=[True, False])
room_type_year_avg.head()
# Membuat chart
fig_RTYA_line = px.line(room_type_year_avg,x="reviews_year",y="avg_review",color="room_type",labels={'room_type': 'Room Type'},template="simple_white",color_discrete_sequence=["#D14D72","#E98EAD","#FEA1BF","#FFC6D3","#FEF2F4"], markers=True)
fig_RTYA_line.update_layout(title="<b>Trend Rata-rata Jumlah Review pada Room Type per Tahun (2018 - 2023)</b>", title_font=dict(size=20,family='century gothic',color="#FF6969"),legend_font=dict(family='century gothic'))
fig_RTYA_line.update_xaxes(title="<b>Tahun</b>",title_font=dict(size=13,family='century gothic'))
fig_RTYA_line.update_yaxes(title="<b>Rata-rata Jumlah Review</b>",title_font=dict(size=13,family='century gothic'))
fig_RTYA_line.update_traces(line=dict(width=3),marker=dict(size=8))

#Roomtype 3
# Data Top 5 Jumlah Review per Room Type per Distrik
ng_RT = dataset.groupby(['neighbourhood', 'room_type'])['date'].count().reset_index()
ng_RT = ng_RT.sort_values('date', ascending=False)
top_5_neighbourhoods = ng_RT.groupby('neighbourhood')['date'].sum().nlargest(5).reset_index()
top_5_neighbourhoods = pd.merge(top_5_neighbourhoods, ng_RT, on='neighbourhood')
# Membuat Chart Top 5 Room Type per Distrik dengan Jumlah Review Terbanyak
fig_top5_rtn = px.bar(top_5_neighbourhoods, y='neighbourhood', x='date_y', color="room_type", barmode='group', orientation='h', template='plotly_white', labels={'room_type':'Room Type'}, color_discrete_sequence=["#D14D72","#E98EAD","#FEA1BF","#FFC6D3","#FEF2F4"])
fig_top5_rtn.update_layout(title='<b>Top 5 Room type per Distrik</b>', title_font=dict(size=20,family='century gothic',color="#FF6969"), legend_font=dict(family='century gothic'))
fig_top5_rtn.update_xaxes(title="<b>Room type</b>",title_font=dict(size=13,family='century gothic'))
fig_top5_rtn.update_yaxes(title="<b>Jumlah Review</b>",title_font=dict(size=13,family='century gothic'))


# Select box 2 dan 3
st.header("Jumlah Review")
b1,b2 = st.columns(2)
with b1:
    st.subheader("Distrik")
    options = ['Presentase Jumlah Review per Distrik','Distribusi Jumlah Review per Distrik']
    factor_group2 = st.selectbox("", options, key="factor_group2")
    st.markdown("Berdasarkan Distrik, jumlah review tertinggi terdapat pada **:red[Khlong Toei]** sebesar 17,6% dengan jumlah review sebanyak 41.033 dan **:red[Vadhana]** sebesar 14,9% dengan jumlah review sebanyak 34.656.")
    if factor_group2 == 'Presentase Jumlah Review per Distrik':
        st.plotly_chart(fig_pie_RTN)
        st.caption("")
    elif factor_group2 == 'Distribusi Jumlah Review per Distrik':
       st.plotly_chart(fig_jrd)
       st.caption("")
with b2:
    st.subheader("Room type")
    options = ['Presentase Jumlah Review per Room type', 'Trend Rata-rata Jumlah Review pada Room Type per Tahun (2018 - 2023)','Top 5 Room type per Distrik']
    factor_group3 = st.selectbox("", options, key="factor_group3")
    if factor_group3 == 'Presentase Jumlah Review per Room type':
        st.markdown("Berdasarkan room type, jumlah review tertinggi terdapat pada **:red[Entire home/ Apartment]** yang mendominasi bahkan mencapai lebih dari 3/4 total review yaitu 76,8%, selanjutnya diikuti oleh Private Room sebesar 18,8% dan Hotel Room serta Shared Room yang memilikipresentase di bawah 5%.")
        st.plotly_chart(fig_pie_mr)
    elif factor_group3 == 'Trend Rata-rata Jumlah Review pada Room Type per Tahun (2018 - 2023)':
       st.markdown("Berdasarkan trend rata-rata jumlah review pada room type per tahun, **:red[Entire home/ Apartment]** selalu berada di posisi teratas pada saat sebelum dan sesudah pandemi dan bahkan mengalami peningkatan yang sangat signifikan setelah pandemi.")
       st.plotly_chart(fig_RTYA_line)
    elif factor_group3 == 'Top 5 Room type per Distrik':
       st.markdown("Berdasarkan data 5 room type per Distrik dengan jumlah review tertinggi, room type **:red[Entire home/ Apartment]** mendominasi ke 5 Distrik teratas dan dipimpin oleh Distrik **:red[Khlong Toei]** dan **:red[Vadhana]** yang jumlah reviewnya mencapai lebih dari 30.000.")
       st.plotly_chart(fig_top5_rtn)
       

# Tabel harga neighbourhood
allprice_n = dataset.groupby('neighbourhood').agg(
    total_review=('date', 'count'),
    sum=('price', 'sum'),
    min=('price', 'min'),
    max=('price', 'max'),
    mean=('price', 'mean'),
    median=('price', lambda x: x.median())
).sort_values('total_review', ascending=False).reset_index()

# Tabel harga roomtype
allprice_r = dataset.groupby('room_type').agg(
total_review=('date', 'count'),
total_income=('price', 'sum'),
min_price=('price', 'min'),
mid_price=('price', lambda x: np.median(x)),
max_price=('price', 'max'),
avg_price=('price', 'mean')
).sort_values('total_review', ascending=False).reset_index()

# Tabel harga properti
properti_night = dataset.groupby(['name', 'neighbourhood', 'room_type']).agg(
total_review=('date', 'count'),
minimum_nights=('minimum_nights', 'first'),
price=('price', 'first')
).reset_index()
properti_night = properti_night.sort_values('total_review', ascending=False).reset_index()

maps_price = all_listings.groupby('neighbourhood').agg(
latitude=('latitude', 'first'),
longitude=('longitude', 'first'),
mid_price=('price', lambda x: np.median(x)),
avg_price=('price', 'mean')
).reset_index().sort_values('mid_price', ascending=False)
with open('neighbourhoods.geojson') as f:
    geojson_data = json.load(f)
df_geojson = pd.json_normalize(geojson_data['features'])
merged_df = df_geojson.merge(maps_price, left_on='properties.neighbourhood', right_on='neighbourhood', how='inner')
fig_map_p = px.choropleth_mapbox(merged_df, geojson=geojson_data, color='mid_price', labels={'mid_price':'Median Harga'},
                           locations='neighbourhood', featureidkey='properties.neighbourhood',
                           mapbox_style='carto-positron', zoom=8.9,
                           center={'lat': merged_df['latitude'].mean(), 'lon': merged_df['longitude'].mean()},
                           opacity=0.7,
                           color_continuous_scale= ["#fff3e6","#fdbdc4","#fa87a1","#f8517f","#f51b5c"])
fig_map_p.update_layout(margin={'r': 0, 't': 40, 'l': 0, 'b': 0})


# Tab 2
tab3, tab4, tab5 = st.tabs(["Harga per Distrik", "Harga per Room Type", "Harga per Property"])

with tab3:
    st.header("Harga per Distrik")
    st.dataframe(allprice_n.style.highlight_max(axis=0),use_container_width=True)
    st.header("")
    c6,c7  = st.columns((6,4))
    with c6:
        st.subheader("Peta Median Harga per Distrik")   
        fig_map_p
    with c7:
        st.header("")
        st.header("")
        st.header("")
        st.header("")
        st.markdown("Berdasarkan data pada tabel dan peta sebaran median harga per distrik didapatkan bahwa beberapa property yang jauh dengan pusat kota Bangkok dan juga yang berdeketan memiliki nilai median yang tinggi. Adapun nilai median tertinggi terdapat pada Nong Chok yang berada di ujung barat dengan nilai sebesar 3000 THB, kedua tertinggi terdapat pada Pathum Wan yang berada di pusat kota Bangkok dengan nilai sebesar 2476 THB. Akan tetapi ada baiknya dalam memilih property melihat juga dari skala range harga tertinggi dan terendahnya agar bisa menyesuaikan dengan budget yang dimiliki.")
  

with tab4:
    st.header("Harga per Room Type")
    st.dataframe(allprice_r.style.highlight_max(axis=0),use_container_width=True)
    st.markdown("Entire home/ Apartment yang menempati posisi pertama dengan review tertinggi ternyata memiliki harga maksimum, harga mid, dan rata-rata tertinggi akan tetapi juga memiliki harga minimum terendah. Walaupun memiliki harga relative tinggi diantara semua aspek, penyewa tetap lebih memilih room dengan tipe ini. Hal ini mungkin tetap masih ditolerir oleh para penyewa dikarenakan dengan lengkapnya fasilitas yang ditawarkan tipe room ini dan range harganya yang cukup besar sehingga penyewa masih bisa memilih property yang sesuai dengan kebutuhan. Adapun fasilitas pada entire home/ apartment biasanya sudah termasuk kamar tidur, kamar mandi dan dapur.")
    st.markdown("Selanjutnya shared room yang memiliki harga maksimum, harga mid, dan rata-rata terendah serta harga minimum terendah kedua tetap memiliki jumlah review terendah. Hal ini mungkin dikarenakan kurangnya privasi pada tipe room ini dan adanya fenomena pandemi selama 3 tahun terakhir membuat shared room makin kurang diminati oleh penyewa.")

with tab5:
    st.header("Harga per Property")
    st.dataframe(properti_night.style.highlight_max(axis=0),use_container_width=True)
    st.markdown('Berdasarkan property yang disewakan “Beautiful One Bedroom Apartment Near Skytrain” yang berada di Distrik Phaya Thai memiliki jumlah review terbanyak dengan jumlah minimum harinya adalah 1 malam dengan harga 1393 THB. Distrik Phaya Thai merupakan salah satu distrik yang juga berada di pusat Kota Bangkok.')
    st.markdown('Selanjutnya, dapat dilihat bahwa property dengan jumlah review terbanyak memiliki nama atau keyword yang berkaitan dengan transportasi. Maka dapat disimpulkan bahwa penyewa memilih property berdasarkan lokasi strategis yang dekat dengan sarana transportasi.')
    st.markdown('Jumlah minimum hari yang ditetapkan pada tiap property dapat dilihat juga bahwa sangat berpengaruh terhadap jumlah penyewaan, semakin sedikit hari yang ditetapkan semakin banyak penyewa yang menyewa dan sebaliknya*. Hal ini dikarenakan pengguna Airbnb biasanya merupakan wisatawan yang ingin menginap beberapa hari saja bukan untuk menetap.')
    st.markdown('Entire home/ apartment juga mendominasi property dan ada juga private room yang berada di posisi 10 besar yaitu di posisi 4. Private room berdasarkan jumlah review menempati posisi kedua tertinggi setelah entire home/ apartment, fasilitas yang dimiliki adalah kamar sendiri untuk tidur namun berbagi beberapa area dengan orang lain. Private room memiliki harga minimum, mid, dan rata-rata terendah kedua dan memiliki harga maksimum kedua tertinggi.')
    st.markdown('_:orange[* = Hal ini tidak bersifat mutlak karena pasti ada faktor lain juga yang mempengaruhi jumlah penyewaan semisalnya yaitu preferensi.]_')


st.header("")
st.header("Rekomendasi")
st.markdown('- Penyewa sebaiknya menyewa property di Khlong Toei dan Vadhana yang memiliki jumlah review tertinggi dan berada di dekat pusat kota. Adapun harga property di Khlong Toei sebesar 340 - 650.910 THB dengan median harga 1700 THB dan Vadhana sebesar 120 - 226.193 THB dengan median harga 1700 THB, distrik Vadhana memiliki harga minimum terendah')
st.markdown('- Penyewa sebaiknya menyewa property di sekitar pusat kota Bangkok dengan mempertimbangkan lokasi dan dekat sarana transportasi. Adapun property yang dekat dengan pusat kota dan sarana transportasi dengan jumlah review terbanyak terdapat pada “Beautiful One Bedroom Apartment Near Skytrain” yang berada di Distrik Phaya Thai dengan tipe room Entire home/ apartment')
st.markdown('- Penyewa sebaiknya menyewa tipe Entire Home/ Apartment yang memiliki jumlah review tertinggi walaupun memiliki harga tertinggi, adapun harganya yaitu 120 - 1.000.000 THB dengan median harga 1.500 THB. Namun apabila ingin tipe lain penyewa bisa memilih private room yang memiliki jumlah review tertinggi kedua dan harga terendah kedua yaitu sebesar 304 - 650910 THB dengan median harga 950 THB.')
st.header("")
st.header("")
st.markdown('Source : Inside Airbnb, Wikipedia, Asia Media Centre, Touropia, TTR WEEKLY')