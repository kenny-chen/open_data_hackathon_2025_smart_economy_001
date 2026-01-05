import { useEffect } from 'react'

function App() {
  return (
    <ef-layout style={{maxWidth: '1200px', margin: '0 auto'}}>
      <ef-header level="1">LSEG Refinitiv - Retail Bond Demand Model Backtest</ef-header>

      <ef-layout>
      <ef-tab-bar level="1">
      <ef-tab label="Data Preparation" active value="data-preparation"></ef-tab>
      <ef-tab label="Stationarity Check" value="stationarity-check"></ef-tab>
      <ef-tab label="Lag Selection" value="lag-selection"></ef-tab>
      <ef-tab label="Model Specification" value="model-specification"></ef-tab>
      <ef-tab label="Estimation" value="estimation"></ef-tab>
      <ef-tab label="Diagnostics" value="diagnostics"></ef-tab>
      <ef-tab label="Interpretation" value="interpretation"></ef-tab>
      <ef-tab label="Visualization" value="visualization"></ef-tab>
      <ef-tab label="Forecasting" value="forecasting"></ef-tab>
      </ef-tab-bar>
      </ef-layout>

      <ef-layout>
      <ef-panel spacing>
        <div role="group" aria-labelledby="header">
          <h6 id="header">Select Factors</h6>
          <ef-checkbox checked>bond annual interest rate_t</ef-checkbox>
          <ef-checkbox checked>bond annual interest rate_t-1</ef-checkbox>
          <ef-checkbox checked>bond annual interest rate_t-2</ef-checkbox>
          <ef-checkbox checked>num of population above 60_t</ef-checkbox>
          <ef-checkbox checked>num of population above 60_t-1</ef-checkbox>
          <ef-checkbox checked>num of population above 60_t-2</ef-checkbox>
          <ef-checkbox checked>money market fund nav_t</ef-checkbox>
          <ef-checkbox checked>money market fund nav_t-1</ef-checkbox>
          <ef-checkbox checked>money market fund nav_t-2</ef-checkbox>
          <ef-checkbox checked>demand deposit hkd_t</ef-checkbox>
          <ef-checkbox checked>demand deposit hkd_t-1</ef-checkbox>
          <ef-checkbox checked>demand deposit hkd_t-2</ef-checkbox>
          <ef-checkbox checked>time deposit hkd_t</ef-checkbox>
          <ef-checkbox checked>time deposit hkd_t-1</ef-checkbox>
          <ef-checkbox checked>time deposit hkd_t-2</ef-checkbox>
          <ef-checkbox checked>hsi close price_t</ef-checkbox>
          <ef-checkbox checked>hsi close price_t-1</ef-checkbox>
          <ef-checkbox checked>hsi close price_t-2</ef-checkbox>
        </div>

        <p>
          <label for="curr1" class="label">Backtest Steps</label>
          <ef-number-field value="50" step="1" min="1" id="curr1"></ef-number-field>

          <label for="backtest-date">Backtest date</label>
          <ef-datetime-picker id="backtest-date" range duplex opened value="2026-01-05"></ef-datetime-picker>

          <span class="label">Export Excel</span><ef-toggle checked></ef-toggle>
        </p>

        <p><ef-button>Submit</ef-button></p>
      </ef-panel>
      </ef-layout>

      <ef-led-gauge top-label="87.45" top-value="70" range-label="Average True & Accurate & Valid" range="[0, 100]"></ef-led-gauge>

      <ef-layout style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px'}}>
        <ef-swing-gauge
          primary-value="87.39"
          secondary-value="12.61"
          primary-label="True"
          secondary-label="False"
          primary-legend="True Backtest"
          secondary-legend="False Backtest">
        </ef-swing-gauge>
        <ef-swing-gauge
          primary-value="75.20"
          secondary-value="24.80"
          primary-label="Accurate"
          secondary-label="Inaccurate"
          primary-legend="Accurate Predictions"
          secondary-legend="Inaccurate Predictions">
        </ef-swing-gauge>
        <ef-swing-gauge
          primary-value="92.15"
          secondary-value="7.85"
          primary-label="Valid"
          secondary-label="Invalid"
          primary-legend="Valid Model Results"
          secondary-legend="Invalid Model Results">
        </ef-swing-gauge>
      </ef-layout>

      <ef-layout style={{textAlign: 'center'}}><br /><ef-pagination max="9"></ef-pagination></ef-layout>

    </ef-layout>
  )
}

export default App