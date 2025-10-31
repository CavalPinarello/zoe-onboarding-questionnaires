# Tasks: ZOE Sleep Optimization Platform

**Input**: Design documents from `/specs/001-comprehensive-sleep-optimization/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **iOS app**: `ios/ZoeApp/`, `ios/ZoeAppTests/`
- **watchOS app**: `watchos/ZoeWatch/`, `watchos/ZoeWatchTests/`
- **Patient portal**: `patient-portal/src/`, `patient-portal/tests/`
- **Physician portal**: `physician-portal/src/`, `physician-portal/tests/`
- **API**: `api/src/`, `api/tests/`

## Phase 3.1: Setup & Infrastructure

### Project Initialization
- [ ] T001 Create project structure per implementation plan (ios/, watchos/, patient-portal/, physician-portal/, api/)
- [ ] T002 [P] Initialize iOS project with SwiftUI and iOS 16 minimum in ios/
- [ ] T003 [P] Initialize watchOS project with SwiftUI and watchOS 9 minimum in watchos/
- [ ] T004 [P] Initialize Next.js 14 patient portal with TypeScript in patient-portal/
- [ ] T005 [P] Initialize Next.js 14 physician portal with TypeScript in physician-portal/
- [ ] T006 [P] Initialize Node.js API with TypeScript and Express in api/

### Dependencies & Configuration
- [ ] T007 [P] Configure HealthKit capabilities and permissions in ios/ZoeApp/Info.plist
- [ ] T008 [P] Configure CloudKit container and entitlements in ios/ and watchos/
- [ ] T009 [P] Install and configure PostgreSQL with HIPAA-compliant settings in api/
- [ ] T010 [P] Setup Redis for caching and session management in api/
- [ ] T011 [P] Configure ESLint and Prettier for TypeScript projects
- [ ] T012 [P] Configure SwiftLint for iOS/watchOS projects

### Libraries Setup
- [ ] T013 Create sleep-analytics-lib with CLI in api/src/lib/sleep-analytics/
- [ ] T014 Create protocol-engine-lib with CLI in api/src/lib/protocol-engine/
- [ ] T015 Create community-matching-lib with CLI in api/src/lib/community-matching/
- [ ] T016 Create medical-escalation-lib with CLI in api/src/lib/medical-escalation/

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3

### API Contract Tests
- [ ] T017 [P] Contract test POST /auth/register in api/tests/contract/test_auth_register.ts
- [ ] T018 [P] Contract test POST /auth/login in api/tests/contract/test_auth_login.ts
- [ ] T019 [P] Contract test GET /users/me in api/tests/contract/test_users_me.ts
- [ ] T020 [P] Contract test PATCH /users/me in api/tests/contract/test_users_update.ts
- [ ] T021 [P] Contract test GET /sleep-sessions in api/tests/contract/test_sleep_sessions_list.ts
- [ ] T022 [P] Contract test POST /sleep-sessions in api/tests/contract/test_sleep_sessions_create.ts
- [ ] T023 [P] Contract test GET /sleep-sessions/{id} in api/tests/contract/test_sleep_sessions_get.ts
- [ ] T024 [P] Contract test GET /protocols in api/tests/contract/test_protocols_list.ts
- [ ] T025 [P] Contract test POST /protocols in api/tests/contract/test_protocols_create.ts
- [ ] T026 [P] Contract test GET /protocols/{id}/actions in api/tests/contract/test_protocol_actions.ts
- [ ] T027 [P] Contract test POST /protocol-actions/{id}/complete in api/tests/contract/test_action_complete.ts
- [ ] T028 [P] Contract test POST /check-ins in api/tests/contract/test_checkins_create.ts
- [ ] T029 [P] Contract test GET /insights in api/tests/contract/test_insights_list.ts
- [ ] T030 [P] Contract test GET /community/protocols in api/tests/contract/test_community_protocols.ts
- [ ] T031 [P] Contract test POST /community/protocols/{id}/adopt in api/tests/contract/test_protocol_adopt.ts
- [ ] T032 [P] Contract test POST /medical/escalate in api/tests/contract/test_medical_escalate.ts

### Integration Tests
- [ ] T033 [P] Integration test new user onboarding in api/tests/integration/test_onboarding.ts
- [ ] T034 [P] Integration test morning voice check-in in watchos/ZoeWatchTests/VoiceCheckInTests.swift
- [ ] T035 [P] Integration test daily protocol generation in api/tests/integration/test_protocol_generation.ts
- [ ] T036 [P] Integration test community protocol discovery in api/tests/integration/test_community_discovery.ts
- [ ] T037 [P] Integration test medical escalation flow in api/tests/integration/test_medical_escalation.ts
- [ ] T038 [P] Integration test physician patient monitoring in physician-portal/tests/integration/test_patient_monitoring.ts
- [ ] T039 [P] Integration test cross-platform synchronization in api/tests/integration/test_sync.ts
- [ ] T040 [P] Integration test protocol A/B testing in patient-portal/tests/integration/test_ab_testing.ts

### iOS/watchOS Tests
- [ ] T041 [P] Test HealthKit integration in ios/ZoeAppTests/HealthKitTests.swift
- [ ] T042 [P] Test CloudKit synchronization in ios/ZoeAppTests/CloudKitTests.swift
- [ ] T043 [P] Test voice processing in watchos/ZoeWatchTests/VoiceProcessingTests.swift
- [ ] T044 [P] Test notification scheduling in watchos/ZoeWatchTests/NotificationTests.swift

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Data Models
- [ ] T045 [P] User model in api/src/models/User.ts
- [ ] T046 [P] SleepSession model in api/src/models/SleepSession.ts
- [ ] T047 [P] Protocol model in api/src/models/Protocol.ts
- [ ] T048 [P] ProtocolAction model in api/src/models/ProtocolAction.ts
- [ ] T049 [P] CommunityProtocol model in api/src/models/CommunityProtocol.ts
- [ ] T050 [P] HealthcareProfessional model in api/src/models/HealthcareProfessional.ts
- [ ] T051 [P] PatientRecord model in api/src/models/PatientRecord.ts
- [ ] T052 [P] CheckIn model in api/src/models/CheckIn.ts
- [ ] T053 [P] BiometricReading model in api/src/models/BiometricReading.ts
- [ ] T054 [P] Insight model in api/src/models/Insight.ts

### API Services
- [ ] T055 [P] AuthService implementation in api/src/services/AuthService.ts
- [ ] T056 [P] UserService CRUD in api/src/services/UserService.ts
- [ ] T057 [P] SleepSessionService in api/src/services/SleepSessionService.ts
- [ ] T058 [P] ProtocolService in api/src/services/ProtocolService.ts
- [ ] T059 [P] CommunityService in api/src/services/CommunityService.ts
- [ ] T060 [P] MedicalEscalationService in api/src/services/MedicalEscalationService.ts
- [ ] T061 [P] InsightGenerationService in api/src/services/InsightService.ts

### API Routes
- [ ] T062 POST /auth/register endpoint in api/src/routes/auth.ts
- [ ] T063 POST /auth/login endpoint in api/src/routes/auth.ts
- [ ] T064 GET /users/me endpoint in api/src/routes/users.ts
- [ ] T065 PATCH /users/me endpoint in api/src/routes/users.ts
- [ ] T066 GET /sleep-sessions endpoint in api/src/routes/sleep-sessions.ts
- [ ] T067 POST /sleep-sessions endpoint in api/src/routes/sleep-sessions.ts
- [ ] T068 GET /sleep-sessions/{id} endpoint in api/src/routes/sleep-sessions.ts
- [ ] T069 GET /protocols endpoint in api/src/routes/protocols.ts
- [ ] T070 POST /protocols endpoint in api/src/routes/protocols.ts
- [ ] T071 GET /protocols/{id}/actions endpoint in api/src/routes/protocols.ts
- [ ] T072 POST /protocol-actions/{id}/complete endpoint in api/src/routes/protocol-actions.ts
- [ ] T073 POST /check-ins endpoint in api/src/routes/check-ins.ts
- [ ] T074 GET /insights endpoint in api/src/routes/insights.ts
- [ ] T075 GET /community/protocols endpoint in api/src/routes/community.ts
- [ ] T076 POST /community/protocols/{id}/adopt endpoint in api/src/routes/community.ts
- [ ] T077 POST /medical/escalate endpoint in api/src/routes/medical.ts

### iOS Implementation
- [ ] T078 [P] Dashboard view in ios/ZoeApp/Views/DashboardView.swift
- [ ] T079 [P] Protocol view in ios/ZoeApp/Views/ProtocolView.swift
- [ ] T080 [P] Community view in ios/ZoeApp/Views/CommunityView.swift
- [ ] T081 [P] Medical support view in ios/ZoeApp/Views/MedicalSupportView.swift
- [ ] T082 [P] HealthKit manager in ios/ZoeApp/Services/HealthKitManager.swift
- [ ] T083 [P] CloudKit sync manager in ios/ZoeApp/Services/CloudKitManager.swift
- [ ] T084 [P] API client in ios/ZoeApp/Services/APIClient.swift

### watchOS Implementation
- [ ] T085 [P] Voice check-in view in watchos/ZoeWatch/Views/VoiceCheckInView.swift
- [ ] T086 [P] Complication provider in watchos/ZoeWatch/ComplicationProvider.swift
- [ ] T087 [P] Notification handler in watchos/ZoeWatch/Services/NotificationHandler.swift
- [ ] T088 [P] HealthKit sync in watchos/ZoeWatch/Services/HealthKitSync.swift

### Patient Portal Implementation
- [ ] T089 [P] Dashboard page in patient-portal/src/pages/dashboard.tsx
- [ ] T090 [P] Protocols page in patient-portal/src/pages/protocols.tsx
- [ ] T091 [P] Community page in patient-portal/src/pages/community.tsx
- [ ] T092 [P] Analytics page in patient-portal/src/pages/analytics.tsx
- [ ] T093 [P] Settings page in patient-portal/src/pages/settings.tsx

### Physician Portal Implementation
- [ ] T094 [P] Patient overview in physician-portal/src/pages/patients.tsx
- [ ] T095 [P] Protocol validation in physician-portal/src/pages/protocols.tsx
- [ ] T096 [P] Analytics dashboard in physician-portal/src/pages/analytics.tsx
- [ ] T097 [P] Communication hub in physician-portal/src/pages/communications.tsx

## Phase 3.4: Integration & Middleware

### Database Integration
- [ ] T098 Connect API to PostgreSQL with Prisma ORM in api/src/lib/database.ts
- [ ] T099 Implement database migrations in api/prisma/migrations/
- [ ] T100 Setup Redis caching layer in api/src/lib/cache.ts
- [ ] T101 Configure CloudKit for iOS/watchOS sync

### Authentication & Security
- [ ] T102 JWT authentication middleware in api/src/middleware/auth.ts
- [ ] T103 HIPAA audit logging in api/src/middleware/audit.ts
- [ ] T104 Rate limiting middleware in api/src/middleware/rateLimit.ts
- [ ] T105 CORS and security headers in api/src/middleware/security.ts

### Real-time Features
- [ ] T106 WebSocket setup for real-time sync in api/src/lib/websocket.ts
- [ ] T107 Push notification service in api/src/services/NotificationService.ts
- [ ] T108 Background sync for iOS/watchOS

### AI Integration
- [ ] T109 Claude AI integration for Lumos in api/src/services/LumosService.ts
- [ ] T110 Medical escalation detection in api/src/lib/medical-escalation/detector.ts

## Phase 3.5: Polish & Optimization

### Unit Tests
- [ ] T111 [P] Unit tests for sleep score calculation in api/tests/unit/test_sleep_score.ts
- [ ] T112 [P] Unit tests for protocol adaptation in api/tests/unit/test_protocol_adapt.ts
- [ ] T113 [P] Unit tests for digital twin matching in api/tests/unit/test_matching.ts
- [ ] T114 [P] Unit tests for validation logic in api/tests/unit/test_validation.ts

### Performance Optimization
- [ ] T115 Database query optimization and indexing
- [ ] T116 API response caching strategy
- [ ] T117 Image and asset optimization for web portals
- [ ] T118 iOS/watchOS battery optimization

### Documentation
- [ ] T119 [P] API documentation with Swagger in api/docs/
- [ ] T120 [P] User guides in docs/user-guides/
- [ ] T121 [P] Physician documentation in docs/physician-guides/
- [ ] T122 [P] Deployment guide in docs/deployment.md

### Final Integration
- [ ] T123 End-to-end testing across all platforms
- [ ] T124 Security audit and penetration testing
- [ ] T125 Performance load testing (10K concurrent users)
- [ ] T126 HIPAA compliance verification

## Dependencies
- Setup (T001-T016) blocks all other tasks
- Tests (T017-T044) must pass before implementation (T045-T097)
- Models (T045-T054) block services (T055-T061)
- Services block routes (T062-T077)
- Integration (T098-T110) requires core implementation
- Polish (T111-T126) requires all implementation complete

## Parallel Execution Example
```bash
# Launch setup tasks together:
Task: "Initialize iOS project with SwiftUI and iOS 16 minimum"
Task: "Initialize watchOS project with SwiftUI and watchOS 9 minimum"
Task: "Initialize Next.js 14 patient portal with TypeScript"
Task: "Initialize Next.js 14 physician portal with TypeScript"
Task: "Initialize Node.js API with TypeScript and Express"

