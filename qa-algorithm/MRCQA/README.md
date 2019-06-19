# MRCQA
Inspired by the Match-LSTM+ implementation of [laddie132](https://github.com/laddie132/Match-LSTM), we build our machine reading comprehension question answering system. Furthermore, domain adaption techiniques, including tagging and finetuning have been employed.

## Requirements
- python3
- hdf5
- spaCy 2.0
- [pytorch 0.4](https://github.com/pytorch/pytorch/tree/v0.4.0)
- [GloVe word embeddings](https://nlp.stanford.edu/projects/glove/)

## Usage

```bash
python run.py [preprocess/train/test] [-c config_file] [-o ans_path]
```

- -c config_file: Defined dataset, model, train methods and so on. Default: `config/global_config.yaml`.
- -o ans_path: *see in test step*
- To employ domain adaption techniques, you should set `use_domain_tag` or `fine_tune` in `global_config.yaml` to `true`, as the `config/tagging.yaml`  and `config/finetunning.yaml`
show.

### Preprocess

1. Put the GloVe embeddings file to the `data/` directory
2. Put the SQuAD dataset to the `data/` directory
3. Run `python run.py preprocess` to generate hdf5 file of SQuAD dataset

> Note that preprocess will take a long time if multi-features used. Maybe close to an hour.

### Train

```bash
python run.py train
```

### Test

```bash
python run.py test [-o ans_file]
```

- -o ans_file: Output the answer of question and context with a unique id to ans_file. 

> Note that we use `data/model-weight.pt` as our model weights by default. You can modify the config_file to set model weights file.

### Evaluate

```bash
python helper_run/evaluate-v1.1.py [dataset_file] [prediction_file]
```

- dataset_file: ground truth of dataset. example: `data/SQuAD/dev-v1.1.json`
- prediction_file: your model predict on dataset. you can use the `ans_file` from test step.

### Analysis

```bash
python helper_run/analysis_[*].py
```
### Server
You can run a Flask application from `server.py` as
```bash
app.run(debug=True, threaded=True, port=5000, host=’0.0.0.0’) 
```

