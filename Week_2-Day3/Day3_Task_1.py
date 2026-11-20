import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
df = pd.DataFrame({
    "age": [25, None, 40, 35, None] ,
    "income":[30000, 45000, None, 80000, 52000],
    "city":['Chennai', 'Mumbai', None, 'Chennai', 'Delhi'],
    'Size':['S', 'L', 'M','S', 'L']})


#fill age with simple imputation 
num_cols = ["age"]
cat_cols = ["city"]

# Combine separate imputers using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ("num_imputer", SimpleImputer(strategy="median"), num_cols),
        ("cat_imputer", SimpleImputer(strategy="most_frequent"), cat_cols)
    ]
)

kimputer= KNNImputer(n_neighbors=2)

result=kimputer.fit_transform(df[['age','income']])
print(result)

encode= OneHotEncoder( handle_unknown= "ignore", sparse_output=False)
encoded =encode.fit_transform(df[['city']])

presult= pd.DataFrame(encoded, columns=encode.get_feature_names_out(['city']))
print(presult)

#ordinal encoder
ecode=OrdinalEncoder(categories=[['S','M','L']])
df['Size Encoded']=ecode.fit_transform(df[['Size']])
print(df)
#lable encoder

le=LabelEncoder()
#df[['Size', 'city','age']]=le.fit_transform(df[['Size','city','age']])
from sklearn.preprocessing import LabelEncoder

df[['Size']] = df[['Size']].apply(LabelEncoder().fit_transform)
df[['city']] = df[['city']].apply(LabelEncoder().fit_transform)
df[['age']] = df[['age']].apply(LabelEncoder().fit_transform)

print(df[['Size', 'city', 'age']])
    