# CMU Kids Corpus Annotations

**Children's Reading Assessment** is the task of evaluating the correctness of a child's read aloud speech of a passage. The main goal is to provide meaningful feedback of the read speech so that it can be used to improve their reading fluency. 

**Disfluency Detection and Classification** thus becomes an important step to achieve this goal. This is a very challenging problem because of two reasons:

- Fewer number of datasets that have children's speech
- Lack of task-oriented annotations in the existing datasets 

This repository provides a simple script `annotate_cmuk.py` that uses a novel labelling scheme for the [CMU Kids Corpus](https://catalog.ldc.upenn.edu/LDC97S63) 
as well as the final labels `cmuk_labels.csv` generated based on the proposed scheme. The main motivation is to encourage future work towards collecting more children’s speech datasets for building robust reading assessment models.


**Prerequisites:** [Python](https://www.python.org/downloads/)
## About the dataset

The [CMU Kids Corpus](https://catalog.ldc.upenn.edu/LDC97S63) has 24 male speakers and 52 female speakers
in the age range of six to eleven, with a total of 5,180 utterances. The dataset consists of the following files:

| Files | Contents |
| ------------- | ------------- |
| Sentence | All the sentences used for the read aloud task |
| Point  | The remarks describing the speech by a human annotator for each of speech files  |
| Transcrip | The transcripts of the child's read aloud speech  |
| Kids | The recorded audio of the child reading a passage |

## Annotations

The speech is labeled at the word level. These labels 
fall under the following categories:

| Labels| Definition |
| ------------- | ------------- |
| Stutter | Some syllables in a word are repeated |
| Repeat  | A word is uttered more than once  |
| Incorrect | The uttered word does not match the actual word in the passage  |
| Skip | A word is omitted while reading the passage |
| Correct  | The rest of the uttered words that do not fall under the previous categories |

## Labelling Scheme

Based on the remarks provided in the dataset by the human annotator, we used the following 
pattern matching scheme to generate the labels:

| Remarks from the dataset | Labels |
| ------------- | ------------- |
| False starts & phone additions in a word | stutter  |
| Repeating and restarting words  | repeat  |
| Word substitutions, word additions & word replacements | incorrect  |
| Word deletions  | skip |
| No remarks | correct |


## License

Apache 2.0, see [LICENSE](LICENSE).
