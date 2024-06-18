import os
import sys
from dataclasses import dataclass

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from xgboost import XGBRegressor

from src.common.exception import CustomException
from src.common.logger import logging

from src.common.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("models","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
            }
            params={
                "Random Forest":{                
                    'max_depth':[3,5,7],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                }                
            }

            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                             models=models,param=params)
            
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted=best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            return r2_square
            
           
        except Exception as e:
            raise CustomException(e,sys)
        
# """
# Train a scikit-learn model on UCI Wine Quality Dataset
# https://archive.ics.uci.edu/ml/datasets/wine+quality
# """

# import logging
# from pathlib import Path

# import pandas as pd
# from joblib import dump
# from sklearn import preprocessing
# from sklearn.experimental import enable_hist_gradient_boosting  # noqa
# from sklearn.ensemble import HistGradientBoostingRegressor
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import train_test_split

# logger = logging.getLogger(__name__)


# def prepare_dataset(test_size=0.2, random_seed=1):
#     dataset = pd.read_csv(
#         "https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv",
#         delimiter=";",
#     )
#     dataset = dataset.rename(columns=lambda x: x.lower().replace(" ", "_"))
#     train_df, test_df = train_test_split(dataset, test_size=test_size, random_state=random_seed)
#     return {"train": train_df, "test": test_df}


# def train():
#     logger.info("Preparing dataset...")
#     dataset = prepare_dataset()
#     train_df = dataset["train"]
#     test_df = dataset["test"]

#     # separate features from target
#     y_train = train_df["quality"]
#     X_train = train_df.drop("quality", axis=1)
#     y_test = test_df["quality"]
#     X_test = test_df.drop("quality", axis=1)

#     logger.info("Training model...")
#     scaler = preprocessing.StandardScaler().fit(X_train)
#     X_train = scaler.transform(X_train)
#     X_test = scaler.transform(X_test)
#     model = HistGradientBoostingRegressor(max_iter=50).fit(X_train, y_train)

#     y_pred = model.predict(X_test)
#     error = mean_squared_error(y_test, y_pred)
#     logger.info(f"Test MSE: {error}")

#     logger.info("Saving artifacts...")
#     Path("artifacts").mkdir(exist_ok=True)
#     dump(model, "artifacts/model.joblib")
#     dump(scaler, "artifacts/scaler.joblib")


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     train()        