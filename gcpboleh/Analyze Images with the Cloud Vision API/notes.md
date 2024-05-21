
Enable Cloud Vision API

Try the `images.annotate` API

```
https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate?apix=true
```

Request body

```json
{
  "requests": [
    {
      "features": [
        {
          "type": "LABEL_DETECTION"

        }

      ],
      "image": {
        "source": {
          "imageUri": "gs://qwiklabs-gcp-02-128af12e9a8c/demo-image.jpg"

        }

      }

    }

  ]

}
```

Text Detection Method

```
curl -s -X POST -H "Content-Type: application/json" --data-binary @ocr-request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY}
```

```json
{
  "requests": [
      {
        "image": {
          "source": {
              "gcsImageUri": "gs://my-bucket-name/sign.jpg"
          }
        },
        "features": [
          {
            "type": "TEXT_DETECTION",
            "maxResults": 10
          }
        ]
      }
  ]
}
```

```
curl -s -X POST -H "Content-Type: application/json" --data-binary @ocr-request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY} -o ocr-response.json
```

Translation API

translation-request.json
```json
{
  "q": "your_text_here",
  "target": "en"
}
```

```
STR=$(jq .responses[0].textAnnotations[0].description ocr-response.json) && STR="${STR//\"}" && sed -i "s|your_text_here|$STR|g" translation-request.json
```

```
curl -s -X POST -H "Content-Type: application/json" --data-binary @translation-request.json https://translation.googleapis.com/language/translate/v2?key=${API_KEY} -o translation-response.json
```

Analyzing the image's text with the Natural Language API

The Natural Language API helps you understand text by extracting entities, analyzing sentiment and syntax, and classifying text into categories. Use the analyzeEntities method to see what entities the Natural Language API can find in the text from your image.

nl-request.json
```json
{
  "document":{
    "type":"PLAIN_TEXT",
    "content":"your_text_here"
  },
  "encodingType":"UTF8"
}
```

The Natural Language API also supports sending files stored in Cloud Storage for text processing. To send a file from Cloud Storage, replace content with gcsContentUri and use the value of the text file's uri in Cloud Storage.

copy the translated text into the content block of the Natural Language API request

```
STR=$(jq .data.translations[0].translatedText  translation-response.json) && STR="${STR//\"}" && sed -i "s|your_text_here|$STR|g" nl-request.json
```

Call the analyzeEntities endpoint of the Natural Language API

```
curl "https://language.googleapis.com/v1/documents:analyzeEntities?key=${API_KEY}"   -s -X POST -H "Content-Type: application/json" --data-binary @nl-request.json
```


## Detect Labels, Faces, and Landmarks in Images with the Cloud Vision API

request.json
```json
{
  "requests": [
      {
        "image": {
          "source": {
              "gcsImageUri": "gs://my-bucket-name/donuts.png"
          }
        },
        "features": [
          {
            "type": "LABEL_DETECTION",
            "maxResults": 10
          }
        ]
      }
  ]
}
```

#### Label detection

```
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY}
```


#### Web detection

the Cloud Vision API can also search the internet for additional details on your image. Through the API's WebDetection method, you get a lot of interesting data back:

A list of entities found in your image, based on content from pages with similar images.
URLs of exact and partial matching images found across the web, along with the URLs of those pages.
URLs of similar images, like doing a reverse image search.

same request.json, but change type from LABEL_DETECTION to WEB_DETECTION

```
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY}
```

#### Face Detection

The face detection method returns data on faces found in an image, including the emotions of the faces and their location in the image.

request.json

```json
{
  "requests": [
      {
        "image": {
          "source": {
              "gcsImageUri": "gs://my-bucket-name/selfie.png"
          }
        },
        "features": [
          {
            "type": "FACE_DETECTION"
          },
          {
            "type": "LANDMARK_DETECTION"
          }
        ]
      }
  ]
}
```

call the API

```
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY}
```

#### Landmark annotation

Landmark detection can identify common (and obscure) landmarks. It returns the name of the landmark, its latitude and longitude coordinates, and the location of where the landmark was identified in an image


request.json
```json
{
  "requests": [
      {
        "image": {
          "source": {
              "gcsImageUri": "gs://my-bucket-name/city.png"
          }
        },
        "features": [
          {
            "type": "LANDMARK_DETECTION",
            "maxResults": 10
          }
        ]
      }
  ]
}
```

call the API

```
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY}
```


#### Object localization

The Vision API can detect and extract multiple objects in an image with Object Localization. Object localization identifies multiple objects in an image and provides a LocalizedObjectAnnotation for each object in the image. Each LocalizedObjectAnnotation identifies information about the object, the position of the object, and rectangular bounds for the region of the image that contains the object.

Object localization identifies both significant and less-prominent objects in an image.

request.json

```json
{
  "requests": [
    {
      "image": {
        "source": {
          "imageUri": "https://cloud.google.com/vision/docs/images/bicycle_example.png"
        }
      },
      "features": [
        {
          "maxResults": 10,
          "type": "OBJECT_LOCALIZATION"
        }
      ]
    }
  ]
}
```

call the API

```
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY}
```

#### Other Methods

You've looked at the Vision API's label, face, landmark detection and object localization methods, but there are three others you haven't explored. Dive into the Method: images.annotate documentation to learn about the other three:

Logo detection: Identify common logos and their location in an image.
Safe search detection: Determine whether or not an image contains explicit content. This is useful for any application with user-generated content. You can filter images based on four factors: adult, medical, violent, and spoof content.
Text detection: Run OCR to extract text from images. This method can even identify the language of text present in an image.

- https://cloud.google.com/vision/docs/reference/rest/v1/images/annotate#Feature


### Analyze Images with the Cloud Vision API: Challenge Lab


1. Create API key from `Credentials`
1. export API_KEY=<API_KEY>
1. Create GCS bucket with public access allowed
1. Upload image to GCS and allow public read access
1. Create request.json

```json
{
  "requests": [
      {
        "image": {
          "source": {
              "gcsImageUri": "gs://qwiklabs-gcp-03-58241be709e6/sign.jpg"
          }
        },
        "features": [
          {
            "type": "TEXT_DETECTION",
            "maxResults": 10
          }
        ]
      }
  ]
}
```

1. Call API and save response

```
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY} -o text-response.json
```

1. Upload response to GCS

```
gsutil cp text-response.json gs://qwiklabs-gcp-03-58241be709e6-bucket
```

1. Update file for LANDMARK_DETECTION

```
curl -s -X POST -H "Content-Type: application/json" --data-binary @request.json  https://vision.googleapis.com/v1/images:annotate?key=${API_KEY} -o landmark-response.json
```