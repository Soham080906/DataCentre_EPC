-- ==============================================================================
-- Seed Data for Data Centre EPC Project (TITAN-DC01)
-- ==============================================================================

-- 1. Insert Project
INSERT INTO projects (id, name, code, description, location, client, contractor, target_completion_date, total_budget, currency, status, created_at, updated_at)
VALUES (
    'a0000000-0000-0000-0000-000000000001',
    'Project Titan DC-01 — 50MW Hyperscale Data Centre Campus',
    'TITAN-DC01',
    'Turnkey EPC delivery of a Tier III / Uptime certified 50MW Hyperscale Data Centre facility with 2N electrical redundancy and N+1 mechanical cooling.',
    'North Virginia Data Center Corridor, Ashburn, VA',
    'Apex Cloud Infrastructure Global Inc.',
    'Nova EPC Data Centre Solutions Consortium',
    NOW() + INTERVAL '240 days',
    345000000.0,
    'USD',
    'active',
    NOW(),
    NOW()
) ON CONFLICT (code) DO NOTHING;

-- 2. Insert Equipment
INSERT INTO equipment (id, project_id, tag_number, name, system_category, specification_code, location, criticality, status, technical_specs, created_at, updated_at)
VALUES
(
    'e0000000-0000-0000-0000-000000000001',
    'a0000000-0000-0000-0000-000000000001',
    'UPS-01A',
    'Uninterruptible Power Supply (UPS) 2000kVA Modular Static Double-Conversion',
    'Electrical',
    '26 33 53',
    'Building A - Electrical Switchgear Room 101',
    'critical',
    'procured',
    '{"rating_kva": 2000, "input_voltage": 480, "output_voltage": 480, "battery_type": "Lithium-Ion"}',
    NOW(),
    NOW()
),
(
    'e0000000-0000-0000-0000-000000000002',
    'a0000000-0000-0000-0000-000000000001',
    'GEN-01A',
    'Standby Diesel Generator Set 2500kVA / 11kV with Sound Attenuated Enclosure',
    'Electrical',
    '26 32 13',
    'Outdoor Generator Yard - Bay 1',
    'critical',
    'procured',
    '{"rating_kva": 2500, "output_voltage": 11000, "fuel_type": "Diesel"}',
    NOW(),
    NOW()
),
(
    'e0000000-0000-0000-0000-000000000003',
    'a0000000-0000-0000-0000-000000000001',
    'CH-01A',
    'Water-Cooled Centrifugal Chiller 500TR with Variable Frequency Drive (VFD)',
    'Mechanical / HVAC',
    '23 64 16',
    'Central Energy Plant (CEP) - Chiller Bay 1',
    'high',
    'procured',
    '{"capacity_tr": 500, "refrigerant": "R-1233zd(E)"}',
    NOW(),
    NOW()
),
(
    'e0000000-0000-0000-0000-000000000004',
    'a0000000-0000-0000-0000-000000000001',
    'TR-01A',
    '33kV/11kV 25MVA Cast Resin Power Transformer with On-Load Tap Changer (OLTC)',
    'Electrical',
    '26 12 16',
    'Outdoor Primary Substation Yard - Bay A',
    'critical',
    'procured',
    '{"primary_voltage_kv": 33, "secondary_voltage_kv": 11, "capacity_mva": 25}',
    NOW(),
    NOW()
),
(
    'e0000000-0000-0000-0000-000000000005',
    'a0000000-0000-0000-0000-000000000001',
    'CRAH-01A',
    '150kW Computer Room Air Handler (CRAH) with Electronically Commutated (EC) Fans',
    'Mechanical / HVAC',
    '23 81 23',
    'Data Hall 1 - Perimeter Zone North',
    'high',
    'delivered',
    '{"cooling_capacity_kw": 150, "airflow_cfm": 28000}',
    NOW(),
    NOW()
),
(
    'e0000000-0000-0000-0000-000000000006',
    'a0000000-0000-0000-0000-000000000001',
    'SWG-01A',
    '33kV Gas-Insulated Medium Voltage Switchgear (GIS) Lineup',
    'Electrical',
    '26 13 26',
    'Substation Control Building - MV Room',
    'critical',
    'installed',
    '{"rated_voltage_kv": 33, "busbar_rating_a": 2500, "short_circuit_ka": 31.5}',
    NOW(),
    NOW()
) ON CONFLICT DO NOTHING;
