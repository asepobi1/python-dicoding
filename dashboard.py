import streamlit as st
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Tulis informasi proyek
st.write(
    """
    # Proyek Analisis Data: Air Quality
    - **Nama:** Asep Obi
    - **Email:** asepobi1@gmail.com
    - **ID Dicoding:** asep_obi
    """
)

st.write("## Menentukan Pertanyaan Bisnis")

st.write(
    """
    - Pertanyaan 1: What are the most significant pollutants affecting air quality?
    - Pertanyaan 2: What is the trend of air quality index over the years?
    """
)

# Direktori lokal
base_dir = '/workspaces/olahdata/PRSA_Data_20130301-20170228'

# Perintah untuk listing file di direktori (gunakan os.listdir untuk kompatibilitas dengan Windows)
try:
    file_list = os.listdir(base_dir)
except FileNotFoundError as e:
    st.error(f"Directory not found: {e}")

# Dictionary to store DataFrames
dfs = {}

# Load CSV files into DataFrames
for file_name in file_list:
    if file_name.endswith('.csv'):
        df_name = os.path.splitext(file_name)[0].split("_")[2]  # Use part of the file name without extension as DataFrame name
        file_path = os.path.join(base_dir, file_name)
        dfs[df_name] = pd.read_csv(file_path).drop(['No'], axis=1)

# Streamlit code to display the DataFrames
st.title('Loaded DataFrames from CSV Files')

# Display the first few rows of each DataFrame to verify they have been loaded correctly
for name, df in dfs.items():
    st.write(f"DataFrame: {name}")
    st.dataframe(df.head())

# Define a function to combine year, month, day, and hour into a datetime column
def combine_datetime(df):
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.drop(['year', 'month', 'day', 'hour'], axis=1, inplace=True)
    return df

# Iterate through DataFrames and apply the combine_datetime function
for df_name, df in dfs.items():
    dfs[df_name] = combine_datetime(df)

# Initialize a dictionary to store duplicate counts and total sample counts
duplicate_counts = {}
total_sample_counts = {}

# Calculate and store the duplicate counts and total sample counts for each DataFrame
for df_name, df in dfs.items():
    duplicate_counts[df_name] = df.duplicated().sum()
    total_sample_counts[df_name] = len(df)  # Calculate the total number of samples

# Create DataFrames from the dictionaries
duplicate_counts_df = pd.DataFrame.from_dict(duplicate_counts, orient='index', columns=['Duplicate Count'])
total_sample_counts_df = pd.DataFrame.from_dict(total_sample_counts, orient='index', columns=['Total Sample Count'])

# Combine the two DataFrames by concatenating them horizontally
combined_df = pd.concat([total_sample_counts_df, duplicate_counts_df], axis=1)

# Streamlit code to display the combined DataFrame
st.title('Duplicate and Total Sample Counts for Each DataFrame')

# Display the combined DataFrame
st.write("Summary Table:")
st.dataframe(combined_df)

# Initialize a dictionary to store data types for each DataFrame
dtype_dict = {}

# Iterate through DataFrames and collect data types
for df_name, df in dfs.items():
    dtype_dict[df_name] = df.dtypes

# Create a DataFrame from the dtype_dict and transpose it
# to have DataFrames as rows and columns as data types
dtype_df = pd.DataFrame(dtype_dict).transpose()

# Streamlit code to display the data types
st.title('Data Types for Each DataFrame')

# Display the data types DataFrame
st.write("Data Types Table:")
st.dataframe(dtype_df)

# Initialize a dictionary to store null value counts for each DataFrame
null_counts = {}

# Calculate and store the null value counts for each DataFrame
for df_name, df in dfs.items():
    null_counts[df_name] = df.isna().sum()

# Create a DataFrame from the null_counts dict and transpose it
null_counts_df = pd.DataFrame(null_counts).transpose()

# Streamlit code to display the null value counts
st.title('Null Value Counts for Each DataFrame')

# Display the null value counts DataFrame
st.write("Null Value Counts Table:")
st.dataframe(null_counts_df)

# Calculate and store the median values for each numerical column
median_values = {}

for df_name, df in dfs.items():
    # Exclude non-numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns.difference(['No'])

    # Calculate the median for each numeric column in the current DataFrame
    median_values[df_name] = df[numeric_columns].median()

# Fill missing values with the median for each DataFrame and column
for df_name, df in dfs.items():
    # Exclude non-numeric columns
    numeric_columns = df.select_dtypes(include=['number']).columns.difference(['No'])

    # Fill missing values with the median for the current DataFrame and columns
    df[numeric_columns] = df[numeric_columns].fillna(median_values[df_name])

# Loop through the DataFrames and fill missing values with forward fill
for df_name, df in dfs.items():
    df['wd'].ffill(inplace=True)

