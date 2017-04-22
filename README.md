# Miniproject-Bioinformatics2

This is a mini project code files for "Topics in Bioinformatics 2" course in BGU. 

Article: Parikh Mapping-based algorithm for finding gene clusters  
Link: http://www.sciencedirect.com/science/article/pii/S1570866703000352  

This is an implementation in python2.7.

Before use, please install redis.  
* For Linux: https://redis.io/download  
* For Windows: https://github.com/MSOpenTech/redis/releases


Install modules via pip, if they are not already installed:  
```
pip install redis
pip install ast
pip install datetime
```


Before running the program:  
```
cd <project-folder>
python src/preprocess.py -taxa <path-to-taxa-data-file>
python src/preprocess.py -sigma <path-to-sigma-data-file>
python src/preprocess.py -strings <path-to-strings-data-file>
python src/preprocess.py -cogs <path-to-cogs-info-file>
```

Available options for preprocess.py:
* -taxa <path-to-taxa-data-file>:  
    Builds the taxa DB accordingly
* -sigma <path-to-sigma-data-file>:  
    Builds the sigma DB accordingly
* -strings <path-to-strings-data-file>:  
    Builds the strings DB and strains DB accordingly
* -cogs <path-to-cogs-info-file>:
    Builds the COGs function DB and the COGs list DB accordingly
    

Now you can run the program (No need to repeat the previous steps on your machine anymore):  
```
cd <project-folder>
python src/run.py <option> <arg>
```

Available options for run.py:  
* -f <family-name> :  
    Runs algorithm for a specific family, for example: -f bacgroup_Acidobacteria.
* -t <family-type>:  
    Runs algorithm for a specific family type, for example: -t bacgroup.
    
For postprocessing: 
```
cd <project-folder>
python src/postprocess.py <fingerprints-file-path> <option>
```

Available options for postprocess.py:
* -threshold :  
    Runs postprocessing for thresholds of [0.05, 0.1, 0.2, 0.3, 0.5, 0.8], where x in thresholds array is the % of strings of all the strings for this family with the same fingerprint.
* -cogs <list-of-cogs-function> :  
    Runs postprocessing for a specific COGs function list, for example: -cogs ['S','V','V'].  
    Finds all fingerprints with those functions that are above threshold (as in the previous option).
