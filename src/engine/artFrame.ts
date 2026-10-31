export type ArtFrame = { left: number; top: number; side: number };

/** A single uniform SVG-to-screen transform, shared by ink, pointers and export. */
export function artFrame(width: number, height: number, trayHeight: number): ArtFrame {
  const available = Math.max(1, height - trayHeight);
  const side = Math.max(1, Math.min(width, available) * .9);
  return { left: (width - side) / 2, top: (available - side) / 2, side };
}
export function toArtPoint(x: number, y: number, frame: ArtFrame) {
  return { x: (x - frame.left) * 400 / frame.side, y: (y - frame.top) * 400 / frame.side };
}
