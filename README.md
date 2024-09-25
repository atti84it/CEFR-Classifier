CEFR-Classifier is a Python package that evaluates the CEFR level of a given text. It's packed in a way you can easily include it into your project. 

It's language-agnostic, so it works with most languages. 

It's based on the assumption that we can use the relative frequency of word endings to determine the complexity of a text. For example in Italian, endings like "-o, -i, -are" are more frequent in beginner levels, while endings like "-eranno, -issero, -zialità" are more frequent in advanced levels. The training script creates a list of endings and assigns a relative frequency value to each of them based on how many times they appear in the corpus files. Then, when you want to evaluate the CEFR level of a text, the classifying function will weight the probability of each level according to the endings in the given text.

# How to use

Clone this repository and put it in a subfolder of your project.

This package is already trained on Italian language, and ready to use. If you want to train on another language, refer to the [How to train](#how-to-train) section.

Then using the package is very easy:

```
from cefr_classifier import CEFRClassifier
classifier = CEFRClassifier()
result = classifier.classify("This is a sample text")

> result = 'A1'
```


Check the `evaluate.py` file in the root folder to find some sample code.

# How to train

This package is already trained on Italian language. If you want to train on your own corpus, follow these steps.

You can use in the training two types of files:

1. **Dirty files**: files that are eventually made of multiple parts. The text might have **hyphens** splitting words in two parts at the end of the line. If you have such kind of files, you can put them in the `assets/CEFR_corpus_dirty_files` in the corresponding subfolder for each CEFR level, e.g. 'A1', 'A2', etc.
2. **Clean files**: files that are ready to be used for training. These will go in the `assets/CEFR_corpus_files` in the corresponding subfolder for each CEFR level.

If you have "dirty files" you can run the script that will clean them (e.g. remove hyphens) and put them in the right folders before training.

**Important**: the files must be in .txt format. Don't include any metadata.

## Cleaning the data

Here are two examples of what do "dirty" and "clean" files mean.

Contents of `assets/CEFR_corpus_dirty_files/A1/any_name.txt`:

```
This is the first text. There are many lines, some have hyphens, like 'pas-
sion'. This kind of lines will be reconstructed by the cleaning script. Some lines like this one
end without a dot. This kind of lines will be fixed by the cleaning script too.
This line is still part of the first text.

This line as well is part of the first text, since it's separated from the previous text by only 2 returns.


This is the SECOND text. It's a separate text. It's separated from the previous one by 3 returns.
```

Example of a "clean file": `assets/CEFR_corpus_files/A1/any_name.txt`

```
This is the first text. There are many lines, some have hyphens, like 'passion'. This kind of lines will be reconstructed by the cleaning script. Some lines like this one end without a dot. This kind of lines will be fixed by the cleaning script too.
This line is still part of the first text.

This line as well is part of the first text, since it's separated from the previous text by only 2 returns. 
```

## The cleaning script

If you already have "clean files", you can skip this section.

The cleaning script does the following:

1. Recognizes the parts of text that are separated by 3 returns ("`\n\n\n`"). It creates a new clean file from each of these parts. Using or not the three returns should not affect the final results since the math is based on the frequency of each word. You could even put all A1 text in one single file and the final weights *should* not change.
2. Joins one line with the next one if the first ends with an hyphen and if the merged word is recognized as valid by the spellchecker.
3. Joins one line with the next one if the first doesn't end with a punctuation mark. 
4. Writes the words that aren't recognized by the spellchecker in `assets/CEFR_weights/parole_sconosciute.txt`

To run the cleaning script run `clean_corpus_files.sh`. This script will output the clean (unwrapped, etc.) files in `assets/CEFR_corpus_files` folder. 

## Do the training

Run the `train.sh` script. This script will train the model and save the weights in the `assets/CEFR_weights/rime.csv` file.

## Evaluate controls

You can evaluate control texts to check the accuracy of your trained model. Put your texts to be evaluated in the directory `assets/CEFR_controls`. In the name of control files you have to include the CEFR level, e.g. 'lorem a1 ipsum.txt' will be recognized as A1. It's case insensitive.

The content of control files must be pure text, without metadata.

Finally run the `evaluate controls.sh` script.

# Windows users

The package has been created on Linux. However it should work on Windows as well. The `.bat` files for cleaning files and training are not provided, but if you check the `.sh` files it should be straightforward. 

