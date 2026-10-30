# Magic Colors Kids: artwork and repository audit

Review base: `c9d451869e626243d3edc9bbeb5788ebd6c5b3dd` (30 October 2026).

This is the requested first review stage: audit the complete repository, redesign
an animal, vehicle and landscape, and validate the approach before replacing the
72-picture library. **Three subjects have been redesigned in three levels; the
remaining 69 subjects have not yet been redesigned.** The original 72 assets stay
available until the art direction is approved.

## Architecture and findings

| Area | Current design | Finding / response |
|---|---|---|
| Library | 72 SVGs, 12 categories, 6 subjects each; `src/data/pages.ts` | All files and registration examined. No duplicate subject IDs or identical asset hashes. Full region inventory in `inventory.json`. |
| Generation | `scripts/generate_art.py`; 400 × 400 viewBox; primitive helpers and inline path arrays | Repeated circles, ellipses and block shapes dominate anatomy. A single thick stroke weight suppresses subtle contours. Hand-authored Bézier masters now demonstrate a more natural silhouette and graduated detail. |
| Existing quality | Both complete 36-picture sheets inspected | Animals have oversized round heads and disconnected limbs; vehicles lack believable wheel arches, proportions and panel construction; landscapes repeat geometric crowns and triangular mountains. Some decorative shapes cross unrelated outlines (for example the old ball stripes and Saturn ring). |
| Regions | SVG `data-region`, filled by DOM attribute | Stable within each SVG, but old tests only checked counts/uniqueness. Pig `tail` is an **open colorable path**. Recorded as a legacy defect; the review does not overwrite the old library. New samples require closed regions and visible hit targets. |
| Complexity | Per-page `easy / medium / advanced` metadata | Labels only, with no alternate drawings. Review subjects have separate Easy, Medium and Detailed assets; core region names are shared across levels and extra details are additive. |
| Painting | Bucket sets an SVG fill; 10 other tools render strokes to a separate canvas | Existing brush coordinates stretch to the stage independently of the contained SVG. V2 uses one uniform art-to-screen transform for input and canvas rendering. Drawing remains possible across the white stage, including outside the illustration. |
| Animation | SVG bounce plus independently moving tail | Canvas marks stayed behind. Both layers now move in one parent, with independent tail motion removed so all selected colors stay registered. Reduced motion disables that shared animation. |
| Completion | 80% of named regions, excluding background | Preserved. This is a **region-count heuristic**, not a pixel coverage detector for freehand coloring. The manual button still works for brush-only pictures. |
| Persistence | IndexedDB `magic-colors`, drawings keyed by page ID; JSON stroke list | Geometry cannot safely be substituted under old stroke coordinates. Old IDs/assets remain unchanged; new IDs such as `cat@v2:easy` isolate new documents. Gallery resolves both versions. No destructive migration or automatic recoloring. |
| History / reset | Immutable snapshots; up to 60 entries; serialized save queue | Preserved. Reset deletes the active version's saved document, fills, strokes and completion state. |
| Responsive editor | Full-screen stage; overlay tool tray; fixed CSS reservations | New artwork measures the actual tray and fits without changing aspect ratio. A side tray on landscape phones gives the illustration more space. New brush marks remain registered through rotation or tray collapse. |
| Offline | Vite bundles local assets; Capacitor uses `dist` | No network artwork, fonts, image APIs, raster dependencies or remote animation. Production bundle tested with networking disabled and a simulated local asset server. Browser deployment itself has no service worker; offline capability is provided by the installed Android bundle. |
| Build | React / TypeScript / Vite, Capacitor Android, two Actions workflows | Lint, typecheck, unit tests, production build, Capacitor sync and Playwright are exercised. Browser workflow now builds the production bundle before the offline test. Review APK has a separate application ID. |
| Visual QA | Previously screenshots only, no assertions against baselines | Nine SVG screenshot baselines and four phone/tablet editor baselines added, plus geometry/hit testing. Baselines are new reviewed references, not historical evidence of art quality. |

## Three representative masters

| Subject | Easy | Medium | Detailed | Direction |
|---|---:|---:|---:|---|
| Garden kitten | 11 regions | 16 regions | 20 regions | Seated weight, tapered tail, ears integrated with cranium, rounded paws, expressive feline eyes; selected tabby details and garden leaves. |
| Family hatchback | 9 regions | 16 regions | 19 regions | Consistent wheelbase and arches, curved roof, separate window pillars; doors, mirror, hubs, lights and restrained road detail. |
| Alpine lake | 12 regions | 16 regions | 20 regions | Layered ridges, snowcaps, shore, lake and winding trail; foreground pines and rocks, selective mountain and foliage detail. |

