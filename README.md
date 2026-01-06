# CoolingAISImFinal

## Overview
CoolingAISImFinal is a simulation project designed to model and analyze cooling systems. The project includes a logging mechanism to track various parameters during the simulation, making it easier to analyze performance and behavior.

## Project Structure
```
CoolingAISImFinal
├── src
│   ├── main.py
│   ├── simulation
│   │   ├── __init__.py
│   │   └── logger.py
│   ├── models
│   │   └── __init__.py
│   └── utils
│       └── __init__.py
├── tests
│   └── test_logger.py
├── requirements.txt
├── setup.py
└── README.md
```

## Installation
To set up the project, clone the repository and install the required dependencies. You can do this by running:

```
pip install -r requirements.txt
```

## Usage
To run the simulation, execute the main entry point:

```
python src/main.py
```

## Logger Class
The project includes a `Logger` class located in `src/simulation/logger.py`. This class is responsible for logging simulation data. It has the following methods:
- `__init__`: Initializes an empty list to store log data.
- `log(t, Q_IT, mdot_liq, mdot_air, T_rack)`: Logs the provided parameters as a tuple.
- `get()`: Returns the list of logged data.

## Testing
Unit tests for the Logger class are located in `tests/test_logger.py`. To run the tests, use:

```
pytest tests/test_logger.py
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.