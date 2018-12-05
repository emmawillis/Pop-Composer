# Pop-Composer

## To train from scratch:

python model.py retrain 100  

= train for 100 epochs (can leave off epoch number to use default of 200 epochs)

****************************************************************************************

## To train starting from most recently saved weights (saved in weights.hdf5):

python model.py train 100

****************************************************************************************

## To evaluate on test data:

python model.py test

****************************************************************************************

## To generate a song:

python model.py generate  

= generate 100 note song using most recently saved weights

or just python model.py  

****************************************************************************************
## Notes:

This code requires Python 3.6, Keras 2.2.4, and Music21