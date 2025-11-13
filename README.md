# Dalberg Data Pipeline

A comprehensive data pipeline system for ingesting, processing, analyzing, and distributing insights from various data sources. This project focuses on generating actionable insights related to credit access, food security, and women's agency.

## Overview

This project provides a modular data pipeline architecture that:
- Ingests data from multiple sources (APIs, databases, files)
- Validates and transforms data
- Harmonizes data from different sources
- Performs bias checks and data quality assessments
- Generates actionable insights
- Distributes insights via SMS alerts

## Project Structure

```
dalberg/
├── data_ingestion/
│   ├── data_sources.py      # Abstract data source classes
│   ├── fetch_data.py        # API data fetching utilities
│   ├── data_transformers.py # Data transformation functions
│   └── validate_data.py     # Data validation and quality checks
├── data_processing/
│   ├── harmonize.py         # Data harmonization across sources
│   └── bias_checks.py       # Bias detection and mitigation
├── insights_engine/
│   └── generate_insights.py # Insight generation from processed data
└── distribution/
    └── sms_delivery.py      # SMS alert distribution via Twilio
```

## Features

### Data Ingestion
- **Multiple Data Sources**: Support for APIs, databases, and file-based sources
- **Data Validation**: Comprehensive validation checks for data quality
- **Data Transformation**: Flexible transformation pipeline

### Data Processing
- **Data Harmonization**: Aligns data from different sources with varying schemas
- **Bias Detection**: Uses AIF360 library for bias detection and mitigation
- **Quality Assurance**: Ensures data integrity throughout the pipeline

### Insights Generation
- **Credit Access Metrics**: Calculates credit approval rates and loan amounts
- **Food Security Analysis**: Analyzes agriculture output and food security indicators
- **Women's Agency Assessment**: Evaluates women's inclusion and participation metrics

### Distribution
- **SMS Alerts**: Sends insights and alerts via Twilio SMS service

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/petergt44/dalberg.git
cd dalberg
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:

Create a `.env` file in the root directory:
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+1234567890
API_KEY=your_api_key
```

Or export them in your shell:
```bash
export TWILIO_ACCOUNT_SID=your_account_sid
export TWILIO_AUTH_TOKEN=your_auth_token
export TWILIO_FROM_NUMBER=+1234567890
export API_KEY=your_api_key
```

## Usage

### Data Ingestion

```python
from data_ingestion.fetch_data import fetch_data_from_api

data = fetch_data_from_api(
    url="https://api.example.com/data",
    api_key="your_api_key"
)
```

### Data Validation

```python
from data_ingestion.validate_data import validate_data

df = validate_data(data)
```

### Data Harmonization

```python
from data_processing.harmonize import harmonize_data

harmonized_df = harmonize_data(df1, df2)
```

### Bias Checking

```python
from data_processing.bias_checks import check_for_bias

has_bias = check_for_bias(
    df,
    privileged_groups=[{"gender": 1}],
    unprivileged_groups=[{"gender": 0}]
)
```

### Insights Generation

```python
from insights_engine.generate_insights import generate_insights

insights = generate_insights(df)
print(insights['credit_access'])
print(insights['food_security'])
print(insights['women_agency'])
```

### SMS Distribution

```python
from distribution.sms_delivery import send_sms_alert

result = send_sms_alert(
    phone_number="+1234567890",
    message="Your insight alert message"
)
print(f"Message SID: {result['sid']}, Status: {result['status']}")
```

## Dependencies

See `requirements.txt` for the complete list. Main dependencies include:
- `pandas` - Data manipulation and analysis
- `requests` - HTTP library for API calls
- `twilio` - SMS delivery service
- `aif360` - Bias detection and fairness metrics
- `numpy` - Numerical computing

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Contact

For questions or issues, please open an issue on GitHub.

