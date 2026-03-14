---
name: manage-outbound-api
description: Implement outbound REST integration in Moqui using the RestClient through ec.service.rest().
---

# Skill: manage-outbound-api

## Goal
Securely and reliably call external REST APIs from Moqui logic, handling various content types, authentication methods, and error conditions.

## Triggers
**ALWAYS** read this skill when:
- Implementing a Groovy script that needs to call an external API.
- Configuring a service that acts as a client to an external system (e.g., Shopify, NetSuite).
- Managing API timeouts, retries, and header configurations.

## Use when
- Posting data to an external webhook.
- Fetching JSON or XML data from a third-party service.
- Building a connector component for an external platform.

## Don't use when
- Defining endpoints for external systems to call (use `manage-rest`).

## Inputs
- Target URL and HTTP method.
- Request body (Map, JSON string, etc.).
- Authentication details (API Key, Bearer Token).

## Outputs
- Groovy logic using `ec.service.rest()`.

## Rules & Guardrails
1. **RestClient Entry Point**: Always use `ec.service.rest()` to access the builder-style API.
2. **Method & URI**: Chain `.method("GET|POST|PUT|PATCH|DELETE")` and `.uri("url")`.
3. **Data Mapping**:
    - Use `.jsonObject(map)` to automatically convert a Map to a JSON request body.
    - Use `.xmlNode(node)` for XML requests (using `MNode`).
    - Use `.text(string)` for raw body content.
4. **Headers & Parameters**: 
    - Use `.header("Name", "Value")` for custom headers.
    - Use `.addQueryParameter("name", "value")` for URL parameters.
    - Use `.addBodyParameter("name", "value")` for form-encoded POST data.
    - Use `.addPathElement("segment")` to build the URI dynamically.
5. **Authentication**: Use `.basicAuth("user", "pass")` for standard basic authentication.
6. **Response Handling**: Always check the response after `.call()`.
    - `response.checkError()`: Throws exception if not 2xx.
    - `response.statusCode`: HTTP status code (int).
    - `response.jsonObject()` / `response.xmlNode()` / `response.text()`: Parsed or raw body.
    - `response.bytes()`: For binary data.
    - `response.headerFirst("Name")`: Get specific header value.
7. **Reliability**:
    - Use `.timeout(seconds)` (default 30).
    - Use `.retry()` or `.retry(initialWait, maxRetries)` for 429 (Too Many Requests) or timeout retries (`.timeoutRetry(true)`).
8. **Multipart**: For POST only, use `.addFieldPart(name, value)` and `.addFilePart(name, fileName, streamOrString)`.

## Failure handling
- **API Down**: Log the error using `ec.logger.error()` and consider adding a user message if appropriate.
- **Malformed Response**: Use safe navigation and try-catch blocks when parsing complex responses.

## Minimal example
**Requirement**: Send a POST request with JSON body and Bearer token.

**Good Output (Groovy)**:
```groovy
def resp = ec.service.rest().method("POST")
    .uri("https://api.example.com/v1/notify")
    .header("Authorization", "Bearer ${apiKey}")
    .jsonObject([id: "123", status: "Active"])
    .call()

if (resp.statusCode != 200) {
    ec.logger.error("API [URI: ${resp.request.uri}] - Call failed with status ${resp.statusCode}: ${resp.error}")
} else {
    def data = resp.jsonObject()
    ec.logger.info("API [URI: ${resp.request.uri}] - Successfully notified: ${data.message}")
}
```
