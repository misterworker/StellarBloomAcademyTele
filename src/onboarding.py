from user_scores import update_user_score, get_top_celestial
from user_state import get_state, set_state
from telegram import send_message, send_message_with_buttons


# Define Celestial score mapping
celestial_score_map = {
    "Orion": 0,
    "Caelum": 0,
    "Riven": 0
}

# Button flows for each question
QUESTION_FLOW = {
    "soul_sync_1": {
        "text": "🔹 Q1: Why are you here, Cadet?",
        "buttons": [
            ("🔥 I want to feel strong again.", "Orion"),
            ("🌸 I want to stop hating how I eat.", "Caelum"),
            ("🌌 I need consistency.", "Riven"),
            ("🌿 I just want to feel good.", "Caelum")
        ],
        "next": "soul_sync_2"
    },
    "soul_sync_2": {
        "text": "🔹 Q2: How do you move your body now?",
        "buttons": [
            ("🚫 Not at all", "Caelum"),
            ("🚶 Light walking", "Caelum"),
            ("🧘 Yoga/Pilates", "Caelum"),
            ("💪 Workout often", "Orion"),
            ("🕺 Fun/casual", "Riven"),
            ("🔁 Short/effective", "Orion"),
            ("🌿 Calm/slow", "Caelum"),
            ("📋 Structured", "Orion"),
            ("🙅 None", "Caelum")
        ],
        "next": "soul_sync_3"
    },
    "soul_sync_3": {
        "text": "🔹 Q3: What’s your food relationship like?",
        "buttons": [
            ("😵‍💫 Stress eat/restrict", "Caelum"),
            ("🤷‍♀️ Inconsistent", "Riven"),
            ("🌱 Working on balance", "Caelum"),
            ("🍽 I love to eat!", "Riven"),
            ("🍳 Homecooked", "Orion"),
            ("🥡 Mixed", "Riven"),
            ("🧃 Takeout", "Caelum")
        ],
        "next": "soul_sync_4"
    },
    "soul_sync_4": {
        "text": "🔹 Q4: How do you feel when you wake up?",
        "buttons": [
            ("😴 Tired", "Caelum"),
            ("🌥 Mixed", "Riven"),
            ("🌞 Energized", "Orion"),
            ("🕑 <5hr sleep", "Caelum"),
            ("🕖 5–6hr", "Riven"),
            ("🕘 7–8hr", "Orion"),
            ("🕔 9+hr", "Caelum")
        ],
        "next": "soul_sync_5"
    },
    "soul_sync_5": {
        "text": "🔹 Q5: What does your day usually look like?",
        "buttons": [
            ("🧠 Work from home", "Riven"),
            ("🏃 Busy job", "Orion"),
            ("🧒 Caregiver", "Caelum"),
            ("🌀 Unstructured", "Caelum")
        ],
        "next": "soul_sync_6"
    },
    "soul_sync_6": {
        "text": "🔹 Q6: How much time can you dedicate daily?",
        "buttons": [
            ("🌱 Casual – 5 mins/day", "Caelum"),
            ("🌿 Regular – 10 mins/day", "Riven"),
            ("🌟 Dedicated – 15 mins/day", "Orion")
        ],
        "next": "soul_sync_7"
    },
    "soul_sync_7": {
        "text": "🔹 Q7: What kind of support draws out your best?",
        "buttons": [
            ("🛡 Accountability. Push me.", "Orion"),
            ("🫶 Gentle encouragement.", "Caelum"),
            ("🎉 Keep it fun.", "Riven"),
            ("🧠 Reflect & understand.", "Caelum")
        ],
        "next": "celestial_reveal"
    }
}

# Celestial final dialogue
CELESTIAL_DIALOGUE = {
    "Orion": "💬 Orion: “You say you want to rise—but the stars demand proof. Let’s see what you’re made of.”",
    "Caelum": "💬 Caelum: “You don’t have to fight your way through this. You just have to begin.”",
    "Riven": "💬 Riven: “Knew it’d be you. Fire flickering behind those eyes. Let’s spark it up, Starlet.”"
}

