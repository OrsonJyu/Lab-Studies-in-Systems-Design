"""Locate and keep a lock on one animal inside the detection area (stdlib only).

Works on the grey substream frames the motion detector already decodes, and only
on the pixels inside the detection area (a few thousand at 160x90), so plain
Python is fast enough on the ROCK.

  1. Background: per-pixel median of frames taken while nothing moves. If the
     animal is already sitting still at start-up it ends up in the background.
  2. Foreground: pixels that differ from the background by more than
     fg_threshold, grouped into 8-connected blobs.
  3. Lock: the first blob of a plausible size that shows frame-to-frame change
     (the change image from the motion detector) becomes the target.
  4. Ghost: when an animal that was in the start-up background moves, the spot it
     left also differs from the background but never changes again. A non-target
     blob that stays unchanged for absorb_s is copied into the background; so are
     unchanged foreground pixels that match the surrounding substrate, which removes
     a ghost still joined to the target. Until then (about absorb_s after a short
     move) the reported position is pulled towards the old spot.
  5. Selective update: background pixels drift slowly towards the current frame
     (slow light changes), except under foreground blobs, so a still target stays
     foreground however long it rests.
  6. Appearance: while the target moves, its grey patch is stored. While it rests,
     the patch at its position is compared with the stored one every confirm_s.
     After a scene change the background is rebuilt and the target is kept by
     appearance alone until it moves again.

States: 'learning' (building the background), 'searching' (no target yet),
'moving', 'still', 'lost' (not seen where it was last; last position kept).
Positions are fractions of the full frame.
"""
import statistics

DEFAULTS = {
    'enabled': True,
    'learn_frames': 15,        # background samples (every learn_every-th still frame)
    'learn_every': 2,
    'fg_threshold': 30,        # grey difference from the background for a foreground pixel
    'min_px': 12,              # smallest plausible animal blob, pixels at analysis size
    'max_fraction': 0.35,      # larger blobs (hand, person) are never the target
    'lock_activity_px': 3,     # changed pixels inside a blob needed to lock onto it
    'still_activity_px': 2,    # at most this many changed pixels counts as resting
    'absorb_s': 2.0,           # unchanged non-target blob -> copied into the background
    'alpha': 0.05,             # background drift per frame outside foreground
    'max_jump': 0.15,          # largest target move between frames, fraction of frame width
    'move_px': 2.0,            # centroid travel over move_window_s that counts as moving
    'move_window_s': 1.0,
    'confirm_s': 5.0,
    'template_tolerance': 18,  # mean grey difference accepted as "still the same animal"
    'lost_s': 3.0,             # unconfirmed this long -> lost
}


