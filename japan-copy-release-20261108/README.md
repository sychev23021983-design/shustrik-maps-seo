---
type: seo-page-brief
profile: shustrik-maps
url: https://shustrik-maps.com/product/japan-3d-model-terrain/
status: approved-for-publication
date: 2026-11-08
sources: [baseline.json, public-baseline.json, manifest.json]
next_action: Publish the exact reviewed commit through vps-deploy and verify the live page.
---

# Japan terrain copy correction

The owner approved correcting the mismatch between the printing/CNC promise and the listed C4D format and open base: «Согласен, надо исправить. Сделай.» This authorizes publication of this targeted correction. The previously proposed SEO title is retained. The same promise is also present in the meta description and is corrected with the introduction.

## Scope and intent

Existing product 11358, same URL and H1. English, Google US. Primary intent: Japan terrain 3D model for visualization. No new keyword volumes or ranking claims. No new page, redirects, schema, menu or canonical changes.

SEO title: **Japan Terrain 3D Model — C4D with Satellite Texture**

Meta description: Japan terrain model in C4D with a TIF satellite texture for visualization. OBJ/FBX export on request. Prepare the mesh for your printing or CNC workflow.

Introduction:

Use this Japan terrain model to create rendered maps, landscape illustrations and scenes. The model is supplied in C4D format with a TIF satellite texture; OBJ or FBX export is available on request.

The mesh has an open base. Before 3D printing or CNC machining, check and prepare the geometry for your intended workflow. For an STL version, see the separate Japan STL product linked below.

## Evidence and boundaries

The live product specification and CMS snapshot list C4D, OBJ/FBX on request, open base, TIF texture. Configured download basename points to a Japan C4D archive. The remotely stored archive itself was not downloaded or inspected; suitability for a particular machine, slicer, scale or production process is not certified. Open base does not prove universal incompatibility with printing/CNC. No unsupported accuracy, resolution or manufacturing guarantees are introduced.

Only SEO title, meta description and the first description text block change. All shortcodes, images, links, remaining copy, H1, excerpt/specs, commerce fields, downloadable configuration and taxonomy are guarded. Six previously edited products are additionally guarded. Yoast's matching indexable row is updated with the same title and description. New post modification timestamps are expected. Page-specific cache invalidation only.

## Deployment and rollback

Use the isolated worktree, commit and push exact source before deployment. Preview requires exact old content/metadata/indexable and protected-field hashes. Apply uses an InnoDB transaction, locks and conditional content update. A non-autoloaded WordPress option `_shustrik_japan_copy_backup_20261108` preserves the baseline. Never reapply after an uncertain failure; inspect state first.

On the existing VPS runtime, execute `deploy.sh FULL_COMMIT` only through `/usr/local/sbin/vps-deploy`, with project shustrik-maps, the exact commit, both registered immutable image IDs and the product URL health check. Content-only deployment; no new QA environment, image build, container restart or full database restore.

Acceptance: PHP lint and non-mutating preview, CMS verify, public HTTP/title/meta/one H1/canonical/robots/specs/links/media checks, browser desktop/mobile inspection and non-mutating rollback-preview. Preserve registry evidence and verify the off-host copy by SHA256. Checkout, payment and fabrication are outside this copy-only check.

Rollback: after inspecting current state, run `release.php --rollback-preview`, then an explicitly selected rollback through the same deployment wrapper with a unique immutable rollback release ID and `release.php --rollback`. It restores the saved three fields and corresponding Yoast row only if live hashes still match this release. No automatic rollback or full-DB restoration.

Source/evidence files contain public copy and hashes only. Original dirty canonical worktree remains untouched. Post-publication evidence is retained in the project vault. SEO/sales effect requires a subsequent observation window; this release establishes copy correctness only.
