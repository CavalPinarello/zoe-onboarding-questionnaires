# Data Model: ZOE Sleep Optimization Platform

**Feature**: ZOE Sleep Optimization Platform  
**Date**: 2025-09-15  
**Phase**: 1 - Design & Contracts

## Overview
This document defines the core data entities, relationships, and validation rules for the ZOE Sleep Optimization Platform. All entities are designed to be platform-agnostic and will be implemented consistently across iOS, watchOS, web portals, and backend services.

## Core Entities

### 1. User
**Description**: Individual using the platform for sleep optimization

```yaml
User:
  id: UUID
  email: String (unique, required)
  passwordHash: String (required)
  createdAt: DateTime
  updatedAt: DateTime
  lastLoginAt: DateTime
  isActive: Boolean
  profile:
    firstName: String (required)
    lastName: String (required)
    dateOfBirth: Date (required)
    gender: Enum [male, female, other, prefer_not_to_say]
    timezone: String (IANA timezone)
    photoUrl: String
  preferences:
    notificationsEnabled: Boolean
    dataSharing: Enum [private, anonymous, full]
    language: String (ISO 639-1)
    units: Enum [metric, imperial]
  chronotype:
    category: Enum [extreme_early, moderate_early, neutral, moderate_late, extreme_late]
    confidence: Float (0-1)
    lastCalculated: DateTime
  subscriptionTier: Enum [free, premium, professional]
  
Validations:
  - email must be valid format
  - age must be 13+ years
  - timezone must be valid IANA zone
```

### 2. SleepSession
**Description**: Nightly sleep data record

```yaml
SleepSession:
  id: UUID
  userId: UUID (foreign key)
  startTime: DateTime (required)
  endTime: DateTime (required)
  duration: Integer (minutes)
  source: Enum [apple_watch, manual, import]
  quality:
    overallScore: Float (0-10)
    efficiency: Float (0-100)
    latency: Integer (minutes to fall asleep)
    awakenings: Integer
    awakeTime: Integer (minutes)
  stages:
    deep: Integer (minutes)
    rem: Integer (minutes)
    light: Integer (minutes)
    awake: Integer (minutes)
  disruptions:
    count: Integer
    reasons: Array[String]
  environment:
    temperature: Float (celsius)
    humidity: Float (percentage)
    noise: Float (decibels)
    light: Float (lux)
  biometrics:
    avgHeartRate: Float
    minHeartRate: Float
    maxHeartRate: Float
    hrvAverage: Float
    respiratoryRate: Float
  createdAt: DateTime
  updatedAt: DateTime
  
Validations:
  - endTime must be after startTime
  - duration must match endTime - startTime
  - quality scores must be within valid ranges
  - stage durations must sum to total duration ± 5%
```

### 3. Protocol
**Description**: Set of daily sleep optimization interventions

```yaml
Protocol:
  id: UUID
  name: String (required)
  description: String
  version: String (semver format)
  authorId: UUID (User or System)
  isTemplate: Boolean
  isActive: Boolean
  category: Enum [timing, behavioral, environmental, supplement, medical]
  evidenceLevel: Enum [strong, moderate, limited, experimental]
  targetConditions: Array[String]
  schedule:
    startDate: Date
    endDate: Date (nullable)
    frequency: Enum [daily, weekdays, weekends, custom]
  metrics:
    adoptionCount: Integer
    successRate: Float (0-100)
    avgImprovement: Float
    lastValidated: DateTime
  createdAt: DateTime
  updatedAt: DateTime
  
Validations:
  - name must be 3-100 characters
  - endDate must be after startDate if present
  - version must follow semver format
```

### 4. ProtocolAction
**Description**: Individual intervention within a protocol

```yaml
ProtocolAction:
  id: UUID
  protocolId: UUID (foreign key)
  title: String (required)
  description: String
  type: Enum [timing, duration, consumption, environment, behavioral, physical]
  scheduledTime: Time (nullable)
  duration: Integer (minutes, nullable)
  importance: Enum [critical, high, medium, low]
  completionMethod: Enum [simple, duration, quantity, rating, binary]
  parameters:
    quantity: Float (nullable)
    unit: String (nullable)
    notes: String
  evidence:
    level: Enum [strong, moderate, limited, anecdotal]
    sources: Array[String]
    contraindications: Array[String]
  order: Integer
  isOptional: Boolean
  createdAt: DateTime
  
Validations:
  - title must be 3-200 characters
  - duration must be positive if present
  - quantity must be positive if present
```

