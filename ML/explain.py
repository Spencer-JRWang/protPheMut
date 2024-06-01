import shap
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
<<<<<<< HEAD
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import xgboost as xgb
import matplotlib.pyplot as plt

shap.initjs()

def model_explain(model_name, X, y, name, type="Tree"):
    """
    Explain the predictions of a machine learning model using SHAP (SHapley Additive exPlanations) method.

    Args:
        model_name (str): Name of the model ("LightGBM", "RandomForest", "XGBoost", "GradientBoost").
        X (array-like or DataFrame): Features data.
        y (array-like or DataFrame): Target variable data.
        name (str): Name for saving the explanation results.
        type (str, optional): Type of the model. Defaults to "Tree".

    Returns:
        array-like: SHAP values.
    """
=======
import matplotlib.pyplot as plt

shap.initjs()
def model_explain(model_name, X, y, name, type = "Tree"):
>>>>>>> origin/main
    if type == "Tree":
        if model_name == "LightGBM":
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
            d_train = lgb.Dataset(X_train, label=y_train)
            d_test = lgb.Dataset(X_test, label=y_test)

            params = {
                "max_bin": 512,
                "learning_rate": 0.05,
                "boosting_type": "gbdt",
                "objective": "binary",
                "metric": "binary_logloss",
                "num_leaves": 10,
                "verbose": -1,
                "boost_from_average": True,
<<<<<<< HEAD
                "early_stopping_rounds": 50,
                "verbose_eval": 1000
=======
                "early_stopping_rounds":50, 
                "verbose_eval":1000
>>>>>>> origin/main
            }

            model = lgb.train(
                params,
                d_train,
                1000,
                valid_sets=[d_test],
            )
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)
        elif model_name == "RandomForest":
<<<<<<< HEAD
            model = RandomForestClassifier()  # Assuming RandomForestClassifier for classification tasks
            model.fit(X_train, y_train)
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)
        elif model_name == "XGBoost":
            model = xgb.XGBClassifier()  # Assuming XGBClassifier for classification tasks
            model.fit(X_train, y_train)
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)
        elif model_name == "GradientBoost":
            model = GradientBoostingClassifier()  # Assuming GradientBoostingClassifier for classification tasks
            model.fit(X_train, y_train)
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)

        # Save force plot
        p = shap.force_plot(explainer.expected_value[1], 
                            shap_values[1], 
                            X,
                            link="logit")
        shap.save_html(f'/home/wangjingran/APMA/Outcome/Figure/Explain/{model_name}_force_plot_{name}.html', p)

        # Save summary plot
        fig = shap.summary_plot(shap_values[1], X, alpha=0.75, show=False)
        plt.title(f"{name}", fontweight='bold', fontsize=15)
=======
            model = None
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)
        elif model_name == "XGBoost":
            model = None
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)
        elif model_name == "GradientBoost":
            model = None
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)
        # 保存forceplot
        p = shap.force_plot(explainer.expected_value[1], 
                shap_values[1], 
                X,
                link = "logit")
        shap.save_html(f'/home/wangjingran/APMA/Outcome/Figure/Explain/{model_name}_force_plot_{name}.html', p)

        # 保存summaryplot
        fig = shap.summary_plot(shap_values[1], X, alpha=0.75, show = False)
        plt.title(f"{name}",fontweight='bold',fontsize = 15)
>>>>>>> origin/main
        plt.xlabel("Impact on model output")
        plt.savefig(f"/home/wangjingran/APMA/Outcome/Figure/Explain/{model_name}_shap_summary_plot_{name}.pdf", bbox_inches='tight')
        plt.close()
        return shap_values
<<<<<<< HEAD

# Example usage:
# model_explain("LightGBM", X_train, y_train, "example")
=======
>>>>>>> origin/main
