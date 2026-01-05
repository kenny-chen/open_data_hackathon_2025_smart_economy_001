import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss
import statsmodels.api as sm
import numpy as np
import os
from itertools import combinations
import matplotlib.pyplot as plt

# Configuration
output_path = 'output'
os.makedirs(output_path, exist_ok=True)
start_date = '2022-01-01'
min_data_points = 10
all_cols = ['total bond subscription amount in hkd', 'bond annual interest rate', 'num of population above 60', 'money market fund nav', 'demand deposit hkd', 'time deposit hkd', 'hsi close price']

# Path to your Excel file
file_path = "../data/前沿資本-零售債券模型-回測結果-20251231a.xlsx"

# Read all sheets at once with column specifications
sheet_configs = {
    "前沿資本-零售債券-市場認購": ["datetime", "total bond subscription amount in hkd", "bond annual interest rate"],
    "政府統計處-各年出生人口": ["datetime", "num of population above 60"],
    "香港交易所-泰康開泰港元貨幣基金": ["datetime", "money market fund nav"],
    "香港金融管理局-港元及外幣存款": ["datetime", "demand deposit hkd", "time deposit hkd"],
    "Wind-盈富基金": ["datetime", "hsi close price"]
}

dfs = {sheet: pd.read_excel(file_path, sheet_name=sheet, usecols=cols) 
       for sheet, cols in sheet_configs.items()}

# Extract individual DataFrames
df_bond_subscription = dfs["前沿資本-零售債券-市場認購"]
df_population = dfs["政府統計處-各年出生人口"]
df_fund_nav = dfs["香港交易所-泰康開泰港元貨幣基金"]
df_deposits = dfs["香港金融管理局-港元及外幣存款"]
df_tracker_fund = dfs["Wind-盈富基金"]

# Convert datetime and set index for all dataframes
for df in [df_bond_subscription, df_population, df_fund_nav, df_deposits, df_tracker_fund]:
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

# Resample all data to monthly end-of-month
df_bond_subscription = df_bond_subscription.resample('ME').last()
df_population = df_population.resample('ME').last()
df_fund_nav = df_fund_nav.resample('ME').last()
df_deposits = df_deposits.resample('ME').last()
df_tracker_fund = df_tracker_fund.resample('ME').last()

# Combine all dataframes
combined_df = df_bond_subscription.join([df_population, df_fund_nav, df_deposits, df_tracker_fund], how='outer')

# Apply forward fill to specified columns
combined_df[all_cols] = combined_df[all_cols].ffill()

# Filter data to start from configured date
combined_df = combined_df.loc[start_date:]

# Save combined data to CSV
combined_df.to_csv(f'{output_path}/001_combined_financial_data.csv')

# Apply ADF and KPSS tests
test_results = []
for col in combined_df.columns:
    if combined_df[col].notna().sum() > min_data_points:  # Only test columns with sufficient data
        # ADF test
        adf_stat, adf_pvalue, _, _, adf_critical, _ = adfuller(combined_df[col].dropna())
        
        # KPSS test
        kpss_stat, kpss_pvalue, _, kpss_critical = kpss(combined_df[col].dropna())
        
        test_results.append({
            'variable': col,
            'adf_statistic': adf_stat,
            'adf_pvalue': adf_pvalue,
            'adf_critical_1%': adf_critical['1%'],
            'adf_critical_5%': adf_critical['5%'],
            'adf_critical_10%': adf_critical['10%'],
            'kpss_statistic': kpss_stat,
            'kpss_pvalue': kpss_pvalue,
            'kpss_critical_1%': kpss_critical['1%'],
            'kpss_critical_5%': kpss_critical['5%'],
            'kpss_critical_10%': kpss_critical['10%']
        })

# Create DataFrame with test results
test_results_df = pd.DataFrame(test_results)

# Save test results to CSV
test_results_df.to_csv(f'{output_path}/002_stationarity_tests.csv', index=False)

# Apply log transformation to create new dataframe
combined_df_log = combined_df.copy(deep=True)
for col in all_cols:
    combined_df_log[col] = np.log(combined_df[col])

# Apply z-score standardization to money market fund nav only
combined_df_log['money market fund nav'] = (combined_df_log['money market fund nav'] - combined_df_log['money market fund nav'].mean()) / combined_df_log['money market fund nav'].std()

# Save log-transformed data to CSV
combined_df_log.to_csv(f'{output_path}/003_log_transformed_data.csv')