All assets start white with near-black outlines. There are no embedded images,
filters, raster masks or external references. Core silhouettes are consistent
between levels. Small natural features are retained, but Easy avoids the extra
stripes, panel details and foreground decoration in Detailed.

The new SVGs intentionally use painter's-order occlusion for inset features and
foreground objects. This is normal SVG compositing, not accidental line crossing.
An automated browser grid verifies that every region remains reachable; sampled
path segments check for self-intersections. These checks supplement, rather than
replace, visual inspection. They do not prove mathematical nonintersection at
arbitrary precision.

## Validation

- Python XML inventory across all 81 assets; every new fillable path explicitly
  closes and every region key is unique.
- Browser geometry, bounds and visible hit-target checks for all nine new assets.
- Nine line-art screenshot comparisons and four editor layout comparisons at
  412×915, 915×412, 800×1340 and 1340×800 CSS pixels.
- Bucket fill, undo/redo, autosave, reload, gallery, legacy/new save separation.
- Brush registration through rotation and tray collapse, shared colored animation,
  clear, automatic completion and reduced-motion behavior.
- Production bundle loaded with browser networking offline, all nine review SVGs
  fetched locally, and a picture colored successfully.
- Existing seven end-to-end tests retained; total: 24 browser tests, 5 unit tests.

Physical Tab A9 / S23+ hardware testing is still required before a production
release. Viewport tests and a successful APK build are not device-performance
measurements. Stable release signing and production distribution are also still
outside this art-direction review.

## Rollout after art-direction approval

1. Record any requested changes to the kitten, car and landscape. Re-render and
   inspect the nine reference variants before treating them as masters.
2. Author the remaining 69 subjects individually, not by adding decoration to the
   old primitives. Deliver all three levels: 216 new assets total for 72 subjects.
3. Preserve subject IDs, use explicit versioned artwork/save identities and retain
   v1 assets for legacy saves. Offer the new library for fresh pictures; never
   stretch or silently remap old strokes onto new anatomy.
4. Review each category as a contact sheet, then every subject at phone size and
   at 1:1 resolution. Require silhouette recognition without its caption, sensible
   anatomy/construction and no visible line collisions.
5. Run the same structural, interaction, offline and visual-regression checks for
   every variant; measure APK size and rendering on actual target devices.
6. Build the complete-library APK through Actions after approval and validation.

| Category | Next subjects / visual priorities |
|---|---|
| Animals | Dog, rabbit, turtle, butterfly, horse: joints, paws/hooves, muzzle and ear shapes, shell segmentation, species-specific wings. |
| Nature | Garden, tree, rainbow, mushroom, forest: organic plant silhouettes, believable branching, grouped petals, depth and paths. |
| Vehicles | Bus, train, plane, boat, truck: functional wheels, cabins, wings, hull construction and consistent proportions. |
| Fantasy | Dragon, unicorn, wizard, fairy, robot, griffin: original character silhouettes, coherent limbs, wings, costume and machinery. |
| Dinosaurs | Baby dinosaur, stegosaurus, triceratops, pterodactyl, brontosaurus, T. rex: distinguish species through body proportions, limbs, skull and plates. |
| Ocean | Fish, octopus, crab, whale, seahorse, dolphin: species-specific body curves, fins, limbs and restrained marine context. |
| Space | Rocket, astronaut, moon, alien, Saturn, lander: coherent equipment, suit joints and clear planet/ring occlusion. |
| Food | Apple, banana, cupcake, pizza, strawberry, pineapple: natural contour, stems, peel, frosting and leaf construction; avoid generic faces as the main detail. |
| Fairy tales | Castle, crown, tower, carriage, knight, cottage: coherent architectural proportions, doors/windows, wheels and costume. |
| Seasons | Snowman, umbrella, sunflower, pumpkin, Christmas tree, autumn park: seasonal silhouettes and balanced contextual detail. |
| Farm | Cow, sheep, pig, hen, barn, tractor: species anatomy, correct closed pig tail, feathers/fleece and agricultural construction. |
| Toys | Teddy, kite, drum, ball, blocks, rocking horse: seams, perspective, stable construction and noncrossing surface patterns. |
