import pygame
from melo.api import TTS
import numpy as np

def load_tts_model():
    device = 'auto'
    model = TTS(language='EN', device=device)
    return model

import pygame
import numpy as np

def run_hinabot(model, text):
    # Initialize pygame mixer
    pygame.mixer.init(frequency=model.hps.data.sampling_rate, size=-16, channels=1)

    try:
        # Generate speech and get audio as a NumPy array (in-memory)
        audio_data = model.tts_to_file(text, model.hps.data.spk2id['EN-US'],quiet=True,speed=1)
        
        # Convert NumPy array to an integer format that pygame can play
        audio_data_int16 = (audio_data * 32767).astype(np.int16)
        
        # Reshape the audio data to be 2D for pygame (n_samples, 1) for mono
        audio_data_int16 = np.array([np.array([item,item]) for item in audio_data_int16])
        
        # Convert the NumPy array into a playable sound object
        sound = pygame.sndarray.make_sound(audio_data_int16)

        # Play the sound
        sound.play()

        # Wait for playback to finish
        while pygame.mixer.get_busy():
            pygame.time.Clock().tick(10)

    finally:
        # Clean up pygame mixer after playback
        pygame.mixer.quit()

# speech_model = load_tts_model()