# Apply ADF and KPSS tests on log-transformed data
test_results_log = []
for col in combined_df_log.columns:
    if combined_df_log[col].notna().sum() > min_data_points:
        # ADF test
        adf_stat, adf_pvalue, _, _, adf_critical, _ = adfuller(combined_df_log[col].dropna())
        
        # KPSS test
        kpss_stat, kpss_pvalue, _, kpss_critical = kpss(combined_df_log[col].dropna())
        
        test_results_log.append({
            'variable': col,
            'adf_statistic': adf_stat,
            'adf_pvalue': adf_pvalue,
            'adf_critical_1%': adf_critical['1%'],
            'adf_critical_5%': adf_critical['5%'],
            'adf_critical_10%': adf_critical['10%'],
            'kpss_statistic': kpss_stat,
            'kpss_pvalue': kpss_pvalue,
            'kpss_critical_1%': kpss_critical['1%'],
            'kpss_critical_5%': kpss_critical['5%'],
            'kpss_critical_10%': kpss_critical['10%']
        })

# Create DataFrame with log-transformed test results
test_results_log_df = pd.DataFrame(test_results_log)

# Save log-transformed test results to CSV
test_results_log_df.to_csv(f'{output_path}/004_stationarity_tests_log.csv', index=False)

# AIC/BIC Lag Selection for dependent variable
dependent_var = 'total bond subscription amount in hkd'
y = combined_df_log[dependent_var].dropna()

# Test different lag orders (1 to 12 for monthly data)
max_lags = min(12, len(y) // 4)  # Ensure sufficient observations
lag_results = []

for lag in range(1, max_lags + 1):
    try:
        model = sm.tsa.AutoReg(y, lags=lag, trend='c')
        fitted_model = model.fit()
        
        lag_results.append({
            'lag': lag,
            'aic': fitted_model.aic,
            'bic': fitted_model.bic,
            'log_likelihood': fitted_model.llf,
            'params': fitted_model.nobs
        })
    except:
        continue

# Create DataFrame with lag selection results
lag_selection_df = pd.DataFrame(lag_results)

# Find optimal lags
if not lag_selection_df.empty:
    optimal_aic_lag = lag_selection_df.loc[lag_selection_df['aic'].idxmin(), 'lag']
    optimal_bic_lag = lag_selection_df.loc[lag_selection_df['bic'].idxmin(), 'lag']
    
    lag_selection_df['optimal_aic'] = lag_selection_df['lag'] == optimal_aic_lag
    lag_selection_df['optimal_bic'] = lag_selection_df['lag'] == optimal_bic_lag

# Save lag selection results to CSV
lag_selection_df.to_csv(f'{output_path}/005_lag_selection_aic_bic.csv', index=False)

# Multi-variable Distributed Lag Model (DLM) with Lag = 2
def create_multi_dlm_data(df, y_col, x_cols, lags=2):
    """Create lagged variables for multi-variable DLM"""
    cols_needed = [y_col] + x_cols
    data = df[cols_needed].dropna().copy()
    
    # Create lagged variables for each X variable
    X_columns = []
    for x_col in x_cols:
        for i in range(lags + 1):
            if i == 0:
                col_name = f'{x_col}_t'
            else:
                col_name = f'{x_col}_t-{i}'
            data[col_name] = data[x_col].shift(i)
            X_columns.append(col_name)
    
    return data.dropna(), X_columns

# Multi-variable DLM: Model bond subscription using all variables with 2 lags
y_var = 'total bond subscription amount in hkd'
x_vars = ['bond annual interest rate', 'num of population above 60', 'money market fund nav', 'demand deposit hkd', 'time deposit hkd', 'hsi close price']

# Create multi-variable DLM dataset
dlm_data, X_columns = create_multi_dlm_data(combined_df_log, y_var, x_vars, lags=2)

# Prepare variables for regression
y = dlm_data[y_var]
X = dlm_data[X_columns]
X = sm.add_constant(X)  # Add intercept

# Fit multi-variable DLM model
dlm_model = sm.OLS(y, X).fit()

# Print results
print("Multi-variable DLM Results (Lag=2):")
print(dlm_model.summary())

# Save DLM summary as CSV
conf_int = dlm_model.conf_int()
summary_data = {
    'Variable': dlm_model.params.index,
    'Coefficient': dlm_model.params.values,
    'Std_Error': dlm_model.bse.values,
    'T_Statistic': dlm_model.tvalues.values,
    'P_Value': dlm_model.pvalues.values,
    'CI_Lower': conf_int.iloc[:, 0].values,
    'CI_Upper': conf_int.iloc[:, 1].values
}
summary_df = pd.DataFrame(summary_data)
summary_df.to_csv(f'{output_path}/006_dlm_summary.csv', index=False)

# Save detailed model summary statistics
from scipy import stats
residuals = dlm_model.resid
omni_stat, omni_pval = stats.normaltest(residuals)
jb_stat, jb_pval = stats.jarque_bera(residuals)
skewness = stats.skew(residuals)
kurt = stats.kurtosis(residuals)
dw_stat = sm.stats.durbin_watson(residuals)

detailed_stats = pd.DataFrame({
    'Metric': ['Dep. Variable', 'Model', 'Method', 'R-squared', 'Adj. R-squared', 'F-statistic', 
               'Prob (F-statistic)', 'Log-Likelihood', 'AIC', 'BIC', 'No. Observations', 
               'Df Residuals', 'Df Model', 'Omnibus', 'Prob(Omnibus)', 'Skew', 'Kurtosis', 
               'Durbin-Watson', 'Jarque-Bera (JB)', 'Prob(JB)', 'Cond. No.'],
    'Value': [y_var, 'OLS', 'Least Squares', dlm_model.rsquared, dlm_model.rsquared_adj, 
              dlm_model.fvalue, dlm_model.f_pvalue, dlm_model.llf, dlm_model.aic, dlm_model.bic,
              dlm_model.nobs, dlm_model.df_resid, dlm_model.df_model, 
              omni_stat, omni_pval, skewness, kurt, dw_stat, jb_stat, jb_pval, dlm_model.condition_number]
})
detailed_stats.to_csv(f'{output_path}/007_dlm_detailed_summary.csv', index=False)

# Plot Lag Impact Curve
import matplotlib.pyplot as plt

# Parse variable names and create pivot
lag_data = summary_df[summary_df['Variable'] != 'const'].copy()
lag_data[['base_var', 'lag']] = lag_data['Variable'].str.extract(r'(.+)_t(?:-([12]))?')
lag_data['lag'] = lag_data['lag'].fillna('0').astype(int)
pivot_df = lag_data.pivot(index='base_var', columns='lag', values=['Coefficient', 'P_Value']).fillna(0)

# Create grouped bar chart
fig, ax = plt.subplots(figsize=(12, 8))
bar_width = 0.25
x = np.arange(len(pivot_df.index))

for i, lag in enumerate([0, 1, 2]):
    if lag in pivot_df['Coefficient'].columns:
        bars = ax.bar(x + i*bar_width, pivot_df['Coefficient'][lag], bar_width, 
                     label=f'L{lag} (t{"" if lag==0 else f"-{lag}"})', alpha=0.8,
                     edgecolor=['red' if p < 0.05 else 'none' for p in pivot_df['P_Value'][lag]], 
                     linewidth=2)

ax.set_xlabel('Variables')
ax.set_ylabel('Coefficient')
ax.set_title('Lag Impact Curve - DLM Coefficients by Variable and Lag')
ax.set_xticks(x + bar_width)
ax.set_xticklabels([var.replace('_', ' ').title() for var in pivot_df.index], rotation=45, ha='right')
ax.legend()
ax.grid(True, alpha=0.3)
ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)

