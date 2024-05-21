Create API key

```
gcloud auth list

export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value core/project)

gcloud iam service-accounts create my-natlang-sa \
  --display-name "my natural language service account"

gcloud iam service-accounts keys create ~/key.json \
  --iam-account my-natlang-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS="/home/USER/key.json"
```

OR from `Credentials`

export API_KEY=<API_KEY>

call API from inside VM

```
gcloud ml language analyze-entities --content="Michelangelo Caravaggio, Italian painter, is known for 'The Calling of Saint Matthew'." > result.json
```

## Challenge Lab

Entity analysis request and call the Natural Language API

```
curl "https://language.googleapis.com/v1/documents:analyzeEntities?key=${API_KEY}" \
  -s -X POST -H "Content-Type: application/json" --data-binary @nl_request.json > nl_response.json
```

Speech analysis request and call the Speech API

gs://cloud-samples-tests/speech/brooklyn.flac


```
curl -s -X POST -H "Content-Type: application/json" --data-binary @speech_request.json \
"https://speech.googleapis.com/v1/speech:recognize?key=${API_KEY}"
```

Analyze sentiment with the Natural Language API
