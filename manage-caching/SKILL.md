---
name: manage-caching
description: Optimize performance in Moqui by implementing manual and automatic caching using the CacheFacade.
---

# Skill: manage-caching

## Goal
Improve application performance and reduce database load by implementing strategic caching for frequently accessed, semi-static data using Moqui's `CacheFacade`.

## Triggers
**ALWAYS** read this skill when:
- Designing performance-critical services or entity fetches.
- Implementing manual caching in Groovy scripts (`ec.cache`).
- Configuring automatic entity caching in `manage-entities`.

## Use when
- Caching the results of expensive calculations or API calls.
- Storing semi-static configuration data in memory.
- Reducing DB hits for high-frequency "one" fetches.

## Don't use when
- Dealing with highly dynamic data where staleness cannot be tolerated.
- The default Moqui entity cache (if enabled) already provides sufficient performance.

## Inputs
- Data to be cached.
- Cache name and expiration policies.

## Outputs
- Groovy logic using `ec.cache.getCache(name)`.
- XML entity definitions with `use-cache="true"`.

## Rules & Guardrails
1. **Cache Facade**: Use `ec.cache.getCache("myCacheName")` to get or create a named cache.
2. **Entity Caching**:
    - Set `use-cache="true"` on an entity definition for automatic caching of `find().one()` lookups.
    - Set `use-cache="true"` on a relationship to cache the related record.
3. **Groovy Cache Operations**:
    - `cache.get(key)`: Retrieves a value.
    - `cache.put(key, value)`: Stores a value.
    - `cache.remove(key)`: Explicitly evicts a record.
4. **Cache Configuration**: Caches are configured in `moqui-conf.xml`. You can specify `max-elements`, `idle-timeout`, and `live-timeout`.
5. **Distributed Caching**: For clusters, use `moqui.context.CacheFacade.getDistributedCache(name)` (if a distributed cache provider like Hazelcast is configured).
6. **Key Design**: Ensure cache keys are unique and consistent (e.g., using a Map or a composite string ID).
7. **Staleness Handling**: Be mindful of when to clear the cache. For manual caches, you may need an EECA (see `manage-eca`) to clear a cache entry when the underlying entity is updated.

## Failure handling
- **Memory Pressure**: Monitor cache sizes; avoid caching massive datasets that could lead to OutOfMemory errors.
- **Data Inconsistency**: If a user reports seeing old data, verify the cache eviction logic.

## Minimal example
**Requirement**: Cache the result of a complex tax calculation in Groovy.

**Good Output (Groovy)**:
```groovy
def taxCache = ec.cache.getCache("SalesTaxCache")
def cacheKey = [zipCode: zip, amount: amount]

BigDecimal tax = taxCache.get(cacheKey)
if (tax == null) {
    // Expensive calculation or API call
    tax = calculateComplexTax(zip, amount)
    taxCache.put(cacheKey, tax)
}

return tax
```
