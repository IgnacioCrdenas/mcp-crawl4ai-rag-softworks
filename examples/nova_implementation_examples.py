#!/usr/bin/env python3
"""
Nova Models Implementation Examples
==================================

This script demonstrates practical implementations of Amazon Nova models
with the MCP Crawl4AI RAG server. It includes real-world scenarios, 
performance optimizations, and cost analysis.

Author: MCP Crawl4AI Team
Version: 1.0.0
"""

import sys
import os
import time

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from providers.aws_bedrock import invoke_bedrock_model
except ImportError:
    print("Warning: aws_bedrock provider not available. This is for demonstration purposes.")
    
    def invoke_bedrock_model(model_id, prompt, max_tokens, temperature, top_p):
        """Mock function for demonstration when provider is not available."""
        # Use all parameters to avoid linting warnings
        return f"[MOCK] Generated response for {model_id} with prompt length {len(prompt)}, {max_tokens} tokens, temp {temperature}, top_p {top_p}"

class NovaExamples:
    """Examples and utilities for Amazon Nova models implementation."""
    
    def __init__(self):
        self.models = {
            'nova_micro': 'amazon.nova-micro-v1:0',
            'nova_lite': 'amazon.nova-lite-v1:0', 
            'nova_pro': 'amazon.nova-pro-v1:0',
            'claude': 'anthropic.claude-3-5-sonnet-20240620-v1:0'
        }
        
        self.cost_per_1k_tokens = {
            'nova_micro': 0.0004,  # $0.4 per 1M tokens
            'nova_lite': 0.0008,   # $0.8 per 1M tokens
            'nova_pro': 0.0016,    # $1.6 per 1M tokens
            'claude': 0.003        # $3.0 per 1M tokens
        }
    
    def example_1_startup_context_generation(self):
        """
        Example 1: Startup Context Generation
        
        Use case: A startup needs cost-effective context generation
        for their knowledge base with 50K documents.
        """
        print("=== Example 1: Startup Context Generation ===")
        
        # Sample document content
        document_content = """
        Product Requirements Document - AI Assistant Platform
        
        Overview: We are building an AI-powered customer service platform
        that uses natural language processing to understand customer queries
        and provide relevant responses from our knowledge base.
        
        Key Features:
        - Real-time query processing
        - Semantic search capabilities
        - Multi-language support
        - Integration with existing CRM systems
        """
        
        # Context generation prompt
        prompt = f"""
        Analyze the following document and generate a concise context summary
        that will help improve semantic search and RAG retrieval:
        
        {document_content}
        
        Provide:
        1. Key concepts and terminology
        2. Main topics covered
        3. Relevant keywords for search
        """
        
        # Using Nova Micro for cost optimization
        model_id = self.models['nova_micro']
        
        print(f"Using model: {model_id}")
        print(f"Input document length: {len(document_content)} characters")
        
        start_time = time.time()
        context = invoke_bedrock_model(
            model_id=model_id,
            prompt=prompt,
            max_tokens=200,  # Keep low for cost efficiency
            temperature=0.3,  # Low for consistency
            top_p=0.8
        )
        end_time = time.time()
        
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Generated context: {context}")
        
        # Cost calculation
        estimated_tokens = len(prompt.split()) + len(context.split()) if context else 0
        cost = (estimated_tokens / 1000) * self.cost_per_1k_tokens['nova_micro']
        print(f"Estimated cost: ${cost:.4f}")
        
        return context
    
    def example_2_multimodal_processing(self):
        """
        Example 2: Multimodal Document Processing
        
        Use case: Processing technical documentation that contains
        both text and images/diagrams.
        """
        print("\n=== Example 2: Multimodal Document Processing ===")
        
        # Simulate a technical document with mixed content
        document_description = """
        Technical Manual - API Integration Guide
        
        This document contains:
        - Text descriptions of API endpoints
        - UML diagrams showing data flow
        - Code examples in multiple languages
        - Architecture diagrams
        - Screenshots of API responses
        """
        
        prompt = f"""
        This document contains both text and visual elements:
        
        {document_description}
        
        Generate comprehensive metadata that captures both textual and visual
        information for optimal search and retrieval. Focus on:
        1. Technical concepts mentioned
        2. Visual elements description
        3. Integration points
        4. Code-related content
        """
        
        # Using Nova Lite for multimodal capabilities
        model_id = self.models['nova_lite']
        
        print(f"Using model: {model_id}")
        print("Processing multimodal technical documentation...")
        
        start_time = time.time()
        context = invoke_bedrock_model(
            model_id=model_id,
            prompt=prompt,
            max_tokens=300,
            temperature=0.4,
            top_p=0.9
        )
        end_time = time.time()
        
        print(f"Response time: {end_time - start_time:.2f} seconds")
        print(f"Generated context: {context}")
        
        return context
    
    def example_3_enterprise_migration(self):
        """
        Example 3: Enterprise Migration from Claude
        
        Use case: Large enterprise migrating from Claude to Nova
        for cost optimization while maintaining quality.
        """
        print("\n=== Example 3: Enterprise Migration Strategy ===")
        
        complex_document = """
        Enterprise Data Governance Policy
        
        This comprehensive policy document outlines our organization's
        approach to data management, privacy compliance, security protocols,
        and regulatory requirements across multiple jurisdictions.
        
        Sections include:
        - Data Classification Framework
        - Privacy by Design Principles
        - GDPR and CCPA Compliance
        - Security Controls and Monitoring
        - Incident Response Procedures
        - Third-party Data Sharing Agreements
        """
        
        prompt = f"""
        Analyze this enterprise policy document and create detailed
        metadata for regulatory compliance search and retrieval:
        
        {complex_document}
        
        Provide comprehensive analysis including:
        1. Regulatory frameworks mentioned
        2. Compliance requirements
        3. Key policy areas
        4. Risk management topics
        5. Legal terminology
        """
        
        # Compare Nova Pro vs Claude for quality assessment
        models_to_compare = ['nova_pro', 'claude']
        results = {}
        
        for model_name in models_to_compare:
            model_id = self.models[model_name]
            print(f"\nTesting {model_name}: {model_id}")
            
            start_time = time.time()
            try:
                context = invoke_bedrock_model(
                    model_id=model_id,
                    prompt=prompt,
                    max_tokens=400,
                    temperature=0.3,
                    top_p=0.85
                )
                end_time = time.time()
                
                results[model_name] = {
                    'context': context,
                    'response_time': end_time - start_time,
                    'success': True
                }
                
                print(f"Response time: {results[model_name]['response_time']:.2f}s")
                print(f"Context length: {len(context) if context else 0} characters")
                
            except Exception as e:
                results[model_name] = {
                    'error': str(e),
                    'success': False
                }
                print(f"Error: {e}")
        
        # Cost comparison
        print("\n--- Cost Comparison ---")
        for model_name in models_to_compare:
            if results[model_name].get('success'):
                context = results[model_name]['context']
                estimated_tokens = len(prompt.split()) + len(context.split()) if context else 0
                cost = (estimated_tokens / 1000) * self.cost_per_1k_tokens[model_name]
                savings = 0
                if model_name != 'claude':
                    claude_cost = (estimated_tokens / 1000) * self.cost_per_1k_tokens['claude']
                    savings = ((claude_cost - cost) / claude_cost) * 100
                
                print(f"{model_name}: ${cost:.4f} per request (savings: {savings:.1f}%)")
        
        return results
    
    def example_4_performance_optimization(self):
        """
        Example 4: Performance Optimization Strategies
        
        Use case: Optimizing Nova models for different performance
        requirements (speed, cost, quality).
        """
        print("\n=== Example 4: Performance Optimization ===")
        
        test_prompt = """
        Summarize this product review for search indexing:
        
        "This AI-powered productivity app has completely transformed how I manage
        my daily tasks. The natural language interface is intuitive, and the
        smart scheduling feature helps me prioritize effectively. However, the
        battery drain on mobile devices could be improved. Overall, it's a
        solid tool for professionals looking to streamline their workflow."
        """
        
        # Different optimization strategies
        optimization_configs = {
            'speed_optimized': {
                'model': 'nova_micro',
                'max_tokens': 100,
                'temperature': 0.1,
                'top_p': 0.7,
                'description': 'Optimized for fastest response'
            },
            'cost_optimized': {
                'model': 'nova_micro', 
                'max_tokens': 75,
                'temperature': 0.2,
                'top_p': 0.8,
                'description': 'Optimized for lowest cost'
            },
            'quality_optimized': {
                'model': 'nova_lite',
                'max_tokens': 200,
                'temperature': 0.4,
                'top_p': 0.9,
                'description': 'Balanced quality and cost'
            },
            'premium_quality': {
                'model': 'nova_pro',
                'max_tokens': 250,
                'temperature': 0.3,
                'top_p': 0.85,
                'description': 'Maximum quality'
            }
        }
        
        results = {}
        
        for config_name, config in optimization_configs.items():
            print(f"\n--- {config['description']} ---")
            model_id = self.models[config['model']]
            
            start_time = time.time()
            try:
                response = invoke_bedrock_model(
                    model_id=model_id,
                    prompt=test_prompt,
                    max_tokens=config['max_tokens'],
                    temperature=config['temperature'],
                    top_p=config['top_p']
                )
                end_time = time.time()
                
                response_time = end_time - start_time
                estimated_tokens = len(test_prompt.split()) + len(response.split()) if response else 0
                cost = (estimated_tokens / 1000) * self.cost_per_1k_tokens[config['model']]
                
                results[config_name] = {
                    'response': response,
                    'response_time': response_time,
                    'cost': cost,
                    'model': config['model'],
                    'success': True
                }
                
                print(f"Model: {model_id}")
                print(f"Response time: {response_time:.2f}s")
                print(f"Estimated cost: ${cost:.6f}")
                print(f"Response: {response}")
                
            except Exception as e:
                results[config_name] = {
                    'error': str(e),
                    'success': False
                }
                print(f"Error: {e}")
        
        # Performance summary
        print("\n--- Performance Summary ---")
        successful_results = {k: v for k, v in results.items() if v.get('success')}
        
        if successful_results:
            fastest = min(successful_results.items(), key=lambda x: x[1]['response_time'])
            cheapest = min(successful_results.items(), key=lambda x: x[1]['cost'])
            
            print(f"Fastest configuration: {fastest[0]} ({fastest[1]['response_time']:.2f}s)")
            print(f"Cheapest configuration: {cheapest[0]} (${cheapest[1]['cost']:.6f})")
        
        return results
    
    def calculate_monthly_savings(self, monthly_requests: int = 100000, avg_tokens: int = 200):
        """
        Calculate monthly cost savings when migrating from Claude to Nova models.
        """
        print(f"\n=== Monthly Cost Analysis ===")
        print(f"Assumptions: {monthly_requests:,} requests/month, {avg_tokens} tokens average")
        
        total_tokens_monthly = (monthly_requests * avg_tokens) / 1000  # Convert to thousands
        
        costs = {}
        for model_name, cost_per_1k in self.cost_per_1k_tokens.items():
            costs[model_name] = total_tokens_monthly * cost_per_1k
        
        print("\nMonthly costs by model:")
        for model_name, cost in costs.items():
            print(f"{model_name}: ${cost:.2f}")
        
        print("\nSavings compared to Claude:")
        claude_cost = costs['claude']
        for model_name, cost in costs.items():
            if model_name != 'claude':
                savings = claude_cost - cost
                savings_percent = (savings / claude_cost) * 100
                print(f"{model_name}: ${savings:.2f}/month ({savings_percent:.1f}% savings)")
        
        return costs

def main():
    """Run all Nova implementation examples."""
    print("Amazon Nova Models - Implementation Examples")
    print("=" * 50)
    
    examples = NovaExamples()
    
    # Run all examples
    try:
        examples.example_1_startup_context_generation()
        examples.example_2_multimodal_processing()
        examples.example_3_enterprise_migration()
        examples.example_4_performance_optimization()
        examples.calculate_monthly_savings()
        
    except Exception as e:
        print(f"\nExample execution failed: {e}")
        print("Make sure you have:")
        print("1. AWS credentials configured")
        print("2. Access to Bedrock Nova models")
        print("3. Correct environment variables set")

if __name__ == "__main__":
    main()
