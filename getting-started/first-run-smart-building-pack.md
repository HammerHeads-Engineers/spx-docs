---
description: >-
  First-run UI walkthrough after installing the Smart Building Pack with the
  spx-examples installer.
---

# Smart Building Pack: First Run Walkthrough

This walkthrough assumes you used the Installer and selected the Smart Building Pack. After starting the generated stack, open the UI at http://localhost:3000.

Learn the UI structure here: [UI Overview](../ui-reference/general-view.md).

<figure><img src="../.gitbook/assets/Zrzut ekranu 2026-01-19 o 10.51.51.png" alt=""><figcaption></figcaption></figure>

## Walkthrough

1.  Open the UI at http://localhost:3000 and confirm you see the Instances list (active running instances).

    <figure><img src="../.gitbook/assets/Zrzut ekranu 2026-01-19 o 10.47.24.png" alt=""><figcaption></figcaption></figure>
2.  Open an instance from the list (example: Vaisala WXT530). Confirm the instance shows as running/active.

    <figure><img src="../.gitbook/assets/image (16).png" alt=""><figcaption></figcaption></figure>
3.  Open the Logger tab and confirm there are no errors.

    <figure><img src="../.gitbook/assets/image (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>
4.  Run a weather-related scenario (for example "change weather") and confirm chart/values update immediately.

    <figure><img src="../.gitbook/assets/image (3) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

## Pass criteria

* UI loads at http://localhost:3000 and shows the Instances list.
* Selected instance opens and shows as active.
* Logger shows no errors during the check.
* Scenario change updates values immediately.

## If something fails

* See [Common Issues and Solutions](../troubleshooting-and-support/common-issues-and-solutions.md).
* Use [How to Get Support](../troubleshooting-and-support/how-to-get-support.md) to collect logs and contact the team.
