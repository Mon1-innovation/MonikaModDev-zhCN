init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_chess_moves_test",
            category=["dev"],
            prompt="CHESS SPECIAL MOVES AND PROMOTIONS",
            pool=True,
            unlocked=True
        )
    )

label dev_chess_moves_test:

    m 1eua "What do you want to test?{nw}"
    $ _history_list.pop()
    menu:
        m "What do you want to test?{fast}"

        "White promotion.{#dev_chess_moves_test_1}":
            $ player_color = chess.WHITE
            $ starting_fen = "8/PPPPPPPP/8/8/8/8/8/k6K w - - 0 1"

        "Black promotion.{#dev_chess_moves_test_2}":
            $ player_color = chess.BLACK
            $ starting_fen = "k6K/8/8/8/8/8/pppppppp/8 w - - 0 1"

        "White castling.{#dev_chess_moves_test_3}":
            $ player_color = chess.WHITE
            $ starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1"

        "Black castling.{#dev_chess_moves_test_4}":
            $ player_color = chess.BLACK
            $ starting_fen = "r3k2r/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        "White en passant.{#dev_chess_moves_test_5}":
            $ player_color = chess.WHITE
            $ starting_fen = "8/8/8/3pP3/8/8/8/k6K w - d6 0 1"

        "Black en passant.{#dev_chess_moves_test_6}":
            $ player_color = chess.BLACK
            $ starting_fen = "k6K/8/8/8/3Pp3/8/5Pp1/8 b - d3 0 1"

        "White stalemate.{#dev_chess_moves_test_7}":
            $ player_color = chess.WHITE
            $ starting_fen = "k7/3Q4/8/3K4/8/8/8/8 w - - 0 1"

        "Black stalemate.{#dev_chess_moves_test_8}":
            $ player_color = chess.BLACK
            $ starting_fen = "8/8/8/8/3k4/8/3q4/K7 b - - 0 1"

    m "Casual rules?{nw}"
    $ _history_list.pop()
    menu:
        m "Casual rules?{fast}"

        "Yes.{#dev_chess_moves_test_9}":
            $ casual_rules = True

        "No.{#dev_chess_moves_test_10}":
            $ casual_rules = False


    python:
        chess_displayable_obj = MASChessDisplayable(is_player_white=player_color, starting_fen=starting_fen, practice_mode=True, casual_rules=casual_rules)
        chess_displayable_obj.show()
        results = chess_displayable_obj.game_loop()
        chess_displayable_obj.hide()

    m 1eua "Do you want to test anything else?{nw}"
    $ _history_list.pop()
    menu:
        m "Do you want to test anything else?{fast}"

        "Yes.{#dev_chess_moves_test_11}":
            jump dev_chess_moves_test

        "No.{#dev_chess_moves_test_12}":
            return
