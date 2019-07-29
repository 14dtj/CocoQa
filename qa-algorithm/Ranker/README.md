# Ranker


## Requirements
- python3
- MRCQA
- Flask==1.0.2
- Flask-Cors==3.0.7
- gunicorn==19.9.0
- SPARQLWrapper==1.8.2
- stanfordcorenlp==3.9.1.1

## Usage

```bash
cd Ranker
gunicorn -b 0.0.0.0:${port} server:app
```





