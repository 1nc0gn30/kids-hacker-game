# KidGame3 Storyline

## Purpose

This file is the story and tone reference for the whole project.
Future scenes should follow this document unless we intentionally revise canon.

The goal is to let kids feel like they are working through a real security incident while still making enough visual sense to an adult who knows what terminals, mail clients, packet captures, and malware warnings look like.

## Core fantasy

The player is not a fantasy hacker.
The player is a young but capable incident responder inside a home lab / desktop environment that starts behaving like it is under real attack.

The fantasy is:

- "I can read the signals before the machine collapses."
- "My typing helps me move through real-looking tools."
- "I am tracing a breach, not casting spells."

## Non-negotiable tone rules

- No supernatural hacking.
- No impossible UI magic.
- No fake neon nonsense that breaks credibility.
- No giant exposition dumps during play.
- No visible scoreboards, XP, combo meters, WPM meters, or typed-key counters on screen.
- Pressure should come from motion, warnings, bad system states, and the feeling that the machine is getting less trustworthy.
- Every scene should look like a screen a real person might plausibly see.

## Audience rules

- A kid should understand the immediate objective from the screen language alone.
- An adult should recognize the tools, labels, and workflow as grounded enough to feel intentional.
- The game can feel tense and noisy, but it should not become grotesque or absurd.

## Story pillars

- The threat begins locally and ambiguously.
- The player learns by observing the machine, not by hearing lectures.
- The attack feels bigger over time, but every escalation must still have a believable technical cause.
- The player mostly advances by typing naturally.
- Special key combinations are rare and used only for memorable milestone actions.
- Each scene should end with a stronger question than it started with.

## Canon setting

- Primary machine: Parrot OS desktop / home-lab workstation.
- Environment: local desktop, mail client, loopback traffic, browser/admin panels, logs, packet views, and incident-response style tools.
- Threat style: mail relay abuse, local persistence, hidden forwarding, deceptive loopback traffic, credential exposure, and service misconfiguration.
- Villain style: taunting is allowed in small doses, but the adversary should feel like a real intruder, not a comic-book mastermind.

## Player role

The player is effectively a junior defender working alone at first.
They are fast enough to react, but not so powerful that they instantly control the whole situation.

This matters because the scenes should emphasize:

- triage
- observation
- narrowing uncertainty
- containment
- recovery

It should not emphasize:

- cinematic offensive hacking
- magical instant exploits
- implausible access to everything

## Main story arc

The full game follows one incident from first warning to cleanup.

### Section 1: The Machine Stops Feeling Safe

This section is about noticing that the local desktop is lying to the player.
The machine still works, but too many surfaces start telling the same story.

Section outcome:
The player confirms that the threat is not just a weird email. The host is already compromised and local traffic is part of the story.

### Section 2: The Threat Has a Route

This section is about discovering how the malicious activity moves through services and where trust is breaking down.

Section outcome:
The player identifies the relay path, suspicious services, and the first containment targets.

### Section 3: Trust Is Broken

This section is about credentials, persistence, and fake legitimacy.
The intruder is not only present. They are hiding inside normal behavior.

Section outcome:
The player identifies the persistence method and understands which accounts or services can no longer be trusted.

### Section 4: Containment Without Panic

This section is about isolation and careful response.
The player starts containing the incident without shutting the whole machine down blindly.

Section outcome:
The player limits the blast radius and preserves enough evidence to continue.

### Section 5: The Adversary Pushes Back

This section is about the threat reacting.
Popups, service failures, strange reconnects, and misleading local behavior become more aggressive.

Section outcome:
The player proves the intruder is still active and adapts the response.

### Section 6: Follow The Data

This section is about logs, packet evidence, and timeline reconstruction.

Section outcome:
The player understands what happened first, what spread next, and what was just noise.

### Section 7: Regain Control

This section is about turning partial knowledge into stable system control.

Section outcome:
The player regains admin-level confidence over the machine and begins removing footholds.

### Section 8: Clean Rebuild Decisions

This section is about whether to repair in place or rebuild trust from a cleaner state.

Section outcome:
The player makes realistic recovery decisions and separates salvageable data from unsafe state.

### Section 9: Recovery

This section is about restoring normal operation carefully.

Section outcome:
The machine becomes usable again, but only after verification and trust checks.

### Section 10: Aftermath

This section is about proving the incident is over and understanding what changed.

Section outcome:
The player closes the case, documents what happened, and leaves with a stronger sense of how real systems fail.

## Section 1 detailed scene plan

Section 1 should have 10 scenes.
The current build already covers Scene 1 and starts Scene 2.

### Scene 01: Desktop Breach Intro

Current role:
The desktop starts normal enough, then a warning email and malware-style intrusion signal appear.

