# SD5531 · Lab Studies in Systems Design

**Leopard gecko observation and recording · PolyU · Project 2 / Video Recording Module**  
[中文](README.md) · Version **v1.3.0** · Updated **30 October 2026, Hong Kong**

This repository preserves the course project, laboratory exercises, design process, discussions, deliverables and supporting evidence. The project aims to provide video and thermal-array records that students, teachers and carers can replay and compare. Proposed analysis remains subject to validation.

## Where to start

| Audience / purpose | Entry point |
| --- | --- |
| New visitor | [Document index](docs/INDEX.md) and [current status](docs/STATUS.md) |
| Project collaborator | [Scope](docs/SCOPE.md), [architecture](docs/ARCHITECTURE.md), [decisions](docs/DECISIONS.md) |
| Deliverables and presentation | [Camera project](project-camera/README.md) |
| Coursework and code | [Laboratory exercises](activities/README.md) |
| Progress on a piece of work | [Workstreams](docs/workstreams/README.md) |
| Evidence review | [Evidence index](docs/EVIDENCE.md) |
| Site and network conditions | [Environments](project-camera/environments/README.md) |
| Reproduce the home hardware and software experiment | [Step-by-step guide in Chinese](docs/guides/HOME_HARDWARE_AND_EXPERIMENT_GUIDE.md) |
| School wired networking, SSH recovery and ROCK access point | [School profile](project-camera/environments/school/README.md) and [configuration guide](docs/guides/SCHOOL_NETWORK_AND_PREVIEW_GUIDE.md) |
| Research connections | [Knowledge network](knowledge/NETWORK.md) and [JSON graph](knowledge/GRAPH.json) |
| Agent handover | [AGENTS.md](AGENTS.md) and [PROJECT_STATE.json](PROJECT_STATE.json) |

## Current baseline

The user explicitly updated the hardware on 23 October 2026 to **Radxa ROCK 4C+ with a local SATA hard disk**. Earlier ROCK 5C, SSD and cloud-storage diagrams are retained as historical proposals.

The **home** environment now has a limited hardware baseline: Debian 12 and SSH on ROCK 4C+, a synthetic system-card test, a real camera recording of about 60 seconds with full software decode, and user-confirmed live viewing on Mac through the board. These tests used the system microSD; SATA was not validated. Camera clock and packet-timestamp warnings, temporary addressing, rolling segments, events, pre-roll and endurance remain open. This is not a persistent deployed recording service.

The user named the household setup **home** on 30 October 2026. The later **school** session established limited SSH/hotspot evidence and user-confirmed IINA viewing, ending with camera → switch → Mac over Ethernet. The direct video probe and three-second decode passed. Final board wired IPv4/SSH recovery remained pending, and no school recording was made. The [school record](project-camera/experiments/2026-10-30-school-network-preview/README.md) separates computer hotspot, iPhone, ROCK AP and wired variants. The generic **hotspot** profile remains reserved. Actual addresses, interfaces, SSIDs and access-bearing stream configuration stay local. Neither campus-wide client isolation nor a single cause of all SSH/preview failures has been established.

The wider scope includes video and thermal capture, storage and remote access, localization and identity exploration, behavior timelines, spatial use and cross-team record alignment. Pre-recording is one step within that scope. Automated health diagnosis is outside the current presentation's deliverables.

The archive includes presentation PDF/PPTX files, collaboration plans, meeting transcripts and AI-generated minutes, Figma snapshots, eight Arduino exercises, compilation logs and hardware recordings. Compilation, simulated host tests, hardware observations and assignment submission are recorded separately.

## Structure and reproducibility

`docs/` contains current guidance and historical discussions; `docs/workstreams/` tracks active and completed work, and `docs/guides/` explains how the repository is organized as project memory. `project-camera/` contains design deliverables and meeting references; camera code conventions go in `project-camera/src/`, dated test records in `project-camera/experiments/`, and site-specific evidence boundaries in `project-camera/environments/`. `activities/` holds coursework. `references/` and `archive/` preserve source materials and earlier versions. `knowledge/` provides a source-backed graph; `provenance/` maps source files to repository paths and SHA-256 checksums.

Original videos and raw capture frames use Git LFS. Install Git LFS before cloning, or run `git lfs pull` after cloning to retrieve their contents. See the [migration report](docs/SYNC_REPORT.md) for exact coverage and missing items. Historic documents may contain obsolete local links; current navigation is maintained separately.

For updates, follow [CONTRIBUTING.md](CONTRIBUTING.md) and the [versioning policy](docs/VERSIONING.md). Third-party course materials retain their original ownership and licensing; this archive does not grant a new license to them.
