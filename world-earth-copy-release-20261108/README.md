---
type: seo-page-brief
site_profile: shustrik-maps
url: https://shustrik-maps.com/product/world-3d-model/
status: approved
created_at: 2026-11-08
sources: [baseline.json, public-baseline.json, other-world-baseline.json, manifest.json]
next_action: Publish the exact reviewed commit through vps-deploy and verify the live page.
---

# World Earth product copy correction

The owner instructed «Продолжи дальше» after the World Map 10238 release. The documented next action is this second World product, 15954. The instruction authorizes the single-product correction and publication; exact scope and proposed wording were summarized before publication. No keyword ownership reassignment, URL change or GSC mutation is authorized or performed.

## Intent and factual basis

Buyer intent: a rectangular world terrain asset for Cinema 4D with supporting surface maps, used for rendered maps, presentations and animation. Keep the World Earth Map 3D product identity and its existing keyword mapping; emphasize the bundle to distinguish it from World Map 10238 with ready C4D/FBX/OBJ files.

The fresh CMS/public specification lists C4D/OBJ (on request), geographic projection, open base, height/normal/satellite/water/pseudo-color/boundary maps. The format icon and configured World C4D.zip basename support C4D as the supplied format; OBJ is described as export on request, not included. Height map is TIF 16-bit. The image was visually checked and shows a rectangular world map. The remote archive was not downloaded or inspected; specific software-version compatibility, positional accuracy and fabrication performance are not certified.

## On-page requirements

SEO title: **World Earth Map 3D — C4D with Height & Texture Maps**

Meta description: Rectangular world terrain model for Cinema 4D, with height, normal, satellite and water maps. OBJ export on request for your visualization workflow.

Keep H1 **World Earth Map 3D Model**, self-canonical, robots, schema, URL and product ID. Only title/meta and the first two Description blocks change. Preserve excerpt/specification, lower DEM/satellite/normal-map sections, CTA, links, all images, pricing and downloadable configuration.

Intro: Build rendered world maps in Cinema 4D with a rectangular terrain model and a set of surface maps. The download is supplied in C4D format; OBJ export is available on request.

### Height, normal and satellite maps

Use the 16-bit TIF height map to drive displacement on a surface in your 3D software. The normal map helps show fine relief detail, while the satellite texture provides the color imagery. Map dimensions and bit depths are listed in the specification above.

### Water, elevation color and boundary maps

The package also includes a water map, a pseudo-color elevation map and a boundary mask. These give you additional inputs for building your scene: the pseudo-color map represents elevation with color, and the boundary mask can be used with your background.

### Working with the terrain model

The model uses a geographic projection and has an open base. Set your camera, lighting and materials in your 3D software for map illustrations, presentations or animation. Before 3D printing or CNC machining, check and prepare the geometry for your intended workflow.

## Acceptance and deployment

Check exact baseline, metadata/indexable and protected hashes before writing. Preserve shortcode/anchor markup and six earlier products, including World Map 10238, Japan and Taiwan. Apply the two exact text replacements in an InnoDB transaction with locks and conditional updates. Backup option: `_shustrik_world_earth_copy_backup_20261108`.

Lint/preview precede commit and push. Deploy only the exact hash-verified commit archive via `/usr/local/sbin/vps-deploy` with the registered immutable WordPress/DB images and target product health URL. No image build/restart or new full QA environment. Verify CMS/Yoast, HTTP/title/meta/one H1/canonical/robots, JSON-LD Product/offers, links/media, desktop/mobile and rollback-preview. Compare previous World Map URL to its baseline. Sync authoritative registry to Vault and dated off-host storage with SHA256 equality.

Rollback: inspect current state, run `release.php --rollback-preview`, then execute `--rollback` through the wrapper with an explicit rollback ID. Restore only these fields and the Yoast row; do not restore the full database. Preserve source archive, baseline and option backup. Inspect any failed or ambiguous apply before retrying.

Copy correctness is not evidence of improved sales. No payment, order, form submission, automation or GSC ownership change is part of this release. Measure after a sufficient post-recrawl observation window.
