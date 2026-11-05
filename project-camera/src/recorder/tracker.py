"""Locate and keep a lock on one animal inside the detection area (stdlib only).

Works on the substream frames the motion detector already decodes (grey plus,
when given, the U/V colour planes), and only on the pixels inside the detection
area (a few thousand at 160x90), so plain Python is fast enough on the ROCK.

  1. Background: per-pixel median of frames taken while nothing moves. If the
     animal is already sitting still at start-up it ends up in the background.
  2. Foreground: pixels whose grey differs from the background by more than
     fg_threshold, or whose colour (|dU| + |dV|) differs by more than
     chroma_threshold, grouped into 8-connected blobs. Colour matters: a green
     toy or a yellow gecko can be close to the floor in grey alone.
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
  6. Appearance: while the target moves, its patch is stored. While it rests, the
     patch at its position is compared with the stored one every confirm_s. Grey is
     compared after removing each patch's mean, so slow exposure drift does not
     count; lost_misses failed checks in a row are needed before 'lost'.
     After a scene change the background is rebuilt and the target is kept by
     appearance alone until it moves again.

States: 'learning' (building the background), 'searching' (no target yet),
'moving', 'still', 'lost' (not seen where it was last; last position kept).
Positions are fractions of the full frame.
"""
import operator, statistics

