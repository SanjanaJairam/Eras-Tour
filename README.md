## Taylor Swift Eras Tour Exploration

## Overview

Taylor Swift's Eras Tour Exploration

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [File Structure](#file-structure)


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.iu.edu/sajairam/eras_tour.git
   cd eras_tour
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app locally:

```bash
streamlit run app.py
```

Access the app in your browser at [http://localhost:8501](http://localhost:8501).

## Dependencies


```plaintext
streamlit==0.86.0
numpy==1.21.2
pandas==1.3.3
plotly==5.3.1
seaborn==0.11.2
matplotlib==3.4.3
pydeck==0.7.0
```

## File Structure


```
- app.py            # Main Streamlit app script
- data_processing.py    # Module for data loading and preprocessing
- charts.py         # Module for chart functions
- requirements.txt  # List of project dependencies
- ts_data/          # Directory containing data files
- README.md         # Project documentation
```