async def handle_onboarding(chat_id, text, username):
    state = get_state(chat_id)
    print("Handle Onboarding: ", state)

    # START
    if text == "/start" or state == "start":
        set_state(chat_id, "waiting_for_ready")
        await send_message_with_buttons(
            chat_id,
            f"Hello, cadet {username}.\nYou’ve been selected to begin Stellar Bloom Training.\nThis is your onboarding.",
            [[("👉 I’m Ready", "onboarding_ready")]]
        )
        return None

    # "I'm Ready" button was pressed
    if text == "onboarding_ready" or state == "waiting_for_ready":
        set_state(chat_id, "ask_identity")
        await send_message(chat_id, "🔒 Please verify your identity.\nTell me your:\nName:\nAge:\nEmail:")
        return None

    # Handle identity collection
    if state == "ask_identity":
        # Optionally parse the input and store it
        set_state(chat_id, "ready_for_whats_in_store")
        await send_message_with_buttons(
            chat_id,
            "✅ Identity verified. Welcome aboard, cadet.\nYou’re not just here to “get healthy.”\nYou’re here to grow stronger, feel better, and earn your spot in the Astral Corps.",
            [[("👉 What’s in store?", "whats_in_store")]]
        )
        return None

    if text == "whats_in_store":
        set_state(chat_id, "intro_mission")
        await send_message_with_buttons(
            chat_id,
            "Only 2.3% of cadets make it past Initiation.\nMost quit after Day 5.\nReady to see what you're made of?",
            [
                [("👉 Let’s go", "lets_go")],
                [("👉 Wait—what is Stellar Bloom?", "what_is_sb")],
            ]
        )
        return None

    if text in ["lets_go", "what_is_sb"]:
        set_state(chat_id, "what_is_objective")
        await send_message_with_buttons(
            chat_id,
            "You’ve been invited to join Stellar Bloom Academy—a secret interstellar training program where only the most emotionally resilient cadets are chosen.",
            [[("👉 What’s the objective?", "whats_objective")]]
        )
        return None

    if text == "whats_objective":
        set_state(chat_id, "ready_to_match")
        await send_message_with_buttons(
            chat_id,
            "🌸 Complete daily Bloom rituals.\n🔥 Level up with your Celestial.\n🌌 Unlock weekly Astral Portal meet-ups.\n🌱 Earn your place in the Corps.",
            [[("👉 Okay I’m in", "im_in")]]
        )
        return None

    if text == "im_in":
        set_state(chat_id, "start_questionnaire")
        await send_message_with_buttons(
            chat_id,
            "We’ll need to understand your rhythm to assign your Celestial mentor.\n👉 Ready to begin?",
            [[("👉 Continue", "continue_intro")]]
        )
        return None

    if text == "continue_intro":
        set_state(chat_id, "soul_sync_1")
        return await ask_question(chat_id, "soul_sync_1")

    # Generic handler for Soul Sync questionnaire answers
    celestial = get_celestial_from_choice(text)
    if celestial:
        print(f"User {chat_id} selected: {text} -> {celestial}")

        current_question = get_state(chat_id)
        next_question = QUESTION_FLOW.get(current_question, {}).get("next")

        if next_question:
            set_state(chat_id, next_question)
            return await ask_question(chat_id, next_question)
        else:
            # All questions done — determine top celestial and reveal
            update_user_score(chat_id, celestial)

    return "I didn’t understand that. Try again or type /start to restart onboarding."

async def ask_question(user_id, key):
    q = QUESTION_FLOW[key]
    buttons = [[(label, label)] for label, _ in q["buttons"]]
    return await send_message_with_buttons(user_id, q["text"], buttons)


def get_celestial_from_choice(choice):
    """Get label from question"""
    for q in QUESTION_FLOW.values():
        for label, celestial in q["buttons"]:
            if choice == label:
                return celestial
    return None
