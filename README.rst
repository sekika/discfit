Discfit: Disc permeameter fitting program
=======================

Discfit reads disc permeameter data in the field and calculates hydraulic parameters of the soil; saturated hydraulic conductivity and Gardner's alpha constant.

`Disc permeameter`_ is a tool for measuring hydraulic properties in the field. Steady-state periods in multiple constant head period are selected automatically from the data, and infiltration rate for each steady-state period is calculated. After that, infiltration rate at saturated condition is estimated by Gardner's exponential model,

.. _Disc permeameter: https://en.wikipedia.org/wiki/Disc_permeameter

 K(h) = Ks exp(αh)

where K is unsaturated hydraulic conductivity (cm/s), h is matric head (cm), Ks is saturated hydraulic conductivity (cm/s), α is a constant (/cm). Note that h is negative and αh is negative. Based on this equation, the linear relationship ln(q) = ln(qs) + αh is used for estimating qs (cm/s), the infiltration rate at the saturated condition, and α constant, as we have multiple point of (h, q) data from the disc permeameter. The hydraulic conductivity is calculated from the infiltration rate based on steady-state analysis of Wooding (1968);

 q = K(1 + 4 / παr)

where α is the Gardner's α and r is the diameter of the disc (cm). See equations (10) and (13) in Minastry and George (1999).

Install
---------------

Python 2 or 3 is required. Install Python at https://www.python.org/ . After that, install discfit by running

.. code-block:: bash

 pip install discfit

Usage
---------------

.. code-block:: bash

 discfit Filename dd dp

where

- Filename: File name of data file
- dd: diameter of the disc (cm)
- dp: inner diameter of the pipe (cm)

Format of data file
---------------

It is a csv file with time, water level, and suction head (absolute value of the matric head) as follows.

.. code-block:: csv

 # Comment line starts with '#'
 # Time (sec), Water level (cm), Suction head (cm)
 0, 58.32, 10.53
 10, 58.30, 10.57
 20, 58.33, 10.48

Reference
---------------
- Minasny, B., and B. H. George. 1999. `The measurement of soil hydraulic properties in the field.`_ in Cattle S.R. & George B.H. (Eds) Describing, Analysing and Managing Our Soil.
- Wooding, R.A., 1968. Steady infiltration from a shallow circular pond. Water Resources Research 4, 1259-1273.

.. _The measurement of soil hydraulic properties in the field.: http://www.academia.edu/download/6505821/Minasny___George_2001_DAMOS_hydraulic_Ch_12.pdf
