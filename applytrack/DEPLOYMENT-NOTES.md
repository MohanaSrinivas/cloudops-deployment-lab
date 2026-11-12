# Workload note
The vendored `applytrack/` directory is a snapshot of the companion ApplyTrack project at bootstrap time. Keep its API contract and environment variables aligned when changing either repository. This avoids a hidden dependency on a mutable Git submodule.