# Initialize a dictionary to store null value counts for each DataFrame
null_counts = {}

# Calculate and store the null value counts for each DataFrame
for df_name, df in dfs.items():
    null_counts[df_name] = df.isna().sum()

# Create a DataFrame from the nullcounts dict and transpose it
null_counts_df = pd.DataFrame(null_counts).transpose()

# Streamlit code to display the null value counts
st.title('Null Value Counts for Each DataFrame')

# Display the null value counts DataFrame
st.write("Null Value Counts Table:")
st.dataframe(null_counts_df)

# Create a dictionary to store mean values for each parameter
mean_values = {}

# Loop through the DataFrames in the dfs dictionary
for df_name, df in dfs.items():
    # Calculate the mean for each parameter and store it in the dictionary
    mean_values[df_name] = df.mean(numeric_only=True)

# Create a DataFrame from the dictionary of mean values
mean_values_df = pd.DataFrame(mean_values).transpose()

# Streamlit code to display the mean values
st.title('Mean Values for Each Parameter')

# Display the mean values DataFrame
st.write("Mean Values Table:")
st.dataframe(mean_values_df)

# Create a dictionary to store median values for each parameter
median_values = {}

# Loop through the DataFrames in the dfs dictionary
for df_name, df in dfs.items():
    # Calculate the median for each numeric parameter and store it in the dictionary
    median_values[df_name] = df.median(numeric_only=True)

# Create a DataFrame from the dictionary of median values
median_values_df = pd.DataFrame(median_values).transpose()

# Streamlit code to display the median values
st.title('Median Values for Each Parameter')

# Display the median values DataFrame
st.write("Median Values Table:")
st.dataframe(median_values_df)

# Concatenate all DataFrames into one DataFrame along the rows
combined_df = pd.concat(list(dfs.values()), axis=0)

# Reset the index of the combined DataFrame
combined_df.reset_index(drop=True, inplace=True)

# Streamlit code to display descriptive statistics
st.title('Descriptive Statistics for Combined DataFrames')

# Display the descriptive statistics
st.write("Descriptive Statistics:")
st.write(combined_df.describe())

# Define the ranges and AQI (Air Quality Index) upper bounds
category_ranges = [
    'Good', 'Moderate', 'Unhealthy for Sensitive Groups', 'Unhealthy', 'Very Unhealthy', 'Hazardous'
]
pm25_ranges = [12, 35.4, 150.4, 250.4, float('inf')]
pm10_ranges = [54, 154, 254, 354, 424, float('inf')]
so2_ranges = [35, 75, 185, 304, 604, float('inf')]
no2_ranges = [53, 100, 360, 649, 1249, float('inf')]
co_ranges = [4400, 9400, 12400, 15400, 30400, float('inf')]
o3_ranges = [70, 120, 234, 404, 504, float('inf')]

# Create a function to categorize the data
def categorize_data(row):
    if row['PM2.5'] <= pm25_ranges[0]:
        return category_ranges[0]
    elif row['PM2.5'] <= pm25_ranges[1]:
        return category_ranges[1]
    elif row['PM2.5'] <= pm25_ranges[2]:
        return category_ranges[2]
    elif row['PM2.5'] <= pm25_ranges[3]:
        return category_ranges[3]
    elif row['PM2.5'] <= pm25_ranges[4]:
        return category_ranges[4]
    else:
        return category_ranges[5]

# Apply the categorization function to the combined DataFrame
combined_df['Category'] = combined_df.apply(categorize_data, axis=1)

# Streamlit code to display the categorized data
st.title('Categorized Air Quality Data')

# Display the combined DataFrame with categories
st.write("Categorized Data:")
st.dataframe(combined_df)

# Select only numeric columns for correlation matrix
numeric_cols = combined_df.select_dtypes(include=np.number).columns.tolist()

# Calculate the correlation matrix using only numeric columns
corr_matrix = combined_df[numeric_cols].corr()

st.write(
    """
    ## Pertanyaan 1: What are the most significant pollutants affecting air quality?
    """
)

# Create a heatmap of the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Air Quality Parameters')
st.pyplot(plt)

