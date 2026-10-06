#!/usr/bin/env python
# coding: utf-8

# In[1]:


#districts and their ten year population estimates
Kampala = [1200, 1250, 1300, 1350, 1420, 1500, 1580, 1650, 1720, 1800]
Wakiso  = [ 950, 1000, 1070, 1150, 1220, 1300, 1390, 1480, 1570, 1670]
Gulu    = [ 320,  330,  345,  360,  375,  390,  410,  430,  455,  480]
Luweero = [200, 5000, 4000, 300, 1000, 2300, 2400, 500, 210, 300]
Jinja = [210, 3400, 500, 6500, 400, 350, 2400, 260, 900,1000]
years=[2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]


# In[2]:


#import numpy and create numpy arrays
import numpy as np
Kampala=np.array([1200, 1250, 1300, 1350, 1420, 1500, 1580, 1650, 1720, 1800])
Wakiso=np.array([ 950, 1000, 1070, 1150, 1220, 1300, 1390, 1480, 1570, 1670])
Gulu=np.array([320,  330,  345,  360,  375,  390,  410,  430,  455,  480])
Luweero=np.array([200, 5000, 4000, 300, 1000, 2300, 2400, 500, 210, 300])
Jinja=np.array([210, 3400, 500, 6500, 400, 350, 2400, 260, 900,1000])
years=([2015,2016,2017,2018,2019,2020,2021,2022,2023,2024])


# In[3]:


#create the class
import numpy as np
class DistrictPopulation:
    def __init__(self, districtname,population,years):
        self.districtname=districtname
        self.years=np.array(years)
        self.population=np.array(population)
        if len(self.years) != len(self.population):
            raise ValueError("Years and population must have the same length.")
        if np.any(self.population < 0):
            raise ValueError(" All district population values must be positive")
    def __len__(self):
        return len(self.population)
    def __repr__(self):
        return (
            f"DistrictPopulation("
            f"districtname='{self.districtname}', "
            f"years={self.years[0]}-{self.years[-1]}, "
            f"observations={len(self)})"
        )


# In[4]:


#objects
Kampala = DistrictPopulation("Kampala", Kampala, years)
Wakiso = DistrictPopulation("Wakiso", Wakiso, years)
Gulu = DistrictPopulation("Gulu", Gulu, years)
Luweero = DistrictPopulation("Luweero", Luweero, years)
Jinja = DistrictPopulation("Jinja", Jinja, years)
districts = [Kampala,Wakiso,Gulu, Luweero,Jinja]
print(Kampala)


# In[5]:


#Computing the mean, median, variance and standard deviation for each district with statistics module
import statistics 
import pandas as pd
def statistics_summary(district):
     data = [int(value) for value in district.population]
     return {
        "District": district.districtname,
        "Mean": statistics.mean(data),
        "Median": statistics.median(data),
        "Variance": statistics.variance(data),
        "Standard Deviation": statistics.stdev(data)
    }
stats_results = []
for district in districts:
    stats_results.append(statistics_summary(district))
stats_table = pd.DataFrame(stats_results)
print(stats_table)


# In[6]:


#Computing the mean, median, variance and standard deviation for each district with NumPy.
def numpy_summary(district):
    data = district.population
    return {
        "District": district.districtname,
        "Mean": np.mean(data),
        "Median": np.median(data),
        "Variance": np.var(data),
        "Standard Deviation": np.std(data)
    }
numpy_results = []
for district in districts:
    numpy_results.append(numpy_summary(district))
numpy_table = pd.DataFrame(numpy_results)
print(numpy_table)


# In[7]:


#computing ddof
for district in districts:
    data = district.population
    print(district.districtname)
    print("statistics variance:",
          statistics.variance(data))
    print("NumPy variance ddof=0:",
          np.var(data, ddof=0))
    print("NumPy variance ddof=1:",
          np.var(data, ddof=1))
    print()


# In[8]:


#Computing year-on-year growth rates and the Compound Annual Growth Rate (CAGR) for each district to identify the fastest growing district
def year_on_year_growth(district):
    population = district.population
    growth = ((population[1:] - population[:-1])
              / population[:-1]) * 100
    return growth

