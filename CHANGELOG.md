# Changelog

All notable changes to this project will be documented in this file.

## 2026-05-05
- fix: handle NoneType summary in extraction_service logging
- docs: update CHANGELOG.md and GEMINI.md
- feat: extend export_service with UUID-based export support

## 2026-05-02
- feat: add main_country and main_city fields to articles and update extraction service
- docs: update changelog for location extraction
- feat: implement granular location extraction logic (Phase 2)

## 2026-04-30
- docs: update changelog
- feat: add bulk article reset endpoint
- feat: Used readbility and mardownify to clean up html to reduce token usage config: Added markdownify, readability-lxml to requirements.txt

## 2026-04-29
- feat: add article export CLI tool and fix .env loading in database service

## 2026-04-28
- scripts: Added scripts to invoke apis
- feat: Added Crime as a category

## 2026-04-27
- docs: add Phase 3 for narrative synthesis and event clustering to roadmap

## 2026-04-26
- feat: implement single-category article classification; - Added backend/config.py with predefined categories; - Updated Article models with classification field; - Updated extraction_service.py to handle LLM-based classification; - Updated roadmap and changelog

## 2026-04-24
- feat: add single article retrieval via path and query parameters
- feat: implement structured API response for articles and entities
- docs: update changelog with article reset feature
- feat: add article reset endpoint to clear summary and entities
- docs: update roadmap for phase 2 progress
- docs: update CHANGELOG.md

## 2026-04-23
- feat: implement LLM-powered summarization and targeted extraction
- feat: add .env.sample for backend configuration

## 2026-04-21
- refactor: use BrowserConfig and CrawlerRunConfig in crawler service
- feat: add configurable wait time before extraction in crawler service
- feat: add debug mode and preview logging to crawler service
- docs: add PowerShell command chaining notes to GEMINI.md
- feat: add support for targeted article crawling by UUID
- docs: update changelog for Phase 1 completion
- feat: implement Crawl4AI integration and complete Phase 1

## 2026-04-19
- docs: add multi-crawler scaling plan, update roadmap and architecture
- Finalize changelog
- Update GEMINI.md with Crawl4AI and summarization details
- Update changelog with recent changes
- Update roadmap and models for Crawl4AI integration and LLM summarization
- Add .gitignore and update CHANGELOG.md
- Configure backend package, update DB password, and refine feed services
- Initial Phase 1 implementation: FastAPI backend, SQLModel models, and RSS service

