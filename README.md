# 🧠 AutoEIT: Learner-Aware Transcription System

### A Multi-Layered, Intelligence-Driven Pipeline for Non-Native Speech

---

## 🚀 Overview

AutoEIT is a **learner-aware speech transcription and analysis system** designed for processing **non-native speaker audio** from Elicited Imitation Tasks (EIT).

Unlike traditional ASR systems optimized for clean, native speech, AutoEIT is built to handle:

* Accents and pronunciation variation
* Disfluencies and interruptions
* Code-switched (multilingual) speech
* Structurally inconsistent learner output

Beyond transcription, the system performs **multi-level linguistic analysis** to produce structured, interpretable, and research-ready outputs.

---

## 🎯 Core Idea

> Move from *“what was said”* → to → *“how it was said and how reliable it is”*

---

## ⚙️ System Architecture

### 🧩 Layered Pipeline Design

```
Audio Input
   ↓
Preprocessing Layer
   ↓
ASR Layer (Whisper)
   ↓
Intelligence Layer (Level 3)
   ↓
Refinement Layer (Level 3.5)
   ↓
Unified Output Layer
```

---

## 📁 Project Structure

```
speech-text/
├── preprocessing/
│   ├── audio_normalization.py
│   ├── noise_reduction.py
│   └── audio_enhancer.py
│
├── models/
│   └── base_asr/
│       └── whisper_model.py
│
├── analysis/
│   ├── speech_dynamics.py
│   ├── language_detection.py
│   ├── lexical_handler.py
│   ├── annotation_builder.py
│   ├── segment_quality.py
│   ├── phonetic_analyzer.py
│   ├── disfluency_detector.py
│   ├── quality_aggregator.py
│   └── unified_output_builder.py
│
├── pipeline/
│   └── full_pipeline.py
│
├── data/
│   └── sample.wav
│
├── main.py
├── validate_level3.py
├── validate_level35.py
├── validate_unified.py
├── requirements.txt
└── README.md
```

---

# 🧠 System Layers Explained

---

## 🔊 1. Preprocessing Layer

Handles real-world audio imperfections:

* Noise reduction (spectral gating)
* Volume normalization
* Audio validation and cleanup
* Robust handling of corrupted/silent inputs

---

## 📝 2. ASR Layer

* Whisper-based transcription
* Handles non-native speech variability
* Fallback-safe and validated outputs

---

## 🧠 3. Intelligence Layer (Level 3)

Adds linguistic awareness:

### 🎤 Speech Dynamics

* Duration, speech rate, pause detection

### 🌍 Language Detection

* Word-level multilingual identification
* Code-switch handling

### 🧩 Lexical Handling

* Slang detection
* Merged words
* Unknown token classification

### 🧾 Structured Annotation

* Word-level metadata
* Confidence scoring
* Research-ready JSON output

---

## 🚀 4. Refinement Layer (Level 3.5)

Adds deeper speech understanding:

---

### 🟩 Segment Quality Analysis

* Splits speech into segments
* Labels each as HIGH / MEDIUM / LOW
* Uses:

  * unknown word ratio
  * disfluency presence
  * language consistency

---

### 🔊 Phonetic Error Awareness

* Detects pronunciation-based variations
* Uses edit distance + phonetic heuristics
* Example:

  * *“bery” → “very”*
* Annotates errors without correction

---

### 🗣️ Disfluency Detection

* Identifies:

  * fillers (“uh”, “um”)
  * repetitions
  * restarts and corrections
* Tracks positions and patterns

---

## 🧩 5. Unified Output Layer (KEY FEATURE)

This is what makes the system feel *complete*.

### 🔥 Quality Aggregator

Combines:

* segment quality
* phonetic errors
* disfluencies

→ produces:

* overall quality score
* detected issues
* critical regions

---

### 📊 Unified Output Builder

Outputs a **single coherent structure**:

```json
{
  "transcription": "...",
  "speech_analysis": {...},
  "linguistic_analysis": {...},
  "quality_summary": {
    "overall_quality": "medium",
    "critical_regions": [...],
    "issues_detected": [...]
  }
}
```

---

# 🎯 Key Contributions

* ✅ Learner-aware transcription pipeline
* ✅ Multi-level linguistic analysis (word, segment, phonetic, fluency)
* ✅ Code-switch and multilingual handling
* ✅ Segment-level quality assessment
* ✅ Phonetic error detection without correction
* ✅ Disfluency-aware speech modeling
* ✅ Unified reliability-aware output
* ✅ Fully robust, fault-tolerant system

---

# 🧠 Design Philosophy

1. **Preserve learner behavior**
   → No forced correction

2. **Model speech, not just text**
   → Capture production patterns

3. **Enable evaluation readiness**
   → Structured and interpretable outputs

---

# 🔮 Applications

* EIT transcription pipelines
* Language learning research
* Fluency and pronunciation analysis
* Code-switching studies
* Curriculum and assessment design
* Preprocessing for automated scoring systems

---

# 🛠️ Tech Stack

* Python
* PyTorch
* Whisper
* Librosa
* NumPy

---

# ▶️ Usage

```bash
pip install -r requirements.txt
python main.py
```

---

# 🛡️ Robustness & Validation

Validation scripts:

* `validate_level3.py`
* `validate_level35.py`
* `validate_unified.py`

System handles:

* missing files
* corrupted audio
* silent inputs
* invalid data
* model failures

👉 Always fails gracefully

---

# 📈 Future Work

* ASR fine-tuning on learner datasets
* Integration with automated scoring systems
* Real-time streaming support
* Expanded multilingual capabilities

---

# 🎯 Final Statement

AutoEIT is not just a transcription system.

It is a **multi-layered, learner-aware linguistic analysis pipeline** that transforms raw speech into structured, reliable, and evaluation-ready data.


