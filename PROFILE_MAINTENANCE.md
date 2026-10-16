# GitHub Profile — Maintenance Map

This repository contains the profile README and the source for its animated graphics. Generated assets live on separate output branches so the main branch stays focused on editable source files.

## Asset map

| What appears on the profile | Source / generator | Published output |
| --- | --- | --- |
| Dithered portrait → DIU Foundry wordmark animation | `portrait_masks.json` + `render_profile_from_masks.py` | `profile-assets`: `dark.svg`, `light.svg` |
| Public profile statistics | `scripts/generate_profile_stats.py` | `profile-stats`: `stats-dark.svg`, `stats-light.svg` |
| Public language distribution | `scripts/generate_profile_stats.py` | `profile-stats`: `top-languages-dark.svg`, `top-languages-light.svg` |
| Liquid-glass / clay buttons | `scripts/generate_liquid_buttons.py` + `.github/workflows/profile-banner.yml` | `profile-assets/buttons/*.svg` |
| Contribution snake | `.github/workflows/snake.yml` | `output`: `github-snake.svg`, `github-snake-dark.svg` |

The profile README selects a light or dark SVG using HTML `<picture>` and `prefers-color-scheme`. If you rename a published asset or its branch, update the README references at the same time.

## Workflows

- **Build animated profile banners** — `.github/workflows/profile-banner.yml`. Rebuilds the portrait-to-DIU morph and liquid-glass/clay buttons when source files change, and supports manual dispatch.
- **Generate public profile stats cards** — `.github/workflows/profile-stats.yml`. Refreshes daily and can be run manually. It uses the short-lived `GITHUB_TOKEN` supplied by GitHub Actions; it does not require a personal access token or Vercel project.
- **Generate Snake Animation** — `.github/workflows/snake.yml`. Refreshes twice daily and on pushes to `main`; it supports manual dispatch.

The workflows need repository Actions permissions that allow the workflow token to write repository contents so they can publish generated output branches.

## Data and privacy notes

- The stats cards use **public repositories only**. Stars and forks are summed from owned public repositories; the language card estimates share from GitHub's language-byte counts for owned, non-fork public repositories.
- The language chart measures code volume, not developer skill. Private repository activity is not included.
- `portrait_masks.json` contains derived dot masks, not the original photograph. Keep the original photo out of the public repository.
- Never commit access tokens or put them in the README. The workflows use GitHub's built-in `GITHUB_TOKEN`.

## Troubleshooting

1. Open the repository's **Actions** tab and inspect the latest run for the relevant workflow.
2. If the workflow passed but the profile looks unchanged, open the asset's raw URL and append a harmless cache-busting query, for example `?v=3`.
3. Check the relevant branch: banner SVGs are on `profile-assets`, stats/language SVGs are on `profile-stats`, and snake SVGs are on `output`.
4. Confirm the README points to the matching branch and file name. Dark and light assets are separate files, so check the matching GitHub appearance theme.

## Current look

The visual system combines a violet–cyan–pink–amber portrait that dissolves into the DIU Foundry wordmark, compact ocean-glass/soft-clay buttons with muted slate, aqua and periwinkle accents, light/dark-aware surfaces, project labels, generated public statistics, and the contribution snake. Keep badges honest: technology and role badges describe the profile; GitHub achievements are awarded by GitHub and should only be claimed once they appear on the account's native achievement shelf.
