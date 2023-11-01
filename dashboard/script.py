import streamlit as st
import pandas as pd
# import altair as alt
# import os.path
import os
from babel.numbers import format_currency
from eda.eDA import create_monthly_orders_df, create_order_sales_items_df, create_byregion_df, create_pay_type_byregion_df
from rfm.rFM import create_rfm_df, create_rfm_df_quantile, customer_segment, create_rfm_segment_distribution
# from pathlib import Path

path = os.path.dirname(os.path.abspath(__file__))
data_source = path+'/merge-dataset.csv'
all_data = pd.read_csv(data_source)
location = os.path.join(path, 'merge_rfm_dataset.csv')
rfm_df_score = pd.read_csv(location)

def intro():
    import streamlit as st
    
    st.write("# Brazilian E-Commerce Public Analysis! 🔎")
    
    st.sidebar.success("Select a demo above.")
    
    st.markdown(
        """
        ### About dataset
        The dataset has information of 100k orders from 2016 to 2018 made at multiple marketplaces in Brazil.
        The available data consists of 9 different file, but for this time only 5 data will be use: 
        - customers_dataset.csv ✔️ 
        - geolocation_dataset.csv ❌ 
        - order_items_dataset.csv ✔️ 
        - order_payments_dataset.csv ✔️ 
        - order_reviews_dataset.csv ❌ 
        - orders_dataset.csv ✔️ 
        - product_category_name_translation.csv ❌ 
        - products_dataset.csv ✔️ 
        - sellers_dataset.csv ❌ 
        ### Task 
        For this project, there are some step I will do:
        - Review the dataset
        - Perform EDA
        - Perform RFM analysis
        """
    )

