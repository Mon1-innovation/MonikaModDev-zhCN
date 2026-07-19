init python:
    def output_persistent():
        import json
        with open(os.path.join(renpy.config.basedir, "persistent_out.json"), "w") as f:
            persistent2 = persistent
            #persistent2.__dict__['_seen_ever'].clear()
            #persistent2.__dict__['_mas_event_init_lockdb'].clear()
            #persistent2.__dict__['_changed'].clear()
            #persistent2.__dict__['_mas_event_init_lockdb'].clear()
            #persistent2.__dict__['event_database'].clear()
            #persistent2.__dict__['farewell_database'].clear()
            #persistent2.__dict__['greeting_database'].clear()
            #persistent2.__dict__['_mas_apology_database'].clear()
            #persistent2.__dict__['_mas_compliments_database'].clear()
            #persistent2.__dict__['_mas_fun_facts_database'].clear()
            #persistent2.__dict__['_mas_mood_database'].clear()
            #persistent2.__dict__['_mas_songs_database'].clear()
            #persistent2.__dict__['_mas_story_database'].clear()
            #persistent2.__dict__['_mas_affection_backups'] = None
            #persistent2.__dict__['greeting_database'].clear()
            #persistent2.__dict__['greeting_database'].clear()
            #persistent2.__dict__['greeting_database'].clear()
            #persistent2.__dict__['greeting_database'].clear()
            #persistent2.__dict__['greeting_database'].clear()
            #persistent2.__dict__['greeting_database'].clear()
            #persistent2.__dict__['greeting_database'].clear()
            #persistent2.__dict__['mas_playername'] = "pp"
            #persistent2.__dict__['mas_player_bday'] = [2002, 1, 1]
            #persistent2.__dict__['mas_affection'] = 2315.1
            #del persistent2.__dict__['_preferences']
            #for i in persistent2.__dict__:
            #    try:
            #        json.dumps(persistent2.__dict__[i])
            #    except:
            #        try:
            #            persistent2.__dict__[i] = str(persistent2.__dict__[i])
            #        except:
            #            persistent2.__dict__[i] = "REMOVED"
            #f.write(json.dumps(persistent2.__dict__, ensure_ascii=False))

        del persistent._voice_mute
        del persistent._mas_acs_pre_list
        del persistent._mas_windowreacts_notif_filters
        renpy.save_persistent()
        renpy.quit()