plt.tight_layout()
plt.savefig(f'{output_path}/008_lag_impact_curve.png', dpi=300, bbox_inches='tight')
plt.show()

# Heatmap: β by variable × lag
import seaborn as sns

# Create coefficient matrix for heatmap
coeff_matrix = pivot_df['Coefficient'].copy()
coeff_matrix.columns = [f'Lag {col}' for col in coeff_matrix.columns]
coeff_matrix.index = [var.replace('_', ' ').title() for var in coeff_matrix.index]

# Create heatmap
fig, ax = plt.subplots(figsize=(8, 10))
sns.heatmap(coeff_matrix, annot=True, cmap='RdBu_r', center=0, 
            fmt='.3f', cbar_kws={'label': 'Coefficient (β)'}, ax=ax)
ax.set_title('Heatmap: β Coefficients by Variable × Lag')
ax.set_xlabel('Lag Period')
ax.set_ylabel('Variables')

plt.tight_layout()
plt.savefig(f'{output_path}/009_coefficient_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# Cumulative impact ranking (L0+L1+L2)
cumulative_impact = pivot_df['Coefficient'].sum(axis=1).sort_values(key=abs, ascending=False)
cumulative_impact.index = [var.replace('_', ' ').title() for var in cumulative_impact.index]

fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(range(len(cumulative_impact)), cumulative_impact.values, 
               color=['green' if x > 0 else 'red' for x in cumulative_impact.values], alpha=0.7)
ax.set_yticks(range(len(cumulative_impact)))
ax.set_yticklabels(cumulative_impact.index)
ax.set_xlabel('Cumulative Impact (L0+L1+L2)')
ax.set_title('Variable Ranking by Cumulative Impact Across All Lags')
ax.axvline(x=0, color='black', linestyle='-', alpha=0.5)
ax.grid(True, alpha=0.3)

for i, v in enumerate(cumulative_impact.values):
    ax.text(v + (0.01 if v >= 0 else -0.01), i, f'{v:.3f}', 
            va='center', ha='left' if v >= 0 else 'right')

plt.tight_layout()
plt.savefig(f'{output_path}/010_cumulative_impact_ranking.png', dpi=300, bbox_inches='tight')
plt.show()