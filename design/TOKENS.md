# Design tokens and frame settings

| Setting | Desktop | Mobile |
| --- | --- | --- |
| Frame width | 1440 CSS px | 390 CSS px |
| Columns | 12 | 4 |
| Margin at required frame width | 72 px | 20 px |
| Gap | 24 px | 20 px |
| Primary touch control | at least 44 px | at least 44 px |
| Project columns | 2 | 1 |
| Navigation | Horizontal Flex | Burger menu |

The desktop viewport includes a classic browser scrollbar during browser previews; its available content width can therefore be slightly narrower than the nominal frame. Figma layout guides should follow the content area of the imported SVG.

| Role | Light | Dark |
| --- | --- | --- |
| Page | `#f5f3ee` | `#191a18` |
| Surface | `#fffefa` | `#232521` |
| Text | `#242421` | `#f3f1e9` |
| Secondary text | `#61615a` | `#b8b9af` |
| Border | `#d3d1c8` | `#45473e` |
| Accent text | `#51406e` | `#d8c5f8` |
| Featured card | `#d8ccf1` | `#c9b7e9` |

Main type: Arial / Helvetica / sans-serif. Expressive italic headings: Georgia / Times New Roman / serif. All exported SVG text is outlined so no installed font is required to view it.

Interactive components use `corner-shape: squircle` when the browser supports it; the existing `border-radius` provides rounded corners in other browsers. SVG frame exports preserve the squircle contour measured in Chrome. This is a progressive enhancement, not a claim of full browser support for the experimental CSS property.

Import each `desktop-light.svg`, `desktop-dark.svg`, `mobile-light.svg`, and `mobile-dark.svg` into Figma. Frame the selection at its SVG dimensions, name it by width and theme, and add the matching column layout grid. The HTML page `frames.html` remains the interactive reference.
