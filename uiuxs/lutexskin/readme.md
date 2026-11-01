# lutexskin

LUTEXskin is the reusable specdocz standard for **portable skinning, semantic colour roles, LUT palette generation/editing, gradients, deterministic procedural textures and zone/part/state theming**.

It draws primarily from:

- **RetroBar-Extreme** for generative texture materials, LUT recolouring, theme parts/properties, texture presets and resilient fallback;
- **XenoField** for dense LUT generation and advanced spatial editing.

The standard extends those approaches with a generalized **zone → part → state → property** model, shared material libraries, cross-part continuity groups, and a more approachable primary **Palette Composer** UI layered above the advanced 16×16 LUT editor.

## Document

- [lutexskin-spec.md](lutexskin-spec.md) — normative LUTEXskin UI/UX and theme-system specification.

## Recommended use

Use LUTEXskin as a baseline or pattern library, then tailor:

- the application's target registry;
- semantic colour roles;
- supported material types;
- LUT bank sizes;
- generator set;
- platform capabilities;
- accessibility fallbacks;
- asset policy.

For detailed numeric generator controls, combine it with [parametermaxing](../parametermaxing/). For task-oriented theme workspaces and high-level aesthetic macros, combine it with [cohesive-techspression](../cohesive-techspression/).
