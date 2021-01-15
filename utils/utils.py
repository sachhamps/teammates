import logging
from pymongo import MongoClient

logger = logging.getLogger(__name__)

class TeammateService():
    """
        Get mutual teammates from mongo
        + other functionality
        todo: make players a list so form can be extended
    """
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client['teammates']
    players = db['players']

    def __init__(self, p_one, p_two):
        self.p_one = p_one
        self.p_two = p_two
    
    def calculate_mutual_teammates(self):
        player_docs = self.players.find({
            "_normalized_name": {
                '$in': [self.p_one, self.p_two]
            }
        })
        try:
            p1_doc = player_docs[0]
            p2_doc = player_docs[1]
            #to do, catch index error properly
        except IndexError:
            logger.warning("Couldnt find players searched for in the db")
            return None

        p1_tmtes_ids = set([p1['teammate_id'] for p1 in p1_doc['teammates']])
        p2_tmtes_ids = set([p2['teammate_id'] for p2 in p2_doc['teammates']])
        mutual_team_ids = p1_tmtes_ids.intersection(p2_tmtes_ids)

        mutual_teammate_docs = self.players.find({
            "_id": {
                "$in": list(mutual_team_ids)
            }
        })
        return [mt["name"] for mt in mutual_teammate_docs]
    

# class Player():
#     def calculate_teammate_meta_data():
#         """Calcualate extra info for the teammates - currently
#         we only have info of where the
#         """
#         pass
