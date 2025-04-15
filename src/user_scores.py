user_scores = {}

def init_user_score(user_id):
    if user_id not in user_scores:
        user_scores[user_id] = {
            "Orion": 0,
            "Caelum": 0,
            "Riven": 0
        }

def update_user_score(user_id, celestial):
    init_user_score(user_id)
    if celestial in user_scores[user_id]:
        user_scores[user_id][celestial] += 1

def get_top_celestial(user_id):
    init_user_score(user_id)
    scores = user_scores[user_id]
    # Return celestial with the highest score
    return max(scores, key=scores.get)
