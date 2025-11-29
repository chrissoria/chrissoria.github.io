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

**Templates**:
- `_layouts/` - Page layout templates
- `_includes/` - Reusable HTML components
- `_sass/` - SCSS stylesheets

**Static Assets**:
- `images/` - Image files
- `files/` - PDFs and downloadable files (accessible at /files/filename.pdf)
- `assets/` - CSS, JS, and other assets

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

Files are named with date prefix: `YYYY-MM-DD-slug.md`
