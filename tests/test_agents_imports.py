"""
Test Agent Imports and Basic Functionality

Phase 1: Validate that all agents can be imported and instantiated
"""

import pytest
from typing import List, Dict, Any

def test_all_agents_can_be_imported():
    """Test that all 6 implemented agents can be imported without errors."""
    try:
        from agents import (
            ResumeParserAgent,
            WebEnrichmentAgent,
            JDAnalyzerAgent,
            MatchingAgent,
            ContentGeneratorAgent,
            AgentOrchestrator
        )
        # If we get here, imports succeeded
        assert True
        print("✅ All 6 agents imported successfully")

    except ImportError as e:
        pytest.fail(f"Failed to import agents: {e}")

def test_agent_config_import():
    """Test that AgentConfig can be imported."""
    try:
        from base_agent import AgentConfig
        assert True
        print("✅ AgentConfig imported successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import AgentConfig: {e}")

def test_resume_parser_agent_instantiation(test_agent_config):
    """Test ResumeParserAgent can be instantiated."""
    try:
        from agents import ResumeParserAgent
        agent = ResumeParserAgent(test_agent_config)
        assert agent is not None
        assert hasattr(agent, 'config')
        assert agent.config.name == "TestAgent"
        print("✅ ResumeParserAgent instantiated successfully")
    except Exception as e:
        pytest.fail(f"ResumeParserAgent instantiation failed: {e}")

def test_content_generator_agent_instantiation(test_agent_config):
    """Test ContentGeneratorAgent can be instantiated."""
    try:
        from agents import ContentGeneratorAgent
        agent = ContentGeneratorAgent(test_agent_config)
        assert agent is not None
        assert hasattr(agent, 'config')
        print("✅ ContentGeneratorAgent instantiated successfully")
    except Exception as e:
        pytest.fail(f"ContentGeneratorAgent instantiation failed: {e}")

def test_all_other_agents_instantiation(test_agent_config):
    """Test remaining agents can be instantiated."""
    agents_to_test = []
    try:
        from agents import WebEnrichmentAgent
        agents_to_test.append(("WebEnrichmentAgent", WebEnrichmentAgent))
    except ImportError:
        pass

    try:
        from agents import JDAnalyzerAgent
        agents_to_test.append(("JDAnalyzerAgent", JDAnalyzerAgent))
    except ImportError:
        pass

    try:
        from agents import MatchingAgent
        agents_to_test.append(("MatchingAgent", MatchingAgent))
    except ImportError:
        pass

    for agent_name, agent_class in agents_to_test:
        try:
            agent = agent_class(test_agent_config)
            assert agent is not None
            print(f"✅ {agent_name} instantiated successfully")
        except Exception as e:
            pytest.fail(f"{agent_name} instantiation failed: {e}")

def test_agent_orchestrator_instantiation(test_agent_config):
    """Test AgentOrchestrator can coordinate agents."""
    try:
        from agents import AgentOrchestrator
        orchestrator = AgentOrchestrator([test_agent_config])
        assert orchestrator is not None
        print("✅ AgentOrchestrator instantiated successfully")
    except Exception as e:
        pytest.fail(f"AgentOrchestrator instantiation failed: {e}")

def test_agents_have_required_methods(test_agent_config):
    """Test agents have required methods: validate_input, execute."""
    from agents import ResumeParserAgent

    agent = ResumeParserAgent(test_agent_config)

    # Check for required methods
    assert hasattr(agent, 'validate_input'), "Agent missing validate_input method"
    assert hasattr(agent, 'execute'), "Agent missing execute method"
    assert callable(getattr(agent, 'validate_input')), "validate_input not callable"
    assert callable(getattr(agent, 'execute')), "execute not callable"

    print("✅ Agent interface methods validated")

def test_input_validation_logic(test_resume_data):
    """Test that input validation works correctly."""
    from agents import ResumeParserAgent
    from base_agent import AgentConfig

    config = AgentConfig(name="TestAgent")
    agent = ResumeParserAgent(config)

    # Valid input should return True
    assert agent.validate_input(resume_data=test_resume_data) == True

    # Invalid input should return False
    assert agent.validate_input() == False  # No arguments
    assert agent.validate_input(resume_data=None) == False
    assert agent.validate_input(resume_data="invalid") == False

    print("✅ Input validation logic working")

def test_dependency_imports():
    """Test that all key dependencies are importable."""
    dependencies = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'uvicorn'),
        ('pydantic', 'BaseModel'),
        ('langchain_openai', 'ChatOpenAI'),  # Test LangChain integration
        ('spacy', 'spacy'),  # spaCy for NLP
        ('fitz', 'fitz'),  # PyMuPDF for PDFs
    ]

    for module_name, import_name in dependencies:
        try:
            if '.' in import_name:
                # Handle nested imports like 'fitz.fitz'
                module = __import__(module_name)
                parts = import_name.split('.')
                obj = module
                for part in parts[1:]:
                    obj = getattr(obj, part)
            else:
                obj = __import__(module_name)
                obj = getattr(obj, import_name)
            print(f"✅ {module_name}.{import_name} imported successfully")
        except (ImportError, AttributeError) as e:
            pytest.fail(f"Failed to import {module_name}.{import_name}: {e}")

def test_agent_config_validation(test_agent_config):
    """Test that agent configuration is properly validated."""
    assert test_agent_config.name == "TestAgent"
    assert test_agent_config.model == "gpt-4-turbo-preview"
    assert test_agent_config.temperature == 0.3
    assert test_agent_config.max_tokens == 2048
    assert test_agent_config.timeout == 30

    print("✅ Agent configuration validation passed")
