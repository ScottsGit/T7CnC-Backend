# T7CnC-Backend
Team 7 - Cash-n-Crunch Backend
A brief description of what I attempted here. Basically tried to do 2 forecasting models, one for a personal account that helped plan for 
discretionary and necessary expenses. And one for a business account that helped forecast sales.
Started off with:
Gathering and Preparing Data: I started by collecting transaction(one for personal one for business) data, focusing on the expenses and quantities sold over time. This data was then cleaned and organized to ensure it was in a suitable format for analysis, with all the dates in order and any missing data addressed.

Exploring the Data: I visually inspected the data to understand its characteristics, such as trends, seasonality, and any patterns in how the quantity sold changes over time. This helped get a feel for what I was working with and how to approach the modeling.

Choosing the Right Model: I decided to use the SARIMA model. SARIMA is a type of forecasting model that's great for data with trends and seasonal patterns, which was suitable for our weekly sales data.

Finding the Best Model Settings: SARIMA models need specific settings (parameters) to work best. Tried to used a systematic approach (grid search) to try out many different settings and find the best ones for our data. This involved running the model many times with different configurations and selecting the one that gave us the most accurate results based on a statistical criterion. (This is where I ran into some trouble, especially with the personal transaction model, the grid search was not producing the best results)

Making Predictions: With the best settings identified, used the SARIMA model to make predictions about future sales. Specifically, we forecasted the weekly mean quantity of products sold for several weeks into the future.

Evaluating the Model: To ensure our predictions were reliable, we looked at how well the model's forecasts matched up with our known data. There was room for imporvement here but produced some useable results.

Forecasting Future Sales: Finally, produced forecasts for future weeks, providing valuable insights into expected sales trends. These forecasts help in planning inventory, understanding future sales patterns, and making informed business decisions.

In summary, through a methodical approach of preparing the data, selecting and tuning the right model, and validating our findings, we were able to create a reliable forecast of weekly sales, aiding in strategic planning and decision-making for the business.

For reference this is what the resulting forecast looked like:
    
    One Step Ahead
    Predicted Weekly Mean of Quantity Sold
  
    2023-12-16    2.384234
    2023-12-23    2.323122
    2023-12-30    3.644494
    2024-01-06    2.738996
    2024-01-13    2.539155

The data ended it 2022 so it forecasted into 2023 and beyond, essentially its saying for the week of Dec 16 the business owner can predict to sell 2.38 units.


