import logging

from .m_db import players

logger = logging.getLogger(__name__)

class TeammateService():
    """
        Get mutual teammates from mongo + other functionality
    """
    def __init__(self, p_one, p_two):
        # TODO make code 'scaleable':
        #   allow for calculation of mut. teammates 
        #   for a variable number of players
        self.p_one = p_one
        self.p_two = p_two
    
    def calculate_mutual_teammates(self):
        player_docs = players.find({
            "_normalized_name": {
                '$in': [self.p_one, self.p_two]
            }
        })
        try:
            p1_doc = player_docs[0]
            p2_doc = player_docs[1]
            #to do, catch index error properly
        except IndexError:
            logger.warning("Invalid players inputted")
            return None

        p1_tmtes_ids = set([p1['teammate_id'] for p1 in p1_doc['teammates']])
        p2_tmtes_ids = set([p2['teammate_id'] for p2 in p2_doc['teammates']])
        mutual_team_ids = p1_tmtes_ids.intersection(p2_tmtes_ids)

        mutual_teammate_docs = players.find({
            "_id": {
                "$in": list(mutual_team_ids)
            }
        })
        return [mt["name"] for mt in mutual_teammate_docs]

        def santise_name(name):
            """
            Ensure name is in correct formate to be searched in mongo,
            as far as I know it only has to be lowered
            """
            return name.lower()

# class Player():
#     def calculate_teammate_meta_data():
#         """Calcualate extra info for the teammates - currently
#         we only have info of where the
#         """
#         pass
