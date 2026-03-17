# AutoEIT Transcription System

## Why this exists

This project started from a very simple observation:

> Transcribing learner speech manually takes too much time.

At first, it sounded like a normal speech-to-text problem.
But once I looked deeper into the data (non-native speakers doing Elicited Imitation Tasks), I realized something important:

**This is not normal speech.**

The audio contains:

* strong accents
* mispronunciations
* incomplete sentences
* inconsistent pacing
* sometimes even mixed languages

Most existing ASR systems are trained on clean, native speech.
So when applied here, they fail in subtle but critical ways.

---

## Initial approach (and why it wasn’t enough)

My first instinct was straightforward:

> Use a pretrained model like Whisper and transcribe the audio.

This worked… but only to an extent.

Problems I observed:

* background noise affected output more than expected
* strong accents caused incorrect word predictions
* fast speakers merged words into one
* slow speakers created unnatural pauses
* learner errors were transcribed literally, even when clearly unintended

At this point, it became clear:

> A single model is not enough.

---

## Key realization

Instead of treating this as “just ASR”, I reframed the problem as:

> **A pipeline that gradually reduces noise (audio + linguistic) at multiple levels**

This led to the current architecture.

---

## System Design

The system is built as a multi-stage pipeline:

```
Audio → Preprocessing → ASR → Post-processing → Final Transcript
```

Each stage exists because of a specific failure I encountered.

---

## 1. Audio Preprocessing

### Problem

Raw audio is inconsistent:

* background noise
* varying volume levels
* long silences
* overlapping sounds

### Solution

A preprocessing layer that:

* reduces noise
* normalizes volume
* segments useful speech
* optionally augments data (speed/pitch variations)

### Why this matters

Even a strong ASR model performs poorly on low-quality input.
Cleaning audio gave noticeable improvements before any model changes.

---

## 2. Base ASR Model

### Problem

Building a model from scratch is unrealistic and unnecessary.

### Solution

Use pretrained models like:

* Whisper
* Wav2Vec2

These provide a strong starting point.

---

## 3. Fine-tuning for Learner Speech

### Problem

Pretrained models assume:

* correct pronunciation
* fluent sentence structure

Learner speech violates both.

### Solution

Fine-tune the ASR model on:

* non-native speech data
* varied accents
* imperfect sentence constructions

### Insight

Instead of explicitly handling accents, the model learns patterns from exposure.

---

## 4. Handling Variability in Speech

### Observations

* Some speakers talk extremely fast → words merge
* Some speak slowly → unnatural segmentation
* Some invent or distort words

### Approach

Rather than hardcoding rules:

* rely on model robustness
* support it through augmentation during training

---

## 5. Multilingual and Mixed Language Handling

### Problem

Learners sometimes mix languages:

* insert native words
* partially translate sentences

### Solution

* use multilingual ASR models
* apply post-processing where needed

This is not fully solved yet, but the system is designed to support it.

---

## 6. Post-processing Layer (Critical Component)

### Problem

Even after ASR, outputs are not reliable enough:

* grammatical inconsistencies
* predictable learner mistakes
* partially correct sentences

### Solution

A post-processing pipeline that:

* cleans text
* applies grammar correction
* fixes common transcription errors

### Key Insight

This stage often improves results more than model tuning alone.

---

## 7. Evaluation

### Goal

Reach transcription quality close to human annotators.

### Metrics used:

* Word Error Rate (WER)
* Character Error Rate (CER)

### Target

~90% agreement with human transcription

---

## Project Structure Philosophy

This project is intentionally modular.

Each component (preprocessing, model, post-processing) is isolated so that:

* improvements can be made independently
* experiments can be run easily
* components can be swapped without breaking the system

---

## What this project is really about

At a surface level:

> Converting audio to text.

At a deeper level:

> Making AI handle imperfect, real-world human input.

---

## Current State

* Basic pipeline structure implemented
* Preprocessing modules in place
* ASR baseline integrated
* Post-processing under active development

---

## Future Work

* better fine-tuning with learner-specific datasets
* stronger post-processing models
* improved multilingual handling
* benchmarking across different proficiency levels

---

## Final Thought

This project evolved from a simple idea into a layered system because:

> Real-world data is messy, and simple solutions don’t hold up.

Instead of forcing a single model to solve everything,
this approach distributes the problem across multiple stages —
each designed to handle a specific type of imperfection.

---
