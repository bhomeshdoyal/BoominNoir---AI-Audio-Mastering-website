from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import os
import uuid

from analyzer import analyze_audio
from mastering import master_audio


# ============================================================
# BOOMINNOIR MASTERLAB STUDIO
# Audio Mastering API
# ============================================================

app = FastAPI(
    title="BoominNoir MASTERLAB STUDIO",
    description="Professional-style audio mastering engine by BoominNoir.",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PROJECT DIRECTORIES
# ============================================================

# Location of this file:
# AI-Mastering-Studio/backend/main.py

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# Project root:
# AI-Mastering-Studio/

PROJECT_DIR = os.path.dirname(BASE_DIR)


# Frontend
FRONTEND_DIR = os.path.join(
    PROJECT_DIR,
    "frontend"
)


# Audio folders
AUDIO_DIR = os.path.join(
    PROJECT_DIR,
    "audio"
)

UPLOAD_DIR = os.path.join(
    AUDIO_DIR,
    "uploads"
)

MASTERED_DIR = os.path.join(
    AUDIO_DIR,
    "mastered"
)


# ============================================================
# CREATE DIRECTORIES IF THEY DON'T EXIST
# ============================================================

os.makedirs(
    FRONTEND_DIR,
    exist_ok=True
)

os.makedirs(
    AUDIO_DIR,
    exist_ok=True
)

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

os.makedirs(
    MASTERED_DIR,
    exist_ok=True
)


# ============================================================
# STATIC AUDIO FILES
# ============================================================

app.mount(
    "/audio",
    StaticFiles(
        directory=AUDIO_DIR
    ),
    name="audio"
)


# ============================================================
# FRONTEND STATIC FILES
# ============================================================

# This makes:
#
# /static/style.css
# /static/app.js
#
# available to the website.

app.mount(
    "/static",
    StaticFiles(
        directory=FRONTEND_DIR
    ),
    name="static"
)


# ============================================================
# WEBSITE HOME PAGE
# ============================================================

@app.get("/")
def home():

    index_file = os.path.join(
        FRONTEND_DIR,
        "index.html"
    )

    return FileResponse(
        index_file
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "online",
        "service": "BoominNoir MASTERLAB STUDIO",
        "version": "1.0.0"
    }


# ============================================================
# MASTER AUDIO
# ============================================================

@app.post("/master")
async def master_track(
    file: UploadFile = File(...),
    preset: str = Form("balanced")
):

    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    if not file.filename:

        return {
            "success": False,
            "error": "No file selected."
        }


    # --------------------------------------------------------
    # ALLOWED AUDIO FORMATS
    # --------------------------------------------------------

    allowed_extensions = {
        ".wav",
        ".mp3",
        ".flac",
        ".ogg",
        ".m4a"
    }

    original_extension = os.path.splitext(
        file.filename
    )[1].lower()


    if original_extension not in allowed_extensions:

        return {
            "success": False,
            "error": (
                "Unsupported audio format. "
                "Use WAV, MP3, FLAC, OGG or M4A."
            )
        }


    # --------------------------------------------------------
    # ALLOWED MASTERING PRESETS
    # --------------------------------------------------------

    allowed_presets = {
        "balanced",
        "clean",
        "loud",
        "club",
        "dark"
    }


    if preset not in allowed_presets:

        preset = "balanced"


    # --------------------------------------------------------
    # CREATE UNIQUE FILE ID
    # --------------------------------------------------------

    file_id = str(
        uuid.uuid4()
    )


    # --------------------------------------------------------
    # FILE NAMES
    # --------------------------------------------------------

    input_filename = (
        file_id +
        original_extension
    )

    output_filename = (
        file_id +
        "_mastered.wav"
    )


    # --------------------------------------------------------
    # FILE PATHS
    # --------------------------------------------------------

    input_path = os.path.join(
        UPLOAD_DIR,
        input_filename
    )

    output_path = os.path.join(
        MASTERED_DIR,
        output_filename
    )


    try:

        # ====================================================
        # SAVE UPLOADED AUDIO
        # ====================================================

        file_data = await file.read()


        with open(
            input_path,
            "wb"
        ) as audio_file:

            audio_file.write(
                file_data
            )


        # ====================================================
        # ANALYZE ORIGINAL TRACK
        # ====================================================

        analysis_before = analyze_audio(
            input_path
        )


        # ====================================================
        # MASTER AUDIO
        # ====================================================

        master_audio(
            input_path,
            output_path,
            preset
        )


        # ====================================================
        # ANALYZE MASTERED TRACK
        # ====================================================

        analysis_after = analyze_audio(
            output_path
        )


        # ====================================================
        # RETURN RESULT
        # ====================================================

        return {

            "success": True,

            "message":
                "Track mastered successfully.",

            "preset":
                preset,

            "original":
                analysis_before,

            "mastered":
                analysis_after,

            "original_url":
                "/audio/uploads/" +
                input_filename,

            "mastered_url":
                "/audio/mastered/" +
                output_filename
        }


    except Exception as error:

        # ----------------------------------------------------
        # PRINT ERROR TO TERMINAL
        # ----------------------------------------------------

        print(
            "=========================================="
        )

        print(
            "MASTERING ERROR:"
        )

        print(
            str(error)
        )

        print(
            "=========================================="
        )


        return {

            "success": False,

            "error":
                str(error)
        }


# ============================================================
# STARTUP MESSAGE
# ============================================================

@app.on_event("startup")
async def startup_event():

    print("")
    print("=" * 60)
    print("")
    print("        BOOMINNOIR MASTERLAB STUDIO")
    print("")
    print("        AUDIO MASTERING ENGINE")
    print("")
    print("        © 2026 Bhomesh Doyal / BoominNoir")
    print("        All rights reserved.")
    print("")
    print("=" * 60)
    print("")
    print("Website:")
    print("http://127.0.0.1:8000/")
    print("")
    print("API Docs:")
    print("http://127.0.0.1:8000/docs")
    print("")
    print("Health:")
    print("http://127.0.0.1:8000/health")
    print("")
    print("=" * 60)
    print("")