House Price Predictor

An end-to-end machine learning application that predicts residential home prices using a Random Forest Regressor trained on the Ames Housing Dataset. This project demonstrates the complete machine learning workflow, from data collection and exploratory data analysis to model deployment through an interactive Streamlit web application.

⸻

Project Overview

This application allows users to estimate the sale price of a home by entering key property characteristics. The prediction is generated using a machine learning model trained on historical housing data.

The project was built to demonstrate practical data science and machine learning skills, including:

- Data preprocessing
- Exploratory data analysis
- Feature engineering
- Regression modeling
- Model evaluation
- Interactive application development

⸻

Features

- Predict home sale prices using a trained Random Forest model
- Interactive Streamlit dashboard
- Adjustable property characteristics with sliders
- Estimated price range based on model error
- Feature importance analysis
- Model performance metrics
- Clean and responsive interface

⸻

Technologies Used

Programming Language

- Python

Machine Learning

- Scikit-learn
- Random Forest Regressor
- Linear Regression

Data Analysis

- Pandas
- NumPy

Visualization

- Matplotlib

Web Application

- Streamlit

Model Serialization

- Joblib

⸻

Project Structure

house-price-predictor/
│
├── data/
│ ├── housing.csv
│ └── housing_cleaned.csv
│
├── models/
│ ├── house_price_model.pkl
│ └── model_features.pkl
│
├── results/
│ ├── eda_report.txt
│ └── feature_importance.csv
│
├── visualizations/
│ ├── saleprice_distribution.png
│ ├── living_area_vs_price.png
│ ├── overall_quality_vs_price.png
│ ├── garage_area_vs_price.png
│ ├── year_built_vs_price.png
│ ├── top_correlations.png
│ ├── feature_importance.png
│ ├── actual_vs_predicted.png
│ └── residual_plot.png
│
├── explore_data.py
├── create_visualizations.py
├── clean_data.py
├── train_model.py
├── analyze_model.py
├── app.py
├── requirements.txt
└── README.md

⸻

Dataset

This project uses the Ames Housing Dataset, a benchmark dataset commonly used for regression and predictive modeling.

Dataset Summary:

- 2,930 residential properties
- 82 original features
- Target variable: SalePrice

⸻

Exploratory Data Analysis

The exploratory analysis included:

- Dataset exploration
- Summary statistics
- Missing value analysis
- Numerical and categorical feature analysis
- Correlation analysis

Visualizations created:

- Sale Price Distribution
- Living Area vs. Sale Price
- Overall Quality vs. Sale Price
- Garage Area vs. Sale Price
- Year Built vs. Sale Price
- Feature Correlation Heatmap
- Feature Importance
- Actual vs. Predicted Prices
- Residual Plot

⸻

Data Preprocessing

The preprocessing pipeline included:

- Handling missing values
- Median imputation for numerical features
- Replacing categorical missing values with “None” where appropriate
- Removing identifier columns (Order and PID)
- One-hot encoding categorical variables

Final processed dataset:

- 2,930 observations
- 278 machine learning features

⸻

Machine Learning Models

Two regression models were trained and evaluated.

Linear Regression

Metric Value
Mean Absolute Error $29,985
Root Mean Squared Error $46,348
R² Score 0.732

Random Forest Regressor

Metric Value
Mean Absolute Error $15,833
Root Mean Squared Error $26,715
R² Score 0.911

The Random Forest model was selected as the final production model due to its significantly higher predictive performance.

⸻

Model Evaluation

The project includes several evaluation techniques to assess model performance:

- Feature Importance Analysis
- Actual vs. Predicted Price Comparison
- Residual Analysis

These visualizations provide insight into the model’s predictive accuracy and the features that contribute most to home valuation.

⸻

Application

The Streamlit application allows users to:

- Enter property characteristics
- Generate an estimated home value
- View an estimated prediction range
- Review model performance metrics
- Explore the most influential pricing factors

⸻

Installation

Clone the repository:

git clone https://github.com/yourusername/house-price-predictor.git

Install the required packages:

pip install -r requirements.txt

Launch the application:

streamlit run app.py

⸻

Future Improvements

Potential enhancements include:

- Support for additional housing datasets
- Regional market-specific models
- Similar home recommendations
- Interactive geographic visualizations
- Feature contribution explanations using SHAP values
- Improved confidence estimation
- Cloud deployment

⸻

Skills Demonstrated

- Machine Learning
- Regression Modeling
- Data Cleaning
- Feature Engineering
- Exploratory Data Analysis
- Model Evaluation
- Data Visualization
- Python Programming
- Streamlit Development
- Software Engineering

⸻

License

This project was developed for educational and portfolio purposes.
