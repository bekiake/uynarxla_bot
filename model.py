from sklearn.neighbors import KNeighborsRegressor
import pandas as pd

df = pd.read_excel('uybor.xlsx')

def prepare_model(df):
    X = df[['rooms', 'size', 'level', 'max_levels', 'lat', 'lng']]
    y = df['price']
    model = KNeighborsRegressor(n_neighbors=5)
    model.fit(X, y)
    return model

model = prepare_model(df)

def predict_price(rooms, size, level, max_levels, lat, lng):
    input_data = [[rooms, size, level, max_levels, lat, lng]]
    return model.predict(input_data)[0]
