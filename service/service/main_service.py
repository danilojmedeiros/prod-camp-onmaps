from loguru import logger
import pickle
import pandas as pd
from shapely.geometry import Point
from shapely.ops import transform
from shapely.wkt import loads
import pyproj
from functools import partial
from collections import Counter
from rtree import index

class GeofusionInsights:
    def __init__(self):
        self.area_de_influencia = 1000
        self.pois_index = index.Index()
        self.model = self.load_model()
        self.df_pois = pd.read_csv(r'C:\Users\danil\Documents\Case\prod-camp-onmaps\geofusion-insights-public\pois.csv')
        self.df_faturamento = pd.read_csv(r'C:\Users\danil\Documents\Case\prod-camp-onmaps\geofusion-insights-public\faturamento.csv')
        with open(r'C:\Users\danil\Documents\Case\prod-camp-onmaps\geofusion-insights-public\campinas.wkt', 'r') as file:
            self.campinas_polygon = loads(file.read())
        self.populate_pois_index()

    def load_model(self):
        with open(r'C:\Users\danil\Documents\Case\prod-camp-onmaps\geofusion-insights-public\model_campifarma.pickle', 'rb') as p:
            return pickle.load(p)

    def populate_pois_index(self):
        for idx, row in self.df_pois.iterrows():
            self.pois_index.insert(idx, (row["longitude"], row["latitude"], row["longitude"], row["latitude"]))

    def lat_lng_to_utm(self, lat_lng_geom):
        project = partial(
            pyproj.transform,
            pyproj.Proj(init="epsg:4326"),
            pyproj.Proj(init="epsg:3857"))
        utm_geom = transform(project, lat_lng_geom)
        return utm_geom

    def utm_to_lat_lng(self, utm_geom):
        project = partial(
            pyproj.transform,
            pyproj.Proj(init="epsg:3857"),
            pyproj.Proj(init="epsg:4326"))
        lat_lng_geom = transform(project, utm_geom)
        return lat_lng_geom

    def gera_isocota(self, ponto, raio):
        raio_ponto_de_estudo_utm = self.lat_lng_to_utm(ponto).buffer(raio)
        raio_ponto_de_estudo_lat_lng = self.utm_to_lat_lng(raio_ponto_de_estudo_utm)
        return raio_ponto_de_estudo_lat_lng

    def obtem_configuracao(self):
        return {'faculdades','escolas', 'ponto_de_onibus', 'concorrentes__grandes_redes',
                'concorrentes__pequeno_varejista', 'minhas_lojas', 'agencia_bancaria', 'padaria',
                'acougue', 'restaurante', 'correio', 'loterica'}

    def contar_pois_proximos(self, lat, lng, isocota):
        min_lng, min_lat, max_lng, max_lat = isocota.bounds
        pois_within_isocota = list(self.pois_index.intersection((min_lng, min_lat, max_lng, max_lat)))
        counter = Counter()
        for idx in pois_within_isocota:
            row_poi = self.df_pois.iloc[idx]
            if Point(row_poi["longitude"], row_poi["latitude"]).within(isocota):
                counter.update([row_poi["tipo_POI"]])
        return counter

    def predict_model(self, lat, lng, pois_counter):
        dados_entrada = []
        for poi_tipo in self.obtem_configuracao():
            dados_entrada.append(pois_counter.get(poi_tipo, 0))

        try:
            predicao = self.model.predict([dados_entrada])[0]
            return predicao
        except:
            return -1

    def ponto_esta_em_campinas(self, lat, lng):
        ponto = Point(lng, lat)
        return ponto.within(self.campinas_polygon)

    def predict(self, lat, lng):
        if not self.ponto_esta_em_campinas(lat, lng):
            return {"error": "The provided coordinates are not within the municipality of Campinas"}, 400
        
        ponto = Point(lng, lat)
        isocota = self.gera_isocota(ponto, self.area_de_influencia)
        pois_counter = self.contar_pois_proximos(lat, lng, isocota)

        predicao = self.predict_model(lat, lng, pois_counter)

        n_grandes_redes = 1 if "concorrentes__grandes_redes" in pois_counter else 0
        n_pequeno_varejista = 1 if "concorrentes__pequeno_varejista" in pois_counter else 0

        response = {
            "latitude": lat,
            "longitude": lng,
            "predicao": predicao,
            "n_grandes_redes": n_grandes_redes,
            "n_pequeno_varejista": n_pequeno_varejista
        }

        return response