def eda():
    import streamlit as st
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    print("==============Currenly run EDA option!==============\n")
    
    st.markdown(f"# {list(page_connector_with_funcs.keys())[1]}")
    st.title("Brazilian E-Commerce Public Dashboard :sparkles:") 
    st.header('Brazilian E-Commerce EDA', divider='rainbow')
    st.subheader('Daily Orders')
    
    datetime_columns = ["order_purchase_timestamp", "order_purchase_date", "order_estimated_delivery_date", "order_delivered_date"]
    all_data.sort_values(by="order_purchase_date", inplace=True)
    all_data.reset_index(inplace=True)
    for column in datetime_columns:
        all_data[column] = pd.to_datetime(all_data[column])


    min_date = all_data["order_purchase_date"].min()
    max_date = all_data["order_purchase_date"].max()

    group_columns = ['order_date_year', 'order_date_month', 'month-year']
    year_monthly_order = all_data.groupby(group_columns)['order_id'].nunique().reset_index()

    year_monthly_order_2017 = year_monthly_order[year_monthly_order['order_date_year'] == 2017]
    year_monthly_order_2018 = year_monthly_order[year_monthly_order['order_date_year'] == 2018]

    year_monthly_order_2017.rename(columns={
        "order_id": "total_order",
        "order_date_month": "month",
    }, inplace=True)

    year_monthly_order_2018.rename(columns={
        "order_id": "total_order",
        "order_date_month": "month",
    }, inplace=True)

    with st.sidebar:
        start_date, end_date = st.date_input(
            label='Date Range',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

    main_df = all_data[(all_data["order_purchase_date"] >= str(start_date)) & 
                (all_data["order_purchase_date"] <= str(end_date))]

    monthly_orders_df = create_monthly_orders_df(main_df)
    order_sales_items_df = create_order_sales_items_df(main_df)
    byregion_df = create_byregion_df(main_df)
    pay_type_byregion_df = create_pay_type_byregion_df(main_df)
 
    col1_left, col2_right = st.columns(2)
 
    with col1_left:
        total_orders = monthly_orders_df.order_count.sum()
        st.metric("Total orders", value=total_orders)

    with col2_right:
        total_sales = format_currency(monthly_orders_df.sales.sum(), "$", locale='es_CO') 
        st.metric("Total Sales", value=total_sales)


    st.markdown("")
    st.subheader('Monthly Orders')
    col1_line_chart, col2_line_chart = st.columns(2)

    with col1_line_chart:
        colors = ["#D3D3D3"]
        st.write("##### Total Order Store in 2017")
        st.line_chart(
            year_monthly_order_2017, 
            x="month", 
            y="total_order", 
            color=colors
        )

    with col2_line_chart:
        colors = ["#90CAF9"]
        st.write("##### Total Order Store in 2018")
        st.line_chart(
            year_monthly_order_2018, 
            x="month", 
            y="total_order", 
            color=colors
        )
    st.markdown("Analysis summary:")
    st.markdown("- From Jan to Desc 2017, the lowest total sales in January with 750 total order")
    st.markdown("- While the highest peak sales was in November with 7289 total order")
    st.markdown("- As we can see, the number of total orders in 2018 has been drop many times")
    st.markdown("- The lowest total order was in June with 6099 total order")

    st.markdown("")
    st.subheader('Product Performance by Total Order')

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 25))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(x="order_count", y="category_name", data=order_sales_items_df.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Number of Order", fontsize=35)
    ax[0].set_title("5 Category from Top by Order", loc="center", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)

    sns.barplot(x="order_count", y="category_name", data=order_sales_items_df.sort_values(by="order_count", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Number of Order", fontsize=35)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("5 Category from Bottom by Order", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=35)

    st.pyplot(fig)
    st.markdown("Analysis summary:")
    st.markdown("- According to the chart, 'Alimentos' is product category with the highest total order")
    st.markdown("- On the other hand, 'Seguros E Servicos' achieved the lowest ranking of total order")

    st.markdown("")
    st.subheader('Customer Demographic')
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="num_of_customer", 
        y="region",
        data=byregion_df.sort_values(by="num_of_customer", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Region", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel("customer_count", fontsize=25)
    ax.tick_params(axis='y', labelsize=25)
    ax.tick_params(axis='x', labelsize=20)

    st.pyplot(fig)
    st.markdown("Analysis summary:")
    st.markdown("- As we can see, the most customers come from Southeast area")
    st.markdown("")
    st.markdown("Note: Brazil is geopolitically divided into five regions(also called macroregions), which are formed by the federative units of Brazil.")

    st.markdown("")
    st.subheader('Customer Transaction by Payment Type')
    fig, ax = plt.subplots(figsize=(14, 6))
    labels = pay_type_byregion_df['payment_type']
    ax.pie(pay_type_byregion_df['num_of_order'], labels=labels, autopct='%1.1f%%')
    ax.axis('equal')

    st.pyplot(fig)
    st.markdown("Analysis summary:")
    st.markdown("- Most of the customer (75%) use credit card as a method payment for doing transaction")
    st.markdown("- Customer use less physical voucher (3%) rather than using boleto (19%) for buying things")
    st.markdown("")
    st.markdown("Note: boleto is an official (regulated by the Central Bank of Brazil) payment method in Brazil. To complete a transaction, customers receive a voucher stating the amount to pay for services or goods")


def rfm_analysis():
    import streamlit as st
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    print("==============Currenly run RFM analysis option!==============\n")
        
    st.markdown(f"# {list(page_connector_with_funcs.keys())[2]}")
    datetime_columns = ["order_purchase_timestamp", "order_purchase_date", "order_estimated_delivery_date", "order_delivered_date"]
    
    all_data.sort_values(by="order_purchase_date", inplace=True)
    all_data.reset_index(inplace=True)
    for column in datetime_columns:
        all_data[column] = pd.to_datetime(all_data[column])


    min_date = all_data["order_purchase_date"].min()
    max_date = all_data["order_purchase_date"].max()

    group_columns = ['order_date_year', 'order_date_month', 'month-year']
    year_monthly_order = all_data.groupby(group_columns)['order_id'].nunique().reset_index()

    year_monthly_order_2017 = year_monthly_order[year_monthly_order['order_date_year'] == 2017]
    year_monthly_order_2018 = year_monthly_order[year_monthly_order['order_date_year'] == 2018]

    year_monthly_order_2017.rename(columns={
        "order_id": "total_order",
        "order_date_month": "month",
    }, inplace=True)

    year_monthly_order_2018.rename(columns={
        "order_id": "total_order",
        "order_date_month": "month",
    }, inplace=True)

    with st.sidebar:
        start_date, end_date = st.date_input(
            label='Date Range',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )


    temp_df = all_data[(all_data["order_purchase_date"] >= str(start_date)) & 
                (all_data["order_purchase_date"] <= str(end_date))]

    rfm_df = create_rfm_df(temp_df)
    # rfm_df_score = create_rfm_df_quantile(rfm_df)
    # customer_segment_df = customer_segment(rfm_df_score)

    st.header('Brazilian E-Commerce RFM | Customer Segmentation', divider='rainbow')
    st.subheader('Best Customer Based on RFM Parameters')
    
    col1_left, col2_middle, col3_right = st.columns(3)

    with col1_left:
        avg_recency = round(rfm_df.recency.mean())
        st.metric("Average Recency (days)", value=avg_recency)

    with col2_middle:
        avg_frequency = round(rfm_df.frequency.mean())
        st.metric("Average Frequency", value=avg_frequency)

    with col3_right:
        avg_monetary = format_currency(rfm_df.monetary.mean(), "$", locale='es_CO') 
        st.metric("Average Monetary", value=avg_monetary)


    rfm_df.drop("order_purchase_timestamp", axis=1, inplace=True)
    rfm_df.drop("order_id", axis=1, inplace=True)
    rfm_df.drop("payment_value", axis=1, inplace=True)

    st.markdown("")
    st.subheader('RFM DataTable')
    rfm_df

    st.markdown("")
    st.subheader('RFM/R - Chart')
    fig, ax= plt.subplots(figsize=(10, 5))
    sns.distplot(rfm_df["recency"])
    ax.set_title("Recency value distribution", loc="center", fontsize=30)

    st.pyplot(fig)

    st.markdown("")
    st.subheader('RFM/F - Chart')
    fig, ax= plt.subplots(figsize=(10, 5))
    sns.distplot(rfm_df["frequency"])
    ax.set_title("Frequency value distribution", loc="center", fontsize=30)

    st.pyplot(fig)

    st.markdown("")
    st.subheader('RFM/M - Chart')
    fig, ax= plt.subplots(figsize=(10, 5))
    sns.distplot(rfm_df["monetary"])
    ax.set_title("Monetary value distribution", loc="center", fontsize=30)

    st.pyplot(fig)
    
    rfm_segment_count = create_rfm_segment_distribution(rfm_df_score)
    
    st.markdown("")
    st.subheader('RFM Segmentation DataTable')
    rfm_df_score
    
    st.markdown("")
    st.subheader('Customer Segments Overview')
    rfm_segment_count.info()
    fig, ax= plt.subplots(figsize=(10, 5))    
    ax = sns.barplot(
        x=rfm_segment_count['percentage'], 
        y=rfm_segment_count.index,
        data=rfm_segment_count,
        palette="cool",
        ax=ax
    )
    for i, j in enumerate(rfm_segment_count['percentage']):
        ax.text(j, i+0.20, "{:.2f}".format(j)+"%", color = 'black', ha = 'left')

    plt.ylabel(None)
    plt.xlabel('Customer distribution (%)', fontdict = {'fontsize': 12})
    plt.title('Distribution of Customer Segments', fontdict = {'fontsize': 18}, pad = 12)

    st.pyplot(fig)
    st.markdown("Analysis summary:")
    st.markdown("- There are 3 most dominant type of customer segments that are  as we can see in the graph:")
    st.markdown("- Promising [35.67%] of all customer -> they are recent shoppers and can benefit from limited-time loyalty points and other perks")
    st.markdown("- Cannot lose them [19.12%] of all customer -> this customers demonstrated a strong willingness to pay but haven't returned for a long time")
    st.markdown("- New customers [18.98%] of all customer -> new buyers visiting the store for the first time")
    st.markdown("")


page_connector_with_funcs = {
    "—": intro,
    "EDA": eda,
    "RFM": rfm_analysis
}

demo_name = st.sidebar.selectbox("Select a demo", page_connector_with_funcs.keys())
page_connector_with_funcs[demo_name]()

st.caption('Copyright (c) - Created by Ricky Suhanry - 2023')