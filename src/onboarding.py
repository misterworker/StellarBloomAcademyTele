from user_scores import update_user_score, get_top_celestial
from user_state import get_state, set_state
from telegram import send_message, send_chunked_message, send_message_with_buttons
from config import BOT_LINK
import aiohttp


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
        ],
        "next": "soul_sync_3"
    },
    "soul_sync_3": {
        "text": "🔹 Q3: Do you enjoy any kind of movement?",
        "buttons": [
            ("🕺 Fun/casual", "Riven"),
            ("🔁 Short/effective", "Orion"),
            ("🌿 Calm/slow", "Caelum"),
            ("📋 Structured", "Orion"),
            ("🙅 None", "Caelum")
        ],
        "next": "soul_sync_4"
    },
    "soul_sync_4": {
        "text": "🔹 Q4: What's your food relationship like?",
        "buttons": [
            ("😵‍💫 Stress eat/restrict", "Caelum"),
            ("🤷‍♀️ Inconsistent", "Riven"),
            ("🌱 Working on balance", "Caelum"),
            ("🍽 I love to eat!", "Riven"),
        ],
        "next": "soul_sync_5"
    },
    "soul_sync_5": {
        "text": "🔹 Q5: Do you usually cook or grab meals on the go?",
        "buttons": [
            ("🍳 Homecooked", "Orion"),
            ("🥡 Mixed", "Riven"),
            ("🧃 Takeout", "Caelum")
        ],
        "next": "soul_sync_6"
    },
    "soul_sync_6": {
        "text": "🔹 Q6: How do you feel when you wake up most days?",
        "buttons": [
            ("😴 Tired", "Caelum"),
            ("🌥 Mixed", "Riven"),
            ("🌞 Energized", "Orion"),
        ],
        "next": "soul_sync_7"
    },
    "soul_sync_7": {
        "text": "🔹 Q7: How many hours do you usually sleep?",
        "buttons": [
            ("🕑 <5hr sleep", "Caelum"),
            ("🕖 5-6hr", "Riven"),
            ("🕘 7-8hr", "Orion"),
            ("🕔 9+hr", "Caelum")
        ],
        "next": "soul_sync_8"
    },
    "soul_sync_8": {
        "text": "🔹 Q8: What does your day usually look like?",
        "buttons": [
            ("🧠 Work from home", "Riven"),
            ("🏃 Busy job", "Orion"),
            ("🧒 Caregiver", "Caelum"),
            ("🌀 Unstructured", "Caelum")
        ],
        "next": "soul_sync_9"
    },
    "soul_sync_9": {
        "text": "🔹Q9: How much time can you realistically dedicate daily to yourself?",
        "buttons": [
            ("🌱 Casual - 5 mins/day", "Caelum"),
            ("🌿 Regular - 10 mins/day", "Riven"),
            ("🌟 Dedicated - 15 mins/day", "Orion")
        ],
        "next": "soul_sync_10"
    },
    "soul_sync_10": {
        "text": "🔹 Q10: Every Cadet resonates with a different Celestial. What kind of support draws out your best?",
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
    "Orion": "💬 Orion: “You say you want to rise—but the stars demand proof. Let's see what you're made of.”",
    "Caelum": "💬 Caelum: “You don't have to fight your way through this. You just have to begin.”",
    "Riven": "💬 Riven: “Knew it'd be you. Fire flickering behind those eyes. Let's spark it up, Starlet.”"
}

async def handle_onboarding(chat_id, text, username):
    state = get_state(chat_id)
    print("Handle Onboarding: ", state)

    # START
    if text == "/start" or state == "start":
        set_state(chat_id, "waiting_for_ready")
        await send_message_with_buttons(
            chat_id,
            f"Hello, cadet {username}.\nYou've been selected to begin Stellar Bloom Training.\nThis is your onboarding.",
            [[("👉 I'm Ready", "onboarding_ready")]]
        )
        return None

    # "I'm Ready" button was pressed
    if text == "onboarding_ready" or state == "waiting_for_ready":
        set_state(chat_id, "ask_identity")
        await send_message(chat_id, "🔒 Please verify your identity.\nTell me your:\nName:\nAge:\nEmail:")
        return None

    # Handle identity collection
    if state == "ask_identity":
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BOT_LINK}/identify", json={"user_input": text}) as resp: # Call LLM to check validity of response
                data = await resp.json()
                is_valid = data.get("is_valid", True)

        if not is_valid:
            return await send_message(chat_id, "❌ That doesn't look right. Please send your **Name**, **Age**, and **Email** in one message.")

        set_state(chat_id, "ready_for_whats_in_store")
        await send_chunked_message(
            chat_id,
            "✅ Identity verified. Welcome aboard, cadet.---You're not just here to “get healthy.”---You're here to grow stronger, feel better, and earn your spot in the Astral Corps."
        )
        await send_message_with_buttons(
            chat_id,
            "Choose an option",
            [[("👉 What's in store?", "whats_in_store")]]
        )
        return None

    if text == "whats_in_store":
        await send_chunked_message(
            chat_id,
            "Only 2.3% of cadets make it past Initiation.---Most quit after Day 5.---Ready to see what you're made of?"
        )
        await send_message_with_buttons(
            chat_id,
            "Choose an option",
            [
                [("👉 Let's go", "lets_go")],
                [("👉 Wait—what is Stellar Bloom?", "what_is_sb")],
            ]
        )
        return None

    if text in ["lets_go", "what_is_sb"]:
        await send_chunked_message(
            chat_id,
            "You've been invited to join Stellar Bloom Academy—---a secret interstellar training program where only the most emotionally resilient cadets are chosen."
        )
        await send_message_with_buttons(
            chat_id,
            "Choose an option",
            [[("👉 What's the objective?", "whats_objective")]]
        )
        return None

    if text == "whats_objective":
        await send_chunked_message(
            chat_id,
            "🌸 Complete daily Bloom rituals.---🔥 Level up with your Celestial.---🌌 Unlock weekly Astral Portal meet-ups.---🌱 Earn your place in the Corps."
        )
        await send_message_with_buttons(
            chat_id,
            "Choose an option",
            [[("👉 Okay I'm in", "im_in")]]
        )
        return None

    if text == "im_in":
        await send_chunked_message(
            chat_id,
            "We'll need to understand your rhythm to assign your Celestial mentor.---👉 Ready to begin?"
        )
        await send_message_with_buttons(
            chat_id,
            "Choose an option",
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

    return "I didn't understand that. Try again or type /start to restart onboarding."

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
