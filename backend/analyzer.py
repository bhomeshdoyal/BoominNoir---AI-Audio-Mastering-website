import librosa
import numpy as np
import pyloudnorm as pyln


def analyze_audio(file_path):

    # Load audio
    audio, sr = librosa.load(
        file_path,
        sr=None,
        mono=False
    )

    # Convert stereo to mono for analysis
    if audio.ndim == 1:
        mono = audio
    else:
        mono = np.mean(audio, axis=0)

    # Duration
    duration = len(mono) / sr

    # RMS
    rms = np.sqrt(
        np.mean(mono ** 2)
    )

    if rms > 0:
        rms_db = 20 * np.log10(rms)
    else:
        rms_db = -100

    # Peak
    peak = np.max(
        np.abs(mono)
    )

    if peak > 0:
        peak_db = 20 * np.log10(peak)
    else:
        peak_db = -100

    # LUFS
    meter = pyln.Meter(sr)

    try:
        loudness = meter.integrated_loudness(
            mono
        )
    except Exception:
        loudness = -70

    # Frequency analysis
    spectral_centroid = librosa.feature.spectral_centroid(
        y=mono,
        sr=sr
    )

    centroid = float(
        np.mean(spectral_centroid)
    )

    return {

        "sample_rate": sr,

        "duration": round(
            duration,
            2
        ),

        "rms_db": round(
            float(rms_db),
            2
        ),

        "peak_db": round(
            float(peak_db),
            2
        ),

        "lufs": round(
            float(loudness),
            2
        ),

        "spectral_centroid": round(
            centroid,
            2
        )
    }