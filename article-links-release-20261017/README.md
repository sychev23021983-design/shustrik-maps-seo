# Four article links and OBJ correction 17 October 2026

Approved by the owner in chat: L01/L03/L04/L05 and exact OBJ text replacement. Three published posts: 14594, 14581, 15849. The remaining existing FBX sentence and its blockquote styling are retained outside the approved replacement range.

Only post_content and normal modification timestamps are written. All existing shortcode tokens, other text, media references, title, slug, SEO/post metadata and taxonomy are guarded. Four added a/href links. No orders, purchases, Google indexing requests, plugin settings or runtime restart.

Source baseline: baseline.json; reviewed content.diff and manifest.json; regenerate with prepare.py. Deployment: external https://shustrik-maps.com using the established WordPress container on the VPS. deliver.py prepare exports and verifies the exact pushed commit, then preview/apply/verify/rollback-preview. Transactions guard all three content changes. The backup option is _shustrik_article_links_backup_20261017.

Rollback: python article-links-release-20261017/deliver.py rollback. It refuses to overwrite newer content or protected metadata drift. The original content is restored; modification timestamps reflect the rollback. Do not replay apply after an uncertain outcome; inspect the backup and verify first.
