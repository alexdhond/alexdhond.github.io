# alexdhond.github.io

Personal academic site for Alex Dhond — PhD student in ecology at the
University of Oxford.

Built with [Quarto](https://quarto.org/) and deployed to GitHub Pages via
GitHub Actions.

## Local preview

```bash
quarto preview
```

## Deploy

Pushes to `main` trigger the publish workflow, which renders the site and
deploys to GitHub Pages.

## Canonical copy (`_content/`)

`_content/` is the single source of truth for bio, tagline, research
interests, affiliations, and writing voice. The site pulls from it via
Quarto `{{< include >}}` directives where safe (e.g. `index.qmd` pulls
`research-interests.md`).

### Sync checklist

After editing anything in `_content/`, update each external surface by
hand. (Automated sync is not worth the complexity for a solo PhD.)

- [ ] `index.qmd` intro paragraph (from `bio-long.md`; voice-sensitive — hand-port)
- [ ] LinkedIn About + Headline (paste `bio-long.md` + `bio-short.md`)
- [ ] Email signature (`tagline.md` + relevant fields from `affiliations.md`)
- [ ] Departmental profile page (paste `bio-long.md` + `affiliations.md`)
- [ ] Pinned post / X / Bluesky bio (trimmed `bio-short.md` or `tagline.md`)
- [ ] CV header (from `affiliations.md`)

`writing-voice.md` is a private reference for drafting — never shared publicly.

## License

Content © Alex Dhond. Code under the MIT License (see `LICENSE`).