### 5. CommunityProtocol
**Description**: Protocol shared with community including validation metrics

```yaml
CommunityProtocol:
  id: UUID
  protocolId: UUID (foreign key)
  creatorId: UUID (foreign key to User)
  isAnonymous: Boolean
  shareDate: DateTime
  validation:
    communityScore: Float (0-10)
    expertReviewed: Boolean
    expertReviewerId: UUID (nullable)
    reviewDate: DateTime (nullable)
    safetyRating: Enum [safe, caution, review_required]
  metrics:
    viewCount: Integer
    adoptionCount: Integer
    successCount: Integer
    reportCount: Integer
    avgRating: Float (0-5)
    ratingCount: Integer
  targetProfiles:
    chronotypes: Array[Enum]
    ageRanges: Array[String]
    conditions: Array[String]
  visibility: Enum [public, community, followers, private]
  status: Enum [active, under_review, suspended, deleted]
  createdAt: DateTime
  updatedAt: DateTime
  
Validations:
  - communityScore calculated, not set directly
  - reportCount threshold triggers review
  - expertReviewed requires valid expertReviewerId
```

### 6. HealthcareProfessional
**Description**: Physician or sleep specialist on the platform

```yaml
HealthcareProfessional:
  id: UUID
  userId: UUID (foreign key)
  credentials:
    licenseNumber: String (required)
    licenseState: String (required)
    specialty: Enum [sleep_medicine, pulmonology, neurology, psychiatry, general]
    boardCertifications: Array[String]
    npiNumber: String
    verificationStatus: Enum [pending, verified, expired]
    verificationDate: DateTime
  practice:
    name: String
    address: Address
    phone: String
    website: String
    acceptingPatients: Boolean
  availability:
    schedule: JSON (recurring availability)
    nextAvailable: DateTime
    consultationTypes: Array[Enum]
  metrics:
    patientCount: Integer
    avgRating: Float (0-5)
    responseTime: Integer (hours)
  createdAt: DateTime
  updatedAt: DateTime
  
Validations:
  - license must be valid format for state
  - NPI number must be valid if provided
  - verification required before patient assignment
```

### 7. PatientRecord
**Description**: Link between user and healthcare provider

```yaml
PatientRecord:
  id: UUID
  patientId: UUID (foreign key to User)
  providerId: UUID (foreign key to HealthcareProfessional)
  relationshipType: Enum [primary, consultant, temporary]
  status: Enum [active, pending, terminated]
  consentGiven: Boolean
  consentDate: DateTime
  dataSharing:
    sleepData: Boolean
    protocols: Boolean
    biometrics: Boolean
    aiConversations: Boolean
  notes:
    providerNotes: String (encrypted)
    lastReviewed: DateTime
  appointments:
    lastAppointment: DateTime
    nextAppointment: DateTime
    appointmentCount: Integer
  createdAt: DateTime
  updatedAt: DateTime
  
Validations:
  - consent required for active status
  - at least one dataSharing must be true
  - provider must be verified
```

### 8. CheckIn
**Description**: Voice or manual sleep quality report

```yaml
CheckIn:
  id: UUID
  userId: UUID (foreign key)
  sessionId: UUID (foreign key to SleepSession, nullable)
  timestamp: DateTime (required)
  type: Enum [voice, manual, automated]
  qualityScore: Float (0-10)
  energyLevel: Float (0-10)
  mood: Enum [great, good, okay, poor, terrible]
  voiceData:
    transcript: String
    audioUrl: String (nullable)
    duration: Integer (seconds)
    sentiment: Float (-1 to 1)
    confidence: Float (0-1)
  tags: Array[String]
  notes: String
  device:
    type: Enum [iphone, apple_watch, web]
    model: String
    osVersion: String
  createdAt: DateTime
  
Validations:
  - qualityScore and energyLevel required
  - voiceData required if type is voice
  - duration max 60 seconds for voice
```

### 9. BiometricReading
**Description**: Health sensor data from devices

