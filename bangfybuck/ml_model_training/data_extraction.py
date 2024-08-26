import pandas as pd
import numpy as np

amazon_data="bangfybuck\\ml_model_training\\Amazon.csv"
amazon= pd.read_csv(amazon_data, encoding='ISO-8859-1')
amazon=amazon.drop(['description','price','manufacturer'],axis=1)

google_data="bangfybuck\\ml_model_training\\GoogleProducts.csv"
google= pd.read_csv(google_data, encoding='ISO-8859-1')
google=google.drop(['description','price','manufacturer'],axis=1)

matched_data='bangfybuck\\ml_model_training\\Amzon_GoogleProducts_perfectMapping.csv'
matched= pd.read_csv(matched_data, encoding='ISO-8859-1')

merged_df = pd.merge(matched,amazon, on='idAmazon', how='inner')
joined_df = pd.merge(merged_df, google[['idGoogleBase', 'Googlename']], left_on='idGoogleBase', right_on='idGoogleBase', how='inner')
joined_df.to_csv("data.csv",index=False)



    