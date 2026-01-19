---
icon: sidebar
---

# General View

The General view is the fastest way to confirm that your SPX Server is up and that your simulation is doing what you think it is doing.

<figure><img src="../.gitbook/assets/Zrzut ekranu 2026-01-19 o 10.51.51.png" alt=""><figcaption></figcaption></figure>

#### Typical workflow (Installer → UI sanity check)

{% stepper %}
{% step %}
### Install and start a pack


{% endstep %}

{% step %}
### Open the UI

Go to http://localhost:3000. You should see the Instances list (active running instances).

<figure><img src="../.gitbook/assets/Zrzut ekranu 2026-01-19 o 10.47.24.png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Confirm the server is working

Open any instance from the list (for example Vaisala WXT530):

the instance should show as running/active,

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

Logs should not contain errors.

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### Validate the simulation react

Go to the Scenarios tab and run a weather-related scenario (e.g., “change weather”).

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
### SPX Server connectivity is OK, the simulation is running, and scenarios are applied successfully.
{% endstep %}
{% endstepper %}

#### What to keep in mind

* Use the UI for interactive inspection and debugging (instances, charts, scenarios, logs).
* Use MiL tests as the authoritative regression suite. If a value “does not change” in tests, verify your test/client is advancing time deterministically (step time + run loop) before debugging the UI.
