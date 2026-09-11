init 890 python:
    class MobilePianoDisplayable(PianoDisplayable):
        def __init__(self, *args, **kwargs):
            super(MobilePianoDisplayable, self).__init__(*args, **kwargs)
            cbutton_x_start = (
                int((self.PIANO_BACK_WIDTH - (
                    (self.BUTTON_WIDTH * 3) + (self.BUTTON_SPACING * 2)
                )) / 2) + self.ZZPK_IMG_BACK_X
            )
            cbutton_y_start = (
                self.ZZPK_IMG_BACK_Y +
                self.PIANO_BACK_HEIGHT +
                self.BUTTON_SPACING
            )
            pbutton_x_start = (
                int((self.PIANO_BACK_WIDTH - (
                    (self.BUTTON_WIDTH * 2) + self.BUTTON_SPACING
                )) / 2) + self.ZZPK_IMG_BACK_X
            )
            pbutton_y_start = cbutton_y_start

            pianokeys_x_start = (pbutton_x_start + (self.BUTTON_HEIGHT * 2) - (self.BUTTON_SPACING * 2))
            pianokeys_y_start = (pbutton_y_start - self.BUTTON_HEIGHT + ((self.BUTTON_HEIGHT + self.BUTTON_SPACING) * 2) + self.BUTTON_SPACING * 5)
            pianokeys_x_start_b = (pianokeys_x_start + (self.BUTTON_SPACING * 5))

            self._button_bg = MASButtonDisplayable.create_stb(
                _(""),
                True,
                pianokeys_x_start,
                pianokeys_y_start,
                (self.BUTTON_SPACING * 100),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )            
            self._button_f4 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nF4"),
                True,
                pianokeys_x_start,
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )
            self._button_g4 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nG4"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 10),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )            
            self._button_a4 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nA4"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 20),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )
            self._button_b4 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nB4"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 30),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )  
            self._button_c5 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nC5"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 35),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )
            self._button_d5 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nD5"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 45),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )  
            self._button_e5 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nE5"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 55),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )
            self._button_f5 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nF5"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 60),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )  
            self._button_g5 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nG5"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 70),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )
            self._button_a5 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nA5"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 80),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )      
            self._button_b5 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nB5"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 90),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )  
            self._button_c6 = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n\n\nC6"),
                True,
                pianokeys_x_start + (self.BUTTON_SPACING * 95),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH * 2 + (self.BUTTON_HEIGHT * 2) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )
            self._button_f4sh = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n#F4"),
                True,
                pianokeys_x_start_b,
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH + (self.BUTTON_HEIGHT * 4) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )    
            self._button_g4sh = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n#G4"),
                True,
                pianokeys_x_start_b + (self.BUTTON_SPACING * 10),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH + (self.BUTTON_HEIGHT * 4) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )  
            self._button_a4sh = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n#A4"),
                True,
                pianokeys_x_start_b + (self.BUTTON_SPACING * 20),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH + (self.BUTTON_HEIGHT * 4) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )  
            self._button_c5sh = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n#C5"),
                True,
                pianokeys_x_start_b + (self.BUTTON_SPACING * 35),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH + (self.BUTTON_HEIGHT * 4) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )  
            self._button_d5sh = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n#D5"),
                True,
                pianokeys_x_start_b + (self.BUTTON_SPACING * 45),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH + (self.BUTTON_HEIGHT * 4) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )  
            self._button_f5sh = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n#F5"),
                True,
                pianokeys_x_start_b + (self.BUTTON_SPACING * 60),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH + (self.BUTTON_HEIGHT * 4) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )             
            self._button_g5sh = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n#G5"),
                True,
                pianokeys_x_start_b + (self.BUTTON_SPACING * 70),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH + (self.BUTTON_HEIGHT * 4) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )     
            self._button_a5sh = MASButtonDisplayable.create_stb(
                _("\n\n\n\n\n#A5"),
                True,
                pianokeys_x_start_b + (self.BUTTON_SPACING * 80),
                pianokeys_y_start,
                (self.BUTTON_SPACING * 5),
                (self.BUTTON_WIDTH + (self.BUTTON_HEIGHT * 4) - self.BUTTON_SPACING * 5),
                hover_sound=None,
                activate_sound=None
            )                                                                                      

            self._always_visible_play.extend([
                self._button_bg,
                self._button_f4,
                self._button_g4,
                self._button_a4,
                self._button_b4,
                self._button_c5,
                self._button_d5,
                self._button_e5,
                self._button_f5,
                self._button_g5,
                self._button_a5,
                self._button_b5,
                self._button_c6,
                self._button_f4sh,  
                self._button_g4sh,  
                self._button_a4sh,  
                self._button_c5sh,  
                self._button_d5sh,  
                self._button_f5sh,  
                self._button_g5sh,  
                self._button_a5sh 
            ])
        
        def event(self, ev, x, y, st):
            clicked_f4 = self._button_f4.event(ev, x, y, st)
            clicked_g4 = self._button_g4.event(ev, x, y, st)
            clicked_a4 = self._button_a4.event(ev, x, y, st)
            clicked_b4 = self._button_b4.event(ev, x, y, st)
            clicked_c5 = self._button_c5.event(ev, x, y, st)
            clicked_d5 = self._button_d5.event(ev, x, y, st)
            clicked_e5 = self._button_e5.event(ev, x, y, st)
            clicked_f5 = self._button_f5.event(ev, x, y, st)
            clicked_g5 = self._button_g5.event(ev, x, y, st)
            clicked_a5 = self._button_a5.event(ev, x, y, st)
            clicked_b5 = self._button_b5.event(ev, x, y, st)
            clicked_c6 = self._button_c6.event(ev, x, y, st)
            clicked_f4sh = self._button_f4sh.event(ev, x, y, st)
            clicked_g4sh = self._button_g4sh.event(ev, x, y, st)
            clicked_a4sh = self._button_a4sh.event(ev, x, y, st)
            clicked_c5sh = self._button_c5sh.event(ev, x, y, st)
            clicked_d5sh = self._button_d5sh.event(ev, x, y, st)
            clicked_f5sh = self._button_f5sh.event(ev, x, y, st)
            clicked_g5sh = self._button_g5sh.event(ev, x, y, st)
            clicked_a5sh = self._button_a5sh.event(ev, x, y, st)
            
            if clicked_f4 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.F4] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.F4)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.F4)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.F4)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.F4)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.F4)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.F4], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.F4, False):
                    
                    
                    self.pressed[mas_piano_keys.F4] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            if clicked_g4 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.G4] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.G4)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.G4)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.G4)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.G4)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.G4)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.G4], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.G4, False):
                    
                    
                    self.pressed[mas_piano_keys.G4] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            if clicked_a4 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.A4] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.A4)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.A4)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.A4)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.A4)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.A4)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.A4], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.A4, False):
                    
                    
                    self.pressed[mas_piano_keys.A4] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            if clicked_b4 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.B4] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.B4)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.B4)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.B4)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.B4)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.B4)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.B4], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.B4, False):
                    
                    
                    self.pressed[mas_piano_keys.B4] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            if clicked_c5 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.C5] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.C5)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.C5)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.C5)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.C5)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.C5)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.C5], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.C5, False):
                    
                    
                    self.pressed[mas_piano_keys.C5] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            if clicked_d5 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.D5] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.D5)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.D5)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.D5)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.D5)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.D5)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.D5], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.D5, False):
                    
                    
                    self.pressed[mas_piano_keys.D5] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            if clicked_e5 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.E5] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.E5)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.E5)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.E5)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.E5)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.E5)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.E5], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.E5, False):
                    
                    
                    self.pressed[mas_piano_keys.E5] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            if clicked_f5 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.F5] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.F5)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.F5)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.F5)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.F5)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.F5)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.F5], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.F5, False):
                    
                    
                    self.pressed[mas_piano_keys.F5] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            if clicked_g5 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.G5] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.G5)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.G5)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.G5)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.G5)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.G5)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.G5], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.G5, False):
                    
                    
                    self.pressed[mas_piano_keys.G5] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            if clicked_a5 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.A5] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.A5)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.A5)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.A5)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.A5)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.A5)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.A5], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.A5, False):
                    
                    
                    self.pressed[mas_piano_keys.A5] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            if clicked_b5 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.B5] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.B5)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.B5)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.B5)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.B5)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.B5)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.B5], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.B5, False):
                    
                    
                    self.pressed[mas_piano_keys.B5] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            
            if clicked_c6 is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.C6] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.C6)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.C6)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.C6)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.C6)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.C6)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.C6], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.C6, False):
                    
                    
                    self.pressed[mas_piano_keys.C6] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            if clicked_f4sh is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.F4SH] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.F4SH)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.F4SH)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.F4SH)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.F4SH)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.F4SH)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.F4SH], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.F4SH, False):
                    
                    
                    self.pressed[mas_piano_keys.F4SH] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            if clicked_g4sh is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.G4SH] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.G4SH)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.G4SH)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.G4SH)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.G4SH)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.G4SH)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.G4SH], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.G4SH, False):
                    
                    
                    self.pressed[mas_piano_keys.G4SH] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            if clicked_a4sh is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.A4SH] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.A4SH)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.A4SH)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.A4SH)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.A4SH)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.A4SH)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.A4SH], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.A4SH, False):
                    
                    
                    self.pressed[mas_piano_keys.A4SH] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            if clicked_c5sh is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.C5SH] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.C5SH)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.C5SH)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.C5SH)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.C5SH)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.C5SH)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.C5SH], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.C5SH, False):
                    
                    
                    self.pressed[mas_piano_keys.C5SH] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            if clicked_d5sh is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.D5SH] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.D5SH)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.D5SH)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.D5SH)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.D5SH)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.D5SH)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.D5SH], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.D5SH, False):
                    
                    
                    self.pressed[mas_piano_keys.D5SH] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            if clicked_f5sh is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.F5SH] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.F5SH)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.F5SH)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.F5SH)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.F5SH)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.F5SH)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.F5SH], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.F5SH, False):
                    
                    
                    self.pressed[mas_piano_keys.F5SH] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            if clicked_g5sh is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.G5SH] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.G5SH)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.G5SH)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.G5SH)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.G5SH)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.G5SH)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.G5SH], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.G5SH, False):
                    
                    
                    self.pressed[mas_piano_keys.G5SH] = False
                    
                    
                    
                    renpy.redraw(self, 0)
            
            if clicked_a5sh is not None:
                if self.state == self.STATE_CONFIG_CHANGE:         
                    new_key, old_key = mas_piano_keys._setKeymap(
                        self._sel_ovl.return_value,
                        ev.key
                    )   
                    self.state = self.STATE_CONFIG_WAIT
                    self._button_done.enable()
                    self._button_cancel.disable()
                    self._button_reset.disable()
                    self.pressed[self._sel_ovl.return_value] = False
                    self._initKeymap()  
                    if len(persistent._mas_piano_keymaps) > 0:
                        self._button_resetall.enable()
                    else:
                        self._button_resetall.disable()
                    
                    
                    if old_key in self._keymap_overlays:
                        self._keymap_overlays.pop(old_key)
                    if new_key:
                        self._keymap_overlays[new_key] = (
                            self._buildKeyTextOverlay(new_key)
                        )
                    
                    renpy.play(
                        self.pkeys[self._sel_ovl.return_value],
                        channel="audio"
                    )
                    
                    renpy.redraw(self, 0)
                else:
                    if self.state not in self.CONFIG_STATES:
                        
                        
                        if len(self.played) > self.KEY_LIMIT:
                            self.played = list()
                        
                        
                        elif st-self.prev_time >= self.ev_timeout:
                            self._timeoutFlow()
                        
                        
                        self.prev_time = st
                        self.pressed[mas_piano_keys.A5SH] = True
                        if self.state not in self.CONFIG_STATES:
                            
                            
                            self.note_hit = True
                            
                            
                            self.played.append(mas_piano_keys.A5SH)
                            
                            
                            if self.state == self.STATE_LISTEN:
                                self.stateListen(ev, mas_piano_keys.A5SH)
                            
                            
                            elif self.state in self.POST_STATES:
                                self.statePost(ev, mas_piano_keys.A5SH)
                            
                            
                            elif self.state in self.TRANS_POST_STATES:
                                self.stateWaitPost(ev, mas_piano_keys.A5SH)
                            
                            
                            elif self.state in self.MATCH_STATES:
                                self.stateMatch(ev, mas_piano_keys.A5SH)
                        
                        
                        renpy.play(self.pkeys[mas_piano_keys.A5SH], channel="audio")
                        
                        
                        
                        renpy.redraw(self, 0)                                                                                           
            
            else:
                if self.pressed.get(mas_piano_keys.A5SH, False):
                    
                    
                    self.pressed[mas_piano_keys.A5SH] = False
                    
                    
                    
                    renpy.redraw(self, 0)

            clicked_quit = self._button_quit.event(ev, x, y, st)

            # check for config/quit
            if clicked_quit is not None:
                return self.quitflow()
            super(MobilePianoDisplayable, self).event(ev, x, y, st)

            
            
    PianoDisplayable = MobilePianoDisplayable
