Format your data according to the examples, and leave categorical information for the last column. The wrapper I used for visualization is quite picky, so for now only use a single categorical data column.
Custom visualization libraries fixing this problem is in the works. The file should be called data.txt

Run from main.py, as this program works with permutations, it scales factorially according to the number of dimensions you include in your set. The number of coordinates you include will also affect runtime. On my older computer it can take a few hours for a 8D dataset to complete.

If you wish to add more ranking modules, simply follow those input/output rules and ensure that it's a child class of Structs.rank_method with a function called rank that outputs your rankings. This was done to ensure consistency among the data flow of all modules. Lastly, just paste your module into the Modules folder and it should be incorporated seamlessly.

Gabe Gelgor
gabe.gelgor@stemfellowship.org