DEFAULTS = {
    'enabled': True,
    'learn_frames': 15,        # background samples (every learn_every-th still frame)
    'learn_every': 2,
    'fg_threshold': 30,        # grey difference from the background for a foreground pixel
    'chroma_threshold': 24,    # |dU| + |dV| from the background for a foreground pixel
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
    'template_tolerance': 18,  # appearance difference accepted as "still the same animal"
    'lost_misses': 3,          # failed appearance checks in a row -> lost
    'ghost_share': 0.6,        # blobs this much like the surrounding substrate are ghosts, never the target
    'track_every': 2,          # full analysis on every n-th frame (changes in between are kept)
    'bg_every': 4,             # background drift applied every n-th analysis (alpha scaled to match)
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
    """Grey (+ U/V) frame, change image and scene flag in, target state out. Pure logic."""

    def __init__(self, cfg, w, h, area):
        self.c = {**DEFAULTS, **(cfg or {})}
        self.w, self.h = w, h
        self.set_area(area)

    def set_area(self, area):
        """area: bytes/bytearray of 0/1 per pixel (the detection area minus OSD)."""
        self.area = [i for i, v in enumerate(area) if v]
        self.area_px = len(self.area)
        self.area_set = set(self.area)
        self.index = {p: k for k, p in enumerate(self.area)}
        # Fetch all area pixels of a plane in one C call (much faster than a loop).
        self.get = operator.itemgetter(*self.area) if len(self.area) > 1 else (lambda pl: (pl[self.area[0]],))
        self.reset_background()
        self.target = None
        self.blob_age = {}

    def reset_background(self):
        self.bg = None
        self.samples, self.seen_still = [], 0
        self.pending_moved, self.n_frames, self.n_tracked = set(), 0, 0
        self.last_change = [float('-inf')] * self.area_px

    # ---------------------------------------------------------------- per frame

    def frame(self, t, gray, change, scene=False, u=None, v=None, colour_change=None):
        """gray (and optionally u, v): w*h bytes; change: w*h bytes, non-zero where the
        pixel changed since the previous frame; colour_change: the same for colour
        (computed here from u, v when not given); scene: the motion detector saw a
        scene change."""
        gray = (gray,) if u is None else (gray, u, v)
        moved = self._moved(gray, change, colour_change)
        self.pending_moved |= moved
        self.n_frames += 1
        if scene:
            self.reset_background()      # target and its appearance are kept
            self.pending_moved = set()
        if self.bg is None:
            return self._learn(t, gray, moved)
        if self.n_frames % self.c['track_every'] and not scene:
            return self.state(t)
        change, self.pending_moved = self.pending_moved, set()
        self.pa = [self.get(pl) for pl in gray]
        index = self.index
        for p in change:
            self.last_change[index[p]] = t
        blobs = self._foreground(gray, change)
        self._track(t, gray, blobs)
        self._absorb_ghosts(t, gray, blobs)
        self._update_background(gray, blobs)
        return self.state(t)

    def _moved(self, img, change, colour_change=None):
        """Area pixels that changed since the previous frame: the motion detector's
        grey change image, plus colour changes (a green toy on a beige floor barely
        changes in grey)."""
        area = self.area
        moved = {area[k] for k, c in enumerate(self.get(change)) if c}
        if colour_change is not None:
            moved.update(area[k] for k, c in enumerate(self.get(colour_change)) if c)
            return moved
        self.pa = [self.get(pl) for pl in img]          # this frame's area pixels, per plane
        prev, self.prev_pa = getattr(self, 'prev_pa', None), self.pa
        if len(img) == 3 and prev is not None and len(prev) == 3:
            thr = self.c['chroma_threshold']
            moved.update(area[k] for k, (u, v, pu, pv) in enumerate(zip(self.pa[1], self.pa[2], prev[1], prev[2]))
                         if abs(u - pu) + abs(v - pv) > thr)
        return moved

    def _learn(self, t, gray, change):
        if change:
            self.samples, self.seen_still = [], 0    # need a still stretch
        else:
            self.seen_still += 1
            if self.seen_still % self.c['learn_every'] == 0:
                self.samples.append([self.get(pl) for pl in gray])
        if len(self.samples) >= self.c['learn_frames']:
            self.bg = [[float(statistics.median_low(col)) for col in zip(*(s[c] for s in self.samples))]
                       for c in range(len(gray))]
            self.samples = []
            if self.target:   # rebuilt after a scene change: the resting target is now in it
                self._confirm(t, gray)
        return self.state(t)

    def _differs(self, img, k, p, ref=None):
        """Pixel p (area index k) against the background, or against ref values."""
        ref = ref or [b[k] for b in self.bg]
        if abs(img[0][p] - ref[0]) > self.c['fg_threshold']:
            return True
        return len(img) == 3 and len(ref) == 3 and \
            abs(img[1][p] - ref[1]) + abs(img[2][p] - ref[2]) > self.c['chroma_threshold']

    def _foreground(self, gray, change):
        area = self.area
        if len(gray) != len(self.bg):        # colour planes appeared/disappeared: relearn
            self.reset_background()
            return []
        thr, cthr, pa, bg = self.c['fg_threshold'], self.c['chroma_threshold'], self.pa, self.bg
        if len(pa) == 3:
            fg = [area[k] for k, (y, by, u, bu, v, bv) in enumerate(zip(pa[0], bg[0], pa[1], bg[1], pa[2], bg[2]))
                  if abs(y - by) > thr or abs(u - bu) + abs(v - bv) > cthr]
        else:
            fg = [area[k] for k, (y, by) in enumerate(zip(pa[0], bg[0])) if abs(y - by) > thr]
        blobs = [Blob(g, self.w) for g in connected(fg, self.w, self.h) if len(g) >= self.c['min_px']]
        for b in blobs:
            b.activity = sum(1 for p in b.pixels if p in change)
        return blobs

    def _plausible(self, b):
        return len(b.pixels) <= self.c['max_fraction'] * self.area_px

    def _ghost_share(self, gray, b, fg):
        """Share of the blob's pixels that look like the substrate around it. A ghost
        (substrate exposed where the animal sat when the background was taken) is
        close to 1; the animal itself is low."""
        ref = self._ring(gray, b.box, fg)
        if ref is None:
            return 0.0
        index = self.index
        same = sum(1 for p in b.pixels if not self._differs(gray, index[p], p, ref))
        return same / len(b.pixels)

    def _track(self, t, gray, blobs):
        c, tg = self.c, self.target
        fg = set()
        for b in blobs:
            fg.update(b.pixels)
        blobs = [b for b in blobs if self._ghost_share(gray, b, fg) < c['ghost_share']]
        if tg is not None:
            # A target splitting from its ghost moves its centre by up to its own width.
            reach = max(c['max_jump'] * self.w, tg['box'][2] - tg['box'][0], tg['box'][3] - tg['box'][1])
            near = [b for b in blobs if self._plausible(b)
                    and abs(b.cx - tg['cx']) + abs(b.cy - tg['cy']) <= reach]
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
            if tg['state'] != 'lost' and t - tg.get('checked', tg['confirmed']) >= c['confirm_s']:
                self._confirm(t, gray)
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
        tg.update(cx=b.cx, cy=b.cy, box=b.box, px=len(b.pixels), seen=t, confirmed=t, checked=t, misses=0)
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

    def _patch(self, img, box):
        x0, y0, x1, y1 = box
        return (box, [bytes(pl[y * self.w + x] for y in range(y0, y1) for x in range(x0, x1)) for pl in img])

    @staticmethod
    def _appearance_diff(ref, now):
        """Grey difference with each patch's mean removed (exposure drift does not
        count) plus the mean colour difference."""
        n = max(1, len(ref[0]))
        mr, mn = sum(ref[0]) / n, sum(now[0]) / n
        d = sum(abs((a - mr) - (b - mn)) for a, b in zip(ref[0], now[0])) / n
        if len(ref) == 3 and len(now) == 3:
            d += sum(abs(a - b) for a, b in zip(ref[1], now[1])) / n / 2
            d += sum(abs(a - b) for a, b in zip(ref[2], now[2])) / n / 2
        return d

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
        return self._appearance_diff(ref, self._patch(gray, (nx, ny, nx + bw, ny + bh))[1])

    def _confirm(self, t, gray):
        tg = self.target
        if not tg or not tg['template']:
            return
        box, ref = tg['template']
        diff = self._appearance_diff(ref, self._patch(gray, box)[1])
        tg['match'], tg['checked'] = round(diff, 1), t
        if diff <= self.c['template_tolerance']:
            tg['confirmed'], tg['misses'] = t, 0
            if tg['state'] == 'moving':
                tg['state'], tg['still_since'] = 'still', t
        else:
            tg['misses'] = tg.get('misses', 0) + 1
            if tg['misses'] >= self.c['lost_misses']:
                tg['state'] = 'lost'

    def _absorb_ghosts(self, t, gray, blobs):
        """Remove ghosts from the foreground.

        Per pixel: a foreground pixel unchanged for absorb_s whose grey matches the
        substrate around its blob is exposed substrate (a ghost, even one still joined
        to the target) and goes into the background. Per blob: a non-target blob that
        stays unchanged for absorb_s and does not look like the target is absorbed
        whole (objects put down, ghosts on a different-looking floor)."""
        tg = self.target
        index = self.index
        fg = set()
        for b in blobs:
            fg.update(b.pixels)
        quiet = t - self.c['absorb_s']
        for b in blobs:
            ref = self._ring(gray, b.box, fg)
            if ref is None:
                continue
            for p in b.pixels:
                k = index[p]
                if self.last_change[k] <= quiet and not self._differs(gray, k, p, ref):
                    for c, pl in enumerate(gray):
                        self.bg[c][k] = float(pl[p])
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
                    for c, pl in enumerate(gray):
                        self.bg[c][index[p]] = float(pl[p])
                ages.pop(key)
        self.blob_age = ages

    def _ring(self, gray, box, fg, margin=3):
        """Per-plane median of the non-foreground area pixels around a box, or None."""
        x0, y0, x1, y1 = box
        inside = self.area_set
        ps = [y * self.w + x
              for y in range(max(0, y0 - margin), min(self.h, y1 + margin))
              for x in range(max(0, x0 - margin), min(self.w, x1 + margin))
              if not (x0 <= x < x1 and y0 <= y < y1)
              and (y * self.w + x) in inside and (y * self.w + x) not in fg]
        if len(ps) < 8:
            return None
        return [statistics.median_low([pl[p] for p in ps]) for pl in gray]

    def _update_background(self, gray, blobs):
        covered = set()
        for b in blobs:
            covered.update(b.pixels)
        if self.target and self.target.get('box'):
            x0, y0, x1, y1 = self.target['box']
            covered.update(y * self.w + x for y in range(max(0, y0 - 1), min(self.h, y1 + 1))
                           for x in range(max(0, x0 - 1), min(self.w, x1 + 1)))
        self.n_tracked += 1
        if self.n_tracked % self.c['bg_every']:
            return
        a, index = 1 - (1 - self.c['alpha']) ** self.c['bg_every'], self.index
        keep = bytearray(self.area_px)
        for p in covered:
            k = index.get(p)
            if k is not None:
                keep[k] = 1
        self.bg = [[b if f else b + a * (x - b) for b, x, f in zip(bg, pl, keep)]
                   for bg, pl in zip(self.bg, self.pa)]

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