# Launch all contract tests together:
Task: "Contract test POST /auth/register"
Task: "Contract test POST /auth/login"
Task: "Contract test GET /users/me"
# ... all T017-T032 can run in parallel

# Launch all model creation together:
Task: "User model in api/src/models/User.ts"
Task: "SleepSession model in api/src/models/SleepSession.ts"
Task: "Protocol model in api/src/models/Protocol.ts"
# ... all T045-T054 can run in parallel
```

## Notes
- [P] tasks = different files, no dependencies, can run simultaneously
- Verify tests fail before implementing (RED phase of TDD)
- Commit after each task with descriptive message
- Run integration tests after each platform section

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each endpoint in openapi.yaml → contract test task [P]
   - Each endpoint → implementation task (route)
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each scenario in quickstart.md → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Routes → Integration → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [x] All contracts have corresponding tests (T017-T032)
- [x] All entities have model tasks (T045-T054)
- [x] All tests come before implementation
- [x] Parallel tasks truly independent
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task

## Summary
**Total Tasks**: 126
**Parallel Groups**: 7 major parallel execution opportunities
**Platforms**: 5 (iOS, watchOS, Patient Portal, Physician Portal, API)
**Test Coverage**: 44 test tasks before implementation
**Libraries**: 4 domain libraries with CLI interfaces

Ready for execution following TDD principles!