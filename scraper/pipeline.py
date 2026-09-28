from api.models.program import Program, EligibilityRule
from api.models.constants import RuleType
from datetime import datetime, timezone
from sqlalchemy import select

def save_program(session, name, description, source_url, jurisdiction, state, category, sections):
    stmt = select(Program).where(Program.source_url == source_url)
    program = session.scalars(stmt).first()

    if program is None:
        program = Program()
        session.add(program)

    program.name = name
    program.description = description
    program.source_url = source_url
    program.jurisdiction = jurisdiction
    program.state = state
    program.category = category
    program.last_scraped_at = datetime.now(timezone.utc)

    rules = []

    for section in sections:
        rules.append(EligibilityRule(rule_type = RuleType.OTHER.value, raw_text = section, structured_value = None))

    program.eligibility_rules = rules

    session.commit()
    return program

