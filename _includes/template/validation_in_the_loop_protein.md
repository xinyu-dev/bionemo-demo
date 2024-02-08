Validation in the loop is an optional quality control method. You will provide a dataset that predicts some properties of the protein. For example, you can use a `token-level-classification` task to predict the 3state structure of a protein. You can also use a sequence level `regression` to predict melting temperature of a protein, or`classification` to predict whether a protein in a binder or not.  During training, at user-specified intervals, the foundational model weights will be temporarily frozen, and sequences from this downstream task dataset will be embedded using the foundational model, and a classifier/regressor head will be added on top of it to train a small regressor/classifier. Ideally we would expect increase of accuracy or decrease of error as the training goes on.