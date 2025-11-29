<h1>Aggregated Tables</h1>

<table border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>Page</th>
      <th>Requirements</th>
      <th>Aggregate By</th>
      <th>Tables</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Overview</td>
      <td>
        - Averages (temperature, precipitation, snow depth)<br>
        - Totals (precipitation, snow depth)<br>
        - Maxima &amp; minima (min temp, max temp, precipitation, snow depth)<br>
        - Dates for maxima &amp; minima<br>
        - Counts of extremes
      </td>
      <td>
        - Month<br>
        - Station
      </td>
      <td>
        Table 1: Monthly Aggregates, <br> Table 3: Extreme Events, <br> Table 4: Yearly Extreme Event Counts
      </td>
    </tr>
    <tr>
      <td>Geospatial Map</td>
      <td>
        - Averages (temperature, precipitation, snow depth)<br>
        - Station metadata
      </td>
      <td>
        - Month<br>
        - Station
      </td>
      <td>
        Table 1: Monthly Aggregates
      </td>
    </tr>
    <tr>
      <td>Trends &amp; Time Series</td>
      <td>
        - Values (min temp, max temp, precipitation, snow depth)<br>
        - Outlier thresholds
      </td>
      <td>
        - Month/Year <br>(depending on period length)<br>
        - Station
      </td>
      <td>
        Table 1: Monthly Aggregates, <br> Table 2: Yearly Aggregates (maybe)
      </td>
    </tr>
    <tr>
      <td>Seasonal Patterns</td>
      <td>
        - Averages (temperature, precipitation, snow depth)<br>
        - Totals (precipitation, snow depth)<br>
        - Maxima &amp; minima (min temp, max temp, precipitation, snow depth)
      </td>
      <td>
        - Month<br>
        - Station
      </td>
      <td>
        Table 1: Monthly Aggregates
      </td>
    </tr>
    <tr>
      <td>Extreme Events</td>
      <td>
        - Event count<br>
        - Date of most recent event<br>
        - Maxima &amp; minima (date and value: temperature, precipitation, snow depth)
      </td>
      <td>
        - Month<br>
        - Station
      </td>
      <td>
        Table 1: Monthly Aggregates, <br> Table 3: Extreme Events, <br> Table 4: Yearly Extreme Event Counts
      </td>
    </tr>
    <tr>
      <td>Statistical Analysis</td>
      <td>
        - Bins (1°C, 10 mm, 5 cm)<br>
        <strong>For Temp, Precip, Snow:</strong><br>
        <ul style="margin-top:4px; margin-bottom:4px;">
          <li>Mean</li>
          <li>Median</li>
          <li>Standard Deviation</li>
          <li>Skewness</li>
          <li>Range (min &amp; max)</li>
        </ul>
      </td>
      <td>
        - Month<br>
        - Station
      </td>
      <td>
        Table 1: Monthly Aggregates, <br> Table 6: Distributions
      </td>
    </tr>
    <tr>
      <td>Climate Comparison</td>
      <td>
        - Average temperature<br>
        - Temperature range<br>
        - Total precipitation<br>
        - Extreme event count
      </td>
      <td>
        - Month/Year<br>
        - Station
      </td>
      <td>
        Table 2: Yearly Aggregates, <br> Table 4: Yearly Extreme Event Counts
      </td>
    </tr>
    <tr>
      <td>Data Coverage</td>
      <td>
        - Missing % for 
        <ul style="margin-top:4px; margin-bottom:4px;">
          <li>Temperature</li>
          <li>Precipitation</li>
          <li>Snow Depth</li>
          <li>Total per Station</li>
        </ul>
        - Start and End Date for each Station
      </td>
      <td>
        - Month/Year<br>
        - Station
      </td>
      <td>
        Table 1: Monthly Aggregates, <br> Table 5: Coverage Table
      </td>
    </tr>
  </tbody>
</table>

<h2>Tables</h2>

<h3>Table 1: Monthly Aggregates</h3>
<p>partitioned by (station_id, year)</p>
<table border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>station_id</th>
      <th>year</th>
      <th>month</th>
      <th>avg_tmin</th>
      <th>avg_tmax</th>
      <th>avg_temp</th>
      <th>min_temp</th>
      <th>max_temp</th>
      <th>total_precip</th>
      <th>max_precip</th>
      <th>avg_snow_depth</th>
      <th>max_snow_depth</th>
      <th>missing_tmin</th>
      <th>missing_tmax</th>
      <th>missing_precip</th>
      <th>missing_snow</th>
    </tr>
  </thead>
</table>

<h3>Table 2: Yearly Aggregates</h3>
<p>partitioned by (station_id)</p>
<table border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>station_id</th>
      <th>year</th>
      <th>avg_tmin</th>
      <th>avg_tmax</th>
      <th>avg_temp</th>
      <th>min_temp</th>
      <th>max_temp</th>
      <th>total_precip</th>
      <th>max_precip</th>
      <th>avg_snow_depth</th>
      <th>max_snow_depth</th>
    </tr>
  </thead>
</table>

<h3>Table 3: Extreme Events</h3>
<p>partitioned by (station_id, year)</p>
<table border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>station_id</th>
      <th>date</th>
      <th>event_type</th>
      <th>value</th>
    </tr>
  </thead>
</table>

<h3>Table 4: Yearly Extreme Event Counts</h3>
<table border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>station_id</th>
      <th>year</th>
      <th>heatwave_count</th>
      <th>coldwave_count</th>
      <th>heavy_precip_count</th>
      <th>snowfall_count</th>
    </tr>
  </thead>
</table>

<h3>Table 5: Coverage Table</h3>
<p>partitioned by (station_id)</p>
<table border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>station_id</th>
      <th>year</th>
      <th>missing_tmin</th>
      <th>missing_tmax</th>
      <th>missing_precip</th>
      <th>missing_snow</th>
      <th>missing_percentage</th>
    </tr>
  </thead>
</table>

<h3>Table 6: Distributions</h3>
<p>partitioned by (station_id, variable)</p>
<table border="1" cellspacing="0" cellpadding="6">
  <thead>
    <tr>
      <th>station_id</th>
      <th>variable</th>
      <th>bin_min</th>
      <th>bin_max</th>
      <th>count</th>
    </tr>
  </thead>
</table>