```yaml
BiometricReading:
  id: UUID
  userId: UUID (foreign key)
  sessionId: UUID (foreign key to SleepSession, nullable)
  type: Enum [heart_rate, hrv, temperature, movement, respiratory_rate, spo2]
  value: Float (required)
  unit: String (required)
  timestamp: DateTime (required)
  source:
    device: Enum [apple_watch, iphone, other]
    model: String
    osVersion: String
  confidence: Float (0-1)
  isAnomalous: Boolean
  createdAt: DateTime
  
Validations:
  - value must be within physiological ranges
  - unit must match type
  - timestamp cannot be future
```

### 10. Insight
**Description**: Generated recommendation or observation

```yaml
Insight:
  id: UUID
  userId: UUID (foreign key)
  type: Enum [trend, recommendation, achievement, warning, tip]
  category: Enum [sleep_quality, consistency, chronotype, protocol, health]
  priority: Enum [high, medium, low]
  title: String (required)
  description: String (required)
  data:
    metric: String
    currentValue: Float
    targetValue: Float
    changePercent: Float
    timeframe: String
  actions:
    recommended: Array[String]
    protocolIds: Array[UUID]
    resources: Array[String]
  status: Enum [new, viewed, dismissed, actioned]
  confidence: Float (0-1)
  generatedAt: DateTime
  expiresAt: DateTime (nullable)
  viewedAt: DateTime (nullable)
  
Validations:
  - title max 200 characters
  - description max 1000 characters
  - expiresAt must be future if present
```

## Relationships

### Primary Relationships
```
User (1) ←→ (N) SleepSession
User (1) ←→ (N) Protocol
User (1) ←→ (N) CheckIn
User (1) ←→ (N) BiometricReading
User (1) ←→ (N) Insight
User (1) ←→ (0..1) HealthcareProfessional

Protocol (1) ←→ (N) ProtocolAction
Protocol (1) ←→ (0..1) CommunityProtocol

HealthcareProfessional (1) ←→ (N) PatientRecord
User (1) ←→ (N) PatientRecord

SleepSession (1) ←→ (N) BiometricReading
SleepSession (1) ←→ (0..N) CheckIn
```

### Association Tables
```yaml
UserProtocolAdoption:
  userId: UUID
  protocolId: UUID
  adoptedAt: DateTime
  completionRate: Float
  lastCompleted: DateTime
  status: Enum [active, paused, completed, abandoned]

ProtocolActionCompletion:
  userId: UUID
  actionId: UUID
  completedAt: DateTime
  completionValue: JSON
  notes: String

CommunityProtocolRating:
  userId: UUID
  communityProtocolId: UUID
  rating: Integer (1-5)
  review: String
  helpfulCount: Integer
  createdAt: DateTime
```

## Data Integrity Rules

### Cascade Rules
- User deletion → soft delete, anonymize after 30 days
- Protocol deletion → preserve if adopted, mark inactive
- HealthcareProfessional deletion → preserve records, mark inactive
- SleepSession deletion → preserve aggregates, delete raw data

### Validation Rules
- No overlapping SleepSessions for same user
- ProtocolActions must have unique order within Protocol
- PatientRecord requires bilateral consent
- BiometricReadings outside normal ranges flagged for review

### Privacy Rules
- PHI data encrypted at rest
- PII requires explicit consent for sharing
- Community data always anonymized
- Audit log for all data access

## Migration Strategy

### Version 1.0.0 → 1.1.0
- Add new fields as nullable
- Backfill with defaults where safe
- Maintain backward compatibility
- Version field in all entities

## Performance Considerations

### Indexing Strategy
```sql
-- Primary indexes
CREATE INDEX idx_sleep_sessions_user_date ON SleepSession(userId, startTime DESC);
CREATE INDEX idx_biometric_user_time ON BiometricReading(userId, timestamp DESC);
CREATE INDEX idx_protocols_active ON Protocol(isActive, category);
CREATE INDEX idx_insights_user_status ON Insight(userId, status, priority);

-- Composite indexes for common queries
CREATE INDEX idx_session_quality ON SleepSession(userId, quality_overallScore);
CREATE INDEX idx_community_validation ON CommunityProtocol(validation_communityScore DESC);
```

### Partitioning Strategy
- SleepSession: Partition by month
- BiometricReading: Partition by week
- CheckIn: Partition by month
- Archive data >1 year to cold storage

## Next Steps
1. Generate API contracts from this data model
2. Create database migration scripts
3. Generate model classes for each platform
4. Create validation test suites
5. Document API endpoints for CRUD operations