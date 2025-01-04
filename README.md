# Taylor Swift Eras Tour Exploration

## Overview

This project provides an interactive web application for exploring data and visualizations related to Taylor Swift's Eras Tour. It allows users to dive into detailed insights about songs, eras, cities, and ticket sales through dynamic and customizable charts.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Dependencies](#dependencies)
4. [File Structure](#file-structure)
5. [Features](#features)
6. [Outputs](#outputs)
7. [Contribution](#contribution)
8. [License](#license)

---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the Streamlit app locally:

```bash
streamlit run app.py
```

Access the app in your browser at [http://localhost:8501](http://localhost:8501).

---

## Dependencies

The project requires the following Python libraries:

- `streamlit==0.86.0`
- `numpy==1.21.2`
- `pandas==1.3.3`
- `plotly==5.3.1`
- `seaborn==0.11.2`
- `matplotlib==3.4.3`
- `pydeck==0.7.0`

Install these libraries using the `requirements.txt` file.

---

## File Structure

```plaintext
- app.py              # Main Streamlit app script
- data_processing.py  # Module for data loading and preprocessing
- charts.py           # Module for chart functions
- requirements.txt    # List of project dependencies
- ts_data/            # Directory containing data files and assets
  └── eras-tour.jpg   # Image used in the Streamlit app
- README.md           # Project documentation
```

---

## Features

The Streamlit app offers the following features:

1. **Interactive Charts**: 
   - Frequency of songs played
   - Number of songs performed live
   - Song order by era
   - Musicality for Eras Concert
   - Compare musicality across cities
   - Popularity vs. song occurrences
   - Popularity of recorded songs by album
   - Tickets sold across cities

2. **Custom Filters**:
   - Filter by era, city, or specific metrics.
   - Compare data across multiple cities.

3. **Dynamic Visualizations**:
   - Heatmaps, bar charts, swarm plots, and comparative analysis visualizations.

---

## Outputs

- **Interactive Visualizations**:
  - Explore and compare data in real time based on selected filters and metrics.
- **Data Insights**:
  - Song popularity, performance trends, ticket sales, and more.
- **Visual Analysis**:
  - Gain insights into Taylor Swift's music across eras and cities through visual storytelling.

---

## Contribution

We welcome contributions to improve and expand this project! Feel free to submit issues or pull requests for bug fixes, new features, or data visualizations.

---

## License

This project is licensed under the [MIT License](https://github.com/SanjanaJairam/Eras-Tour/blob/main/LICENSE).

