---
type: seo-page-brief
site_profile: shustrik-maps
url: https://shustrik-maps.com/product/world-map-3d-model/
status: approved
created_at: 2026-11-08
sources: [baseline.json, public-baseline.json, other-world-baseline.json, manifest.json]
next_action: Publish the exact reviewed commit through vps-deploy and verify the live page.
---

# World Map product copy correction

The owner instructed «Продолжай дальше» following completed Japan and Taiwan releases. The next researched product is World Map 10238. This authorizes the next single-product copy correction and publication; the intended text and scope were summarized before publication. It does not authorize automatic keyword ownership reassignment between the two World URLs.

## Intent and factual basis

Buyer intent: a downloadable rectangular world terrain mesh for rendered maps, illustrations and animated scenes. Primary wording is the existing World Map 3D Model product name, qualified by terrain and C4D/FBX/OBJ. Existing keyword ownership, URLs, canonicals, robots and schema remain unchanged; no GSC-driven reassignment is claimed.

Fresh CMS/public specification: C4D/FBX/OBJ, geographic projection, open base, UV mapping, TIF satellite texture 21600 x 10800 px. Configured archive basename: World_Map_C4D_FBX_OBJ.zip. The live product image shows a rectangular world map. The remote archive was not downloaded; precise accuracy, GIS capabilities and manufacturing compatibility are not verified.

The separate `/world-3d-model/` product 15954 lists additional height, normal and water maps. It is preserved, including its title and copy. The existing link to that product remains; the comparison sentence helps buyers distinguish the listed bundles. No claim that either product is an interactive application or globe is retained in the edited blocks.

## On-page requirements

SEO title: **World Map 3D Model — C4D, FBX & OBJ Terrain**

Meta description: Rectangular world terrain model in C4D, FBX and OBJ, with UV mapping and a TIF satellite texture. Create rendered maps, illustrations and animated scenes.

H1: preserve **World Map 3D Model**. Preserve self-canonical and indexable robots, existing Product schema and offers, URL and product ID. Only title, meta description and the first two Description blocks change. The specification excerpt and its existing heading, lower sections, images, links, CTA, pricing and downloads stay unchanged.

Intro: Create rendered world maps with a rectangular 3D terrain model in C4D, FBX and OBJ formats. The map uses a geographic projection and includes a TIF satellite texture.

### A world map with raised terrain

The rectangular layout shows terrain across the world on a map surface. Open the model in your 3D software to compose an overview or choose an angled camera view for map illustrations, presentation graphics and animated scenes.

### Included formats and satellite texture

The C4D, FBX and OBJ files are supplied with UV mapping and a 21600 x 10800 px TIF satellite texture. The mesh has an open base. Before 3D printing or CNC machining, check and prepare the geometry for your intended workflow.

### Choosing between the World models

This product combines the terrain model and satellite texture in a C4D/FBX/OBJ package. For a bundle with height, normal and water maps, compare the separate World Earth Map 3D Model linked below.

## Acceptance, deployment and recovery

Exact baseline, metadata, indexable and protected-field hashes must match. Preserve all WPBakery shortcodes and anchor markup. Guard six previous products, including Japan, Taiwan and World 15954. Apply the two text replacements by exact offsets, inside an InnoDB transaction with locks and conditional writes. Backup option: `_shustrik_world_map_copy_backup_20261108`.

Lint and non-mutating preview precede commit/push. Deploy the exact hash-verified archive through `/usr/local/sbin/vps-deploy`, project shustrik-maps, exact source commit and registered immutable WordPress/DB images. No image build/restart or new QA environment. Verify CMS/Yoast, public HTTP/title/meta/one H1/canonical/robots/schema/media/links/CTA and desktop/mobile rendering. The second World URL must match its baseline. Sync the authoritative registry to Vault and dated off-host storage with SHA256 equality.

Rollback: inspect current state and run `release.php --rollback-preview`; perform `--rollback` only through the same deployment wrapper with an explicit rollback ID. Restore only the edited fields and corresponding Yoast row; do not restore the full DB. Exact source archive, baseline and option backup are retained. If a write fails or is uncertain, inspect state before any retry.

Success means correct published copy, not proven sales/SEO improvement. Payment, form submission, GSC ownership changes and production fabrication are outside this release. Measure search clicks and paid sales after a sufficient post-recrawl window; no automation is created.
