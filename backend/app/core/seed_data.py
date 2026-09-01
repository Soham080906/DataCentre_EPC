import uuid
import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import (
    Project,
    Document,
    DocumentChunk,
    Equipment,
    SpecificationRequirement,
    VendorSubmittal,
    ComplianceCheck,
    ScheduleActivity,
    ProcurementItem,
    Risk,
    RiskMitigation,
    RFI,
    CommissioningTest,
    AuditLog,
)

logger = logging.getLogger(__name__)

def seed_database(db: Session = None):
    close_session = False
    if db is None:
        db = SessionLocal()
        close_session = True

    try:
        existing = db.query(Project).filter(Project.code == 'TITAN-DC01').first()
        if existing:
            logger.info('Sample project TITAN-DC01 already exists. Skipping seeding.')
            return existing.id

        now = datetime.now(timezone.utc)
        project_id = uuid.uuid4()

        project = Project(
            id=project_id,
            name='Project Titan DC-01 — 50MW Hyperscale Data Centre Campus',
            code='TITAN-DC01',
            description='Turnkey EPC delivery of a Tier III / Uptime certified 50MW Hyperscale Data Centre facility with 2N electrical redundancy and N+1 mechanical cooling.',
            location='North Virginia Data Center Corridor, Ashburn, VA',
            client='Apex Cloud Infrastructure Global Inc.',
            contractor='Nova EPC Data Centre Solutions Consortium',
            target_completion_date=now + timedelta(days=240),
            total_budget=345000000.0,
            currency='USD',
            status='active',
        )
        db.add(project)

        eq_ups = Equipment(
            id=uuid.uuid4(),
            project_id=project_id,
            tag_number='UPS-01A',
            name='Uninterruptible Power Supply (UPS) 2000kVA Modular Static Double-Conversion',
            system_category='Electrical',
            specification_code='26 33 53',
            location='Building A - Electrical Switchgear Room 101',
            criticality='critical',
            status='procured',
            technical_specs={'rating_kva': 2000, 'input_voltage': 480, 'output_voltage': 480, 'battery_type': 'Lithium-Ion'},
        )
        eq_gen = Equipment(
            id=uuid.uuid4(),
            project_id=project_id,
            tag_number='GEN-01A',
            name='Standby Diesel Generator Set 2500kVA / 11kV with Sound Attenuated Enclosure',
            system_category='Electrical',
            specification_code='26 32 13',
            location='Outdoor Generator Yard - Bay 1',
            criticality='critical',
            status='procured',
            technical_specs={'rating_kva': 2500, 'output_voltage': 11000, 'fuel_type': 'Diesel', 'emissions_tier': 'EPA Tier 4 Final'},
        )
        eq_chiller = Equipment(
            id=uuid.uuid4(),
            project_id=project_id,
            tag_number='CH-01A',
            name='Water-Cooled Centrifugal Chiller 500TR with Variable Frequency Drive (VFD)',
            system_category='Mechanical / HVAC',
            specification_code='23 64 16',
            location='Central Energy Plant (CEP) - Chiller Bay 1',
            criticality='high',
            status='procured',
            technical_specs={'capacity_tr': 500, 'refrigerant': 'R-1233zd(E)', 'evaporator_leaving_temp_c': 12.0},
        )
        eq_transformer = Equipment(
            id=uuid.uuid4(),
            project_id=project_id,
            tag_number='TR-01A',
            name='33kV/11kV 25MVA Cast Resin Power Transformer with On-Load Tap Changer (OLTC)',
            system_category='Electrical',
            specification_code='26 12 16',
            location='Outdoor Primary Substation Yard - Bay A',
            criticality='critical',
            status='procured',
            technical_specs={'primary_voltage_kv': 33, 'secondary_voltage_kv': 11, 'capacity_mva': 25},
        )
        eq_crah = Equipment(
            id=uuid.uuid4(),
            project_id=project_id,
            tag_number='CRAH-01A',
            name='150kW Computer Room Air Handler (CRAH) with Electronically Commutated (EC) Fans',
            system_category='Mechanical / HVAC',
            specification_code='23 81 23',
            location='Data Hall 1 - Perimeter Zone North',
            criticality='high',
            status='delivered',
            technical_specs={'cooling_capacity_kw': 150, 'airflow_cfm': 28000, 'fan_type': 'EC Fan'},
        )
        eq_swg = Equipment(
            id=uuid.uuid4(),
            project_id=project_id,
            tag_number='SWG-01A',
            name='33kV Gas-Insulated Medium Voltage Switchgear (GIS) Lineup',
            system_category='Electrical',
            specification_code='26 13 26',
            location='Substation Control Building - MV Room',
            criticality='critical',
            status='installed',
            technical_specs={'rated_voltage_kv': 33, 'busbar_rating_a': 2500, 'short_circuit_ka': 31.5},
        )

        db.add_all([eq_ups, eq_gen, eq_chiller, eq_transformer, eq_crah, eq_swg])
        db.flush()

        doc_ups_spec = Document(
            id=uuid.uuid4(),
            project_id=project_id,
            filename='SPEC-ELEC-263353-UPS-V2.pdf',
            file_path='/data/documents/SPEC-ELEC-263353-UPS-V2.pdf',
            file_type='specification',
            file_size=2458000,
            mime_type='application/pdf',
            version='2.0',
            status='indexed',
            total_pages=42,
            metadata_json={'discipline': 'Electrical', 'author': 'Lead Electrical Engineer'},
        )
        doc_ups_sub = Document(
            id=uuid.uuid4(),
            project_id=project_id,
            filename='SUB-ELEC-UPS-001-Vertiv-Rev1.pdf',
            file_path='/data/documents/SUB-ELEC-UPS-001-Vertiv-Rev1.pdf',
            file_type='vendor_submittal',
            file_size=5890000,
            mime_type='application/pdf',
            version='1.0',
            status='indexed',
            total_pages=68,
            metadata_json={'vendor': 'Vertiv Corporation', 'package': 'Static UPS 2000kVA'},
        )
        doc_chiller_spec = Document(
            id=uuid.uuid4(),
            project_id=project_id,
            filename='SPEC-MECH-236416-CHILLER.pdf',
            file_path='/data/documents/SPEC-MECH-236416-CHILLER.pdf',
            file_type='specification',
            file_size=3120000,
            mime_type='application/pdf',
            version='1.0',
            status='indexed',
            total_pages=36,
            metadata_json={'discipline': 'Mechanical', 'package': 'Central Chiller Plant'},
        )
        db.add_all([doc_ups_spec, doc_ups_sub, doc_chiller_spec])
        db.flush()

        chunk_ups = DocumentChunk(
            id=uuid.uuid4(),
            document_id=doc_ups_spec.id,
            chunk_index=14,
            page_number=18,
            section_header='2.04 EFFICIENCY AND OPERATING REQUIREMENTS',
            content='The static uninterruptible power supply (UPS) system shall maintain a minimum double-conversion AC-AC overall efficiency of 96.5% at 100% full rated linear load under nominal AC input voltage conditions.',
            token_count=52,
            chunk_metadata={'section': '2.04', 'discipline': 'Electrical', 'equipment': 'UPS-01A'},
        )
        db.add(chunk_ups)

        req_ups_eff = SpecificationRequirement(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_ups.id,
            document_id=doc_ups_spec.id,
            section_reference='Section 26 33 53 - Para 2.04',
            parameter_name='efficiency',
            operator='>=',
            target_value_numeric=96.5,
            unit='%',
            tolerance=0.0,
            is_mandatory=True,
            description='Minimum full-load double conversion AC-AC efficiency at 100% rated load.',
        )
        req_gen_start = SpecificationRequirement(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_gen.id,
            section_reference='Section 26 32 13 - Para 2.02',
            parameter_name='start_and_load_time',
            operator='<=',
            target_value_numeric=10.0,
            unit='sec',
            tolerance=0.5,
            is_mandatory=True,
            description='Maximum duration from start signal to achieving rated voltage and accepting 100% block load.',
        )
        req_chiller_cop = SpecificationRequirement(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_chiller.id,
            document_id=doc_chiller_spec.id,
            section_reference='Section 23 64 16 - Para 2.06',
            parameter_name='cop',
            operator='>=',
            target_value_numeric=6.20,
            unit='COP',
            tolerance=0.0,
            is_mandatory=True,
            description='Chiller Coefficient of Performance at standard AHRI 550/590 conditions.',
        )
        req_tr_temp = SpecificationRequirement(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_transformer.id,
            section_reference='Section 26 12 16 - Para 2.03',
            parameter_name='winding_temperature_rise',
            operator='<=',
            target_value_numeric=65.0,
            unit='degC',
            tolerance=2.0,
            is_mandatory=True,
            description='Maximum average winding temperature rise above 40°C ambient.',
        )
        req_crah_power = SpecificationRequirement(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_crah.id,
            section_reference='Section 23 81 23 - Para 2.05',
            parameter_name='fan_power_per_100kw',
            operator='<=',
            target_value_numeric=4.20,
            unit='kW',
            tolerance=0.1,
            is_mandatory=False,
            description='Maximum fan electric power draw per 100kW sensible heat removal.',
        )
        req_swg_ka = SpecificationRequirement(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_swg.id,
            section_reference='Section 26 13 26 - Para 2.01',
            parameter_name='short_circuit_withstand',
            operator='>=',
            target_value_numeric=31.5,
            unit='kA',
            tolerance=0.0,
            is_mandatory=True,
            description='Rated short-circuit symmetrical breaking and withstand capacity for 3 seconds.',
        )
        db.add_all([req_ups_eff, req_gen_start, req_chiller_cop, req_tr_temp, req_crah_power, req_swg_ka])
        db.flush()

        sub_ups = VendorSubmittal(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_ups.id,
            document_id=doc_ups_sub.id,
            submittal_number='SUB-ELEC-UPS-001-Rev1',
            vendor_name='Vertiv Corporation',
            model_number='Liebert EXL S1 2000kVA',
            approval_status='rejected',
            extracted_data={'efficiency': 94.0, 'dimensions_mm': '3800x1000x2000'},
        )
        sub_gen = VendorSubmittal(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_gen.id,
            submittal_number='SUB-ELEC-GEN-001-Rev0',
            vendor_name='Caterpillar Power Systems',
            model_number='Cat 3516E-HD 2500kVA',
            approval_status='approved',
            extracted_data={'start_time_sec': 8.5},
        )
        sub_chiller = VendorSubmittal(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_chiller.id,
            submittal_number='SUB-MECH-CH-001-Rev0',
            vendor_name='Trane Commercial HVAC',
            model_number='CenTraVac CVHE 500TR',
            approval_status='approved',
            extracted_data={'cop': 6.45},
        )
        sub_tr = VendorSubmittal(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_transformer.id,
            submittal_number='SUB-ELEC-TR-001-Rev1',
            vendor_name='Siemens Energy',
            model_number='GEAFOL Cast-Resin 25MVA',
            approval_status='approved_with_notes',
            extracted_data={'winding_temp_rise_c': 68.0},
        )
        db.add_all([sub_ups, sub_gen, sub_chiller, sub_tr])
        db.flush()

        chk_ups = ComplianceCheck(
            id=uuid.uuid4(),
            project_id=project_id,
            requirement_id=req_ups_eff.id,
            submittal_id=sub_ups.id,
            equipment_id=eq_ups.id,
            submitted_value_numeric=94.0,
            submitted_unit='%',
            status='FAIL',
            deviation_numeric=-2.5,
            deviation_description='Vendor submittal specifies 94.0% efficiency at 100% load, failing the required minimum of 96.5% by 2.5%.',
            severity='critical',
            ai_explanation='The 2.5% efficiency deficit causes 50kW extra heat dissipation per unit, degrading facility PUE and increasing cooling OPEX.',
            recommended_action='Reject submittal and issue RFI requesting high-efficiency IGBT inverter topology meeting 96.5% specification.',
            checked_by='ComplianceEngine-v1',
        )
        chk_gen = ComplianceCheck(
            id=uuid.uuid4(),
            project_id=project_id,
            requirement_id=req_gen_start.id,
            submittal_id=sub_gen.id,
            equipment_id=eq_gen.id,
            submitted_value_numeric=8.5,
            submitted_unit='sec',
            status='PASS',
            deviation_numeric=-1.5,
            deviation_description='Generator start and block load acceptance achieved in 8.5 seconds, compliant with 10.0s requirement.',
            severity='low',
            ai_explanation='Vendor factory test data confirms rapid electronic governor satisfies NFPA 110 Type 10 and Tier III standards.',
            recommended_action='Approve vendor submittal and schedule witness FAT testing.',
            checked_by='ComplianceEngine-v1',
        )
        chk_chiller = ComplianceCheck(
            id=uuid.uuid4(),
            project_id=project_id,
            requirement_id=req_chiller_cop.id,
            submittal_id=sub_chiller.id,
            equipment_id=eq_chiller.id,
            submitted_value_numeric=6.45,
            submitted_unit='COP',
            status='PASS',
            deviation_numeric=0.25,
            deviation_description='Submitted COP of 6.45 exceeds required minimum specification of 6.20.',
            severity='low',
            ai_explanation='Chiller performance complies with ASHRAE 90.4 and project green data centre sustainability criteria.',
            recommended_action='Approve submittal for manufacturing release.',
            checked_by='ComplianceEngine-v1',
        )
        chk_tr = ComplianceCheck(
            id=uuid.uuid4(),
            project_id=project_id,
            requirement_id=req_tr_temp.id,
            submittal_id=sub_tr.id,
            equipment_id=eq_transformer.id,
            submitted_value_numeric=68.0,
            submitted_unit='degC',
            status='WARNING',
            deviation_numeric=3.0,
            deviation_description='Winding temp rise of 68.0°C exceeds spec limit (65.0°C) by 3.0°C, but falls within allowable tolerance of Class H insulation.',
            severity='medium',
            ai_explanation='Slightly higher temperature rise may reduce lifespan if operated continuously at maximum ambient extremes.',
            recommended_action='Approve subject to contractor providing forced-air ventilation (AF) fans in enclosure.',
            checked_by='ComplianceEngine-v1',
        )
        db.add_all([chk_ups, chk_gen, chk_chiller, chk_tr])

        act1 = ScheduleActivity(
            id=uuid.uuid4(),
            project_id=project_id,
            activity_code='ACT-1010',
            name='Substation Civil Foundations & Cable Trenches',
            wbs='1.1.1',
            planned_start=now - timedelta(days=60),
            planned_end=now - timedelta(days=30),
            actual_start=now - timedelta(days=60),
            actual_end=now - timedelta(days=30),
            duration_days=30,
            percent_complete=100.0,
            predecessors=[],
            successors=['ACT-1020'],
            is_critical_path=True,
            status='completed',
        )
        act2 = ScheduleActivity(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_transformer.id,
            activity_code='ACT-1020',
            name='33kV/11kV MV Power Transformer Rigging & Placement',
            wbs='1.1.2',
            planned_start=now - timedelta(days=30),
            planned_end=now - timedelta(days=16),
            actual_start=now - timedelta(days=30),
            duration_days=14,
            percent_complete=60.0,
            predecessors=['ACT-1010'],
            successors=['ACT-1050'],
            is_critical_path=True,
            status='delayed',
        )
        act3 = ScheduleActivity(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_ups.id,
            activity_code='ACT-1030',
            name='UPS Room Rigging, Battery Rack Mounting & Cabling',
            wbs='1.2.1',
            planned_start=now - timedelta(days=15),
            planned_end=now + timedelta(days=6),
            actual_start=now - timedelta(days=15),
            duration_days=21,
            percent_complete=45.0,
            predecessors=['ACT-1010'],
            successors=['ACT-1060'],
            is_critical_path=True,
            status='in_progress',
        )
        act4 = ScheduleActivity(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_chiller.id,
            activity_code='ACT-1040',
            name='Central Plant Chilled Water Header Piping & Pump Hookup',
            wbs='1.3.1',
            planned_start=now - timedelta(days=10),
            planned_end=now + timedelta(days=18),
            actual_start=now - timedelta(days=10),
            duration_days=28,
            percent_complete=30.0,
            predecessors=['ACT-1010'],
            successors=['ACT-1060'],
            is_critical_path=False,
            status='in_progress',
        )
        act5 = ScheduleActivity(
            id=uuid.uuid4(),
            project_id=project_id,
            activity_code='ACT-1050',
            name='Primary Substation Medium Voltage Energization & Relay Calibration',
            wbs='1.1.3',
            planned_start=now + timedelta(days=7),
            planned_end=now + timedelta(days=17),
            duration_days=10,
            percent_complete=0.0,
            predecessors=['ACT-1020'],
            successors=['ACT-1060'],
            is_critical_path=True,
            status='not_started',
        )
        act6 = ScheduleActivity(
            id=uuid.uuid4(),
            project_id=project_id,
            activity_code='ACT-1060',
            name='Level 4 Functional Testing & Full Load Heat Bank Testing',
            wbs='1.4.1',
            planned_start=now + timedelta(days=20),
            planned_end=now + timedelta(days=35),
            duration_days=15,
            percent_complete=0.0,
            predecessors=['ACT-1030', 'ACT-1040', 'ACT-1050'],
            successors=['ACT-1070'],
            is_critical_path=True,
            status='not_started',
        )
        act7 = ScheduleActivity(
            id=uuid.uuid4(),
            project_id=project_id,
            activity_code='ACT-1070',
            name='Level 5 Integrated Systems Testing (IST) & Commercial Handover',
            wbs='1.5.1',
            planned_start=now + timedelta(days=36),
            planned_end=now + timedelta(days=50),
            duration_days=14,
            percent_complete=0.0,
            predecessors=['ACT-1060'],
            successors=[],
            is_critical_path=True,
            status='not_started',
        )
        db.add_all([act1, act2, act3, act4, act5, act6, act7])
        db.flush()

        proc_ups = ProcurementItem(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_ups.id,
            po_number='PO-ELEC-2026-001',
            item_description='2000kVA Modular Double-Conversion Static UPS Lineup',
            supplier_name='Vertiv Global Supply',
            planned_order_date=now - timedelta(days=180),
            actual_order_date=now - timedelta(days=178),
            lead_time_weeks=26,
            planned_factory_testing_date=now - timedelta(days=30),
            planned_delivery_date=now - timedelta(days=5),
            expected_delivery_date=now + timedelta(days=3),
            status='in_transit',
            cost=850000.0,
            currency='USD',
        )
        proc_gen = ProcurementItem(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_gen.id,
            po_number='PO-ELEC-2026-002',
            item_description='2500kVA Diesel Generator Set with Acoustic Enclosure',
            supplier_name='Caterpillar Inc.',
            planned_order_date=now - timedelta(days=210),
            actual_order_date=now - timedelta(days=210),
            lead_time_weeks=32,
            planned_factory_testing_date=now + timedelta(days=10),
            planned_delivery_date=now + timedelta(days=30),
            expected_delivery_date=now + timedelta(days=30),
            status='manufacturing',
            cost=1200000.0,
            currency='USD',
        )
        proc_chiller = ProcurementItem(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_chiller.id,
            po_number='PO-MECH-2026-003',
            item_description='500TR Water-Cooled Centrifugal Chiller with VFD',
            supplier_name='Trane Commercial HVAC',
            planned_order_date=now - timedelta(days=160),
            actual_order_date=now - timedelta(days=158),
            lead_time_weeks=24,
            planned_factory_testing_date=now - timedelta(days=15),
            planned_delivery_date=now + timedelta(days=10),
            expected_delivery_date=now + timedelta(days=10),
            status='fat_passed',
            cost=620000.0,
            currency='USD',
        )
        proc_tr = ProcurementItem(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_transformer.id,
            po_number='PO-ELEC-2026-004',
            item_description='33kV/11kV 25MVA Cast Resin Transformer',
            supplier_name='Siemens Energy AG',
            planned_order_date=now - timedelta(days=240),
            actual_order_date=now - timedelta(days=240),
            lead_time_weeks=36,
            planned_factory_testing_date=now - timedelta(days=40),
            planned_delivery_date=now - timedelta(days=15),
            expected_delivery_date=now + timedelta(days=12),
            status='customs_hold',
            cost=1450000.0,
            currency='USD',
        )
        proc_crah = ProcurementItem(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_crah.id,
            po_number='PO-MECH-2026-005',
            item_description='150kW Data Hall Computer Room Air Handler Units (8 units)',
            supplier_name='Schneider Electric / Uniflair',
            planned_order_date=now - timedelta(days=120),
            actual_order_date=now - timedelta(days=120),
            lead_time_weeks=16,
            planned_factory_testing_date=now - timedelta(days=25),
            planned_delivery_date=now - timedelta(days=5),
            expected_delivery_date=now - timedelta(days=5),
            actual_delivery_date=now - timedelta(days=5),
            status='delivered',
            cost=480000.0,
            currency='USD',
        )
        db.add_all([proc_ups, proc_gen, proc_chiller, proc_tr, proc_crah])
        db.flush()

        risk_tr = Risk(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_transformer.id,
            activity_id=act2.id,
            procurement_id=proc_tr.id,
            title='Primary Power Transformer Customs Clearance Delay (Port of Baltimore)',
            category='procurement',
            risk_level='CRITICAL',
            risk_score=88.5,
            probability=0.90,
            impact_days=18,
            potential_cost_impact=240000.0,
            root_cause='Heavy machinery customs documentation audit hold and port drayage chassis shortage.',
            downstream_impact_summary='Directly delays 33kV MV Energization (ACT-1050) and prevents Level 4/5 IST commissioning start.',
            status='active',
        )
        mit_tr1 = RiskMitigation(
            id=uuid.uuid4(),
            risk_id=risk_tr.id,
            action_plan='Expedite customs broker with pre-clearance priority bond and mobilize dedicated multi-axle heavy transport carrier.',
            assigned_to='Senior Logistics Lead / Customs Officer',
            due_date=now + timedelta(days=3),
            estimated_cost=25000.0,
            status='in_progress',
            ai_recommended=True,
        )
        mit_tr2 = RiskMitigation(
            id=uuid.uuid4(),
            risk_id=risk_tr.id,
            action_plan='Deploy temporary 11kV mobile generator bank to perform pre-commissioning dead-circuit cold checks prior to grid energization.',
            assigned_to='Electrical Commissioning Director',
            due_date=now + timedelta(days=7),
            estimated_cost=65000.0,
            status='proposed',
            ai_recommended=True,
        )
        risk_ups = Risk(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_ups.id,
            activity_id=act3.id,
            procurement_id=proc_ups.id,
            title='UPS Efficiency Non-Conformance vs Specification (2.5% shortfall)',
            category='compliance',
            risk_level='HIGH',
            risk_score=72.0,
            probability=0.85,
            impact_days=10,
            potential_cost_impact=180000.0,
            root_cause='Vendor submitted baseline standard rectifier model rather than premium high-efficiency IGBT inverter topology.',
            downstream_impact_summary='Client sustainability penalty and increased cooling load requirement for Data Hall 1.',
            status='active',
        )
        mit_ups = RiskMitigation(
            id=uuid.uuid4(),
            risk_id=risk_ups.id,
            action_plan='Issue commercial variance notice requesting vendor upgrade to Liebert Dynamic Online mode firmware and commercial rebate.',
            assigned_to='Lead Commercial Manager',
            due_date=now + timedelta(days=5),
            estimated_cost=0.0,
            status='in_progress',
            ai_recommended=True,
        )
        db.add_all([risk_tr, mit_tr1, mit_tr2, risk_ups, mit_ups])

        rfi1 = RFI(
            id=uuid.uuid4(),
            project_id=project_id,
            rfi_number='RFI-ELEC-001',
            subject='Lithium-Ion Battery Rack Seismic Anchor Embedment Depth Clarification',
            question='Structural drawing S-201 specifies 150mm anchor depth, whereas vendor manual recommends 200mm due to high seismic Zone 2B acceleration.',
            suggested_answer='Increase slab embedment to 200mm using Hilti HIT-HY 200 epoxy anchors.',
            official_response='Approved. Structural engineer confirms 200mm embedment is required. Issue revised drawing S-201-Rev3.',
            status='answered',
            priority='high',
            assigned_to='Lead Structural Engineer',
            date_raised=now - timedelta(days=12),
            date_responded=now - timedelta(days=8),
        )
        rfi2 = RFI(
            id=uuid.uuid4(),
            project_id=project_id,
            rfi_number='RFI-MECH-002',
            subject='Condenser Water Pipe Expansion Loop Support Coordination in CEP Corridor',
            question='Clash detected in BIM model between 600mm condenser water riser and 33kV cable bus duct at Grid Line E-4.',
            suggested_answer='Shift pipe expansion loop 1200mm North into mechanical service corridor.',
            status='under_review',
            priority='urgent',
            assigned_to='BIM Lead & MEP Coordinator',
            date_raised=now - timedelta(days=2),
        )

        comm_test1 = CommissioningTest(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_gen.id,
            test_level='Level 5 - Integrated System IST',
            test_code='IST-ELEC-001',
            name='Full Facility Blackout & Generator Auto-Start Synchronization Test',
            acceptance_criteria='Upon simulated loss of 33kV utility grid, all 4 standby generators must start, synchronize, and assume essential mechanical & IT loads within 10.0 seconds.',
            test_result='pending',
            tested_by='Commissioning Lead Engineer',
            witnessed_by='Client Third-Party Commissioning Agent (CxA)',
        )
        comm_test2 = CommissioningTest(
            id=uuid.uuid4(),
            project_id=project_id,
            equipment_id=eq_chiller.id,
            test_level='Level 1 - Factory Acceptance (FAT)',
            test_code='FAT-MECH-001',
            name='Centrifugal Chiller 500TR Full Load & Part Load Performance Test',
            acceptance_criteria='Verified power input <= 0.545 kW/ton at 100% load and COP >= 6.20 with zero refrigerant leakage under 1.5x test pressure.',
            test_result='PASS',
            tested_by='Trane Certified Factory Inspector',
            witnessed_by='Nova MEP Lead Engineer',
            test_date=now - timedelta(days=15),
        )

        audit1 = AuditLog(
            id=uuid.uuid4(),
            project_id=project_id,
            entity_name='Project',
            entity_id=project_id,
            action='CREATE',
            performed_by='system_admin',
            details_json={'project_code': 'TITAN-DC01', 'name': project.name, 'budget': project.total_budget},
        )
        audit2 = AuditLog(
            id=uuid.uuid4(),
            project_id=project_id,
            entity_name='ComplianceCheck',
            entity_id=chk_ups.id,
            action='COMPLIANCE_RUN',
            performed_by='ComplianceEngine-v1',
            details_json={'status': 'FAIL', 'requirement': 'UPS Efficiency', 'deviation': -2.5},
        )

        db.add_all([rfi1, rfi2, comm_test1, comm_test2, audit1, audit2])
        db.commit()
        logger.info(f'Successfully seeded database for project {project.name} ({project.code}).')
        return project.id

    except Exception as e:
        db.rollback()
        logger.error(f'Failed to seed database: {e}', exc_info=True)
        raise
    finally:
        if close_session:
            db.close()

if __name__ == '__main__':
    seed_database()
