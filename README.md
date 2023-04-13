# presto-toolbox

This project provides Python code that enables debugging and smoke testing for Presto and related queries. Although still in its early stages, the project is designed to meet my current needs and will continue to evolve with time.

## Prerequisites

## Prerequistes

- just (brew install just)
- python 3.9
- pipenv

## Usage

Generate a config.ini file. See example.

Then choose `just run` to see an example with your config.

### Example

```
➜ just run  
pipenv run python -m presto.query
Querying foo...
SELECT * FROM system.runtime.nodes
['i-002c86ea96f9ff61', 'http://10.0.101.125:8889', '0.27-amzn-0', False, 'active']
['i-00df5699f68ef3d6', 'http://10.0.101.137:8889', '0.27-amzn-0', True, 'active']
['i-0273da46c79d3ee6', 'http://10.0.101.166:8889', '0.27-amzn-0', False, 'active']
['i-05beb88027434f4f', 'http://10.0.101.170:8889', '0.27-amzn-0', False, 'active']
Total fetched 4 rows.
Elapsed time: 0.5393 seconds
```
## Develop

Use the `just` recipies.
