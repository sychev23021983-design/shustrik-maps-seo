# Text-only rollback, 2026-10-06

Owner requested restoring text in four products while retaining images. Restore pre-05Oct visual text for Arizona9520 and Grand Canyon10668, and pre-05Oct copy optimization text for California9522/New York9446. Restore old SEO title/meta. Append existing AI section verbatim, preserving all three figures/captions/AI notice/usage terms. Gallery and media metadata stay exact. USA10102 and every other product stay outside scope.

Sources: arizona-visual-release/baseline.json; optimization-three-release/baseline.json; visual-three-release-20261005/baseline.json. Original release backups must match current published content/gallery. Four writes run in a transaction with concurrent-state checks and commerce/media/identity hash protection. Old descriptions can include legacy claims: this is restoration at the owner's request, not factual revalidation.

Modes: --preview (read-only), --apply (one guarded application), --verify. Backup option _shustrik_text_only_rollback_20261006 preserves immediately preceding text/meta/gallery/media hashes. Any subsequent restoration requires a fresh guard against later edits; do not run old full rollback scripts because they restore pre-AI galleries.
