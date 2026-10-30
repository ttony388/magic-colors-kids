# Вълшебни Цветове / Magic Colors

Offline-first coloring game for young children. This release includes 72 original SVG pictures across 12 categories (six in each). The Android app ID is `com.magiccolors.kids`.

## Run in a browser

```bash
npm ci
npm run dev
```

Open the local URL printed by Vite. `npm run build` creates production web files; `npm run preview` serves them locally. The installed Android app uses the bundled web files and needs no network connection.

## Build an Android debug APK

Push to `main` or open **Actions → Android debug APK → Run workflow**. When the job succeeds, download `magic-colors-android-debug` from the run's **Artifacts** section and extract `app-debug.apk`. On your Android phone, open the APK and allow installation from your file manager when Android asks. Keep the same app ID and debug signing key for updates; GitHub hosted runners may produce different debug keys, requiring uninstall before installing a later debug build (which deletes local drawings). Back up exported PNGs first.

For local Android development: `npm run build && npx cap sync android`, then build in Android Studio or run `cd android && ./gradlew assembleDebug` with JDK 21 and Android SDK installed.

## Verify

```bash
npm run lint
npm run typecheck
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

Playwright screenshots are saved in `test-results/`. Browser drawings use IndexedDB; preferences use localStorage. Uninstalling or clearing application data deletes drawings. Assets have stable IDs; source artwork and drawing data are separate.

Verified screenshots from the browser tests are committed in `docs/evidence/`, including the phone home screen and tablet portrait/landscape drawing layouts.

## Implementation checklist

- [x] Bulgarian and English UI, category navigation, daily picture, surprise without repeats until a full cycle, free drawing.
- [x] Seventy-two distinct original coloring SVGs with named closed regions, three difficulty labels, including Farm and Toys.
- [x] Full-screen white drawing area with a collapsible, centered tray of illustrated tools: bucket, magic, pencil, crayon, ballpoint, felt pen, marker, brush, watercolor, glitter, spray and eraser. Centered color palette, 64 preset colors, custom picker, a five-step visual stroke thickness menu, opacity, recent colors.
- [x] Undo/redo, one-tap full reset (including saved drawing), PNG export, IndexedDB auto-save, resume, gallery and a short picture bounce and sparkle animation. When at least 80% of a picture's fillable regions are colored, the animation starts automatically with the child's selected colors; the button can replay it after any coloring.
- [x] Simple mode on by default with larger controls and eight color choices; the full tool tray remains available. Parental arithmetic gate can enable advanced color and size controls.
- [x] Large color-matched sparkle trail on touch and a two-note toy chime while painting, with sound toggle and reduced-motion support.
- [x] Custom rainbow paintbrush logo for the app header, browser tab and Android launcher.
- [x] Capacitor Android project and GitHub Actions debug APK workflow.
- [ ] More illustrations, color by number/letter, sticker mode, original animal sounds, music controls, dedicated stay-inside-lines brush, advanced pan gestures.
- [ ] Gallery thumbnails that preview the saved colors, parental progress reset and storage controls, and a fuller adult verification gate.
- [ ] A stable release signing key and APK update strategy.

These checkboxes describe implementation, not verified CI status. See the GitHub Actions run for actual build results.

Local lint, typecheck, unit tests, production web build, and Playwright browser tests exercise phone and tablet portrait/landscape layouts. GitHub Actions builds the APK and runs the browser tests on every push to `main`.

## Artwork

`scripts/generate_art.py` generates the 72 original SVG illustrations in `public/illustrations/`. Every fillable shape has a stable `data-region` key. Assets contain no copied franchise characters. Contributions should add a unique page ID and localized title to `src/data/pages.ts`.

`scripts/generate_tool_icons.py` creates the original shaded SVG tool drawings in `public/tools/`. The home screen is deliberately colorful while the editor uses a full white page and a small hideable tool tray. The completion animation respects reduced-motion settings.
