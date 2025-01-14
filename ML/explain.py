# -*- coding: utf-8 -*-

"""

@ author: Jingran Wang

@ Email: jrwangspencer@stu.suda.edu.cn

@ Address: Center for Systems Biology, Department of Bioinformatics, School of Biology and Basic Medical Sciences, Soochow University, Suzhou 215123, China.

@ GitHub: https://github.com/Spencer-JRWang/APMA

"""

#############################################
### Introduction of shap module
#
# @ This module is to excute explain ML model
#
#############################################



import shap
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
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
                "early_stopping_rounds": 50,
                "verbose_eval": 1000
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
        fig = shap.summary_plot(
            shap_values, 
            X, 
            alpha=0.8, 
            show=False, 
            cmap='coolwarm'
        )

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12,  rotation=45, ha='right')  # 标签旋转60度，右对齐
        plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        ax = plt.gca()
        ax.tick_params(axis='y', pad=-16)
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_color('black')
            spine.set_linewidth(1)
        plt.tight_layout()
        plt.title(f"{name}", fontweight='bold', fontsize=15)
        plt.xlabel("Impact on model output")
        plt.savefig(f"/home/wangjingran/APMA/Outcome/Figure/Explain/{model_name}_shap_summary_plot_{name}.pdf", bbox_inches='tight')
        plt.close()
        return shap_values

# Example usage:
# model_explain("LightGBM", X_train, y_train, "example")
