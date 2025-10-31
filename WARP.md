# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

ZOE is a specification-driven development system that follows a strict Test-Driven Development (TDD) workflow. It provides a structured approach to feature development through specification templates, implementation planning, and task generation - all while enforcing constitutional principles around simplicity, testing, and observability.

## Core Architecture

### Specification System (.specify/)
The system is built around a multi-phase development workflow:
- **Phase 0**: Research and technical decisions (generates research.md)
- **Phase 1**: Design contracts and data models (generates data-model.md, contracts/, quickstart.md)
- **Phase 2**: Task planning and generation (generates tasks.md via /tasks command)
- **Phase 3-5**: Implementation, validation, and deployment

### Command Structure (.claude/commands/)
Three primary commands orchestrate the workflow:
- **specify.md**: Creates feature specifications from natural language descriptions
- **plan.md**: Generates implementation plans and design artifacts
- **tasks.md**: Creates actionable, dependency-ordered task lists

### Constitutional Principles
The system enforces strict development principles defined in `.specify/memory/constitution.md`:
- Library-first architecture (every feature as a standalone library)
- CLI interface for all libraries
- Test-first development (TDD is NON-NEGOTIABLE)
- Integration testing focus
- Observability and structured logging
- Semantic versioning with parallel migration support

## Development Commands

### Feature Creation
```bash
# Create a new feature branch and specification
.specify/scripts/bash/create-new-feature.sh --json "feature description"

# Setup implementation plan for current feature
.specify/scripts/bash/setup-plan.sh --json

# Check task prerequisites
.specify/scripts/bash/check-task-prerequisites.sh --json

# Update AI assistant context files
.specify/scripts/bash/update-agent-context.sh claude
```

### Working with Features
```bash
# Get current feature paths
.specify/scripts/bash/get-feature-paths.sh

# Common workflow pattern:
# 1. Create feature: create-new-feature.sh
# 2. Generate spec: Use /specify command
# 3. Create plan: Use /plan command  
# 4. Generate tasks: Use /tasks command
# 5. Execute tasks following TDD principles
```

## Project Structure Patterns

The system supports three project structures, determined during planning:

### Option 1: Single Project (Default)
```
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/
```

### Option 2: Web Application
```
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/
```

### Option 3: Mobile + API
```
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

## Feature Documentation Structure

Each feature lives in its own directory under `specs/[###-feature-name]/`:
```
specs/001-feature-name/
├── spec.md          # Feature specification (business requirements)
├── plan.md          # Implementation plan (technical approach)
├── research.md      # Technical decisions and research
├── data-model.md    # Entity definitions and relationships
├── contracts/       # API contracts (OpenAPI/GraphQL schemas)
├── quickstart.md    # Test scenarios and validation
└── tasks.md         # Ordered, executable task list
```

## TDD Workflow (CRITICAL)

The system enforces strict Test-Driven Development:

1. **RED Phase**: Write tests first - they MUST fail
2. **GREEN Phase**: Implement minimum code to pass tests
3. **REFACTOR Phase**: Improve code while maintaining green tests

### Test Order (Strictly Enforced)
1. Contract tests (API schemas)
2. Integration tests (user flows)
3. End-to-end tests (full scenarios)
4. Unit tests (only after implementation)

### Git Commit Pattern
Commits must show TDD compliance:
```
git log should show:
- "Add failing test for X"
- "Implement X to pass test"
- "Refactor X implementation"
```

## Task Execution

Tasks are marked with parallel execution indicators:
- `[P]` - Can run in parallel (different files, no dependencies)
- Tasks without `[P]` must run sequentially

Example parallel execution:
```bash
# Launch multiple [P] tasks together
Task: "Contract test POST /api/users"
Task: "Contract test GET /api/users/{id}"
Task: "Integration test registration"
```

## Constitution Compliance Gates

Each phase includes compliance checks:
- **Simplicity**: Max 3 projects, direct framework usage, single data model
- **Architecture**: Every feature as library with CLI
- **Testing**: TDD enforcement, real dependencies (no mocks)
- **Observability**: Structured logging, error context
- **Versioning**: MAJOR.MINOR.BUILD format

Violations must be justified in Complexity Tracking section of plan.md.

## Script Utilities

### Common Functions (common.sh)
- `get_repo_root()`: Get repository root path
- `get_current_branch()`: Get current Git branch
- `check_feature_branch()`: Validate feature branch naming (###-feature-name)
- `get_feature_paths()`: Export all feature-related paths as environment variables

### Path Resolution
All scripts use absolute paths via `git rev-parse --show-toplevel` to avoid path issues.

## Template System

Templates in `.specify/templates/` are executable specifications:
- **spec-template.md**: Feature specification with execution flow
- **plan-template.md**: Implementation planning with phase gates
- **tasks-template.md**: Task generation with dependency ordering
- **agent-file-template.md**: AI assistant context updates

Each template includes:
- Execution Flow function with error handling
- Gate checks for phase transitions
- Progress tracking checkpoints
- Validation checklists

## Working with the System

### Starting a New Feature
1. Describe the feature in natural language
2. System creates feature branch (###-feature-name format)
3. Generate specification focusing on WHAT not HOW
4. Plan implementation with constitution compliance
5. Generate executable tasks following TDD
6. Execute tasks maintaining RED-GREEN-REFACTOR cycle

### Key Principles to Remember
- Never implement before tests are written and failing
- Each feature must be a standalone library with CLI
- Focus on simplicity - avoid patterns without proven need
- Use real dependencies in tests, not mocks
- Maintain structured logging throughout
- Version everything with MAJOR.MINOR.BUILD

### Error Handling Patterns
The system uses consistent error handling:
- `ERROR`: Fatal issues requiring immediate resolution
- `WARN`: Issues that should be addressed but don't block progress
- `[NEEDS CLARIFICATION]`: Ambiguities requiring user input

## Integration with AI Assistants

The system supports context generation for various AI assistants:
- Claude: CLAUDE.md
- GitHub Copilot: .github/copilot-instructions.md
- Gemini: GEMINI.md
- Cursor: .cursor/rules/ or .cursorrules

Context files are updated incrementally via `update-agent-context.sh` script.

<citations>
  <document>
    <document_type>WARP_DOCUMENTATION</document_type>
    <document_id>getting-started/quickstart-guide/coding-in-warp</document_id>
  </document>
</citations>