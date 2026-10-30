# Вълшебни Цветове / Magic Colors

Offline-first coloring game for young children. The first playable release includes 50 original SVG pictures, five in each planned category. The Android app ID is `com.magiccolors.kids`.

## Run in a browser

```bash
npm ci
npm run dev
```

Open the local URL printed by Vite. `npm run build` creates production web files; `npm run preview` serves them locally. The installed Android app uses the bundled web files and needs no network connection.

## Build an Android debug APK

Push to `main` or open **Actions → Android debug APK → Run workflow**. When the job succeeds, download `magic-colors-android-debug` from the run's **Artifacts** section and extract `app-debug.apk`. On your Android phone, open the APK and allow installation from your file manager when Android asks. Keep the same app ID and debug signing key for updates; GitHub hosted runners may produce different debug keys, requiring uninstall before installing a later debug build (which deletes local drawings). Back up exported PNGs first.

For local Android development: `npm run build && npx cap sync android`, then build in Android Studio or run `cd android && ./gradlew assembleDebug` with JDK 17 and Android SDK installed.

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

- [x] Bulgarian and English UI, category navigation, daily picture, free drawing.
- [x] Fifty distinct original coloring SVGs with named closed regions, three difficulty labels.
- [x] Tap fill, magic fill, pencil, crayon, felt pen, marker, brush, watercolor, glitter, spray, eraser; 64 preset colors, custom picker, size, opacity, recent colors.
- [x] Undo/redo, reset confirmation, zoom, PNG export, IndexedDB auto-save, resume, gallery and completion animation.
- [x] Simple mode on by default with larger controls and eight color choices; parental arithmetic gate can enable advanced tools.
- [x] Capacitor Android project and GitHub Actions debug APK workflow.
- [ ] Remaining 450 unique illustrations, color by number/letter, sticker mode, original animal sounds, music controls, dedicated stay-inside-lines brush, advanced pan gestures.
- [ ] Gallery thumbnails that preview the saved colors, parental progress reset and storage controls, and a fuller adult verification gate.
- [ ] A stable release signing key and APK update strategy.

These checkboxes describe implementation, not verified CI status. See the GitHub Actions run for actual build results.

Local lint, typecheck, two unit tests, production web build, Capacitor sync, and three Playwright browser tests passed. The browser tests exercise phone and tablet portrait/landscape layouts. The Android Gradle build could not run in the development sandbox because `services.gradle.org` is unreachable and no Android SDK is installed there. Verify the APK in GitHub Actions.

## Artwork

`scripts/generate_art.py` generates the 50 original SVG illustrations in `public/illustrations/`. Every fillable shape has a stable `data-region` key. Assets contain no copied franchise characters. Contributions should add a unique page ID and localized title to `src/data/pages.ts`.
