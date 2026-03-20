# Scene 03 Design

## Scene name

Section 1 / Scene 3 - Mail Relay Triage

## Purpose

Scene 03 turns the player from "I saw suspicious loopback traffic" to "I now understand the mail relay itself is part of the compromise."

Scene 03 should make the player feel like they are reading real mail-system evidence, not solving a puzzle box.

## What the player is looking at

A real-looking mail queue / relay inspection surface.

Good candidates:

- a split-view mail admin window
- a queue browser with message rows
- a terminal-pane plus log-pane combo

Best choice for this project:

- a queue browser plus delivery log panel

Reason:

- visually distinct from Scene 01 terminal and Scene 02 packet capture
- still grounded in a real workflow
- easy to make readable for kids if the important rows are highlighted clearly

## Player objective

Find the suspicious message path and realize the local relay is forwarding or reprocessing traffic in a way it should not.

Readable player-facing objective:

- inspect the queue
- notice the repeated warning message
- realize a local service is behaving like an outside route

## New fact learned

The machine is not only receiving suspicious messages.
Its own local mail relay is participating in the incident by re-routing, mirroring, or re-queuing hostile traffic.

This is the main story fact Scene 03 must deliver.

## Why Scene 03 matters

Scene 02 proves the loopback path is suspicious.
Scene 03 proves which service is implicated.

Without Scene 03, the player knows something is wrong but not what system role is helping the breach spread.

## Emotional target

The player should feel:

- more informed
- less confused
- more alarmed

The tone is not "jump scare."
The tone is "this is getting worse because the machine's normal delivery path is no longer trustworthy."

## Visual direction

Primary look:

- pale admin-panel background
- colder steel / gray-blue surfaces
- amber highlights for warning rows
- restrained red only for clearly bad queue states

Window layout recommendation:

- top title bar
- left queue table
- right details / delivery log panel
- bottom status strip

Important visual behavior:

- queue rows should feel dense and operational
- one or two rows should stand out because of repeat delivery attempts or suspicious route labels
- the status strip should imply ongoing activity

## Motion direction

Keep motion subtle and real:

- row highlight pulses
- small spinner / activity lamp
- log pane reveals line by line
- warning row background shifts under pressure

Do not use:

- arcade flashes
- exaggerated bounce
- giant danger overlays

## Input behavior

Scene 03 should still mostly advance through normal typing.

Allowed feeling:

- player is "working through" the interface
- logs fill in faster as the player continues
- details open gradually

Recommended hidden logic:

- valid keys continue to advance progress invisibly
- one optional milestone combo can exist later, but Scene 03 does not need one

Visible UI should never show:

- typed key history
- progress counters
- WPM
- score

## Core beats

### Beat 1: Queue looks busy but ordinary

The player sees a queue table with timestamps, sender, recipient, status, and route.

Initial impression:
This could still be normal operational noise.

### Beat 2: The same warning message appears more than once

The player notices repeated or mirrored entries that should not exist.

Important clue examples:

- same subject appears multiple times with slightly different internal route paths
- local sender/recipient behavior does not make sense
- delivery attempts loop back into the same host

### Beat 3: Delivery log confirms weird local routing

The right-side details/log panel reveals lines that make the problem concrete.

Example signal:

- queued for local relay
- re-injected through loopback
- delivered into alerts mailbox after policy failure

### Beat 4: The queue is not just noisy, it is compromised

The player now understands the relay is part of the breach path.

End-state feeling:
"The system is forwarding danger inside itself."

## Suggested UI labels

Possible title bar:

- Mail Queue Inspector
- Relay Queue Review
- Local Mail Flow

Best current option:

- Relay Queue Review

Possible bottom status bar:

- Queue depth unstable | local relay reprocessing active
- Delivery trace active | suspicious loopback route detected

Best current option:

- Delivery trace active | suspicious local relay route detected

## Suggested table columns

- Time
- Sender
- Recipient
- Queue ID
- Status
- Route

## Suggested suspicious row content

- sender appears external but route says local
- recipient is internal alerts mailbox
- status says deferred, mirrored, retried, or re-queued
- route mentions loopback or local reinjection

## Example believable text fragments

- deferred: policy mismatch on local relay
- re-queued through 127.0.0.1
- duplicate delivery attempt detected
- alert mailbox received mirrored warning payload
- delivery route does not match sender trust state

## Transition to Scene 04

Scene 03 should end by pointing the player toward a management or browser-based surface where the bad relay behavior can be seen as configuration or policy.

Best handoff:

- a note in the details panel references a suspicious rule, cert, or admin endpoint
- this naturally opens Scene 04 as a browser/admin diagnostics view

Required end fact:

The relay behavior is real enough that the player now needs to inspect the configuration or control surface behind it.

## Success criteria

Scene 03 is successful if:

- a kid can tell the queue is acting weird
- an adult can recognize the relay/log vibe as credible
- the player learns one concrete new fact
- the scene points cleanly into Scene 04
