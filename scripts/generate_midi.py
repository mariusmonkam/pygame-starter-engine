import mido
import os

def generate_sound_files():
    # Generate shoot sound
    if not os.path.exists('effects/shoot_sound.mid'):
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)

        # Create a short note for the shoot sound
        track.append(mido.Message('note_on', note=72, velocity=127, time=0))
        track.append(mido.Message('note_off', note=72, velocity=127, time=120))

        mid.save('effects/shoot_sound.mid')

    # Generate collision sound
    if not os.path.exists('effects/collision_sound.mid'):
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)

        # Create a short note for the collision sound
        track.append(mido.Message('note_on', note=36, velocity=127, time=0))
        track.append(mido.Message('note_off', note=36, velocity=127, time=120))

        mid.save('effects/collision_sound.mid')
