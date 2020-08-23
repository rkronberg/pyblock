# pyblock

Python code for calculating error bounds for the average of a correlated dataset using the method of block averages. For mathematical details, see "Computer Simulation of Liquids" by Allen & Tildesley (2nd ed., Oxford University Press, 2017, p. 282-283).

## Usage

```python
from block_average import Blocked

# Pass timeseries and smallest number of blocks (bmin)
blk = Blocked(timeseries, bmin)

# Run the block averaging method
blk.run()

# Error estimation based on the statistical inefficiency
blk.error()
```

Code can also be run from the command line using the ```main.py``` script.

```bash
$ python main.py [-h] -i INPUT [-n BMIN] [-p]
```

Input and minimum number of blocks (defaults to 10) are passed as arguments. Optional flag ```-p``` enables a visualization of the statistical inefficiency estimation. A correlated sample timeseries ```data/sample.dat``` is provided.