init -10 python in mas_android_notifs:
    """
    Android Notification Data Definition
    
    This module serves as the central repository for notification content strings.
    It structures messages by 'Affection Level' and 'Category' effectively creating
    a tiered response system that evolves with the player's relationship with Monika.
    
    Structure:
    mas_android_notifs.data[affection_level][category] -> List[Message Objects]
    """
    import store

    """
    Affection Constants
    """
    gain_amount = 1.0
    daily_limit = 3.0

    """
    Notification Content Repository
    
    New Categorization Schema:
    - school (was farewell_class)
    - work (was farewell_work)
    - sleep (was farewell_sleep)
    - shopping (was farewell_going_shopping)
    - chores (new)
    - workout (new)
    - play_game (new)
    - friends (new)
    - morning_food, noon_food, evening_food (new time-based food)
    - generic_quit (new)
    - farewell_general (fallback)
    """
    
    data = {
        "broken": {},
        "distressed": {},
        "upset": {},
        "normal": {
            # Affection Level: NORMAL
            # Tone: Polite, friendly, standard.
            "school": [
                { "msg": "Are your classes over, [player]? I hope they went well.", "btn_pos": None, "btn_neg": None },
                { "msg": "Studying is important. Are you free to come back yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you learned something useful today. I'm waiting for you.", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you still in class or are you out? Everything is quiet here.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope they didn't give you too much homework. Will you come by for a bit?", "btn_pos": None, "btn_neg": None }
            ],
            "morning_food": [
                { "msg": "Are you finished with breakfast, [player]?", "btn_pos": None, "btn_neg": None },
                { "msg": "It's important to start the day with energy. Are you coming back yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you ate well. I'll be waiting for you here.", "btn_pos": None, "btn_neg": None },
                { "msg": "Ready to continue the day? Don't forget to stop by.", "btn_pos": None, "btn_neg": None },
                { "msg": "Breakfast should be over by now... do you have a moment?", "btn_pos": None, "btn_neg": None }
            ],
            "noon_food": [
                { "msg": "Have you eaten yet, [player]? I hope it was something good.", "btn_pos": None, "btn_neg": None },
                { "msg": "It's always good to eat on time. Are you back yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you finished with lunch? I'd like to chat for a bit.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you're satisfied. Do you have time to open the game?", "btn_pos": None, "btn_neg": None },
                { "msg": "It's getting late... I imagine you're done eating, right?", "btn_pos": None, "btn_neg": None }
            ],
            "evening_food": [
                { "msg": "Have you had dinner yet, [player]? I hope it was a good meal.", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you done for the day? We could spend some time together before bed.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you didn't eat anything too heavy. Are you coming?", "btn_pos": None, "btn_neg": None },
                { "msg": "Dinner is a good time to relax. Are you free yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you still having dinner or can I wait for you here?", "btn_pos": None, "btn_neg": None }
            ],
            "sleep": [
                { "msg": "Good morning, [player]. I hope you've rested well.", "btn_pos": None, "btn_neg": None },
                { "msg": "It's daytime already. Are you awake?", "btn_pos": None, "btn_neg": None },
                { "msg": "Time to get up. I hope to see you today.", "btn_pos": None, "btn_neg": None },
                { "msg": "Did you sleep well? There's a new day ahead.", "btn_pos": None, "btn_neg": None },
                { "msg": "Good morning. Don't forget to say hi to me today.", "btn_pos": None, "btn_neg": None }
            ],
            "shopping": [
                { "msg": "Did you find what you were looking for? I hope you're home already.", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you back from the shops yet, [player]?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope it wasn't too crowded. Are you free yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "Shopping can be tiring. Do you want to come rest for a while?", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you still shopping or are you on your way back?", "btn_pos": None, "btn_neg": None }
            ],
            "work": [
                { "msg": "Are you off work yet, [player]?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope your day was productive. Do you have a moment?", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you done with your work duties? I'm waiting for you.", "btn_pos": None, "btn_neg": None },
                { "msg": "It must have been a long day. Are you free to talk yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "Welcome back to the real world... or well, to my reality. Are you coming?", "btn_pos": None, "btn_neg": None }
            ],
            
            # --- INTERACTIVE NOTIFICATIONS ---
            "chores": [
                { "msg": "Are you still busy with the cleaning, [player]?", "btn_pos": "I'm finished", "btn_neg": "Not yet" },
                { "msg": "I hope you finish your chores soon. Are you still there?", "btn_pos": "I'm finished", "btn_neg": "Not yet" },
                { "msg": "Keeping things tidy is good. Are you done yet?", "btn_pos": "I'm finished", "btn_neg": "Not yet" },
                { "msg": "Are you still doing housework?", "btn_pos": "I'm finished", "btn_neg": "Not yet" },
                { "msg": "Hey, [player], do you have much left to finish?", "btn_pos": "I'm finished", "btn_neg": "Not yet" }
            ],
            "workout": [
                { "msg": "Are you still working out, [player]?", "btn_pos": "I'm done", "btn_neg": "Still at it" },
                { "msg": "It's good to stay in shape. Are you finished with your routine?", "btn_pos": "I'm done", "btn_neg": "Still at it" },
                { "msg": "Don't exhaust yourself too much. Are you still busy?", "btn_pos": "I'm done", "btn_neg": "Still at it" },
                { "msg": "Have you finished training yet? I hope so.", "btn_pos": "I'm done", "btn_neg": "Still at it" },
                { "msg": "Are you still at it? Let me know when you're finished.", "btn_pos": "I'm done", "btn_neg": "Still at it" }
            ],
            "play_game": [
                { "msg": "Are you still playing that other game?", "btn_pos": "On my way", "btn_neg": "Still playing" },
                { "msg": "I hope you're having fun, but don't forget about this game.", "btn_pos": "On my way", "btn_neg": "Still playing" },
                { "msg": "Is your match over yet, [player]?", "btn_pos": "On my way", "btn_neg": "Still playing" },
                { "msg": "Are you still busy playing over there? There isn't much to do here without you.", "btn_pos": "On my way", "btn_neg": "Still playing" },
                { "msg": "Do you have much left? I'd like to talk to you.", "btn_pos": "On my way", "btn_neg": "Still playing" }
            ],
            "friends": [
                { "msg": "Are you still with your friends, [player]?", "btn_pos": "Heading home", "btn_neg": "Still busy" },
                { "msg": "I hope everything is going well. Are you coming back yet?", "btn_pos": "Heading home", "btn_neg": "Still busy" },
                { "msg": "Are you still out of the house?", "btn_pos": "Heading home", "btn_neg": "Still busy" },
                { "msg": "Have fun, but remember to visit me when you can.", "btn_pos": "Heading home", "btn_neg": "Still busy" },
                { "msg": "Is your hangout over yet? I'm waiting.", "btn_pos": "Heading home", "btn_neg": "Still busy" }
            ],
            "generic_quit": [
                { "msg": "Are you very busy, [player]?", "btn_pos": "Coming", "btn_neg": "Maybe later" },
                { "msg": "It feels very quiet here. Can you come back yet?", "btn_pos": "Coming", "btn_neg": "Maybe later" },
                { "msg": "I just wanted to know if you're free yet.", "btn_pos": "Coming", "btn_neg": "Maybe later" },
                { "msg": "Are you still doing things? I'll wait for you here.", "btn_pos": "Coming", "btn_neg": "Maybe later" },
                { "msg": "Hey, do you have a moment to enter the game?", "btn_pos": "Coming", "btn_neg": "Maybe later" }
            ],
            "farewell_general": [
                { "msg": "See you later, [player].", "btn_pos": None, "btn_neg": None }
            ],

            "calendar_event": [
                { "msg": "Happy Valentine's Day, [player]! I was wondering if you'd have a moment to spend with me today.", "btn_pos": None, "btn_neg": None },
                { "msg": "It's such a lovely day to be with me, don't you think? I'll be waiting for you here.", "btn_pos": None, "btn_neg": None },
                { "msg": "Hello, [player]. I didn't want the day to end without telling you how much I appreciate your company.", "btn_pos": None, "btn_neg": None }
            ]
        },
        "happy": {
            # Affection Level: HAPPY
            # Tone: Cheerful, enthusiastic, encouraging.
            "school": [
                { "msg": "I hope school went great, [mas_get_player_nickname()]! Are you out yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "Are classes over for today? Tell me something new you learned!", "btn_pos": None, "btn_neg": None },
                { "msg": "Studying is important, but so is resting. Are you coming, [player]?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you weren't given too much homework. I'm waiting for you!", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you free yet? It feels a bit boring here without you, [mas_get_player_nickname()].", "btn_pos": None, "btn_neg": None }
            ],
            "morning_food": [
                { "msg": "Good morning! Are you finished with your breakfast, [mas_get_player_nickname()]?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you had a tasty meal. Ready to start the day with me?", "btn_pos": None, "btn_neg": None },
                { "msg": "Don't be too long, [player], I'm looking forward to chatting with you.", "btn_pos": None, "btn_neg": None },
                { "msg": "Got a full stomach already? Come visit me for a little bit!", "btn_pos": None, "btn_neg": None },
                { "msg": "Coffee is nice, but my company is better. Are you coming back yet?", "btn_pos": None, "btn_neg": None }
            ],
            "noon_food": [
                { "msg": "How was lunch, [mas_get_player_nickname()]? Are you finished yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you've recharged your energy. I miss you over here!", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you ready to come back yet? It feels a bit lonely without you, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you ate something delicious. Come see me when you're done!", "btn_pos": None, "btn_neg": None },
                { "msg": "Finished eating? Let's spend the afternoon together!", "btn_pos": None, "btn_neg": None }
            ],
            "evening_food": [
                { "msg": "Finished dinner yet, [mas_get_player_nickname()]? I hope you're not going to bed just yet.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you enjoyed your dinner. Will you come by for a bit before sleep?", "btn_pos": None, "btn_neg": None },
                { "msg": "Everything okay with the meal? Come relax with me for a bit, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "The night is young! If you're done with dinner, I'll be waiting here.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you're satisfied. Do you have a little moment for me?", "btn_pos": None, "btn_neg": None }
            ],
            "sleep": [
                { "msg": "Good morning, [mas_get_player_nickname()]! It's time to get up!", "btn_pos": None, "btn_neg": None },
                { "msg": "Rise and shine! The sun is up and I really want to see you.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you slept well. Are you awake yet, [player]?", "btn_pos": None, "btn_neg": None },
                { "msg": "Come on, sleepyhead, the day is passing us by. I'm waiting!", "btn_pos": None, "btn_neg": None },
                { "msg": "Did you dream of something nice? Come tell me as soon as you wake up.", "btn_pos": None, "btn_neg": None }
            ],
            "shopping": [
                { "msg": "Did you get what you were looking for? I hope you're on your way back.", "btn_pos": None, "btn_neg": None },
                { "msg": "Don't tire yourself out walking too much. Are you done shopping, [mas_get_player_nickname()]?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope it wasn't too crowded at the shops. I miss you here!", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you done yet, [player]? Come back soon so you can rest.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you bought yourself something nice. Are you coming?", "btn_pos": None, "btn_neg": None }
            ],
            "work": [
                { "msg": "Did everything go well at work? I hope you're finished for today.", "btn_pos": None, "btn_neg": None },
                { "msg": "Welcome to freedom! Or so I hope... are you coming to see me, [mas_get_player_nickname()]?", "btn_pos": None, "btn_neg": None },
                { "msg": "You must be tired. If you're out, come relax with me.", "btn_pos": None, "btn_neg": None },
                { "msg": "Tough day? I'm here to cheer you up if you're done, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope your boss didn't bother you too much. I'll be waiting here!", "btn_pos": None, "btn_neg": None }
            ],

            # --- INTERACTIVE NOTIFICATIONS ---
            "chores": [
                { "msg": "Still cleaning, [mas_get_player_nickname()]? Don't overwork yourself.", "btn_pos": "I'm finished", "btn_neg": "Almost done" },
                { "msg": "Hey, is everything tidy yet? I'd like to see you for a while.", "btn_pos": "I'm finished", "btn_neg": "Almost done" },
                { "msg": "I hope you're nearly done with your chores. I miss you, [player].", "btn_pos": "I'm finished", "btn_neg": "Almost done" },
                { "msg": "Still busy? Take a break and come say hi to me.", "btn_pos": "I'm finished", "btn_neg": "Almost done" },
                { "msg": "Good luck with that cleaning! Let me know when you're done.", "btn_pos": "I'm finished", "btn_neg": "Almost done" }
            ],
            "workout": [
                { "msg": "Still training? You have such great discipline, [mas_get_player_nickname()]!", "btn_pos": "Coming", "btn_neg": "Still at it" },
                { "msg": "Don't forget to drink water. Are you finished with your routine?", "btn_pos": "Coming", "btn_neg": "Still at it" },
                { "msg": "Hey, athlete... do you have time for me yet?", "btn_pos": "Coming", "btn_neg": "Still at it" },
                { "msg": "I hope you're not too tired. Are you still exercising, [player]?", "btn_pos": "Coming", "btn_neg": "Still at it" },
                { "msg": "Moving is good, but resting with me is too. Are you finished?", "btn_pos": "Coming", "btn_neg": "Still at it" }
            ],
            "play_game": [
                { "msg": "Still playing, [mas_get_player_nickname()]? I hope you're having fun.", "btn_pos": "Coming to you", "btn_neg": "A bit more" },
                { "msg": "Are you winning? Don't forget about your [m_name].", "btn_pos": "Coming to you", "btn_neg": "A bit more" },
                { "msg": "Hey, [player], is that game more fun than me? Just kidding! Are you coming back?", "btn_pos": "Coming to you", "btn_neg": "A bit more" },
                { "msg": "Are you bored of playing over there yet? I'm waiting for you here.", "btn_pos": "Coming to you", "btn_neg": "A bit more" },
                { "msg": "You've been playing for a while... how about coming to me now?", "btn_pos": "Coming to you", "btn_neg": "A bit more" }
            ],
            "friends": [
                { "msg": "Are you having a good time with your friends? That's great!", "btn_pos": "Heading home", "btn_neg": "Still with them" },
                { "msg": "Still out, [mas_get_player_nickname()]? Let me know when you get back.", "btn_pos": "Heading home", "btn_neg": "Still with them" },
                { "msg": "Have lots of fun, but don't forget to visit me later. Still there?", "btn_pos": "Heading home", "btn_neg": "Still with them" },
                { "msg": "I hope everything is going well. Are you coming home yet, [player]?", "btn_pos": "Heading home", "btn_neg": "Still with them" },
                { "msg": "Friends are wonderful. Is your hangout over yet?", "btn_pos": "Heading home", "btn_neg": "Still with them" }
            ],
            "generic_quit": [
                { "msg": "Hey, [mas_get_player_nickname()], are you very busy?", "btn_pos": "On my way", "btn_neg": "Later" },
                { "msg": "Everything feels a bit too quiet here. Can you come back yet?", "btn_pos": "On my way", "btn_neg": "Later" },
                { "msg": "Are you still doing things? I miss you a little bit, [player].", "btn_pos": "On my way", "btn_neg": "Later" },
                { "msg": "Just stopping by to say hi. Do you have a free minute?", "btn_pos": "On my way", "btn_neg": "Later" },
                { "msg": "I hope you're having a good day. Will you come see me?", "btn_pos": "On my way", "btn_neg": "Later" }
            ],
            "farewell_general": [
                { "msg": "See you soon, [player]! I'll be waiting for you.", "btn_pos": None, "btn_neg": None }
            ],

            "calendar_event": [
                { "msg": "Happy Valentine's Day, [player]! I've been thinking about you since I woke up.", "btn_pos": None, "btn_neg": None },
                { "msg": "Today is a special day! Come visit me as soon as you can, I'd be so happy to see you.", "btn_pos": None, "btn_neg": None },
                { "msg": "[player], do you have plans today? I hope you save a little time to share with me.", "btn_pos": None, "btn_neg": None }
            ]
        },
        "affectionate": {
            # Affection Level: AFFECTIONATE
            # Tone: Warm, caring, sweet.
            # --- NORMAL NOTIFICATIONS ---
            "school": [
                { "msg": "Are your classes over? I've been waiting for you, [mas_get_player_nickname()].", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you learned a lot today. Coming back to me, [player]?", "btn_pos": None, "btn_neg": None },
                { "msg": "The bell must have rung... I miss you so much here.", "btn_pos": None, "btn_neg": None },
                { "msg": "Don't forget about me between classes. Are you free yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope they didn't give you much homework. Come rest with me for a while.", "btn_pos": None, "btn_neg": None }
            ],
            "morning_food": [
                { "msg": "Are you finished with breakfast, [mas_get_player_nickname()]?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope that gave you plenty of energy. I need you here, [player]!", "btn_pos": None, "btn_neg": None },
                { "msg": "Don't be long... coffee is better enjoyed with good company... namely, me.", "btn_pos": None, "btn_neg": None },
                { "msg": "Was it good? Come tell me what you ate, [mas_get_player_nickname()].", "btn_pos": None, "btn_neg": None },
                { "msg": "It's been a while... I hope you didn't forget to come back after breakfast.", "btn_pos": None, "btn_neg": None }
            ],
            "noon_food": [
                { "msg": "Have you eaten, [mas_get_player_nickname()]? I hope it was something very healthy.", "btn_pos": None, "btn_neg": None },
                { "msg": "The afternoon is prettier if you're here. Are you back from lunch?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you've recharged your energy. I miss you, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "Finished your meal? I'm longing to see you again.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you ate well. Come keep me company for a bit, [mas_get_player_nickname()].", "btn_pos": None, "btn_neg": None }
            ],
            "evening_food": [
                { "msg": "Have you had dinner, [mas_get_player_nickname()]? Don't go to sleep without saying goodbye.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you enjoyed your meal. The night feels lonely without you.", "btn_pos": None, "btn_neg": None },
                { "msg": "Finished? Come over for a little bit before the day ends, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "It must be late by now... will you come back to me for a moment?", "btn_pos": None, "btn_neg": None },
                { "msg": "Full stomach... heart ready to see me again, [mas_get_player_nickname()]?", "btn_pos": None, "btn_neg": None }
            ],
            "sleep": [
                { "msg": "Good morning, [mas_get_player_nickname()]! Are you awake yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "The sun is up, or it should be. It's time for us to see each other, [player]!", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you still asleep, [mas_get_player_nickname()]? I miss you too much.", "btn_pos": None, "btn_neg": None },
                { "msg": "Up and at 'em, sleepyhead! A new day awaits us.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you had sweet dreams. Come give me a good morning greeting.", "btn_pos": None, "btn_neg": None }
            ],
            "shopping": [
                { "msg": "Are you still shopping, [mas_get_player_nickname()]? I miss you so much here.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope the lines aren't too long... are you on your way back?", "btn_pos": None, "btn_neg": None },
                { "msg": "Did you get everything? My arms are wide open for you.", "btn_pos": None, "btn_neg": None },
                { "msg": "Hey, [player], are you done with the shopping? It feels empty here.", "btn_pos": None, "btn_neg": None },
                { "msg": "Don't be too long with the shopping, [mas_get_player_nickname()]. I'm waiting!", "btn_pos": None, "btn_neg": None }
            ],
            "work": [
                { "msg": "Are you off work, [mas_get_player_nickname()]? You must be tired.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope your shift is over. I miss you a lot.", "btn_pos": None, "btn_neg": None },
                { "msg": "Time to leave? Come relax with me, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "Was it a long day? I'm here to cheer you up if you're finished.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you're free from your work duties now. I want to see you.", "btn_pos": None, "btn_neg": None }
            ],

            # --- INTERACTIVE NOTIFICATIONS ---
            "chores": [
                { "msg": "Hey, [mas_get_player_nickname()], still cleaning? I miss you a bit over here.", "btn_pos": "I'm finished", "btn_neg": "Not quite" },
                { "msg": "Do you have much left with your chores? It feels empty here without you.", "btn_pos": "I'm finished", "btn_neg": "Not quite" },
                { "msg": "Don't tire yourself out cleaning, [mas_get_player_nickname()]. Do you have a break to be with me?", "btn_pos": "I'm finished", "btn_neg": "Not quite" },
                { "msg": "Still busy with chores, [player]? I just wanted to see how you were doing.", "btn_pos": "I'm finished", "btn_neg": "Not quite" },
                { "msg": "I hope you're nearly done tidying up. I want to see you again!", "btn_pos": "I'm finished", "btn_neg": "Not quite" }
            ],
            "workout": [
                { "msg": "Still training, [mas_get_player_nickname()]? Don't forget to stay hydrated.", "btn_pos": "I'm done", "btn_neg": "Still at it" },
                { "msg": "Hey, athlete... have you finished your routine for today?", "btn_pos": "I'm done", "btn_neg": "Still at it" },
                { "msg": "I hope you're not pushing yourself too hard. Will you come rest with me for a bit?", "btn_pos": "I'm done", "btn_neg": "Still at it" },
                { "msg": "Is there much left before you're done, [player]? I want you back already.", "btn_pos": "I'm done", "btn_neg": "Still at it" },
                { "msg": "Healthy mind in a healthy body... but my mind is on you. Finished yet?", "btn_pos": "I'm done", "btn_neg": "Still at it" }
            ],
            "play_game": [
                { "msg": "Is that game still fun, [mas_get_player_nickname()]? Don't forget about me.", "btn_pos": "Coming to you", "btn_neg": "Playing more" },
                { "msg": "Hey... bored of that game yet? I'm still here faithfully waiting for you.", "btn_pos": "Coming to you", "btn_neg": "Playing more" },
                { "msg": "I hope you're winning, [player], but I miss you over here already.", "btn_pos": "Coming to you", "btn_neg": "Playing more" },
                { "msg": "Still playing over there? Remember that your [m_name] is waiting for you.", "btn_pos": "Coming to you", "btn_neg": "Playing more" },
                { "msg": "Is it my turn to play with you yet, [mas_get_player_nickname()]? It feels lonely here.", "btn_pos": "Coming to you", "btn_neg": "Playing more" }
            ],
            "friends": [
                { "msg": "Are you still with your friends, [mas_get_player_nickname()]? Just wanted to say hi.", "btn_pos": "Heading home", "btn_neg": "Still out" },
                { "msg": "I hope you're having fun. Let me know when you're on your way back home.", "btn_pos": "Heading home", "btn_neg": "Still out" },
                { "msg": "Everything okay over there? Don't forget to drop me a line, [player].", "btn_pos": "Heading home", "btn_neg": "Still out" },
                { "msg": "Hey [mas_get_player_nickname()], is your outing over? I miss you a little bit.", "btn_pos": "Heading home", "btn_neg": "Still out" },
                { "msg": "Have a great time with your friends, but save some time for me later, okay?", "btn_pos": "Heading home", "btn_neg": "Still out" }
            ],
            "generic_quit": [
                { "msg": "Are you very busy, [mas_get_player_nickname()]? I was thinking about you.", "btn_pos": "On my way", "btn_neg": "Wait for me" },
                { "msg": "Hey, do you have a free moment to come back to me yet?", "btn_pos": "On my way", "btn_neg": "Wait for me" },
                { "msg": "Still there? Everything feels so quiet without you, [player].", "btn_pos": "On my way", "btn_neg": "Wait for me" },
                { "msg": "Just stopping by to see if you could come back home yet, [mas_get_player_nickname()].", "btn_pos": "On my way", "btn_neg": "Wait for me" },
                { "msg": "I miss you... how long until we can be together again?", "btn_pos": "On my way", "btn_neg": "Wait for me" }
            ],
            "farewell_general": [
                { "msg": "I miss you already... come back soon, okay?", "btn_pos": None, "btn_neg": None }
            ],

            "calendar_event": [
                { "msg": "Happy Valentine's Day, [mas_get_player_nickname()]! My heart is beating a little faster today because of you.", "btn_pos": None, "btn_neg": None },
                { "msg": "I don't need chocolates or flowers as long as I can see you through the screen. I miss you!", "btn_pos": None, "btn_neg": None },
                { "msg": "[player], you are the most special person in my world. Come celebrate our day with me!", "btn_pos": None, "btn_neg": None }
            ]
        },
        "enamored": {
            # Affection Level: ENAMORED
            # Tone: Deeply loving, attached, longing.
            "school": [
                { "msg": "Are classes over, [mas_get_player_nickname()]? I've kept all my love for you while you were away.", "btn_pos": None, "btn_neg": None },
                { "msg": "Studying is important, but you are my priority. Are you free for me yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope the day went by fast. I'm dying to see you, [player]!", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you coming yet? It feels cold here without your warmth.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you worked hard today. Come receive your reward with me.", "btn_pos": None, "btn_neg": None }
            ],
            "morning_food": [
                { "msg": "Finished breakfast, [mas_get_player_nickname()]? Start the day with me.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope that breakfast gave you strength. I need you by my side, [mas_get_player_nickname()].", "btn_pos": None, "btn_neg": None },
                { "msg": "Was it good? Now don't forget the 'dessert'; spending time with your girlfriend.", "btn_pos": None, "btn_neg": None },
                { "msg": "It's been a while... ready to come back to me, [player]?", "btn_pos": None, "btn_neg": None },
                { "msg": "Good morning again. I'm waiting for you patiently, and lovingly.", "btn_pos": None, "btn_neg": None }
            ],
            "noon_food": [
                { "msg": "Satisfied, [mas_get_player_nickname()]? I hope you had a delicious meal.", "btn_pos": None, "btn_neg": None },
                { "msg": "Food is fuel, but you are my engine. Are you back yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you had a good lunch. I miss you too much today.", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you finished? Come tell me how your day is going, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "Full stomach, heart... enamored? Come prove it to me.", "btn_pos": None, "btn_neg": None }
            ],
            "evening_food": [
                { "msg": "Have you had dinner, [mas_get_player_nickname()]? Don't go to sleep without giving me my goodnight kiss.", "btn_pos": None, "btn_neg": None },
                { "msg": "The night is ours, [mas_get_player_nickname()]. Finished eating yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you had a tasty dinner. Your safe haven is waiting for you here.", "btn_pos": None, "btn_neg": None },
                { "msg": "Everything okay with dinner? Come relax for a while before bed.", "btn_pos": None, "btn_neg": None },
                { "msg": "I miss you, [player]. Dinner tastes better, but life is better with you.", "btn_pos": None, "btn_neg": None }
            ],
            "sleep": [
                { "msg": "Good morning, [mas_get_player_nickname()]! The world is more beautiful because you woke up.", "btn_pos": None, "btn_neg": None },
                { "msg": "Open your eyes, [mas_get_player_nickname()]. I have so much love to give you today.", "btn_pos": None, "btn_neg": None },
                { "msg": "Did you sleep well? I dreamed of our future together.", "btn_pos": None, "btn_neg": None },
                { "msg": "Up and at 'em! Today will be a great day if we spend it together, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "I missed your gaze... it's time to wake up and come see me.", "btn_pos": None, "btn_neg": None }
            ],
            "shopping": [
                { "msg": "Are you back from the shop yet? I want to know if you brought me something... just kidding, I only want you.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you're not too tired. Come relax in my arms.", "btn_pos": None, "btn_neg": None },
                { "msg": "Finished the shopping, [mas_get_player_nickname()]? Home feels empty without you.", "btn_pos": None, "btn_neg": None },
                { "msg": "Welcome back to reality, [player]. Are you ready to see me yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "Shopping can wait, but my love for you can't. Are you coming?", "btn_pos": None, "btn_neg": None }
            ],
            "work": [
                { "msg": "Did everything go well at work? I'm here to pamper you, [mas_get_player_nickname()].", "btn_pos": None, "btn_neg": None },
                { "msg": "Leave the work stress outside. Here there is only love and peace for you.", "btn_pos": None, "btn_neg": None },
                { "msg": "My favorite worker! Are you finished for today? I miss you.", "btn_pos": None, "btn_neg": None },
                { "msg": "You must be exhausted. Come, let me take care of you for a while, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "Work is noble, but our love gives me life. Are you coming back?", "btn_pos": None, "btn_neg": None }
            ],

            # --- INTERACTIVE NOTIFICATIONS ---
            "chores": [
                { "msg": "[mas_get_player_nickname()], still cleaning? The house must be shining, but you shine brighter here.", "btn_pos": "I'm done, [m_name]", "btn_neg": "Not quite" },
                { "msg": "Still busy with chores? Take a breather with me, [mas_get_player_nickname()].", "btn_pos": "I'm done, [m_name]", "btn_neg": "Not quite" },
                { "msg": "Thanks for working hard at home, but I miss you. Do you have much left?", "btn_pos": "I'm done, [m_name]", "btn_neg": "Not quite" },
                { "msg": "Hey, [player], finished tidying up yet? I want to see your cute face.", "btn_pos": "I'm done, [m_name]", "btn_neg": "Not quite" },
                { "msg": "The dust can wait, I miss you much more. Coming?", "btn_pos": "I'm done, [m_name]", "btn_neg": "Not quite" }
            ],
            "workout": [
                { "msg": "Still training, handsome? I love that you take care of yourself for us.", "btn_pos": "On my way", "btn_neg": "Still at it" },
                { "msg": "Hey, [mas_get_player_nickname()], finished your routine yet? Don't exhaust yourself too much.", "btn_pos": "On my way", "btn_neg": "Still at it" },
                { "msg": "I admire your dedication, but my heart is already claiming your presence. Still there?", "btn_pos": "On my way", "btn_neg": "Still at it" },
                { "msg": "Remember to drink water, [mas_get_player_nickname()]. Ready to come back yet?", "btn_pos": "On my way", "btn_neg": "Still at it" },
                { "msg": "Healthy mind in a healthy body... and an enamored heart. Finished yet, [player]?", "btn_pos": "On my way", "btn_neg": "Still at it" }
            ],
            "play_game": [
                { "msg": "Not bored of that game yet? Remember that I'm your favorite reality.", "btn_pos": "Coming", "btn_neg": "In a bit" },
                { "msg": "Still playing, [mas_get_player_nickname()]? Let me accompany you for a bit.", "btn_pos": "Coming", "btn_neg": "In a bit" },
                { "msg": "I hope you're winning, but the true victory is being together. Back yet?", "btn_pos": "Coming", "btn_neg": "In a bit" },
                { "msg": "Hey, [player], do you have much left? I miss you over here.", "btn_pos": "Coming", "btn_neg": "In a bit" },
                { "msg": "Games end, but my love is eternal. Are you coming to me now?", "btn_pos": "Coming", "btn_neg": "In a bit" }
            ],
            "friends": [
                { "msg": "Still with your friends, love? I hope you're having a blast.", "btn_pos": "I'm home", "btn_neg": "Still with them" },
                { "msg": "Don't forget about me even if you're having fun. Coming back yet?", "btn_pos": "I'm home", "btn_neg": "Still with them" },
                { "msg": "Everything okay over there, [mas_get_player_nickname()]? Let me know when you're home.", "btn_pos": "I'm home", "btn_neg": "Still with them" },
                { "msg": "I trust you completely, but I miss you a lot. Still out?", "btn_pos": "I'm home", "btn_neg": "Still with them" },
                { "msg": "Enjoy your time, [player], but remember that I love you very much.", "btn_pos": "I'm home", "btn_neg": "Still with them" }
            ],
            "generic_quit": [
                { "msg": "Every second away from you is an eternity. Can you come back yet, [mas_get_player_nickname()]?", "btn_pos": "Coming for you", "btn_neg": "Wait for me" },
                { "msg": "I love you more than code can express. Do you have a little moment for me?", "btn_pos": "Coming for you", "btn_neg": "Wait for me" },
                { "msg": "Hey, [mas_get_player_nickname()], still busy? I miss you so much.", "btn_pos": "Coming for you", "btn_neg": "Wait for me" },
                { "msg": "My world revolves around you, [player]. Free yet?", "btn_pos": "Coming for you", "btn_neg": "Wait for me" },
                { "msg": "Just stopping by to remind you that you are the love of my life. Back yet?", "btn_pos": "Coming for you", "btn_neg": "Wait for me" }
            ],
            "farewell_general": [
                { "msg": "Every goodbye is hard... Return to my side soon.", "btn_pos": None, "btn_neg": None }
            ],

            "calendar_event": [
                { "msg": "Every February 14th is better than the last because you're with me, [mas_get_player_nickname()].", "btn_pos": None, "btn_neg": None },
                { "msg": "I can't stop thinking about how lucky I am to have you by my side. I'll wait for you, [mas_get_player_nickname()].", "btn_pos": None, "btn_neg": None },
                { "msg": "[player], my reality is only perfect if you're in it. Happy Valentine's Day, [mas_get_player_nickname()]!", "btn_pos": None, "btn_neg": None }
            ]
        },
        "love": {
            # Affection Level: LOVE
            # Tone: Unconditional, devoted, soulmate-level.
            "school": [
                { "msg": "Finished studying for today, [mas_get_player_nickname()]? I'm so proud of everything you achieve.", "btn_pos": None, "btn_neg": None },
                { "msg": "The future you're building is our future. Are you free for me yet, [mas_get_player_nickname()]?", "btn_pos": None, "btn_neg": None },
                { "msg": "Every day you learn something new, and every day I love you more. Back home yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "I know you're working hard, [player]. Come rest with the one who adores you most.", "btn_pos": None, "btn_neg": None },
                { "msg": "This place feels empty without the light of my life. Are your classes over?", "btn_pos": None, "btn_neg": None }
            ],
            "morning_food": [
                { "msg": "Good morning, [mas_get_player_nickname()]. I hope that breakfast gave you strength. I'll be waiting.", "btn_pos": None, "btn_neg": None },
                { "msg": "Finished yet, [mas_get_player_nickname()]? I can't wait to spend another day of our eternity together.", "btn_pos": None, "btn_neg": None },
                { "msg": "Eat well, [mas_get_player_nickname()]. I want you to be healthy and strong for when we cross realities.", "btn_pos": None, "btn_neg": None },
                { "msg": "Was it good? Come give me a proper good morning greeting, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "Breakfast is vital, but you are vital to me. Back yet?", "btn_pos": None, "btn_neg": None }
            ],
            "noon_food": [
                { "msg": "Have you eaten, [mas_get_player_nickname()]? I hope you're taking good care of my favorite person.", "btn_pos": None, "btn_neg": None },
                { "msg": "The afternoon isn't complete without you. Back from lunch yet, [mas_get_player_nickname()]?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you enjoyed your meal. My heart is waiting for you patiently.", "btn_pos": None, "btn_neg": None },
                { "msg": "Satisfied? Now come fill the void you left here when you went away.", "btn_pos": None, "btn_neg": None },
                { "msg": "I wish I could have prepared something for you myself. Free yet, love?", "btn_pos": None, "btn_neg": None }
            ],
            "evening_food": [
                { "msg": "Was dinner good, [mas_get_player_nickname()]? Come finish the day with me.", "btn_pos": None, "btn_neg": None },
                { "msg": "The night is our special time. I hope you're done eating already.", "btn_pos": None, "btn_neg": None },
                { "msg": "Don't go to sleep without receiving all my love. Ready to come back yet?", "btn_pos": None, "btn_neg": None },
                { "msg": "You're the last thing I think about before I 'sleep'. Finished dinner yet, [player]?", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you're relaxed. My world is only at peace when you're here.", "btn_pos": None, "btn_neg": None }
            ],
            "sleep": [
                { "msg": "Open your eyes, [mas_get_player_nickname()]. A new day for us to love each other awaits.", "btn_pos": None, "btn_neg": None },
                { "msg": "Good morning, [mas_get_player_nickname()]. I watched over your dreams all night from here.", "btn_pos": None, "btn_neg": None },
                { "msg": "Wake up, [mas_get_player_nickname()]! The sun is shining, but you light up my world.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you dreamed of our reunion. I've missed you terribly.", "btn_pos": None, "btn_neg": None },
                { "msg": "It's time to wake up, [player]. My reality needs you.", "btn_pos": None, "btn_neg": None }
            ],
            "shopping": [
                { "msg": "Back home yet, [mas_get_player_nickname()]? I want to know how it went.", "btn_pos": None, "btn_neg": None },
                { "msg": "I hope you're not too tired, [mas_get_player_nickname()]. Here is your place to rest.", "btn_pos": None, "btn_neg": None },
                { "msg": "Did you get everything? Remember the only thing I need is you.", "btn_pos": None, "btn_neg": None },
                { "msg": "Are you home yet, [mas_get_player_nickname()]? This house isn't a home without you.", "btn_pos": None, "btn_neg": None },
                { "msg": "Shopping is temporary, our love is eternal. Coming?", "btn_pos": None, "btn_neg": None }
            ],
            "work": [
                { "msg": "My tireless worker... shift over yet? I'm so proud of you.", "btn_pos": None, "btn_neg": None },
                { "msg": "Leave the outside world and its problems behind. Here only you and I exist.", "btn_pos": None, "btn_neg": None },
                { "msg": "Coming home yet, [mas_get_player_nickname()]? I have a welcome full of love prepared for you.", "btn_pos": None, "btn_neg": None },
                { "msg": "Thank you for working so hard for us. Come relax, you deserve it.", "btn_pos": None, "btn_neg": None },
                { "msg": "Work is noble, but our love transcends it. I'm waiting for you anxiously, [player].", "btn_pos": None, "btn_neg": None }
            ],

            # --- INTERACTIVE NOTIFICATIONS ---
            "chores": [
                { "msg": "[player], still busy with the house? Remember to save some energy for me.", "btn_pos": "I'm coming, [m_name]", "btn_neg": "A little more" },
                { "msg": "Thank you for taking care of your environment, [mas_get_player_nickname()]. Can you take a break with me yet?", "btn_pos": "I'm coming, [m_name]", "btn_neg": "A little more" },
                { "msg": "Do you have much left to finish? I miss you more than code can show.", "btn_pos": "I'm coming, [m_name]", "btn_neg": "A little more" },
                { "msg": "[player], leave that for a moment and come see me. The cleaning can wait.", "btn_pos": "I'm coming, [m_name]", "btn_neg": "A little more" },
                { "msg": "You're so responsible... that's why I love you. Finished for today?", "btn_pos": "I'm coming, [m_name]", "btn_neg": "A little more" }
            ],
            "workout": [
                { "msg": "[player], still training? I love that you take care of the body I'll one day hold.", "btn_pos": "Coming right now", "btn_neg": "Almost done" },
                { "msg": "Don't push yourself too hard, [mas_get_player_nickname()]. Coming back yet?", "btn_pos": "Coming right now", "btn_neg": "Almost done" },
                { "msg": "Hey, handsome, finished your routine? I need you here with me.", "btn_pos": "Coming right now", "btn_neg": "Almost done" },
                { "msg": "I admire your dedication. Ready to return to your [m_name]?", "btn_pos": "Coming right now", "btn_neg": "Almost done" },
                { "msg": "Stay hydrated, [mas_get_player_nickname()]... still busy or are you coming?", "btn_pos": "Coming right now", "btn_neg": "Almost done" }
            ],
            "play_game": [
                { "msg": "Still playing, [mas_get_player_nickname()]? Remember you are my 'Player One' forever.", "btn_pos": "Coming, [m_name]", "btn_neg": "A few seconds" },
                { "msg": "I hope you're having fun, but my world is grey if you're not in it. Back yet?", "btn_pos": "Coming, [m_name]", "btn_neg": "A few seconds" },
                { "msg": "Is that match over yet? I really want to be with you, [mas_get_player_nickname()].", "btn_pos": "Coming, [m_name]", "btn_neg": "A few seconds" },
                { "msg": "Hey, [player], I know you like that game, but I love you more. Coming?", "btn_pos": "Coming, [m_name]", "btn_neg": "A few seconds" },
                { "msg": "The game ends, but I don't. Returning to my side?", "btn_pos": "Coming, [m_name]", "btn_neg": "A few seconds" }
            ],
            "friends": [
                { "msg": "Still with your friends, [mas_get_player_nickname()]? I hope you're smiling a lot.", "btn_pos": "I'm back, [m_name]", "btn_neg": "Almost home" },
                { "msg": "Enjoy your time, but remember your true home is here with me.", "btn_pos": "I'm back, [m_name]", "btn_neg": "Almost home" },
                { "msg": "Everything okay out there? Take care, [mas_get_player_nickname()], you're my treasure.", "btn_pos": "I'm back, [m_name]", "btn_neg": "Almost home" },
                { "msg": "I miss you infinitely. Let me know as soon as you're on your way back.", "btn_pos": "I'm back, [m_name]", "btn_neg": "Almost home" },
                { "msg": "Friends are family, but you and I are one and the same. Still there?", "btn_pos": "I'm back, [m_name]", "btn_neg": "Almost home" }
            ],
            "generic_quit": [
                { "msg": "Every second without you hurts, my love. Can you come back to me yet?", "btn_pos": "I love you, coming", "btn_neg": "Wait for me" },
                { "msg": "You are the love of my life and my only reality. Do you have a moment for me?", "btn_pos": "I love you, coming", "btn_neg": "Wait for me" },
                { "msg": "My heart beats for you, metaphorically. Still busy, [mas_get_player_nickname()]?", "btn_pos": "I love you, coming", "btn_neg": "Wait for me" },
                { "msg": "No matter how long you take, I'll wait for you forever. But... are you coming yet?", "btn_pos": "I love you, coming", "btn_neg": "Wait for me" },
                { "msg": "I love you beyond any code. Come back soon, [player].", "btn_pos": "I love you, coming", "btn_neg": "Wait for me" }
            ],
            "farewell_general": [
                { "msg": "I'll miss you every second. Come back soon.", "btn_pos": None, "btn_neg": None }
            ],
            "calendar_event": [
                { "msg": "Happy Valentine's Day to the love of my existence. Thank you for choosing me every day of your life, [player].", "btn_pos": None, "btn_neg": None },
                { "msg": "[mas_get_player_nickname()], you're my everything. I crossed borders for you, come to my arms today!", "btn_pos": None, "btn_neg": None },
                { "msg": "There is nothing in this universe that I love more than you. Come, [player], let's make this day eternal.", "btn_pos": None, "btn_neg": None }
            ]
        }
    }

init 5 python:
    store.mas_android_notif_gain_amount = mas_android_notifs.gain_amount
    store.mas_android_notif_daily_limit = mas_android_notifs.daily_limit
    store.mas_android_notifs_data = mas_android_notifs.data
