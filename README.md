# Brazilian-E-Commerce-Public-Customer-Analysis-and-RFM-Analysis

## Project Description
This project contain the code for data analysis project and RFM analysis using brazilian e-Commerce public dataset 
[| custom dataset from Dicoding](https://www.dicoding.com/).

## Project Objective
- Do comprehensive data analysis starting from defining questions to drawing conclusions from the analysis results
- Do data analysis and identify patterns in customer base using the RFM method
- Create an interactive data analysis report in a dashboard

## Brazilian E-Commerce Public Dashoard using Streamlit
### Homepage
![Brazilian_E-Commerce_Public_Dashboard](https://github.com/abliskan/RFM-Analysis-Brazilian-E-Commerce-Public/blob/main/asset/images/screenshot-homepage.png)
### EDA
![Brazilian_E-Commerce_Public_Dashboard](https://github.com/abliskan/RFM-Analysis-Brazilian-E-Commerce-Public/blob/main/asset/images/screenshot-EDA.png)
### RFM
![Brazilian_E-Commerce_Public_Dashboard](https://github.com/abliskan/RFM-Analysis-Brazilian-E-Commerce-Public/blob/main/asset/images/screenshot-RFM.jpg)

## Installation Guide
### Setup Environment
Once you have installed the above and have cloned the repository, you can follow the following steps to get the project up and running:

1. Create a default requirements file:

```bash
pip freeze > requirements.txt
```
note: make sure to customize the dependencies according to project requirement <br>
Babel==2.12.1
matplotlib==3.8.0
matplotlib-inline==0.1.6
numpy==1.26.0
pandas==2.1.1
python-dateutil==2.8.2
python-dotenv==1.0.0
scikit-learn==1.2.0
seaborn==0.13.0
streamlit==1.28.0

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Go to the dashboard directory


```bash
cd C:\RFM-Analysis-Brazilian-E-Commerce-Public\dashboard
```

### Run the app
4. Run the streamlit from your local computer 
```bash
streamlit run [name_file].py
```
We can access the application on your desktop by visiting http://localhost:8501/

## Deploying the dashboard
- Comming soon | streamlit viz
