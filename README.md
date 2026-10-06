# UBOS-DISTRICT-FORECASTER
This mini project is one that aims to develop a model that forecasts 5-year population estimates that will aid a district in planning for the required number of classrooms for the students. The available data has 10 year population estimates (2015 to 2024) for  5 districts.districts. This project was edited with the aid of CODEX, an Artificial Intelligence powered tool.
### IMPLEMENTATION
- Using object oriented programming in python, a class having years and populations as NumPy arrays was created.
- Using the statistics module and NumPy,  the mean, median, variance and standard deviation were calculated per district. 
- Year-on-year growth rates per district and Compound Annual Growth Rate (CAGR) were computed to find out what district was growing fastest.
- Three forecasting models; linear trend, Fibonacci-ratio model and exponential/CAGR growth were implemented to identify the best model.
- The models were trained and tested using Mean Absolute Error (MAE), Mean Absolute Percentage Error(MAPE) and Root Mean Squared Error(RMSE).
 
- Actual, fitted and forecast values per district were plotted.

- An 18%  of primary school children and 53 per class assumption was used to estimated the number of classes needed in 2029.

- Using bootstrap resampling of residuals, 95% predictions were added to the forecasts and plotted.

### FINDINGS, RECOMMENDATIONS AND LIMITATIONS
•	Variance calculated using the statistics module was significantly higher than that calculated using NumPy as shown below;
The statistics module; Kampala , Wakiso, Gulu, Luweero, Jinja  (4.260111e+04 , 6.006667e+04 ,2.885833e+03,      3.031966e+06  ,4.075507e+06) and with  NumPy (  38341.00 , 54060.00 , 2597.25 ,2728769.00 ,3667956.00). The difference is in  the fact that NumPy calculates population variance while the Statistics module calculates the sample variance. Setting the Delta degrees of freedom(ddof) to 1 eliminates the bias in variation associated with the sample letting the variance in the NumPy and Statistics modules be the same.
•	The Compound Annual Growth Rate(CAGR) of the individual districts indicated the Jinja had the highest rate of 18.9% which is probably because the population estimates were made up. The year on year growth rates had fluctuations. The CAGR of other districts were as follows, Kampala (4.6%), Wakiso(6.5%), Gulu(4.6%) and Luweero(4.6%).
•	The linear trend, exponential/CAGR growth and Fibonacci- ratio models were trained using 2015-2021 data and tested using 3033-2024 data. The best models per district with the MAE,RMSE AND MAPE values are as follows;
1. 	Kampala, CAGR( 9.62,10.39,0.55%)
2. 	Wakiso, CAGR(6.80, 8.05, 0.42%)
3. 	Gulu , CAGR( 9.44, 10.87, 2.02%)
4. 	Luweero, Linear Trend( 1513.33, 1516. 26, 519.68%)
5. 	Jinja, Linear Trend (1311.79, 1349.76, 302.21%)
- The differences between the forecast variance and actual variance per district are as follows; Kampala(-21,055 ), Wakiso( -21,955), Gulu( -1,368), Luweero(-2,595,891 ), Jinja(-3,625,853 ) The negative values indicate that the forecast variance is lower than the actual variance and the models are underestimating the amount of variance in the data. Jinja and Luweero have larger variations than the other districts. Overall, the models are producing less variable data than the actual data.
- Assuming that 18% of the population is of primary-school age and a classroom holds 53 pupils. The estimated  additional classrooms per district needs by 2029 are as follows; Kampala(8), Wakiso(8), Gulu(3), Luweero(-2), Jinja(1).
- The Fibonacci model assumes that the population increases at a specific rate which isn’t the case in this data so it fails miserably here due to the population fluctuations in the dataset.
 
