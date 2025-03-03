# Insurance Pricing Example

This directory contains example files for the py-pricer library. You can use these files as a starting point for your own insurance pricing model.

## Directory Structure

- `data/`: Contains example quote data in JSON format
- `rating/`: Contains the rating engine and related files
  - `tables/`: Contains rating tables used by the rating engine
- `transformations/`: Contains data transformation logic

## Customization

You can customize the following components:

1. **Input Data**: Add your own quote data files to the `data/` directory
2. **Rating Tables**: Modify the CSV files in `rating/tables/` to adjust base rates and factors
3. **Transformations**: Edit the transformation logic in `transformations/transform.py`
4. **Rating Engine**: Customize the rating algorithm in `rating/rating_engine.py`

## Workflow

1. The py-pricer library loads quote data from the `data/` directory
2. It applies transformations from `transformations/transform.py`
3. It calculates premiums using the rating engine in `rating/rating_engine.py`
4. Results can be viewed in the Streamlit app or accessed via the API

For more information, see the [py-pricer documentation](https://github.com/PricingFrontier/py-pricer).
