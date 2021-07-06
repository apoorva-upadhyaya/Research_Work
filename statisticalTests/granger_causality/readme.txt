We use Granger causality analysis to statistically test whether the time series of each of the attributes in the feature set may independently forecast (Granger-cause) the spread of the tweets. We perform pairwise(attribute-retweet) and joint tests (all attributes-retweet).  

Steps to be followed 
1. The attributes time series (per 5min interval) containing mean attribute scores and the retweet count per interval are fed to kpss test to test if the series is the stationary or not.
kpss test  : Null hypothesis: The time series is stationary, if p values are more than 0.05, then series is considered to be stationary.

2. Dataframe is created (columns : individual attribute and retweet if pairwise and all attributes and retweet if joint).
We implemnt VAR Model and we use the AIC in selecting the lag order.

3. We perform the Durbin Watson Test that provides a measure of autocorrelation in residuals from regression analysis( model residuals fitted from VAR).

4. We perform granger causality test using a function available on stack_overflow and other blog portals.


