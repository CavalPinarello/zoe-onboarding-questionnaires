# Implementation Plan: ZOE Sleep Optimization Platform

**Branch**: `001-comprehensive-sleep-optimization` | **Date**: 2025-09-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-comprehensive-sleep-optimization/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
Comprehensive sleep optimization platform enabling personalized sleep medicine through multi-device ecosystem including Apple Watch biometric monitoring, iPhone app with dashboard/protocols/community features, web portal for advanced analytics, and physician dashboard for clinical oversight. System uses AI-powered assistance, community validation, and medical integration to improve sleep health outcomes.

## Technical Context
**Language/Version**: Swift 5.9 for iOS/watchOS, TypeScript 4.9+ for web portals  
**Primary Dependencies**: SwiftUI, HealthKit, CloudKit, Next.js 14+, PostgreSQL  
**Storage**: PostgreSQL for user data, CloudKit for Apple ecosystem sync, Redis for caching  
**Testing**: XCTest for iOS/watchOS, Jest/Playwright for web, Postman for API testing  
**Target Platform**: iOS 16+, watchOS 9+, Modern web browsers (Chrome/Safari/Firefox)  
**Project Type**: mobile + web (iOS/watchOS apps + two web portals)  
**Performance Goals**: <2s dashboard load, <3s voice processing, 60fps UI animations  
**Constraints**: HIPAA compliance required, <200ms sync latency, offline-first mobile  
**Scale/Scope**: 10K initial users, scalable to 100K+, 4 main platforms

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 4 (iOS app, watchOS app, patient portal, physician portal) - EXCEEDS max 3
- Using framework directly? Yes - SwiftUI, HealthKit, Next.js without wrappers
- Single data model? Yes - shared entities across all platforms
- Avoiding patterns? Yes - direct framework usage, no unnecessary abstractions

**Architecture**:
- EVERY feature as library? Planning modular libraries for each domain
- Libraries listed: 
  - sleep-analytics-lib (sleep scoring, pattern analysis)
  - protocol-engine-lib (intervention generation, adaptation)
  - community-matching-lib (digital twin algorithms)
  - medical-escalation-lib (symptom detection, routing)
- CLI per library: Each library will expose CLI for testing/debugging
- Library docs: Planning llms.txt format for each library

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? Yes - tests first for all features
- Git commits show tests before implementation? Will enforce in workflow
- Order: Contract→Integration→E2E→Unit strictly followed? Yes
- Real dependencies used? Yes - real PostgreSQL, actual HealthKit data
- Integration tests for: All cross-platform sync, medical escalations, community features

**Observability**:
- Structured logging included? Yes - JSON structured logs throughout
- Frontend logs → backend? Yes - unified logging pipeline planned
- Error context sufficient? Yes - full context with user state, device info

**Versioning**:
- Version number assigned? 1.0.0 for initial release
- BUILD increments on every change? Yes - CI/CD will auto-increment
- Breaking changes handled? API versioning, migration strategies planned

## Project Structure

### Documentation (this feature)
```
specs/001-comprehensive-sleep-optimization/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Mobile Apps
ios/
├── ZoeApp/
│   ├── Core/           # Shared utilities, extensions
│   ├── Models/         # Data models
│   ├── Services/       # Business logic
│   ├── Views/          # SwiftUI views
│   └── Libraries/      # Feature libraries with CLI
└── ZoeAppTests/

watchos/
├── ZoeWatch/
│   ├── Models/
│   ├── Services/
│   ├── Views/
│   └── Libraries/
└── ZoeWatchTests/

# Web Applications
patient-portal/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── lib/           # Feature libraries
└── tests/

physician-portal/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── lib/
└── tests/

# Shared Backend
api/
├── src/
│   ├── models/
│   ├── services/
│   ├── routes/
│   └── lib/
└── tests/
```

**Structure Decision**: Mobile + Web architecture due to multi-platform requirements

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - Data retention period for HIPAA compliance → Research requirement
   - Trend analysis timeframe optimization → 30-day default with customization
   - Concurrent user capacity planning → Start with 10K, architect for 100K
   - Acceptable sync delay tolerances → 500ms target, 2s maximum

