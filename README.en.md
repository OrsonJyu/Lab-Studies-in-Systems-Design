# SD5531 · Lab Studies in Systems Design

**Leopard gecko observation and recording · PolyU · Project 2 / Video Recording Module**  
[中文](README.md) · Version **v1.5.0** · Updated **5 November 2026, Hong Kong**

This repository preserves the course project, laboratory exercises, design process, discussions, deliverables and supporting evidence. The project aims to provide video and thermal-array records that students, teachers and carers can replay and compare. Proposed analysis remains subject to validation.

## Where to start

| Audience / purpose | Entry point |
| --- | --- |
| Shared home/school wired setup | [Shared guide](docs/guides/SHARED_WIRED_NETWORK_GUIDE.md) and [read-only checker](project-camera/src/network/README.md) |
| Resume the next work stage | [Current handoff](docs/handoffs/2026-11-05-shared-wired-baseline.md) |
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

- ROCK 4C+ and local SATA HDD remain the intended hardware; home/school short tests used system microSD, and SATA remains unverified.
- Both sites now adopt one isolated wired network. Mac Wi-Fi supplies Internet independently; lab-wired retains the existing connection UUID/address and starts automatically. Optional board wireless profiles remain manual.
- Home SD recovery, cold start, a later normal reboot, trusted SSH, read-only health checks and three-second video decoding passed. The renamed shared baseline still requires school-site retesting; no blanket Wi-Fi compatibility claim is made.
- A later 30 October school test saved a 60-second board recording and passed full decoding. This update adds its JSON evidence; the video remains local. Earlier school preview records retain their original stage limits.
- [recorder 0.3](project-camera/src/recorder/README.md) keeps a rolling RAM buffer on the ROCK, saves a clip with pre-event footage when substream frame differencing detects motion, and ends it after n seconds without motion. A LAN page shows live view, status and a timeline with one timestamped marker per saved clip. In home hand tests the clips kept 3.7–4.65 s before the hand appeared, detection took about 0.5 s and capture-to-board latency was about 0.23 s. p=4 and n=5 are still test values.
- Next: calibrate detection on the real enclosure and gecko, autostart, stream-loss recovery and endurance, buffer replay and login on the page. The ROCK clock was set from the Mac and the camera clock from the ROCK (on-screen time now matches); clock persistence after power loss, SATA and long runs remain open.
- Video, thermal arrays, localization/identity exploration, behaviour timelines and cross-team alignment remain the complete scope. Classroom and course-submission evidence remain separate.

## Structure and reproducibility

`docs/` contains current guidance and historical discussions; `docs/workstreams/` tracks active and completed work, and `docs/guides/` explains how the repository is organized as project memory. `project-camera/` contains design deliverables and meeting references; camera code conventions go in `project-camera/src/`, dated test records in `project-camera/experiments/`, and site-specific evidence boundaries in `project-camera/environments/`. `activities/` holds coursework. `references/` and `archive/` preserve source materials and earlier versions. `knowledge/` provides a source-backed graph; `provenance/` maps source files to repository paths and SHA-256 checksums.

Original videos and raw capture frames use Git LFS. Install Git LFS before cloning, or run `git lfs pull` after cloning to retrieve their contents. See the [migration report](docs/SYNC_REPORT.md) for exact coverage and missing items. Historic documents may contain obsolete local links; current navigation is maintained separately.

For updates, follow [CONTRIBUTING.md](CONTRIBUTING.md) and the [versioning policy](docs/VERSIONING.md). Third-party course materials retain their original ownership and licensing; this archive does not grant a new license to them.