def calculate_cagr(district):
    beginning = district.population[0]
    ending = district.population[-1]
    n = len(district.population) - 1
    cagr = (ending / beginning) ** (1 / n) - 1
    return cagr

cagr_yoy_results = []
for district in districts:
    cagr = calculate_cagr(district)
    yoy =year_on_year_growth(district)
    cagr_yoy_results.append({"District": district.districtname,"CAGR (%)": cagr * 100,"yoy": yoy})
cagr_table = pd.DataFrame(cagr_yoy_results)
print(cagr_table)


# In[9]:


#Implementing three forecasting models as subclasses of an abstract Forecaster base class that exposes fit() and predict(horizon):
from abc import ABC, abstractmethod
class Forecaster(ABC):
    @abstractmethod
    def fit(self, years, population):
        pass
    @abstractmethod
    def predict(self, horizon):
        pass


# In[10]:


#linear trend with np.polyfit
class LinearTrendForecaster(Forecaster):
    def __init__(self):
        self.coefficients = None

    def fit(self, years, population):
        self.coefficients = np.polyfit(years,population,1)
        return self

    def predict(self, horizon):
        future_years = np.array(horizon)
        predictions = np.polyval(self.coefficients,future_years)
        return predictions


# In[11]:


#exponential/CAGR growth
class CAGRForecaster(Forecaster):
    def __init__(self):
        self.start_year = None
        self.last_year = None
        self.last_population = None
        self.cagr = None

    def fit(self, years, population):
        self.start_year = years[0]
        self.last_year = years[-1]
        self.last_population = population[-1]
        number_of_intervals = len(years) - 1
        self.cagr = ((population[-1] / population[0]) ** (1 / number_of_intervals)) - 1
        return self

    def predict(self, horizon):
        future_years = np.array(horizon)
        years_ahead = future_years - self.last_year
        predictions = (self.last_population *(1 + self.cagr) ** years_ahead)
        return predictions


# In[12]:


#fibonacci -ratio model  
class FibonacciForecaster(Forecaster):
    def __init__(self):
        self.last_population = None
        self.ratios = None

    def fit(self, years, population):
        self.last_population = population[-1]
        fib = [1, 1]
        for i in range(10):
            fib.append(fib[-1] + fib[-2])
        self.ratios = [fib[i + 1] / fib[i]for i in range(len(fib) - 1)]
        return self

    def predict(self, horizon):
        predictions = []
        current = self.last_population
        for i in range(len(horizon)):
            ratio = self.ratios[i]
            current = current * ratio
            predictions.append(current)
        return np.array(predictions)


# In[13]:


#training and testing classes
train_years = np.array([2015, 2016, 2017, 2018,2019, 2020, 2021])

test_years = np.array([2022, 2023, 2024])


# In[14]:


#validating using MAPE, MAE,RMSE
def calculate_mape(actual, predicted):
    return np.mean(np.abs((actual - predicted) / actual)) * 100


# In[ ]:


from sklearn.metrics import mean_absolute_error, mean_squared_error
def evaluate_model(actual, predicted):
    mae = mean_absolute_error(actual,predicted)
    rmse = np.sqrt(mean_squared_error(actual,predicted))
    mape = calculate_mape(actual,predicted)
    return mae, rmse, mape


# In[ ]:


def validate_district(district):
    train_population = district.population[:7]
    test_population = district.population[7:]
    models = {"Linear Trend": LinearTrendForecaster(),"CAGR": CAGRForecaster(),"Fibonacci": FibonacciForecaster()}
    results = []
    for model_name, model in models.items():
        model.fit(train_years,train_population)
        predictions = model.predict(test_years)
        mae, rmse, mape = evaluate_model(test_population,predictions)
        results.append({"District": district.districtname,"Model": model_name,"MAE": mae,"RMSE": rmse, "MAPE": mape})
    return pd.DataFrame(results)


# In[ ]:


all_results = []
for district in districts:
    result = validate_district(district)
    all_results.append(result)
