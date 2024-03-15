import pickle
import pandas as pd
from flask import Flask, request, jsonify
from shapely.geometry import Point
from shapely.ops import transform
from shapely.wkt import loads
import pyproj
from functools import partial
from collections import Counter
from rtree import index

# Inicia o Flask
app = Flask(__name__)

area_de_influencia = 1000

pois_index = index.Index()

# Load dos dados disponíveis: .pickle, pontos de interesse (pois), faturamento e polígono de Campinas
with open(r'C:\Users\danil\Documents\Case\prod-camp-onmaps\geofusion-insights-public\model_campifarma.pickle', 'rb') as p:
    model = pickle.load(p)

df_pois = pd.read_csv(r'C:\Users\danil\Documents\Case\prod-camp-onmaps\geofusion-insights-public\pois.csv')

df_faturamento = pd.read_csv(r'C:\Users\danil\Documents\Case\prod-camp-onmaps\geofusion-insights-public\faturamento.csv')

with open(r'C:\Users\danil\Documents\Case\prod-camp-onmaps\geofusion-insights-public\campinas.wkt', 'r') as file:
    campinas_polygon = loads(file.read())

# Indexação dos POIs
for idx, row in df_pois.iterrows():
    pois_index.insert(idx, (row["longitude"], row["latitude"], row["longitude"], row["latitude"]))

# Conversão de coordenadas
def lat_lng_to_utm(lat_lng_geom):
    project = partial(
        pyproj.transform,
        pyproj.Proj(init="epsg:4326"),
        pyproj.Proj(init="epsg:3857"))
    utm_geom = transform(project, lat_lng_geom)
    return utm_geom

# Conversão de coordenadas
def utm_to_lat_lng(utm_geom):
    project = partial(
        pyproj.transform,
        pyproj.Proj(init="epsg:3857"),
        pyproj.Proj(init="epsg:4326"))
    lat_lng_geom = transform(project, utm_geom)
    return lat_lng_geom

# Gerar uma buffer em torno de um ponto
def gera_isocota(ponto, raio):
    raio_ponto_de_estudo_utm = lat_lng_to_utm(ponto).buffer(raio)
    raio_ponto_de_estudo_lat_lng = utm_to_lat_lng(raio_ponto_de_estudo_utm)
    return raio_ponto_de_estudo_lat_lng

def obtem_configuracao():
    return {'faculdades','escolas', 'ponto_de_onibus', 'concorrentes__grandes_redes',
            'concorrentes__pequeno_varejista', 'minhas_lojas', 'agencia_bancaria', 'padaria',
            'acougue', 'restaurante', 'correio', 'loterica'}

# Conta os pois próximos dentro de uma isocota
def contar_pois_proximos(lat, lng, isocota):
    min_lng, min_lat, max_lng, max_lat = isocota.bounds
    pois_within_isocota = list(pois_index.intersection((min_lng, min_lat, max_lng, max_lat)))
    counter = Counter()
    for idx in pois_within_isocota:
        row_poi = df_pois.iloc[idx]
        if Point(row_poi["longitude"], row_poi["latitude"]).within(isocota):
            counter.update([row_poi["tipo_POI"]])
    return counter

# Faça as previsões usando o modelo treinado
def predict_model(lat, lng, pois_counter):
    dados_entrada = []
    for poi_tipo in obtem_configuracao():
        dados_entrada.append(pois_counter.get(poi_tipo, 0))

    try:
        predicao = model.predict([dados_entrada])[0]
        return predicao
    except:
        return -1

def ponto_esta_em_campinas(lat, lng):
    ponto = Point(lng, lat)
    return ponto.within(campinas_polygon)

@app.route("/predict")
def predict():
    lat = float(request.args.get("lat"))
    lng = float(request.args.get("lng"))

    if lat is None or lng is None:
        return jsonify({"error": "Latitude and longitude parameters are required"}), 400

    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return jsonify({"error": "Latitude and longitude must be valid numbers"}), 400
    
    # Verificar se está dentro de Campinas
    if not ponto_esta_em_campinas(lat, lng):
        return jsonify({"error": "The provided coordinates are not within the municipality of Campinas"}), 400
    
    # Cria o buffer e conta os pois próximos
    ponto = Point(lng, lat)
    isocota = gera_isocota(ponto, area_de_influencia)
    pois_counter = contar_pois_proximos(lat, lng, isocota)

    # Previsões 
    predicao = predict_model(lat, lng, pois_counter)

    # Presença de concorrentes
    n_grandes_redes = 1 if "concorrentes__grandes_redes" in pois_counter else 0
    n_pequeno_varejista = 1 if "concorrentes__pequeno_varejista" in pois_counter else 0

    # Resposta em JSON
    response = {
        "latitude": lat,
        "longitude": lng,
        "predicao": predicao,
        "n_grandes_redes": n_grandes_redes,
        "n_pequeno_varejista": n_pequeno_varejista
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