2. **Generate and dispatch research agents**:
   ```
   Task: "Research HIPAA compliance requirements for sleep health data retention"
   Task: "Find best practices for HealthKit integration and data sync"
   Task: "Research voice processing optimization for Apple Watch"
   Task: "Investigate community matching algorithms for health profiles"
   Task: "Study medical escalation patterns in digital health platforms"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: HIPAA requires 7-year retention for medical records
   - Rationale: Federal regulation compliance, potential litigation
   - Alternatives considered: 3-year minimum (rejected due to state laws)

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - User entity with profile, preferences, sleep history
   - SleepSession with quality metrics, disruptions
   - Protocol and ProtocolAction for interventions
   - CommunityProtocol with validation metrics
   - HealthcareProfessional and PatientRecord
   - CheckIn, BiometricReading, Insight entities

2. **Generate API contracts** from functional requirements:
   - REST API for CRUD operations
   - WebSocket contracts for real-time sync
   - GraphQL schema for complex queries
   - Output OpenAPI/GraphQL schemas to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Schema validation tests
   - Authentication/authorization tests
   - Tests must fail initially (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Voice check-in capture and processing
   - Dashboard data aggregation and display
   - Protocol generation and adaptation
   - Community matching and sharing
   - Medical escalation flows
   - Physician monitoring workflows

5. **Update agent file incrementally**:
   - Run update-agent-context.sh for Claude/Cursor
   - Add ZOE-specific context
   - Include key architectural decisions
   - Document testing approach

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, CLAUDE.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Separate tasks by platform (iOS, watchOS, patient portal, physician portal, API)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models → Services → Views → Integration
- Platform order: API → iOS/watchOS → Web portals
- Mark [P] for parallel execution (independent platforms/files)

**Estimated Output**: 80-100 numbered, ordered tasks in tasks.md across all platforms

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 4 projects instead of 3 | Separate iOS/watchOS apps required, two distinct web portals for different user types | Combining would create poor UX and violate separation of concerns |
| Complex multi-platform sync | Real-time data consistency across devices essential for medical safety | Delayed sync could lead to dangerous medical decisions |

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [x] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS (with justified violations)
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*

# Implementation Plan: [FEATURE]


**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, or `GEMINI.md` for Gemini CLI).
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context
**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: [#] (max 3 - e.g., api, cli, tests)
- Using framework directly? (no wrapper classes)
- Single data model? (no DTOs unless serialization differs)
- Avoiding patterns? (no Repository/UoW without proven need)

**Architecture**:
- EVERY feature as library? (no direct app code)
- Libraries listed: [name + purpose for each]
- CLI per library: [commands with --help/--version/--format]
- Library docs: llms.txt format planned?

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? (test MUST fail first)
- Git commits show tests before implementation?
- Order: Contract→Integration→E2E→Unit strictly followed?
- Real dependencies used? (actual DBs, not mocks)
- Integration tests for: new libraries, contract changes, shared schemas?
- FORBIDDEN: Implementation before test, skipping RED phase

**Observability**:
- Structured logging included?
- Frontend logs → backend? (unified stream)
- Error context sufficient?

**Versioning**:
- Version number assigned? (MAJOR.MINOR.BUILD)
- BUILD increments on every change?
- Breaking changes handled? (parallel tests, migration plan)

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# Option 2: Web application (when "frontend" + "backend" detected)
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

# Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure]
```

**Structure Decision**: [DEFAULT to Option 1 unless Technical Context indicates web/mobile app]

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `/scripts/bash/update-agent-context.sh claude` for your AI assistant
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**Ordering Strategy**:
- TDD order: Tests before implementation 
- Dependency order: Models before services before UI
- Mark [P] for parallel execution (independent files)

**Estimated Output**: 25-30 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [ ] Phase 0: Research complete (/plan command)
- [ ] Phase 1: Design complete (/plan command)
- [ ] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [ ] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [ ] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*