class Blob:
    __slots__ = ('pixels', 'box', 'cx', 'cy', 'activity')

    def __init__(self, pixels, w):
        self.pixels = pixels
        xs = [p % w for p in pixels]
        ys = [p // w for p in pixels]
        self.box = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
        self.cx, self.cy = sum(xs) / len(xs), sum(ys) / len(ys)
        self.activity = 0


def connected(pixels, w, h):
    """8-connected groups of a set of pixel indices."""
    todo, out = set(pixels), []
    while todo:
        stack, group = [todo.pop()], []
        while stack:
            p = stack.pop()
            group.append(p)
            y, x = divmod(p, w)
            for dy in (-w, 0, w):
                for dx in ((-1, 0, 1) if 0 < x < w - 1 else (0, 1) if x == 0 else (-1, 0)):
                    q = p + dy + dx
                    if q in todo:
                        todo.remove(q)
                        stack.append(q)
        out.append(group)
    return out


class Tracker:
    """Grey frame + change image + scene flag in, target state out. Pure logic."""

    def __init__(self, cfg, w, h, area):
        self.c = {**DEFAULTS, **(cfg or {})}
        self.w, self.h = w, h
        self.set_area(area)

    def set_area(self, area):
        """area: bytes/bytearray of 0/1 per pixel (the detection area minus OSD)."""
        self.area = [i for i, v in enumerate(area) if v]
        self.area_px = len(self.area)
        self.area_set = set(self.area)
        self.reset_background()
        self.target = None
        self.blob_age = {}

    def reset_background(self):
        self.bg = None
        self.samples, self.seen_still = [], 0
        self.last_change = [float('-inf')] * self.area_px

    # ---------------------------------------------------------------- per frame

    def frame(self, t, gray, change, scene=False):
        """gray: w*h grey bytes; change: w*h bytes, non-zero where the pixel changed
        since the previous frame; scene: the motion detector saw a scene change."""
        if scene:
            self.reset_background()      # target and its appearance are kept
        if self.bg is None:
            return self._learn(t, gray, change)
        for k, p in enumerate(self.area):
            if change[p]:
                self.last_change[k] = t
        blobs = self._foreground(gray, change)
        self._track(t, gray, blobs)
        self._absorb_ghosts(t, gray, blobs)
        self._update_background(gray, blobs)
        return self.state(t)

    def _learn(self, t, gray, change):
        if any(change[i] for i in self.area):
            self.samples, self.seen_still = [], 0    # need a still stretch
        else:
            self.seen_still += 1
            if self.seen_still % self.c['learn_every'] == 0:
                self.samples.append(bytes(gray[i] for i in self.area))
        if len(self.samples) >= self.c['learn_frames']:
            cols = zip(*self.samples)
            self.bg = [float(statistics.median_low(col)) for col in cols]
            self.samples = []
            if self.target:   # rebuilt after a scene change: the resting target is now in it
                self._confirm(t, gray, force=True)
        return self.state(t)

    def _foreground(self, gray, change):
        thr, bg, area = self.c['fg_threshold'], self.bg, self.area
        fg = [p for k, p in enumerate(area) if abs(gray[p] - bg[k]) > thr]
        blobs = [Blob(g, self.w) for g in connected(fg, self.w, self.h) if len(g) >= self.c['min_px']]
        for b in blobs:
            b.activity = sum(1 for p in b.pixels if change[p])
        return blobs

    def _plausible(self, b):
        return len(b.pixels) <= self.c['max_fraction'] * self.area_px

    def _track(self, t, gray, blobs):
        c, tg = self.c, self.target
        if tg is not None:
            near = [b for b in blobs if self._plausible(b)
                    and abs(b.cx - tg['cx']) + abs(b.cy - tg['cy']) <= c['max_jump'] * self.w]
            if near:
                b = min(near, key=lambda b: abs(b.cx - tg['cx']) + abs(b.cy - tg['cy']) - b.activity)
                self._follow(t, gray, b)
                return
            # Moved further than max_jump (carried, or missed while hidden by a hand):
            # pick the blob that looks like the stored appearance.
            looks = [(self._match_at(gray, b.cx, b.cy), b) for b in blobs if self._plausible(b)]
            looks = [(d, b) for d, b in looks if d is not None and d <= c['template_tolerance']]
            if looks:
                self._follow(t, gray, min(looks, key=lambda x: x[0])[1])
                return
            if tg['state'] != 'lost' and t - tg['confirmed'] >= c['confirm_s']:
                self._confirm(t, gray)
            if tg['state'] != 'lost' and t - tg['confirmed'] > c['lost_s'] + c['confirm_s']:
                tg['state'] = 'lost'
            if tg['state'] != 'lost':
                return
        # No target (or lost): lock onto a plausible blob that is changing.
        active = [b for b in blobs if self._plausible(b) and b.activity >= c['lock_activity_px']]
        if active:
            self._follow(t, gray, max(active, key=lambda b: b.activity), new=True)

    def _follow(self, t, gray, b, new=False):
        c = self.c
        if new or self.target is None:
            self.target = {'since': t, 'trail': [], 'still_since': None, 'template': None}
        tg = self.target
        tg.update(cx=b.cx, cy=b.cy, box=b.box, px=len(b.pixels), seen=t, confirmed=t)
        tg['trail'].append((t, b.cx, b.cy))
        tg['trail'] = [p for p in tg['trail'] if t - p[0] <= max(c['move_window_s'], 60)]
        recent = [p for p in tg['trail'] if t - p[0] <= c['move_window_s']]
        travel = max(abs(p[1] - b.cx) + abs(p[2] - b.cy) for p in recent)
        moving = b.activity > c['still_activity_px'] or travel >= c['move_px']
        if moving:
            tg['state'], tg['still_since'] = 'moving', None
        else:
            if tg.get('state') != 'still':
                tg['still_since'] = t
            tg['state'] = 'still'
        if moving or tg['template'] is None or tg['template'][0] != b.box:
            tg['template'] = self._patch(gray, b.box)   # also after a ghost part is absorbed

    def _patch(self, gray, box):
        x0, y0, x1, y1 = box
        return (box, bytes(gray[y * self.w + x] for y in range(y0, y1) for x in range(x0, x1)))

    def _match_at(self, gray, cx, cy):
        """Mean grey difference between the stored appearance and the same-sized patch
        centred on (cx, cy), or None without a template or near the frame edge."""
        tg = self.target
        if not tg or not tg['template']:
            return None
        (x0, y0, x1, y1), ref = tg['template']
        bw, bh = x1 - x0, y1 - y0
        nx, ny = round(cx - bw / 2 + 0.5), round(cy - bh / 2 + 0.5)
        if nx < 0 or ny < 0 or nx + bw > self.w or ny + bh > self.h:
            return None
        now = self._patch(gray, (nx, ny, nx + bw, ny + bh))[1]
        return sum(abs(a - b) for a, b in zip(ref, now)) / max(1, len(ref))

    def _confirm(self, t, gray, force=False):
        tg = self.target
        if not tg or not tg['template']:
            return
        box, ref = tg['template']
        now = self._patch(gray, box)[1]
        diff = sum(abs(a - b) for a, b in zip(ref, now)) / max(1, len(ref))
        tg['match'] = round(diff, 1)
        if diff <= self.c['template_tolerance']:
            tg['confirmed'] = t
            if tg['state'] == 'moving':
                tg['state'], tg['still_since'] = 'still', t
        elif force:
            tg['state'] = 'lost'

    def _absorb_ghosts(self, t, gray, blobs):
        """Remove ghosts from the foreground.

        Per pixel: a foreground pixel unchanged for absorb_s whose grey matches the
        substrate around its blob is exposed substrate (a ghost, even one still joined
        to the target) and goes into the background. Per blob: a non-target blob that
        stays unchanged for absorb_s and does not look like the target is absorbed
        whole (objects put down, ghosts on a different-looking floor)."""
        tg = self.target
        index = {p: k for k, p in enumerate(self.area)}
        fg = set()
        for b in blobs:
            fg.update(b.pixels)
        thr, quiet = self.c['fg_threshold'], t - self.c['absorb_s']
        for b in blobs:
            ref = self._ring(gray, b.box, fg)
            if ref is None:
                continue
            for p in b.pixels:
                k = index[p]
                if self.last_change[k] <= quiet and abs(gray[p] - ref) <= thr:
                    self.bg[k] = float(gray[p])
        ages = {}
        for b in blobs:
            if tg and tg.get('seen') == t and b.box == tg['box']:
                continue
            key = (b.box[0] // 4, b.box[1] // 4, b.box[2] // 4, b.box[3] // 4)
            if b.activity > self.c['still_activity_px']:
                continue                      # still changing: hand, person, the animal
            d = self._match_at(gray, b.cx, b.cy) if self._plausible(b) else None
            if d is not None and d <= self.c['template_tolerance']:
                continue                      # looks like the target: never absorb it
            first = self.blob_age.get(key, t)
            ages[key] = first
            if t - first >= self.c['absorb_s']:
                for p in b.pixels:
                    self.bg[index[p]] = float(gray[p])
                ages.pop(key)
        self.blob_age = ages

    def _ring(self, gray, box, fg, margin=3):
        """Median grey of the non-foreground area pixels around a box, or None."""
        x0, y0, x1, y1 = box
        inside = self.area_set
        vals = [gray[y * self.w + x]
                for y in range(max(0, y0 - margin), min(self.h, y1 + margin))
                for x in range(max(0, x0 - margin), min(self.w, x1 + margin))
                if not (x0 <= x < x1 and y0 <= y < y1)
                and (y * self.w + x) in inside and (y * self.w + x) not in fg]
        return statistics.median_low(vals) if len(vals) >= 8 else None

    def _update_background(self, gray, blobs):
        covered = set()
        for b in blobs:
            covered.update(b.pixels)
        if self.target and self.target.get('box'):
            x0, y0, x1, y1 = self.target['box']
            covered.update(y * self.w + x for y in range(max(0, y0 - 1), min(self.h, y1 + 1))
                           for x in range(max(0, x0 - 1), min(self.w, x1 + 1)))
        a, bg = self.c['alpha'], self.bg
        for k, p in enumerate(self.area):
            if p not in covered:
                bg[k] += a * (gray[p] - bg[k])

    # ---------------------------------------------------------------- output

    def state(self, t):
        if self.bg is None and not self.target:
            return {'state': 'learning', 'progress': round(len(self.samples) / self.c['learn_frames'], 2)}
        tg = self.target
        if not tg:
            return {'state': 'searching'}
        w, h = self.w, self.h
        x0, y0, x1, y1 = tg['box']
        out = {'state': tg['state'], 'x': round((tg['cx'] + 0.5) / w, 4), 'y': round((tg['cy'] + 0.5) / h, 4),
               'box': [round(x0 / w, 4), round(y0 / h, 4), round(x1 / w, 4), round(y1 / h, 4)],
               'locked_since': round(tg['since'], 3), 'last_seen': round(tg['seen'], 3),
               'last_confirmed': round(tg['confirmed'], 3),
               'still_since': None if tg['still_since'] is None else round(tg['still_since'], 3),
               'learning': self.bg is None}
        if 'match' in tg:
            out['match'] = tg['match']
        return out

    def trail(self, t, seconds=60):
        if not self.target:
            return []
        return [[round((x + 0.5) / self.w, 4), round((y + 0.5) / self.h, 4)]
                for ts, x, y in self.target['trail'] if t - ts <= seconds]
