# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is Chris Soria's personal academic website built with Jekyll, hosted on GitHub Pages at christophersoria.com. It's based on the academicpages template (forked from Minimal Mistakes Jekyll Theme).

## Development Commands

```bash
# Install dependencies (first time setup)
bundle install

# Run local development server (auto-rebuilds on changes)
bundle exec jekyll liveserve

# Build the site without serving
bundle exec jekyll build
```

If you get errors during `bundle install`, delete `Gemfile.lock` and try again.

Changes to `_config.yml` are not hot-reloaded — restart the Jekyll server to see them.

## Deploying / Publishing

The site auto-builds and deploys via **GitHub Pages** on every push to `origin/main`. There is no CI workflow and no staging — **pushing to `origin` publishes the live site at christophersoria.com immediately.** Preview locally with `bundle exec jekyll liveserve` before pushing.

This repo has two remotes: `origin` (the live site, `chrissoria.github.io`) and `academic-template` (the upstream academicpages fork). Always push to `origin` — never `academic-template`.

## Commit Convention

Commit messages use a `section: lowercase imperative` prefix for the area changed — e.g. `publications:`, `talks:`, `cv:`, `research:`, `about:`, `site:`. Commits go straight to `main`.

## Site Architecture

**Content Collections** (in `_config.yml`):
- `_posts/` - Blog posts (date-prefixed markdown files)
- `_publications/` - Academic publications
- `_talks/` - Conference presentations and talks
- `_teaching/` - Teaching experience
- `_portfolio/` - Portfolio projects
- `_pages/` - Static pages (about, cv, publications list, etc.)

**Key Configuration**:
- `_config.yml` - Main site configuration, author info, social links
- `_data/navigation.yml` - Main navigation menu structure
- `_data/authors.yml` - Author metadata

Layouts (`_layouts/`), includes (`_includes/`), and styles (`_sass/`) follow standard Minimal Mistakes conventions. PDFs in `files/` are served at `/files/filename.pdf`.

## Content Format

Posts and collection items use YAML front matter. Example for a blog post:
```yaml
---
title: 'Post Title'
date: 2024-09-08
permalink: /posts/2024/09/post-slug/
tags:
  - tag1
  - tag2
---
```

File naming differs by collection:
- `_posts/YYYY-MM-DD-slug.md`
- `_publications/YYYY-MM-DD-slug.md`
- `_talks/YYYY-MM-DD-talk-N.md` — talks are **numbered**, not slugged

Publications and talks carry richer front matter than posts (`collection`, `type`, `permalink`, `venue`, and for publications `paperurl` + `citation`). `markdown_generator/` has Python scripts (`publications.py`, `talks.py`, `pubsFromBib.py`) to generate these entries from `.tsv`/BibTeX.
