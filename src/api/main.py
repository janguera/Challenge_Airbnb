from typing import List, Dict
from pathlib import Path
import datetime
import pandas as pd
import requests
from fastapi import FastAPI, APIRouter, HTTPException
from joblib import load

from src.api.configuration import ORJSONResponse, Settings
from app.sentiment_analysis.polarity_score import get_polarity, classify_polarity

ROOT_DIR = Path(__file__).parent.parent
scaler = load(ROOT_DIR / "artifacts/scaler.joblib")
model = load(ROOT_DIR / "artifacts/model.joblib")

ROOT_PATH=Settings().api_main_path
prefix_router = APIRouter(prefix=ROOT_PATH)

host = Settings().middleware_host
host = host if host[-1] != "/" else host[:-1]
host = host + Settings().api_version

print('Initialising comment classification API')

app = FastAPI(
        title="Daily price forecast API",
        version="1.0.0",
        openapi_url=f'{ROOT_PATH}/openapi.json',
        docs_url = f'{ROOT_PATH}/docs',
        redoc_url = f'{ROOT_PATH}/redoc',
        default_response_class=ORJSONResponse
    ) 
   
@prefix_router.get("/version")
async def get_version():
    return {"version": app.version}

@prefix_router.get('/number_of_subfeddits')
async def get_number_of_subfeddits() -> int:
    """
    Returns the number of subfeddits in the system.
    """

    res = requests.get(url = host + "/subfeddits")

    data = res.json()

    return len(data['subfeddits'])

@prefix_router.get('/subfeddit_comments')
async def get_subfeddit_comments(
        subfeddit: int,
        time_range: int = None,
        sorted_results: bool = False,
        comments_limit: int = 25) -> List[Dict]:
    """
    Returns a list of comments from the specified subfeddit.

    Parameters:
    - **subfeddit** (int): The ID of the subfeddit to fetch comments from.
    - **time_range** (int, optional): The time range filter in minutes. If provided, comments will be filtered based on this range.
    - **sorted_results** (bool, optional): If true, comments will be sorted by their polarity score.
    - **comments_limit** (int, optional): The maximum number of comments to return. Default is 25.

    Returns:
    - **List[Dict]**: A list of comments with the following data for each comment:
        - **Unique identifier**: A unique identifier of the comment.
        - **Text**: The text of the comment.
        - **Polarity score and classification**: The polarity score of the comment and its classification (positive/negative) based on that score.
    """

    # If subfeddit > number of subfeddits, raise an error 
    number_of_subfeddits = await get_number_of_subfeddits()
    if subfeddit > number_of_subfeddits or subfeddit < 0:
        raise HTTPException(status_code=400, detail='Subfeddit does not exist')
    
    if time_range is not None and time_range < 0:
        raise HTTPException(status_code=400, detail='Time range must be greater than 0')
    
    if comments_limit < 0:
        raise HTTPException(status_code=400, detail='Comments limit must be greater than 0')

    payload = {'subfeddit_id': subfeddit, 
               'skip': 0,
               'limit': comments_limit
               }
    
    res = requests.get(url = host + "/comments", params = payload)

    data = res.json()

    df = pd.DataFrame.from_dict( data['comments'])

    # Filter by time range
    if time_range:
        df['datetime'] = pd.to_datetime(df['created_at'], unit='s')
        df = df[df['datetime'] > datetime.datetime.now() - datetime.timedelta(minutes=time_range)]

    # Get a polarity score for every text in the comments
    df['polarity_score'] = df['text'].apply(get_polarity)
    # Classify the comments based on the polarity score
    df['classification'] = df['polarity_score'].apply(classify_polarity)

    if sorted_results:
        df = df.sort_values(by='polarity_score', ascending=False)

    return df[['id', 'text', 'polarity_score', 'classification']].to_dict(orient='records')


@prefix_router.post("/predict", response_model=Rating)
def predict(response: Response, sample: Wine):
    sample_dict = sample.dict()
    features = np.array([sample_dict[f] for f in feature_names]).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    response.headers["X-model-score"] = str(prediction)
    return Rating(quality=prediction)


@prefix_router.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

# @prefix_router.get("/predict_datapoint")
# async def predict_datapoint():
#         data=CustomData(
#             gender=request.form.get('gender'),
#             race_ethnicity=request.form.get('ethnicity'),
#             parental_level_of_education=request.form.get('parental_level_of_education'),
#             lunch=request.form.get('lunch'),
#             test_preparation_course=request.form.get('test_preparation_course'),
#             reading_score=float(request.form.get('writing_score')),
#             writing_score=float(request.form.get('reading_score'))

#         )
#         pred_df=data.get_data_as_data_frame()
#         print(pred_df)
#         print("Before Prediction")

#         predict_pipeline=PredictPipeline()
#         print("Mid Prediction")
#         results=predict_pipeline.predict(pred_df)
#         print("after Prediction")

app.include_router(prefix_router)
