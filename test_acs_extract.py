#!/usr/bin/python
# Test that the ACS extract process worked by comparing with ground-truth files from American FactFinder

from subprocess import call
from sys import argv
import pandas as pd
import numpy as np
from tempfile import mkstemp

# Define test cases: a specification for columns, a geography, a ground-truth file, and columns to compare between the
# output of acs_extractor and the ground truth file.
testCases = [
    ('B08201_2', 'tracts', 'test_data/ACS_16_5YR_B08201_with_ann.csv', (('B08201_002', 'HD01_VD03'), ('B08201_002_MOE', 'HD02_VD03'))),
    ('B19001_3-6', 'blockgroups', 'test_data/ACS_16_5YR_B19001_with_ann.csv', (
        ('B19001_003', 'HD01_VD03'),
        ('B19001_003_MOE', 'HD02_VD03'),
        ('B19001_004', 'HD01_VD04'),
        ('B19001_004_MOE', 'HD02_VD04'),
        ('B19001_005', 'HD01_VD05'),
        ('B19001_005_MOE', 'HD02_VD05'),
        ('B19001_006', 'HD01_VD06'),
        ('B19001_006_MOE', 'HD02_VD06')
        )),
    ('B25094_*', 'tracts', 'test_data/ACS_16_5YR_B25094_with_ann.csv', (
        ('B25094_001', 'HD01_VD01'),
        ('B25094_001_MOE', 'HD02_VD01'),
        ('B25094_011', 'HD01_VD12'),
        ('B25094_011_MOE', 'HD02_VD12'),
        ('B25094_018', 'HD01_VD19'),
        ('B25094_018_MOE', 'HD02_VD19'),
    )),
    # One that has the weird fractional line numbers, to make sure we're lining everything up right
    ('B02019_*', 'tracts', 'test_data/ACS_16_5YR_B02019_with_ann.csv', (
        ('B02019_001', 'HD01_VD01'),
        ('B02019_001_MOE', 'HD02_VD01'),
        ('B02019_002', 'HD01_VD03'),
        ('B02019_002_MOE', 'HD02_VD03'),
        ('B02019_011', 'HD01_VD14'),
        ('B02019_011_MOE', 'HD02_VD14')
    ))
]

failCount = 0

for spec, geography, groundTruthFile, comparisons in testCases:
    fh, output = mkstemp()
    # Run the ACS Extractor
    call(['python', 'acs_extract.py', '--tracts', argv[1], 'B01003_*', spec, output])

    # Load up the files
    data = pd.read_csv(output)
    groundTruth = pd.read_csv(groundTruthFile)
    data = data.merge(groundTruth, left_on='geoid', right_on='GEO.id2')

    # Logging
    print(f'{spec} ({geography})')
    for left, right in comparisons:
        passed = np.all(data[left] == data[right])
        if not passed:
            anyFailed += 1
        print(f'  {left} - {right}: {"OK" if passed else "Fail!"}')

if failCount == 0:
    print('All tests passed :)')
else:
    print(f'THERE WERE {failCount} TEST FAILURES!')
