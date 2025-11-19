# VW-Bandit

A PoC to experiment building contextual multi-armed bandits with the [Vowpal Wabbit](https://vowpalwabbit.org/) ML library.

The use-case is rolling out new recommender models in production.

## Usage

Sample data can be created via the [create_sample_data](notebooks/create_sample_data.ipynb) notebook, or via:

```bash
uv run generate_data --overwrite true
```

To train the bandit, create the sample data and then execute a round of training via one of:

Shell:
```bash
uv run bandit --country_code UK
```

Docker:
```bash
COUNTRY_CODE=UK docker compose up --build -d
```

Jupyter notebook:
- [notebooks/bandit_training.ipynb](notebooks/bandit_training.ipynb)