validation_table = pd.concat(all_results,ignore_index=True)
print(validation_table)


# In[ ]:


#identifying the best models by MAE
best_models = (validation_table.sort_values("MAE").groupby("District").first().reset_index())
print(best_models)


# In[ ]:


#forecasting for 2025-2029
forecast_years = np.array([2025, 2026, 2027, 2028, 202])
model_classes = { "Linear Trend": LinearTrendForecaster,"CAGR": CAGRForecaster, "Fibonacci": FibonacciForecaster}
forecast_results = {}
for district in districts:
    selected_model_name = best_models[best_models["District"] == district.districtname]["Model"].iloc[0]
    model = model_classes[selected_model_name ]()
    model.fit(district.years,district.population)
    predictions = model.predict(forecast_years)
    forecast_results[district.districtname] = {"model": selected_model_name,"predictions": predictions}
    for district_name, result in forecast_results.items():
    print("\n", district_name)
    print("Selected model:", result["model"])
    for year, prediction in zip(forecast_years,result["predictions"]):
        print(year,round(prediction, 2))


# In[ ]:


variance_results = []
for district in districts:
    forecast = forecast_results[district.districtname]["predictions"]
    actual_variance = np.var(district.population)
    forecast_variance = np.var(forecast)
    variance_results.append({"District": district.districtname,"Actual Variance": actual_variance,"Forecast Variance": forecast_variance,
                             "Difference": (forecast_variance -actual_variance)})
variance_table = pd.DataFrame(variance_results)
print(variance_table)


# In[ ]:


#Assuming 18% of the population is of primary-school age and a classroom holds 53 pupils. Estimate how many additional classrooms each district needs by 2029
#18% = primary-school-age population
#53 pupils = one classroom
classroom_results = []
for district in districts:
    population_2029 = forecast_results[district.districtname]["predictions"][-1]
    primary_school_population = (population_2029 * 0.18)
    classrooms = np.ceil(primary_school_population / 53)
    classroom_results.append({"District": district.districtname,"2029 Population": population_2029,
        "Primary School Age Population":primary_school_population,"Classrooms Required": classrooms})
classroom_table = pd.DataFrame(classroom_results)
print(classroom_table)


# In[ ]:


#plots
import matplotlib.pyplot as plt
fig, axes = plt.subplots(3, 2,figsize=(15, 15))
axes = axes.flatten()
for i, district in enumerate(districts):
    ax = axes[i]
    selected_model_name = forecast_results[district.districtname]["model"]
    model = model_classes[selected_model_name]()
    model.fit(district.years,district.population)
    fitted = model.predict(district.years)
    forecast = forecast_results[district.districtname]["predictions"]

    ax.plot(district.years,district.population,marker="o",label="Actual")
    ax.plot(district.years,fitted,linestyle="--",label="Fitted")
    ax.plot(forecast_years,forecast,marker="o",linestyle=":",label="Forecast")
    ax.axvline(x=2021.5,linestyle="--",label="Train/Test Split")
    ax.set_title(f"{district.districtname} - {selected_model_name}")

    ax.set_xlabel("Year")
    ax.set_ylabel("Population")
    ax.legend()
    ax.grid(True)


# In[26]:


def bootstrap_prediction_interval(model,years,population,future_years,n_bootstrap=1000):
    model.fit(years, population)
    fitted = model.predict(years)
    residuals = population - fitted
    original_forecast = model.predict(future_years)
    bootstrap_forecasts = []
    for _ in range(n_bootstrap):
        sampled_residuals = np.random.choice(residuals,size=len(residuals),replace=True)
        simulated_population = (fitted + sampled_residuals)
        model.fit(years,simulated_population)
        simulated_forecast = model.predict(future_years)
        bootstrap_forecasts.append(simulated_forecast)
    bootstrap_forecasts = np.array(bootstrap_forecasts)
    lower = np.percentile(bootstrap_forecasts,2.5,axis=0)
    upper = np.percentile(bootstrap_forecasts,97.5,axis=0)
    return (original_forecast,lower,upper)


# In[ ]:




