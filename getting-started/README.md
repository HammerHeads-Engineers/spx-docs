---
description: Get up and running with the SPX simulation stack.
icon: flag-checkered
layout:
  width: default
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# Getting Started

This page helps you get up and running with the SPX simulation stack—the SPX Server (REST API for modeling & simulation) and the SPX-Python client (lightweight Python wrapper for that API). You’ll learn how to install the essentials, bring the server up locally with Docker, connect from Python, and perform the core operations you’ll use in day-to-day development and CI.

By the end, you will be able to:

* Start the SPX Server locally via Docker and verify it’s healthy.
* Initialize the SPX-Python client and talk to the server.
* Create models and instances, read/write attributes, and run a basic simulation step.
* Reuse the same flow in unit tests and CI pipelines.

What’s inside this page:

* **Installation Guide** — download the installer from `simplephysx.com/keys`, extract the Windows/Linux delivery archive if needed, complete the native install, run `SPX Setup`, and verify UI/API on localhost.
* **Advanced: Manual Docker Compose** — run the SPX Server API via Compose without the wizard (server-only).
* **Quick Start Guide** — minimal, copy-paste recipes to connect to the server, do basic CRUD on models/instances, tweak attributes, run prepare()/run(), and wire these steps into your unit tests and CI.

**Who is this for?**

Developers, QA, and CI engineers who want a clear, repeatable path to stand up SPX locally and automate it in tests.

Prerequisites (at a glance):

* Docker & Docker Compose (to run the server)
* macOS/Linux: Python `>=3.9`; Windows installer can install Python automatically
* A valid `SPX_PRODUCT_KEY`
* Network access to pull Docker images and install Python dependencies

> Tip: Everything shown here is designed to work the same way locally and in CI, so the commands you practice on your laptop carry straight over to pipelines.
