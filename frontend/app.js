const fileInput = document.getElementById("fileInput");
const uploadButton = document.getElementById("uploadButton");
const uploadZone = document.getElementById("uploadZone");

const processingPanel = document.getElementById("processingPanel");
const processingPercent = document.getElementById("processingPercent");
const processingStatus = document.getElementById("processingStatus");

const results = document.getElementById("results");

const originalAudio = document.getElementById("originalAudio");
const masteredAudio = document.getElementById("masteredAudio");

const originalName = document.getElementById("originalName");
const downloadButton = document.getElementById("downloadButton");

let selectedPreset = "balanced";


/* =====================================
   CURSOR EFFECT
===================================== */

const glow = document.querySelector(".cursor-glow");

document.addEventListener("mousemove", (event) => {

    glow.animate(
        {
            left: `${event.clientX}px`,
            top: `${event.clientY}px`
        },
        {
            duration: 700,
            fill: "forwards"
        }
    );

});


/* =====================================
   PRESETS
===================================== */

document.querySelectorAll(".preset").forEach((button) => {

    button.addEventListener("click", () => {

        document.querySelectorAll(".preset")
            .forEach(btn => btn.classList.remove("active"));

        button.classList.add("active");

        selectedPreset =
            button.dataset.preset;

    });

});


/* =====================================
   UPLOAD BUTTON
===================================== */

uploadButton.addEventListener("click", () => {

    fileInput.click();

});


/* =====================================
   FILE SELECTED
===================================== */

fileInput.addEventListener("change", () => {

    if (fileInput.files.length > 0) {

        handleFile(fileInput.files[0]);

    }

});


/* =====================================
   DRAG & DROP
===================================== */

uploadZone.addEventListener("dragover", (event) => {

    event.preventDefault();

    uploadZone.classList.add("dragging");

});


uploadZone.addEventListener("dragleave", () => {

    uploadZone.classList.remove("dragging");

});


uploadZone.addEventListener("drop", (event) => {

    event.preventDefault();

    uploadZone.classList.remove("dragging");

    const file = event.dataTransfer.files[0];

    if (file) {

        handleFile(file);

    }

});


/* =====================================
   MASTER TRACK
===================================== */

async function handleFile(file) {

    const allowed = [
        "audio/wav",
        "audio/x-wav",
        "audio/mpeg",
        "audio/flac",
        "audio/ogg",
        "audio/mp4"
    ];

    const extension =
        file.name.split(".").pop().toLowerCase();

    const allowedExtensions = [
        "wav",
        "mp3",
        "flac",
        "ogg",
        "m4a"
    ];

    if (!allowed.includes(file.type) &&
        !allowedExtensions.includes(extension)) {

        alert(
            "Please upload WAV, MP3, FLAC, OGG or M4A."
        );

        return;

    }


    /* ORIGINAL AUDIO */

    originalAudio.src =
        URL.createObjectURL(file);

    originalName.textContent =
        file.name;


    /* RESET */

    results.classList.remove("show");

    processingPanel.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });


    /* PROCESSING */

    processingStatus.textContent =
        "ANALYZING";

    let percent = 0;

    const progress = setInterval(() => {

        percent += Math.random() * 8;

        if (percent > 92) {
            percent = 92;
        }

        processingPercent.textContent =
            Math.floor(percent)
                .toString()
                .padStart(2, "0");

    }, 180);


    try {

        const formData = new FormData();

        formData.append("file", file);
        formData.append("preset", selectedPreset);


        processingStatus.textContent =
            "MASTERING";


        const response =
            await fetch("/master", {

                method: "POST",

                body: formData

            });


        const data =
            await response.json();


        clearInterval(progress);


        if (!data.success) {

            throw new Error(
                data.error ||
                "Mastering failed."
            );

        }


        /* COMPLETE */

        processingPercent.textContent =
            "100";

        processingStatus.textContent =
            "COMPLETE";


        /* AUDIO */

        const originalUrl =
            data.original_url;

        const masteredUrl =
            data.mastered_url;


        originalAudio.src =
            originalUrl;

        masteredAudio.src =
            masteredUrl;


        downloadButton.href =
            masteredUrl;


        /* RESULTS */

        setTimeout(() => {

            results.classList.add("show");

            results.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });

        }, 700);


    } catch (error) {

        clearInterval(progress);

        processingStatus.textContent =
            "ERROR";

        alert(
            "Mastering failed: " +
            error.message
        );

    }

}


/* =====================================
   PARTICLE BACKGROUND
===================================== */

const canvas =
    document.getElementById("particles");

const ctx =
    canvas.getContext("2d");

let particles = [];

function resizeCanvas() {

    canvas.width =
        window.innerWidth;

    canvas.height =
        window.innerHeight;

}

resizeCanvas();

window.addEventListener(
    "resize",
    resizeCanvas
);


for (let i = 0; i < 90; i++) {

    particles.push({

        x: Math.random() *
            window.innerWidth,

        y: Math.random() *
            window.innerHeight,

        size:
            Math.random() * 1.5 + .3,

        speed:
            Math.random() * .25 + .05,

        opacity:
            Math.random() * .5 + .1

    });

}


function animateParticles() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    particles.forEach(p => {

        p.y -= p.speed;


        if (p.y < 0) {

            p.y =
                canvas.height;

        }


        ctx.beginPath();

        ctx.arc(
            p.x,
            p.y,
            p.size,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            `rgba(167,139,250,${p.opacity})`;

        ctx.fill();

    });


    requestAnimationFrame(
        animateParticles
    );

}

animateParticles();