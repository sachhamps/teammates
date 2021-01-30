import logging

from .m_db import players

logger = logging.getLogger(__name__)

class TeammateService():
    """
        Get mutual teammates from mongo + other functionality
    """
    def __init__(self, names):
        self.names = names

    def generate_players(self):

        players = []
        for name in self.names:

            player_dict = {}
            self.preprocessed_name = self._preprocess_name(name)
            player_doc = self._get_player_doc()
            if not player_doc:
                logger.error(f"Invalid player name: {name}. Returning Error")
                # raise Exception here - as can be confused with two players
                #  with no mutual teammates
                return None
            player_dict['p_id'] = player_doc['_id']
            player_dict['p_name'] = player_doc['name']
            player_dict['teammate_ids'] = self._get_teammate_ids(player_doc)
            player_dict['team_ids'] = player_doc['team_ids']
            players.append(Player(**player_dict))

        return players

    def _preprocess_name(self, name):
        """
        TODO: Ensure name is in correct formate to be searched in mongo,
        as far as I know it only has to be lowered
        """
        return name.lower().strip()

    def _get_player_doc(self):
        """
        TODO: add check if we find more than one playerdoc
        this would occur if there were two players of the
        same name
        """
        return players.find_one({'_normalized_name': self.preprocessed_name})

    def _get_teammate_ids(self, player_doc):
        return set([t['teammate_id'] for t in player_doc['teammates']])




class Player():

    def __init__(self, p_name, p_id, teammate_ids, team_ids):
        self.p_name = p_name
        self.p_id = p_id
        self.teammate_ids = teammate_ids
        self.team_ids = team_ids

    def generate_mutual_teammates(self, p_two):
        mutual_tmmte_ids = self.teammate_ids.intersection(p_two.teammate_ids)
        mutual_tmmte_docs = players.find({
            "_id": {
                "$in": list(mutual_tmmte_ids)
            }
        })
        return [mt["name"].title() for mt in mutual_tmmte_docs]

    def calculate_teammate_meta_data():
        """Calcualate extra info for the teammates - currently
        we only have info of where the
        """
        pass
