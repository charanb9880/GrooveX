import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from playback_history.playback_controller import PlaybackController


def test_auto_replay():
    ctrl = PlaybackController()

    # Add calming songs
    ctrl.play_song("LoFi Beats", "Calm Artist", 180, genre="Lo-Fi")
    ctrl.play_song("Jazz Night", "Smooth Band", 200, genre="Jazz")
    ctrl.play_song("Ambient Sky", "Chill Guy", 210, genre="Ambient")

    # Add non-calming songs
    ctrl.play_song("Rock Fire", "Loud Band", 220, genre="Rock")
    ctrl.play_song("Pop Star", "Star", 230, genre="Pop")

    print("=== Playing full playlist ===")
    while True:
        s = ctrl.play_next()
        if not s:
            break
        print(f"Played: {s.title} | Genre: {s.genre} | Plays: {s.play_count}")

    print("\n=== Playlist AFTER auto replay triggered ===")
    for s in ctrl.get_playlist_songs():
        print(f"Replay Song: {s.title} ({s.genre}) - Plays: {s.play_count}")


if __name__ == "__main__":
    test_auto_replay()
