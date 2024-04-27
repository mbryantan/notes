## Foundation models

Vertex AI has various genAI foundation models, including:
- Gemini API: For advanced reasoning, multiturn chat, code generation, and multimodal prompts.
- PaLM API: For natural language tasks, text embeddings, and multiturn chat.
- Codey APIs: For code generation, code completion, and code chat.
- Imagen API: For image generation, image editing, and visual captioning.
- MedLM: For summarizing and answering medical questions.


## Sample uses of the Gemini API

- Generate code from natural language descriptions.
- Create image captions that go beyond simple descriptions.
- Answer questions about the content of images and videos.
- Generate different creative text formats, like poems, code, scripts, musical pieces, email, letters, and stories.


**Configure environment and project**

```sh
PROJECT_ID=$(gcloud config get-value project)
REGION=set at lab start
echo "PROJECT_ID=${PROJECT_ID}"
echo "REGION=${REGION}"
```
you must enable a few APIs:

```sh
gcloud services enable cloudbuild.googleapis.com cloudfunctions.googleapis.com run.googleapis.com logging.googleapis.com storage-component.googleapis.com aiplatform.googleapis.com
```

**Set up Python virtual environment**

```sh
python3 -m venv gemini-streamlit
source gemini-streamlit/bin/activate
```
Install dependencies

```sh
cd ~/gemini-app
pip install -r requirements.txt
```

**Run the app**

```sh
streamlit run app.py \
--browser.serverAddress=localhost \
--server.enableCORS=false \
--server.enableXsrfProtection=false \
--server.port 8080
```

To launch the app home page in your browser, click web preview in the Cloud Shell menubar, and then click Preview on port 8080. You can also copy and paste the app URL in a separate browser tab to access the app.

**Deploy the app to Cloud Run**

Verify that the PROJECT_ID, and REGION environment variables are set:

```sh
cd ~/gemini-app
echo "PROJECT_ID=${PROJECT_ID}"
echo "REGION=${REGION}"
```

If these environment variables are not set, then run the command to set them:

```sh
PROJECT_ID=$(gcloud config get-value project)
REGION=set at lab start
echo "PROJECT_ID=${PROJECT_ID}"
echo "REGION=${REGION}"
```

Set environment variables for your service and artifact repository:

```sh
SERVICE_NAME='gemini-app-playground' # Name of your Cloud Run service.
AR_REPO='gemini-app-repo'            # Name of your repository in Artifact Registry that stores your application container image.
echo "SERVICE_NAME=${SERVICE_NAME}"
echo "AR_REPO=${AR_REPO}"
```

Create the Docker repository

To create the repository in Artifact Registry, run the command:

```sh
gcloud artifacts repositories create "$AR_REPO" --location="$REGION" --repository-format=Docker
```

Artifact Registry ia a Google Cloud service that provides a single location for storing and managing your software packages and Docker container images.

Set up authentication to the repository:

```sh
gcloud auth configure-docker "$REGION-docker.pkg.dev"
```

Build the container image

We'll use a Dockerfile to build the container image for our application. A Dockerfile is a text document that contains all the commands that a user could call on the command line to assemble a container image. It is used with Docker, a container platform that builds and runs container images.

To build the container image for your app, run the command:

```sh
gcloud builds submit --tag "$REGION-docker.pkg.dev/$PROJECT_ID/$AR_REPO/$SERVICE_NAME"
```

The gcloud builds submit command submits a build using Cloud Build. When used with the tag flag, Cloud Build uses a Dockerfile to build a container image from the application files in your source directory.

Cloud Build is a service that executes builds based on your specifications on Google Cloud, and produces artifacts such as Docker containers or Java archives.

Wait until the command finishes before advancing to the next step.

Deploy and test your app on Cloud Run

The final task is to deploy the service to Cloud Run with the image that was built and pushed to the repository in Artifact Registry.

To deploy your app to Cloud Run, run the command:

```sh
gcloud run deploy "$SERVICE_NAME" \
  --port=8080 \
  --image="$REGION-docker.pkg.dev/$PROJECT_ID/$AR_REPO/$SERVICE_NAME" \
  --allow-unauthenticated \
  --region=$REGION \
  --platform=managed  \
  --project=$PROJECT_ID \
  --set-env-vars=PROJECT_ID=$PROJECT_ID,REGION=$REGION
```

After the service is deployed, a URL to the service is generated in the output of the previous command. To test your app on Cloud Run, navigate to that URL in a separate browser tab or window.

Choose the app functionality that you want to test. The app will prompt the Vertex AI Gemini API to generate and display the responses.
