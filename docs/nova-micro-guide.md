# Amazon Nova Micro Integration Guide

## Overview

Amazon Nova Micro (`amazon.nova-micro-v1:0`) is a text-only foundation model optimized for lowest latency and cost. This guide explains how to integrate and use Nova Micro with the Crawl4AI RAG MCP server.

## Key Benefits of Nova Micro

- **Cost-Effective**: Optimized for the lowest cost among Bedrock text models
- **Low Latency**: Fast response times for real-time applications
- **Text-Only**: Focused on text generation without multimodal capabilities
- **Simple Integration**: Works with existing Bedrock infrastructure

## Configuration

### Environment Variables

Set these environment variables to use Nova Micro:

```bash
# Use Bedrock for context generation
CONTEXT_PROVIDER="bedrock"

# Set Nova Micro as the model
BEDROCK_CONTEXT_MODEL_ID="amazon.nova-micro-v1:0"

# AWS credentials (required)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
```

### Complete Configuration Example

```bash
# MCP Server Configuration
TRANSPORT=sse
HOST=0.0.0.0
PORT=8051

# Supabase for RAG
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key

# OpenAI for embeddings (or use Bedrock Titan)
OPENAI_API_KEY=your_openai_key
EMBEDDINGS_PROVIDER="openai"

# Nova Micro for context generation
CONTEXT_PROVIDER="bedrock"
BEDROCK_CONTEXT_MODEL_ID="amazon.nova-micro-v1:0"

# AWS credentials
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
```

## Model Comparison

| Model | Use Case | Cost | Capabilities |
|-------|----------|------|--------------|
| `amazon.nova-micro-v1:0` | Cost-sensitive text tasks | Lowest | Text-only |
| `amazon.nova-lite-v1:0` | Fast multimodal tasks | Low | Text, images, video |
| `amazon.nova-pro-v1:0` | Advanced multimodal tasks | Medium | Text, images, video |
| `anthropic.claude-3-5-sonnet-20240620-v1:0` | High-quality text | Higher | Text-only |

## Implementation Details

### Request Format

Nova Micro uses a messages-based API format:

```json
{
  "messages": [
    {"role": "user", "content": "Your prompt here"}
  ],
  "max_tokens": 2048,
  "temperature": 0.7,
  "top_p": 0.9
}
```

### Response Format

Nova Micro returns responses in this format:

```json
{
  "content": "Generated text response",
  "output": {
    "message": {
      "content": [
        {"text": "Generated text response"}
      ]
    }
  }
}
```

## Usage in Context Generation

When `CONTEXT_PROVIDER="bedrock"` and `BEDROCK_CONTEXT_MODEL_ID="amazon.nova-micro-v1:0"`, the system will:

1. Use Nova Micro to generate contextual information for document chunks
2. Enhance retrieval quality through contextual embeddings
3. Provide cost-effective context generation for large document sets

## Testing

Run the included test script to verify Nova Micro integration:

```bash
# Set AWS credentials first
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_REGION=us-east-1

# Run the test
python test_nova_micro.py
```

## Cost Optimization Tips

1. **Use Nova Micro for simple tasks**: Perfect for contextual embedding generation
2. **Batch requests**: Group multiple prompts when possible
3. **Optimize prompt length**: Shorter prompts = lower costs
4. **Monitor usage**: Track token consumption through AWS billing

## Troubleshooting

### Common Issues

1. **Access Denied**: Ensure your AWS credentials have Bedrock permissions
2. **Model Not Available**: Nova Micro might not be available in all regions
3. **Rate Limiting**: Implement retry logic with exponential backoff

### Error Handling

The provider includes comprehensive error handling:

- Automatic retries for throttling
- Graceful fallback on errors
- Detailed logging for debugging

### Logging

Enable debug logging to troubleshoot issues:

```python
import logging
logging.getLogger("providers.aws_bedrock").setLevel(logging.DEBUG)
```

## Migration from Other Models

### From Claude

Replace:
```bash
BEDROCK_CONTEXT_MODEL_ID="anthropic.claude-3-5-sonnet-20240620-v1:0"
```

With:
```bash
BEDROCK_CONTEXT_MODEL_ID="amazon.nova-micro-v1:0"
```

### Expected Changes

- **Cost**: Significant reduction in context generation costs
- **Quality**: Slightly lower quality for complex reasoning tasks
- **Speed**: Faster response times
- **Capabilities**: Text-only (no multimodal features)

## Best Practices

1. **Use for appropriate tasks**: Nova Micro excels at simple text generation
2. **Test thoroughly**: Validate output quality for your specific use case
3. **Monitor performance**: Track both cost and quality metrics
4. **Have fallbacks**: Consider Claude for complex reasoning tasks

## Additional Resources

- [AWS Bedrock Nova Models Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-nova.html)
- [Nova Models Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Bedrock IAM Permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html)