Player feeling:
"Something is wrong, and my own machine is telling on itself."

Beat outcome:
The player opens the first visible thread of evidence.

### Scene 02: Loopback Capture Review

Current role:
The player reviews local traffic and learns that the warning email is tied to suspicious loopback behavior.

Player feeling:
"This is not just a message. The machine is routing hostile behavior internally."

Beat outcome:
The player confirms the relay path is part of the breach.

### Scene 03: Mail Relay Triage

Planned role:
The player inspects mail queue / relay behavior and sees hidden forwarding, malformed headers, or suspicious local delivery events.

Player feeling:
"The inbox is only one symptom. Mail flow itself is compromised."

Beat outcome:
The player identifies the mail relay as an active part of the incident.

### Scene 04: Browser Admin Glimpse

Planned role:
The player opens a real-looking admin or diagnostics page and sees misconfiguration, bad certificates, or a suspicious rule that should not exist.

Player feeling:
"The system has been reshaped to trust the wrong thing."

Beat outcome:
The player finds the first concrete misconfiguration to undo later.

### Scene 05: Service Status Under Load

Planned role:
The player watches services flap, spike, restart, or degrade under pressure.

Player feeling:
"The host is not stable. Whatever is here is still active."

Beat outcome:
The player narrows which service is dragging the rest of the machine with it.

### Scene 06: Suspicious Persistence

Planned role:
The player finds a startup task, script, local job, or altered config that explains why the problem survives.

Player feeling:
"The threat expected to stay."

Beat outcome:
The player identifies the first persistence anchor.

### Scene 07: User Trust Break

Planned role:
The player sees that a user-facing surface has been modified to look normal while doing the wrong thing.

Player feeling:
"I cannot trust appearances anymore."

Beat outcome:
The player learns which interface is deceptive and why.

### Scene 08: First Containment Decision

Planned role:
The player makes a small but meaningful containment move, such as isolating a service, stopping a relay, or severing a local route.

Player feeling:
"I can push back, but I have to be careful."

Beat outcome:
The player slows the incident without ending it.

### Scene 09: Adversary Response

Planned role:
The threat reacts with new warnings, failed service behavior, or an attempted reconnect.

Player feeling:
"They noticed."

Beat outcome:
The player confirms they are in an active contest, not just cleanup.

### Scene 10: Section 1 Close

Planned role:
The player stabilizes the desktop enough to move from discovery into real containment.

Player feeling:
"I know the breach is real, local, and structured. Now I need to control it."

Beat outcome:
Section 2 opens with a stronger, more technical pursuit of the route and foothold.

## Scene construction rules

Every scene should answer these questions:

- What real screen or tool is the player looking at?
- What is the immediate readable objective?
- What new fact becomes true by the end?
- Why does the next scene have to exist?

If a scene cannot answer those four questions cleanly, it should be reworked.

## Input philosophy

The player mostly advances by typing because typing creates rhythm and ownership.
But the screen should not expose the raw game logic.

Visible rule:

- the scene reacts as if the player is working through a tool

Invisible rule:

- the game counts valid key input to advance the scene

Allowed style:

- normal alphanumeric typing
- path-like symbols
- occasional memorable combo moments for milestone actions

Forbidden style:

- constant combo puzzles
- rhythm-game prompts
- giant UI instructions that say exactly how the system works internally

## Visual direction

Section 1 visual language:

- cool desktop blues and steel tones
- warning amber for unstable trust
- constrained red only for malware / critical compromise states
- panels should feel like software windows, not arcade HUD elements
- motion should feel like unstable software, not cartoon animation

Good motion examples:

- slight scanline interference
- panel flicker
- cursor hesitation
- status bars pulsing under load
- windows arriving with weight

Bad motion examples:

- exaggerated bouncing
- impossible distortions
- constant camera shake
- flashy reward effects

## Dialogue and text rules

- System text should be concise.
- Warning text should sound like system language, not villain monologue.
- Any adversary-written text should be brief and credible.
- Important lines should be readable at a glance.
- Long lines should wrap or be shortened before they clip.

## Red lines

Do not introduce:

- fantasy code words with no technical grounding
- "elite hacker" power fantasy language
- comic-book villain speeches
- giant lore dumps
- UI that explains game mechanics instead of showing believable system state

## Current implementation status

- Scene 01 is implemented and visually polished.
- Scene 02 has a starting loopback capture scene.
- The transition from Scene 01 to Scene 02 should feel like a deliberate sync / handoff, not a hard cut.

## Next writing target

Before building more scenes, the next narrative-writing task should be:

Write a dedicated Scene 03 design note covering:

- exact screen type
- exact new fact learned
- exact transition trigger into Scene 04
- exact visual tone shift from Scene 02
