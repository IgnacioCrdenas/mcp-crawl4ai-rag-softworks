# Examples Directory

This directory contains example configurations and practical usage patterns for the Crawl4AI RAG MCP server, with special focus on Amazon Nova models.

## Files

### `nova-micro-config.env`

Example configuration file demonstrating how to use Amazon Nova Micro for cost-effective context generation.

**Key features:**
- Uses Nova Micro (`amazon.nova-micro-v1:0`) for context generation
- Optimized for cost and latency
- Text-only model suitable for simple contextual embedding tasks

**Usage:**
```bash
# Copy the example configuration
cp examples/nova-micro-config.env .env

# Edit with your actual credentials
# Then run the MCP server
```

### `test_nova_micro.py`

Automated testing script for validating Nova Micro integration.

**Features:**
- Tests AWS credentials and configuration
- Validates Nova Micro model availability
- Performs end-to-end testing
- Provides performance metrics

**Usage:**
```bash
# Run the test script
python examples/test_nova_micro.py
```

## Quick Start Examples

### 1. Cost-Optimized Setup (Nova Micro)

For startups and high-volume applications:

```bash
# Copy the Nova Micro configuration
cp examples/nova-micro-config.env .env

# Edit .env with your credentials
nano .env

# Run the server
docker run -d \
  --name crawl4ai-rag-nova \
  --env-file .env \
  -p 8051:8051 \
  ignaciocardenas/mcp-crawl4ai-rag-softworks:latest
```

### 2. Multimodal Setup (Nova Lite)

For documents with images and mixed content:

```bash
# Use Nova Lite configuration
echo "BEDROCK_CONTEXT_MODEL_ID=amazon.nova-lite-v1:0" >> .env
```

### 3. Advanced Analysis (Nova Pro)

For complex document analysis:

```bash
# Use Nova Pro configuration
echo "BEDROCK_CONTEXT_MODEL_ID=amazon.nova-pro-v1:0" >> .env
```

## Model Selection Guide

Choose the right model based on your needs:

| Use Case | Recommended Model | Configuration | Relative Cost |
|----------|------------------|---------------|---------------|
| **Cost-sensitive text processing** | Nova Micro | `BEDROCK_CONTEXT_MODEL_ID="amazon.nova-micro-v1:0"` | 1x (baseline) |
| **Fast multimodal tasks** | Nova Lite | `BEDROCK_CONTEXT_MODEL_ID="amazon.nova-lite-v1:0"` | 2-3x |
| **Advanced multimodal capabilities** | Nova Pro | `BEDROCK_CONTEXT_MODEL_ID="amazon.nova-pro-v1:0"` | 4-6x |
| **High-quality text generation** | Claude 3.5 Sonnet | `BEDROCK_CONTEXT_MODEL_ID="anthropic.claude-3-5-sonnet-20240620-v1:0"` | 8-10x |

## Performance Tuning

### For Maximum Cost Savings (Nova Micro)
```bash
# Optimize for cost
BEDROCK_CONTEXT_MODEL_ID="amazon.nova-micro-v1:0"
# Use shorter context windows
# Process in batches
```

### For Speed (Nova Lite)
```bash
# Optimize for speed
BEDROCK_CONTEXT_MODEL_ID="amazon.nova-lite-v1:0"
AWS_REGION="us-east-1"  # Use closest region
```

### For Quality (Nova Pro)
```bash
# Optimize for quality
BEDROCK_CONTEXT_MODEL_ID="amazon.nova-pro-v1:0"
# Use higher token limits
# Enable detailed analysis
```

## Testing Your Configuration

After setting up your configuration, test it with:

```bash
# Test Nova Micro specifically
python examples/test_nova_micro.py

# Or test the full MCP server
docker run --env-file .env -p 8051:8051 ignaciocardenas/mcp-crawl4ai-rag-softworks:latest
```

## Migration from Claude

### Step-by-Step Migration

1. **Backup current configuration:**
   ```bash
   cp .env .env.claude.backup
   ```

2. **Update to Nova:**
   ```bash
   # For cost optimization
   sed -i 's/anthropic.claude-3-5-sonnet-20240620-v1:0/amazon.nova-micro-v1:0/' .env
   ```

3. **Test the change:**
   ```bash
   python examples/test_nova_micro.py
   ```

4. **Deploy:**
   ```bash
   docker-compose restart
   ```

## Cost Comparison

Approximate costs for 100K requests/month with 200 tokens average:

| Model | Monthly Cost | Savings vs Claude |
|-------|--------------|-------------------|
| Nova Micro | $8 | 86% |
| Nova Lite | $16 | 73% |
| Nova Pro | $24 | 60% |
| Claude 3.5 Sonnet | $60 | 0% (baseline) |

## Troubleshooting

Common issues and solutions:

1. **Model not available**: Check AWS region support
2. **Access denied**: Verify IAM permissions for Nova models
3. **High latency**: Use us-east-1 region for best performance
4. **Quality issues**: Consider Nova Lite/Pro for better results

For detailed troubleshooting, see [../docs/NOVA_USAGE_EXAMPLES.md](../docs/NOVA_USAGE_EXAMPLES.md).

- **Nova Micro**: 1x (baseline)
- **Nova Lite**: 2-3x
- **Claude 3.5 Sonnet**: 4-6x
- **Nova Pro**: 5-8x

*Note: Actual costs depend on token usage and AWS pricing. Check current Bedrock pricing for exact figures.*
