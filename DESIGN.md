---
name: Intelligence Command
colors:
  surface: '#051424'
  surface-dim: '#051424'
  surface-bright: '#2c3a4c'
  surface-container-lowest: '#010f1f'
  surface-container-low: '#0d1c2d'
  surface-container: '#122131'
  surface-container-high: '#1c2b3c'
  surface-container-highest: '#273647'
  on-surface: '#d4e4fa'
  on-surface-variant: '#c6c6cd'
  inverse-surface: '#d4e4fa'
  inverse-on-surface: '#233143'
  outline: '#909097'
  outline-variant: '#45464d'
  surface-tint: '#bec6e0'
  primary: '#bec6e0'
  on-primary: '#283044'
  primary-container: '#0f172a'
  on-primary-container: '#798098'
  inverse-primary: '#565e74'
  secondary: '#bcc7de'
  on-secondary: '#263143'
  secondary-container: '#3e495d'
  on-secondary-container: '#aeb9d0'
  tertiary: '#b9c7e0'
  on-tertiary: '#233144'
  tertiary-container: '#09182a'
  on-tertiary-container: '#738298'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#d8e3fb'
  secondary-fixed-dim: '#bcc7de'
  on-secondary-fixed: '#111c2d'
  on-secondary-fixed-variant: '#3c475a'
  tertiary-fixed: '#d5e3fd'
  tertiary-fixed-dim: '#b9c7e0'
  on-tertiary-fixed: '#0d1c2f'
  on-tertiary-fixed-variant: '#3a485c'
  background: '#051424'
  on-background: '#d4e4fa'
  surface-variant: '#273647'
typography:
  display-xl:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.5'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.4'
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 10px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.08em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 16px
  margin: 24px
  container-max: 1440px
  stack-xs: 4px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 24px
---

## Brand & Style

This design system is engineered for high-stakes operational environments where rapid data synthesis and situational awareness are paramount. The brand personality is **authoritative, precise, and vigilant**, mimicking the high-reliability interface of a global command center. 

The aesthetic leverages a **Modern Corporate** foundation infused with **Subtle Glassmorphism** to create a sense of depth without sacrificing clarity. Visual noise is aggressively minimized to ensure that critical alerts remain the focal point. The interface prioritizes "at-a-glance" comprehension, using crisp borders and a dark-mode-first approach to reduce eye strain during extended monitoring sessions.

## Colors

The palette is anchored by deep, nocturnal tones to provide a stable, low-distraction backdrop for complex data. 

- **Primary & Secondary:** Utilize `#0F172A` for the base canvas and `#1E293B` for elevated containers and sidebars. This creates a clear hierarchy of spatial layers.
- **Action Palette:** This design system employs a strict semantic color logic. **Alert Red** (`#EF4444`) is reserved exclusively for critical failures or high-priority hotspots. **Amber** (`#F59E0B`) indicates warnings or deteriorating conditions. **Emerald** (`#10B981`) signals stable, healthy, or optimal status.
- **Neutral:** Slate and gray tones facilitate secondary information and metadata without competing with primary telemetry.

## Typography

The typography in this design system utilizes **Inter** for its exceptional legibility at small sizes and its neutral, systematic character. 

Hierarchy is established through weight and capitalization rather than excessive scale. For data-dense environments, utilize `body-sm` and `label-md` frequently. Labels use uppercase styling and increased letter spacing to distinguish metadata from live content. Tabular numbers should be enabled via OpenType features to ensure columns of data remain perfectly aligned in monitoring tables and dashboards.

## Layout & Spacing

This design system employs a **fixed-fluid hybrid grid** model. The core dashboard uses a 12-column grid with a maximum container width of 1440px for desktop viewing, ensuring data points do not stretch beyond the user's peripheral vision.

A 4px base unit dictates all spatial relationships. High data density is achieved by using tight `stack-sm` (8px) gaps between related data points, while `stack-lg` (24px) is used to separate distinct functional modules or dashboard widgets. Gutters are kept at a crisp 16px to maximize horizontal real estate for complex maps and charts.

## Elevation & Depth

Visual hierarchy is communicated through **tonal layering** and **glassmorphism** rather than traditional drop shadows. 

1.  **Level 0 (Canvas):** The primary background (#0F172A).
2.  **Level 1 (Card/Widget):** Surfaces using #1E293B with a 1px border of #334155 for definition.
3.  **Level 2 (Overlay/Modal):** Semi-transparent surfaces (80% opacity) with a `24px` backdrop blur. This provides a "glass" effect that keeps the underlying map or data context visible while focusing the user's attention.

Avoid heavy shadows; use thin, high-contrast borders to separate elements, maintaining the "crisp" command center aesthetic.

## Shapes

The shape language is professional and restrained, utilizing a **Soft (0.25rem)** roundedness. 

This subtle rounding prevents the interface from feeling "sharp" or hostile while maintaining a technical, engineered appearance. Larger components, like main dashboard cards, may use `rounded-lg` (0.5rem), but internal elements such as input fields, buttons, and status chips must adhere to the 0.25rem standard to maximize space efficiency in dense layouts.

## Components

### Buttons & Inputs
Buttons feature high-contrast fills for primary actions and "ghost" styles (transparent background with a crisp border) for secondary actions. Input fields use the charcoal background with a 1px slate border, shifting to the primary accent color on focus.

### Data Visualization
Charts and maps are the core of this design system. Use thin stroke weights (1px to 1.5px) for line charts. Map markers for "Alerts" should use a subtle pulse animation to draw attention without obstructing text labels.

### Status Chips
Chips are used to categorize telemetry. They feature a low-opacity background tint of the semantic color (Red, Amber, Emerald) with a high-contrast text label and a leading dot icon to ensure accessibility.

### Cards & Containers
Every container must have a 1px border. In the "Command Center" view, cards should be header-driven, with a distinct background color for the header area to clearly separate the title from the data payload.

### List & Tables
Rows should use "zebra-striping" with very subtle tonal shifts rather than borders to minimize visual clutter. Hover states must be clearly defined with a slight lightening of the background.