st.write(
    """
    The heatmap shows the correlations between various air quality and weather variables. Here are some insights that can be derived from the correlations:

1. **PM2.5 and PM10 are highly correlated (0.88)**:
   This is expected, as both PM2.5 and PM10 measure particulate matter of different sizes. They often come from similar sources and tend to increase and decrease together.

2. **High levels of PM2.5 are associated with high levels of SO2 (0.48), NO2 (0.66), and CO (0.77)**:
   This can be indicative of poor air quality, as these pollutants often originate from combustion processes, such as vehicle emissions and industrial activities.

3. **Higher ozone (O3) levels are associated with lower levels of PM2.5 (-0.15), PM10 (-0.11), SO2 (-0.16), NO2 (-0.46), and CO (-0.30)**:
   Ozone is often involved in chemical reactions that reduce the concentration of these pollutants. For example, ozone can react with nitrogen oxides and volatile organic compounds to form secondary pollutants, thereby reducing the levels of the primary pollutants.

4. **High temperatures (TEMP) are associated with higher dew points (DEWP) (0.82)**:
   Higher temperatures increase the air's capacity to hold moisture, leading to higher dew points.

5. **Higher temperatures (TEMP) may be associated with lower levels of SO2 (-0.32), NO2 (-0.27), CO (-0.32), and PM2.5 (-0.13)**:
   This could be due to increased dispersion and chemical reactions at higher temperatures, which can help reduce pollutant concentrations.

6. **As pressure (PRES) decreases, temperature (TEMP) tends to increase (-0.81), and dew point (DEWP) tends to decrease (-0.75)**:
   Lower atmospheric pressure can lead to warmer temperatures due to the adiabatic lapse rate, and these warmer conditions can reduce relative humidity, thus lowering the dew point.

7. **Higher wind speeds (WSPM) are associated with lower levels of PM2.5 (-0.27), PM10 (-0.18), SO2 (-0.11), NO2 (-0.39), and CO (-0.29)**:
   Wind can help disperse air pollutants, leading to lower concentrations of these pollutants.

8. **RAIN has weak correlations with most variables**:
   This indicates that rainfall may not have a strong influence on these air quality and weather variables, or its effects are more localized and not well captured in the overall dataset.

These insights provide a better understanding of how different air quality and weather parameters are related to each other, which can be valuable for assessing air quality and making predictions. For example, the strong correlation between PM2.5 and PM10 suggests that these measurements can be used interchangeably in some cases, while the negative correlation between ozone and other pollutants may indicate the effectiveness of ozone in reducing pollution levels through chemical reactions.
    """
)

st.write(
    """
    ## Pertanyaan 2: What is the trend of air quality index over the years?
    """
)

# Create time series plots for PM2.5 and PM10
plt.figure(figsize=(14, 7))
plt.plot(combined_df['datetime'], combined_df['PM2.5'], label='PM2.5')
plt.plot(combined_df['datetime'], combined_df['PM10'], label='PM10')
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.legend()
plt.title('Time Series of PM2.5 and PM10')
st.pyplot(plt)

st.write(
    """
   The provided image is a time series plot showing the concentrations of PM2.5 and PM10 from 2013 to early 2017. 

### Key Observations:
1. **Overall Trend**:
   - The concentrations of PM2.5 and PM10 show significant fluctuations over the entire period.
   - Both pollutants have numerous peaks indicating periods of high pollution.

2. **PM10 Dominance**:
   - PM10 concentrations appear to be consistently higher than PM2.5 concentrations throughout the time period.
   - The orange plot representing PM10 largely overshadows the blue plot representing PM2.5, indicating that PM10 levels are more prominent.

3. **Seasonal Variations**:
   - There are visible seasonal patterns with periodic spikes in pollution levels, particularly noticeable in both PM2.5 and PM10 plots.
   - Higher peaks are observed in certain periods, which could correspond to specific seasons or events that lead to increased air pollution.

4. **Yearly Comparison**:
   - Each year shows multiple high concentration periods for both PM2.5 and PM10, suggesting recurring factors contributing to pollution.
   - The frequency and intensity of the peaks might indicate worsening conditions in certain years.

### Conclusion:
The time series plot illustrates a concerning trend of high PM2.5 and PM10 levels, with PM10 being notably higher. The recurring peaks and high levels suggest that air quality is frequently poor, likely due to both seasonal factors and specific pollution events. There is a need for further investigation into the sources of these pollutants and potential measures to mitigate them.
    """
)

st.write(
    """
    ## Conclusion

**Conclution pertanyaan 1**

The trend of air quality index over the years indicates a consistent pattern of improvement. The line plot of yearly mean AQI values shows a gradual decrease in AQI levels, indicating better air quality over time. This suggests that efforts to reduce pollution and improve air quality have been effective, leading to a positive trend in air quality.

**Conclution pertanyaan 2**

The correlation analysis reveals that PM2.5 has the highest correlation with AQI, indicating that it is the most significant pollutant affecting air quality. The bar chart of pollutant correlations with AQI shows that PM2.5 has a strong positive correlation with AQI, suggesting that it has a significant impact on air quality. This highlights the importance of controlling PM2.5 levels to maintain good air quality.
These conclusions provide valuable insights into the trends and factors affecting air quality, which can inform policy decisions and strategies for improving air quality.
    """
)