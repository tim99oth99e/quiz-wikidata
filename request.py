import pandas as pd
import random
import re
from SPARQLWrapper import SPARQLWrapper, JSON

class RequestManager():
    def __init__(self, url = "https://query.wikidata.org/sparql"):
        self.url = url
        self.sparql = SPARQLWrapper(url)
        self.safety_limit = 30
        self.conflit_request =  """
                                SELECT ?item ?itemLabel ?locationLabel ?countryLabel ?participantLabel ?startDate ?endDate WHERE {
                                BIND(SHA512(CONCAT(STR(RAND()), STR(?item))) AS ?random).
                                ?item wdt:P31 wd:Q180684.
                                ?item wdt:P276 ?location.
                                ?item wdt:P710 ?participant.
                                ?location wdt:P17 ?country.
                                ?item wdt:P580 ?startDate.
                                ?item wdt:P582 ?endDate.
                                SERVICE wikibase:label { bd:serviceParam wikibase:language 'en'}
                                }
                                ORDER BY ?random
                                LIMIT %s
                                """ %self.safety_limit


    def execute(self, request):
        self.sparql.setQuery(request)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()
        results_df = pd.io.json.json_normalize(results['results']['bindings'])
        return results_df

    def filter_attributes(self, attributes):
        properties = [property for property in attributes \
                      if property.endswith("value") and \
                      property != "item.value"
                      ]
        return properties

    def check_candidate_validity(self, df, candidate, attribute):
        #check attributes is not an url
        if '//' in attribute:
            return
        # check that name is not an url
        name = list(df[df["item.value"] == candidate]["itemLabel.value"].drop_duplicates())[0]
        if '//' in name:
            return
        return name


    def select_answer(self, df):
        # tous les éléments renvoyés
        ids = list(df["item.value"].drop_duplicates())
        selected = False # critère d'arret
        # choix de la proprité à demander dans la question
        attributes = self.filter_attributes(df.columns)
        answer_attribute = random.choice(attributes)
        # choisir un bon element comme réponse
        while not selected:
            if len(ids) == 0:
                print("An error occured, relaunch app")
                exit(0)
            #choix element
            candidate_id = random.choice(ids)
            ids.remove(candidate_id)
            #verifier qu'il a un nom et la propriété
            name = self.check_candidate_validity(df,
                                             candidate_id,
                                             answer_attribute)
            if name:
                selected = True
        answer = list(df[df["item.value"] == candidate_id][answer_attribute].drop_duplicates())[0]
        options = set(list(df[df["item.value"] != candidate_id][answer_attribute].drop_duplicates()))
        return name, answer_attribute, answer, options



    def generate_conflict_question(self):
        result_df = self.execute(self.conflit_request)
        element, to_ask, answer, options = self.select_answer(result_df)
        return element, to_ask, answer,list(options)[:3]

    def generate_city_question(self):
        """_summary_

        Returns:
            str: _description_
            str: city name of which the country name has to be guessed
        """
        self.request = """SELECT ?cityLabel ?countryLabel
            WHERE {
            ?city wdt:P31 wd:Q1549591 . hint:Prior hint:runFirst true .
            ?city wdt:P17 ?country .

            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            LIMIT 30"""
        # retrieves only city and country names
        result_array = self.execute(self.request)[["cityLabel.value", "countryLabel.value"]].to_numpy()
        # select randomly one city
        random_result = random.randint(0, len(result_array)-1)
        city, country = result_array[random_result]
        # list the other countries
        other_countries = [c for c in result_array[:, 1] if (c != country) & (c!= 'Nazi Germany')]
        others_countries=list(set(other_countries))
        if len(other_countries)>=3:
            options=random.sample(other_countries, 3)
        else:
            options=other_countries
        return None, city, country, options

