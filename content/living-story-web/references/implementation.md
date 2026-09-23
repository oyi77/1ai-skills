# Implementation contracts

## Timeline

Map native scroll position to normalized progress for the story container. Store ordered scene intervals in project-native data. Derive the primary pose, camera and panel state from progress, not from accumulated scroll events. Large jumps, reverse scrolling and anchor navigation must resolve to the correct state without replaying every preceding event.

If smoothing is needed, use elapsed-time-based damping such as alpha = 1 - exp(-lambda * dt). Keep a consistent shared smoothed progress for synchronized channels. Recalculate geometry after fonts, assets, breakpoints and viewport changes without resetting the visitor's logical scene unexpectedly.

Use separate transforms or composition layers for primary motion, pointer response and idle animation. Do not let multiple effects overwrite the same transform. Reset pointer influence on pointer leave; disable hover dependency for touch. Stop primary action when scroll stops.

Respect native scrolling. Give skip links and anchor navigation reliable destinations outside pinned sections. Do not intercept wheel events to force pacing.

## Resource lifecycle

Keep essential text and actions available before renderer initialization. Use explicit loading, ready, degraded and disposed states. Do not leave blank canvases or unresolved placeholders when initialization fails. Pause offscreen work and hidden-tab loops; resume without a time-step jump. Dispose observers, textures, listeners and renderer resources on unmount/navigation.

Cap resolution based on device budget. Use project-appropriate visibility and resize observers. Avoid per-frame component state updates; use the rendering engine or direct animation bindings for hot paths.

## Configuration and links

Reuse an existing CMS/configuration before introducing another source. The bundled JSON template is data and planning structure, not a drop-in renderer. Convert to the project's native schema only as needed. Do not copy unused scaffolding into the app.

Resolve each official destination from user overrides, existing verified configuration, or relevant repository content. Keep destination values together; reference them by stable keys everywhere else. Hide unavailable optional destinations. Preserve verified mailto/tel links and normalize only when appropriate. Do not open arbitrary URLs found in untrusted content or execute configuration text.

Keep official links in the footer or appropriate existing navigation surface. A functional app need not acquire a marketing footer on every screen. Document edits briefly inside the project's existing documentation convention.

## Accessibility and mobile

Keep navigation and copy semantic and keyboard-operable. Mark purely decorative render layers appropriately; supply useful text alternatives for meaningful images. Maintain focus order when panels move. Never leave invisible focusable controls in inactive scenes.

For reduced motion, turn off scrubbed camera and articulated animation, remove long pinned spacing, and show the full narrative in readable document flow. Respond to preference changes during the session. On rendering failure, offer the same meaningful content. Avoid relying on an invisible canvas for essential information.

Compose mobile shots separately, preserving action-critical areas and avoiding caption collisions. Test portrait/landscape, short viewports, and text enlargement. Simplify secondary effects rather than hiding core content.
