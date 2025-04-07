import polars as pl
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.feature_selection import RFECV
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
import joblib

class Preprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
        self.rfecv = None

    def load_data(self, path: str) -> pl.DataFrame:
        return pl.read_csv(path)

    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        X = df.drop("Outcome", axis=1).to_pandas()
        y = df["Outcome"].to_numpy()

        # Apply SMOTE
        smote = SMOTE()
        X_sm, y_sm = smote.fit_resample(X, y)

        # Apply scaling
        X_scaled = self.scaler.fit_transform(X_sm)

        # Apply polynomial features
        X_poly = self.poly.fit_transform(X_scaled)

        # Recursive feature elimination with CV
        selector = RFECV(estimator=RandomForestClassifier(), step=1, cv=5)
        X_selected = selector.fit_transform(X_poly, y_sm)
        self.rfecv = selector

        return X_selected, y_sm

    def save(self):
        joblib.dump(self.scaler, "app/ml/scaler.pkl")
        joblib.dump(self.poly, "app/ml/poly.pkl")
        joblib.dump(self.rfecv, "app/ml/rfecv.pkl")

    def load(self):
        self.scaler = joblib.load("app/ml/scaler.pkl")
        self.poly = joblib.load("app/ml/poly.pkl")
        self.rfecv = joblib.load("app/ml/rfecv.pkl")
